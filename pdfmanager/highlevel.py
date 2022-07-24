import logging
from pdfminer.converter import XMLConverter
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.layout import LAParams
from .xmlparser import wellFormatXml, removeNoTextBox, mergeAllTextBox, getDictFromXml
from .drawer import createOverlaysFromXmlDict, overlaidPdf
import os, json

def pdfTranslation(inputPdfPath:str, outputPdfPath:str = None, language:str = None, fontsize:int = None) : 

    if language is None : language = 'en2fr'
    if fontsize is None : fontsize = 8
    
    logging.info(f'Traduction of {os.path.basename(inputPdfPath)} ({language.split("2")[0]}) to {os.path.basename(outputPdfPath)} ({language.split("2")[1]})')
    logging.info('Parsing your pdf file.')
    # create xml
    rsrcmgr = PDFResourceManager()
    tmpXmlPath = './.tmp.xml'
    outfp = open(tmpXmlPath, 'w')
    device = XMLConverter(rsrcmgr, 
                            outfp,
                            laparams = LAParams())
    with open(inputPdfPath, 'rb') as fp:
            interpreter = PDFPageInterpreter(rsrcmgr, device)
            for page in PDFPage.get_pages(fp, set(), check_extractable=True):
                interpreter.process_page(page)
    device.close()
    outfp.close()
    logging.info('Prettifying parsing.')
    # remove non utf8 chars
    wellFormatXml(tmpXmlPath)
    # get only textbox tag from xml
    removeNoTextBox(tmpXmlPath)
    # merge textbox which is include in other textbox
    mergeAllTextBox(tmpXmlPath)

    ans = getDictFromXml(tmpXmlPath)
    with open('/Users/giovannimazzobel/Scripts/PDFManager/output.json','w', encoding=('utf-8')) as f :
        json.dump(ans, f, indent = 4)
    with open('/Users/giovannimazzobel/Scripts/PDFManager/output.json','r', encoding=('utf-8')) as f :
        ans = json.load(f)

    logging.info('In translation.')
    canvas = createOverlaysFromXmlDict(ans, language, fontsize)
    logging.info('Pdf dressing.')
    overlaidPdf(canvas, inputPdfPath, outputPdfPath)
    os.remove(tmpXmlPath)
    logging.info(f'Your pdf is ready at "{outputPdfPath}"')
