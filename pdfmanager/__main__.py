import argparse
import logging

from pdfmanager import renamer, util

def main():
    # logging.basicConfig(
    #     level=logging.DEBUG, 
    #     format= f"{util.bcolors.OKBLUE}|*pdfmanager|{util.bcolors.ENDC} %(message)s."
    #     )

    # parser = argparse.ArgumentParser(
    #     description="Manage your pdfs. (for the moment only rename them)", 
    #     prog = "pdfmanager",
    # )
    # parser.add_argument('-f', '--filepath', help='the pdf to rename', nargs='?')
    # parser.add_argument('-d', '--dirpath', help='the folder containing the pdfs to rename', nargs='?')

    # args = vars(parser.parse_args())

    # if args.get('dirpath') is not None :
    #     dirpath = args.get('dirpath')
    #     renamer.process_all_pdf_in_dir(dirpath)
        
    # elif args.get('filepath') is not None : 
    #     filepath =  args.get('filepath')
    #     renamer.process_pdf(filepath)

