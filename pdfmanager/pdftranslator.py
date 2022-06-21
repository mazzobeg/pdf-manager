from fpdf import FPDF
import xml.etree.ElementTree as ET
import numpy as np
from googletrans import Translator
import time
from PyPDF2 import PdfFileWriter, PdfFileReader
import io
from reportlab.pdfgen import canvas
from reportlab.lib import colors

from reportlab.lib.pagesizes import letter
from string import printable
from textwrap import wrap

import logging


translator = Translator()

def progressBar(progress, total) :
    percent = int(100 * (progress/float(total)))
    bar = '\033[92m' + '<' + '-' * percent + '>' +  '\033[0m' + '-' * (100-int(percent))
    print(f'\rIn translation … {bar} \033[92m{percent:.2f}%\033[0m', end = '')

def centroid(bbox) :
    return (np.mean([bbox[0],bbox[2]]), np.mean([bbox[1],bbox[3]]))

def getBboxFromElement(element) :
    if not 'bbox' in element.attrib.keys() : return -1
    return [float(x) for x in element.attrib['bbox'].split(',')]

def compareBbox(bbox1, bbox2) :
    """
    1 : bbox1 in bbox2
    0 : bbox1 out of bbox2
    """
    if (bbox1[0] >= bbox2[0] -5 
    and bbox1[1] >= bbox2[1] -5
    and bbox1[2] <= bbox2[2] +5
    and bbox1[3] <= bbox2[3] +5) :
        return 1
    else :
        return 0

def mergeTextbox(src, dest) :
    yDest = np.array([centroid(getBboxFromElement(x))[1] for x in dest])
    # foreach textline src
    for textline in src :
        # find textline dest
        ySrc = centroid(getBboxFromElement(textline))[1]
        idTextline = np.argmin(abs(yDest - ySrc))
        destTextline = dest[idTextline]
        # foreach word src 
        for word in textline : 
            # find previous word in textline dest
            try :
                xDest = np.array([getBboxFromElement(x)[0] for x in destTextline])
                xSrc = getBboxFromElement(word)[0]
                idPreviousWord = np.argmin(abs(yDest - ySrc))
                # insert word
                destTextline.insert(idPreviousWord+1, word)
            except : 
                pass

def mergeTextboxes(textboxes:list) :
    toMerge = {}
    for textbox1 in textboxes :
        for textbox2 in textboxes : 
            if textbox1.attrib['id'] != textbox2.attrib['id'] :
                comparaison = compareBbox(getBboxFromElement(textbox1), getBboxFromElement(textbox2))
                if comparaison == 1 :
                    toMerge[int(textbox1.attrib['id'])] = int(textbox2.attrib['id'])
                else :
                    pass
    for key, value in toMerge.items() :
        mergeTextbox(textboxes[key], textboxes[value])
    for key in list(toMerge.keys())[::-1] :
        textboxes.remove(textboxes[key])
    return textboxes

def bboxFromBLtoTL(bbox, gridHeight, wh=False) : 
    if wh :
        return [bbox[0], gridHeight-bbox[1], bbox[2], -bbox[3]]
    else :
        return [bbox[0], gridHeight-bbox[1], bbox[2], gridHeight-bbox[3]]

def bboxWithWH(bbox) :
    return [bbox[0], bbox[1], bbox[2]-bbox[0], bbox[3]-bbox[1]]


def textBoxToText(textbox) :
    words = []
    for textline in textbox :
        if textline.tag == 'textline' :
            for text in textline :
                if text.tag == 'text' :
                    words.append(str(text.text))
    text = ''.join(words)
    #text = text.replace('\n', '')
    text = text.replace('None', '[~]')
    try :
        text = translator.translate(text, 'fr', 'en').text
    except :
        time.sleep(2)
        text = translator.translate(text, 'fr', 'en').text
    #text = ''.join(char for char in text if char in printable)
    return text

def isValidTextBox(textbox, format) :
    bbox = getBboxFromElement(textbox)
    bbox = bboxWithWH(bbox)
    if bbox[2] > (((format[0])/2) - 100):
        return True
    else :
        return False

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

def overlayPDFPage(canvasAsPacket:list, inputPdfPath, outputPdfPath) :
    existing_pdf = PdfFileReader(open(inputPdfPath, "rb"))
    existing_pdfForTraduction = PdfFileReader(open(inputPdfPath, "rb"))
    output = PdfFileWriter()
    idPage = 0
    for canvas in canvasAsPacket :
        # create a new PDF with Reportlab
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

def getMinSizeFontInTextbox(textbox) :
    elementsAsSize = textbox.findall('./textline/text[@size]')
    elementsAsSize1 = textbox.findall('./text[@size]')

    allSizes = [float(x.attrib['size']) for x in elementsAsSize]
    allSizes1 = [float(x.attrib['size']) for x in elementsAsSize1]
    allSizes += allSizes1
    return np.min(allSizes)

def addOverlay(root, pdfPath, outputPath) : 
    bboxFirstPage = ([float(x) for x in root.find('page').attrib['bbox'].split(',')])
    format = (bboxFirstPage[2], bboxFirstPage[3])
    canvas = []
    i = 0
    progressBar(0, len([x for x in root]))
    for page in root :
        textboxes = [x for x in page if x.tag == 'textbox']
        bboxes = []
        textes = []
        textSizes = []
        for textbox in textboxes : 
            if isValidTextBox(textbox, format) :
                
                bbox = getBboxFromElement(textbox)
                bbox = bboxWithWH(bbox)
                bboxes.append(bbox)
                text = textBoxToText(textbox)
                textes.append(text)
                getMinSizeFontInTextbox(textbox)
                textSizes.append(getMinSizeFontInTextbox(textbox))
                
        can = createOverlayFromPage((format[0],format[1]), bboxes, textes, textSizes)
        canvas.append(can)
        i += 1
        progressBar(i, len([x for x in root]))
    overlayPDFPage(canvas, pdfPath, outputPath)

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

def mergeAllTextBox(root, path) :
    for page in root :
        mergeTextboxes(page)
    tree.write(path)

def removeNoTextBox(root, path) :
    for page in root :
        to_remove = []
        for element in page:
            if element.tag != "textbox" :
                to_remove.append(element)
        for element in to_remove :
            page.remove(element)
    tree.write(path)

def wellFormatXml(xmlPath:str) :
    with open(xmlPath, 'r') as f :
        xmlDatas = f.read()
    xmlDatasWellFormat = ''.join(char for char in xmlDatas if char in printable)
    with open(xmlPath, 'w') as f :
        f.write(xmlDatasWellFormat)
    #logging.info('xml formatted.')

# srcXml = "/Users/giovannimazzobel/Downloads/test/test.xml"
# # wellFormatXml(srcXml)
# tree = ET.parse(srcXml)
# root = tree.getroot()
# # removeNoTextBox(root, srcXml)
# # mergeAllTextBox(root, srcXml)
# #showTextbox(root, srcXml, "/Users/giovannimazzobel/Downloads/test/testBoundaries.pdf")
# addOverlay(root, "/Users/giovannimazzobel/Downloads/test/test.pdf")

import argparse
from pdfminer.converter import XMLConverter
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.layout import LAParams
import os

if __name__ == "__main__" :
    parser = argparse.ArgumentParser()
    parser.add_argument('--inputFilePath', '-i')
    parser.add_argument('--fontSize', '-s')
    parser.add_argument('--outputFilePath', '-o')

    args = parser.parse_args()
    inputFilePath = args.inputFilePath
    outputFilePath = args.outputFilePath
    fontSize = args.fontSize

    if fontSize is None :
        fontSize = 8
    
    if outputFilePath is None :
        outputFilePath =  os.path.join(os.path.dirname(inputFilePath),'[FR]' + os.path.basename(inputFilePath))

    logging.info('I read yout pdf.')
    # create xml
    rsrcmgr = PDFResourceManager()
    tmpXmlPath = './.tmp.xml'
    outfp = open(tmpXmlPath, 'w')
    device = XMLConverter(rsrcmgr, outfp,
                              imagewriter=None,
                              laparams = LAParams(),
                              stripcontrol=False)
    fname = inputFilePath
    with open(fname, 'rb') as fp:
            interpreter = PDFPageInterpreter(rsrcmgr, device)
            for page in PDFPage.get_pages(fp, set(),
                                          check_extractable=True):
                interpreter.process_page(page)
    device.close()
    outfp.close()
    
    # preprocess xml
    wellFormatXml(tmpXmlPath)
    tree = ET.parse(tmpXmlPath)
    root = tree.getroot()
    removeNoTextBox(root, tmpXmlPath)
    mergeAllTextBox(root, tmpXmlPath)

    # create traducted pdf
    logging.info('I start creating new one.')
    addOverlay(root, inputFilePath, outputFilePath)

    # trash tmp
    os.remove(tmpXmlPath)