from sqlite3 import Date
from pdfminer.pdfparser import PDFParser, PDFSyntaxError
from pdfminer.pdfdocument import PDFDocument

def get_title_from_filepath(filepath:str) -> str or None :
    with open(filepath, 'rb') as f : 
        try : 
            parser = PDFParser(f)
            doc = PDFDocument(parser)
            infos = doc.info[0]
            if 'Title' in infos.keys() :
                title = doc.info[0]['Title']
                return title
            else :
                return None
        except PDFSyntaxError :
            return None

def get_date_from_filepath(filepath:str) -> str or None :
    with open(filepath, 'rb') as f : 
        try :
            parser = PDFParser(f)
            doc = PDFDocument(parser)
            infos = doc.info[0]
            if 'CreationDate' in infos.keys() :
                date = doc.info[0]['CreationDate']
                return date
            else :
                return None
        except PDFSyntaxError :
            return None