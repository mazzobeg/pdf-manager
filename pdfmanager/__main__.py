import argparse
import pathlib
import logging

from regex import A
from pdfmanager import renamer, pdf, manager
import os

def main():
    logging.basicConfig(level=logging.DEBUG)

    parser = argparse.ArgumentParser(description="Rename your pdf.")
    parser.add_argument('--filePath', type=str, nargs = '+', help='PDF to be renamed')
    parser.add_argument('--dirPath', type=str, nargs = '+', help='Dir which contain pdfs to be renamed')
    args = vars(parser.parse_args())

    if args.get('dirPath') is not None :
        dirpath = args.get('dirPath')[0]
        for file in pathlib.Path(dirpath).iterdir() : 
            if os.path.isfile(file): 

                title = pdf.get_title_from_filepath(file.absolute())
                date = pdf.get_date_from_filepath(file.absolute())

                if not title is None and not date is None : 
                    title = str(title)
                    date = str(date)
                    pretty_title = renamer.get_pretty_title(title, date)
                    if pretty_title == '' :
                        # store in missing folder
                        manager.store_in_missing(file.absolute())
                    else :
                        new_path = renamer.get_new_path(pretty_title)
                        renamer.rename_pdf(file.absolute(), new_path)
                else : 
                    logging.warning(f'{os.path.basename(file.absolute())} have title of date as None : {title}, {date}')
                    manager.store_in_missing(file.absolute())

    elif args.get('filePath') is not None : 
        pass

