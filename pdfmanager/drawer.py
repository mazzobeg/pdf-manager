import xml.etree.ElementTree as ET

from fpdf import FPDF
from PyPDF2 import PdfFileWriter, PdfFileReader
import io
from numpy import deprecate
from reportlab.pdfgen import canvas
from reportlab.lib import colors

from .util import progressBar
from .calculator import bboxWithWH, bboxFromBLtoTL
from .xmlparser import isValidTextBox, getBboxFromElement, textBoxToText

# @deprecate
# def addOverlay(xmlPath, pdfPath, outputPath) : 
#     # fetch modeled xml
#     tree = ET.parse(xmlPath)
#     root = tree.getroot()
#     # fetch document dimensions
#     bboxFirstPage = ([float(x) for x in root.find('page').attrib['bbox'].split(',')])
#     format = (bboxFirstPage[2], bboxFirstPage[3])
#     canvas = []
#     i = 0
#     progressBar(0, len([x for x in root]))
#     for page in root :
#         # fetch textbox
#         textboxes = [x for x in page if x.tag == 'textbox']
#         bboxes = []
#         textes = []
#         textSizes = []
#         for textbox in textboxes : 
#             # check if is valid
#             if isValidTextBox(textbox, format) :
#                 # get bbox from tag
#                 bbox = getBboxFromElement(textbox)
#                 # convert xyxy to xywh
#                 bbox = bboxWithWH(bbox)
#                 bboxes.append(bbox)
#                 # get text of textbox
#                 text = textBoxToText(textbox)
#                 textes.append(text)

#                 #getMinSizeFontInTextbox(textbox)
#                 #textSizes.append(getMinSizeFontInTextbox(textbox))
                
#         can = createOverlayFromPage((format[0],format[1]), bboxes, textes, textSizes)
#         canvas.append(can)
#         i += 1
#         progressBar(i, len([x for x in root]))
#     overlayPDFPage(canvas, pdfPath, outputPath)

def showTextbox(root, pathXml, pathOutputPdf) :
    bboxFirstPage = ([float(x) for x in root.find('page').attrib['bbox'].split(',')])
    format = (bboxFirstPage[2], bboxFirstPage[3])
    pdf = FPDF(orientation='P', unit='mm', format=format)
    for page in root :
        pdf.add_page()
        textboxes = [x for x in page if x.tag == 'textbox']
        for textbox in textboxes : 
            if isValidTextBox(textbox, pdf) :
                bbox = getBboxFromElement(textbox)
                bbox = bboxWithWH(bbox)
                bbox = bboxFromBLtoTL(bbox, pdf.h, True)
                pdf.rect(*bbox)
                text = textBoxToText(textbox)
                pdf.set_xy(bbox[0],bbox[1]+bbox[3] )
                pdf.set_font('Arial', 'B', 13)
                pdf.set_text_color(0,0,255)
                pdf.multi_cell(w=bbox[2],h=8,txt=text, border=0)
    outfp = open(pathOutputPdf, 'w')
    outfp.close()
    pdf.output(pathOutputPdf, 'F')

def createOverlaysFromXmlDict(xmlDict) :
    overlays = []
    
    d = xmlDict
    
    for page in xmlDict['pages'].values() :
        packet = io.BytesIO()
        can = canvas.Canvas(packet, pagesize=(d['docInfo'].values()))
        for area in page.values() :
            if not 'bbox' in area.keys() : break
            bbox = area['bbox']
            text = area['text']
            # background of area
            can.setFillColor(colors.lightgrey)
            can.setStrokeColor(colors.grey)
            can.rect(bbox[0],bbox[1],bbox[2],bbox[3], fill=1)
            # text writing
            textobject = can.beginText()
            textobject.setTextOrigin(bbox[0]+2,bbox[1]+bbox[3]-9)
            textobject.setFont('Times-Roman', 9)
            textobject.setFillColor(colors.black)
            textobject.textLines(text)
            can.drawText(textobject)
        can.save()
        packet.seek(0)
        overlays.append(packet)
    
    return overlays

@deprecate
def createOverlayFromPage(pageSize, bboxes, textes:list[str], textSizes) :
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=pageSize)
    for bbox, text, size in zip(bboxes, textes, textSizes) :
        #textBreaked = ''wrap(text, 80)
        can.setFillColor(colors.lightgrey)
        can.setStrokeColor(colors.grey)
        can.rect(bbox[0],bbox[1],bbox[2],bbox[3], fill=1)
        textobject = can.beginText()
        textobject.setTextOrigin(bbox[0]+2,bbox[1]+bbox[3]-9)
        textobject.setFont('Times-Roman', 9)
        textobject.setFillColor(colors.black)

        textobject.textLines(text)
        can.drawText(textobject)
        
        can.setLineWidth(5)
        can.setStrokeColor(colors.blue)
        can.rect(2.5,2.5,pageSize[0]-5,pageSize[1]-5, fill=False, stroke = True)
        can.setLineWidth(1)

        can.setFont('Times-Roman', 5)
        can.setFillColor(colors.white)
        can.drawString(0,0, "traducted with pdfmanager :)")

    can.save()
    packet.seek(0)
    return packet

def overlaidPdf(canvasAsPacket:list, inputPdfPath, outputPdfPath) :
    existing_pdf = PdfFileReader(open(inputPdfPath, "rb"))
    existing_pdfForTraduction = PdfFileReader(open(inputPdfPath, "rb"))
    output = PdfFileWriter()
    idPage = 0
    for canvas in canvasAsPacket :
        new_pdf = PdfFileReader(canvas)
        pageUntraducted = existing_pdf.getPage(idPage)
        output.addPage(pageUntraducted)
        pageTraducted = existing_pdfForTraduction.getPage(idPage)
        pageTraducted.mergePage(new_pdf.getPage(0))
        output.addPage(pageTraducted)
        idPage += 1
    outputStream = open(outputPdfPath, "wb")
    output.write(outputStream)
    outputStream.close()