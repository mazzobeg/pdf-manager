import argparse, logging
from pdfmanager.highlevel import pdfTranslation


if __name__ == '__main__':
    FORMAT = '[pdfmanager] %(message)s'
    logging.basicConfig(format=FORMAT, level=logging.INFO)  

    parser = argparse.ArgumentParser()
    parser.add_argument('--inputFilePath', '-i')
    parser.add_argument('--outputFilePath', '-o')
    parser.add_argument('--fontSize', '-s')
    parser.add_argument('--language', '-l')
    
    args = parser.parse_args()

    pdfTranslation( inputPdfPath = args.inputFilePath, 
                    outputPdfPath = args.outputFilePath,
                    language = args.language, 
                    fontsize = args.fontSize)
