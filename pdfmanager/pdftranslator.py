import logging
import argparse
from pdfminer.converter import XMLConverter
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.layout import LAParams
from .xmlparser import wellFormatXml, removeNoTextBox, mergeAllTextBox, getDictFromXml
from .drawer import createOverlaysFromXmlDict, overlaidPdf
import os, json

#if __name__ == "__main__" :
# parser = argparse.ArgumentParser()
# parser.add_argument('--inputFilePath', '-i')
# parser.add_argument('--fontSize', '-s')
# parser.add_argument('--outputFilePath', '-o')

# args = parser.parse_args()
# inputFilePath = args.inputFilePath
# outputFilePath = args.outputFilePath
# fontSize = args.fontSize

# if fontSize is None :
#     fontSize = 8

# if outputFilePath is None :
#     outputFilePath =  os.path.join(os.path.dirname(inputFilePath),'[FR]' + os.path.basename(inputFilePath))

def main() :
    inputFilePath = '/Users/giovannimazzobel/Downloads/Social_Security_Fraud.pdf'

    logging.info('I read yout pdf.')
    # create xml
    rsrcmgr = PDFResourceManager()
    tmpXmlPath = './.tmp.xml'
    outfp = open(tmpXmlPath, 'w')
    device = XMLConverter(rsrcmgr, 
                            outfp,
                            laparams = LAParams())
    fname = inputFilePath
    with open(fname, 'rb') as fp:
            interpreter = PDFPageInterpreter(rsrcmgr, device)
            for page in PDFPage.get_pages(fp, set(), check_extractable=True):
                interpreter.process_page(page)
    device.close()
    outfp.close()

    # remove non utf8 chars
    wellFormatXml(tmpXmlPath)
    # get only textbox tag from xml
    removeNoTextBox(tmpXmlPath)
    # merge textbox which is include in other textbox
    mergeAllTextBox(tmpXmlPath)

    outputFilePath = '/Users/giovannimazzobel/Scripts/PDFManager/test.pdf'

    ans = getDictFromXml(tmpXmlPath)
    with open('/Users/giovannimazzobel/Scripts/PDFManager/output.json','w', encoding=('utf-8')) as f :
        json.dump(ans, f, indent = 4)

    canvas = createOverlaysFromXmlDict(ans)
    overlaidPdf(canvas, inputFilePath, outputFilePath)
    # create traducted pdf
    # addOverlay(tmpXmlPath, inputFilePath, outputFilePath)
    # trash tmp xml
    os.remove(tmpXmlPath)