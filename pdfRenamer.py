from sre_compile import isstring
from pdfminer.pdfparser import PDFParser, PDFSyntaxError
from pdfminer.pdfdocument import PDFDocument
from nltk.tokenize import word_tokenize
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords

import nltk
import argparse
import os
import pathlib
import string
import random
import re

def prepare_pdf_string(lambda_string) :
    lambda_string = str(lambda_string)
    return lambda_string[2:-1]

def pretty_title2(title) : 
    title = pretty_title(title)
    new_title = title.split('_')
    new_title = [x[0].upper() for x in new_title]
    return ''.join(new_title) + '.pdf'

def pretty_title(title, date) :
    new_title = prepare_pdf_string(title)
    year = str(date)
    # remove pseudo hexa
    new_title = re.sub('[xX][0-9a-fA-F]+','', new_title) 
    new_title = new_title.replace('\\', '')
    new_title = new_title.replace(':', '')
    new_title = new_title.replace('?', '')


    tokens = word_tokenize(new_title)
    tokens = [w.lower() for w in tokens]
    table = str.maketrans('', '', string.punctuation)
    stripped = [w.translate(table) for w in tokens]
    words = [word for word in stripped if word.isalpha()]

    stop_words = set(stopwords.words('english'))
    words = [w for w in tokens if not w in stop_words]
    porter = PorterStemmer()
    stemmed = [porter.stem(word) for word in words]
    stemmed = [s.capitalize() for s in stemmed]
    stemmed = ''.join(stemmed)
    
    return f"[{year[4:8]}]" + stemmed + ".pdf"
    # valid_characters = string.printable
    # new_title = prepare_pdf_string(title)
    # new_title = ''.join(str(i) for i in new_title if str(i) in valid_characters)
    # new_title = new_title.replace(" ", '_')
    # new_title = new_title.lower()
    # new_title = new_title.replace('-', '_')
    # new_title = new_title.replace(':', '_')
    # new_title = new_title.replace('/', '')
    # new_title = new_title.replace('__', '_')
    
    # new_title_as_array = new_title.split('_')
    # print(new_title_as_array)
    # random.shuffle(new_title_as_array)
    # print(new_title_as_array[0:3])
    # tmp = []
    # # remove accessor words
    # # short words
    # # for w in new_title_as_array : 
    # #     if len(w) > 3 :
    # #         tmp.append(w[0:5])
    # # new_title = '_'.join(tmp)
    # return new_title + ".pdf"

def rename_file(path) :
    path_to_pdf = path 
    fp = open(path_to_pdf, 'rb')
    try :
        parser = PDFParser(fp)
        doc = PDFDocument(parser)
        if 'Title' in doc.info[0].keys() :
            if isstring(doc.info[0]['Title']) and len(doc.info[0]['Title']) <= 2 : 
                print('Oops title is weird on this document.')
            else : 
                #directory = '/'.join(path_to_pdf.split('/')[:-1])
                directory = pathlib.Path(path_to_pdf).parent.absolute()
                #directory = os.path.basename(your_path)
                new_title = pretty_title(doc.info[0]['Title'], doc.info[0]['CreationDate'])

                if os.path.exists(os.path.join(directory, new_title)) : 
                    print('Un fichier portant se nom existe déjà.')
                else :
                    fp.close()
                    os.rename(path_to_pdf, os.path.join(directory, new_title))
        else : 
            print('Oops title not exist on this document.')
    except PDFSyntaxError :
        print('chelou')

def is_valid(pdf_document) :
    return 'Title' in doc.info[0].keys() 

if __name__ == "__main__" :  

    nltk.download('punkt')
    nltk.download('stopwords')

    parser = argparse.ArgumentParser(description="Rename your pdf.")
    parser.add_argument('--filePath', type=str, nargs = '+', help='PDF to be renamed')
    parser.add_argument('--dirPath', type=str, nargs = '+', help='Dir which contain pdfs to be renamed')

    args = vars(parser.parse_args())

    # if dir which contain pdfs
    if args.get('dirPath') is not None :
        dir_path = str(' '.join(args.get('dirPath')))
        for file in pathlib.Path(dir_path).iterdir() : 
            rename_file(str(file))
    elif args.get('filePath') is not None : 
        path_to_pdf = str(' '.join(args.path_to_pdf))
        rename_file(path_to_pdf)
        

