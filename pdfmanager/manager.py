def store_in_shelf(path_to_shelf : str, pdf_path:str) -> bool:
    pass

def save_in_summary(path_to_summary : str, pdf_path:str) -> bool :
    pass

from dotenv import load_dotenv
import os, shutil

def store_in_missing(pdf_path:str) :
    dotenv_path = os.path.join(os.getcwd(), '.env')
    load_dotenv(dotenv_path)
    directory = os.environ.get("SHELFPATH")
    missing_directory = os.path.join( directory,  "missing")
    # check if missing folder exist 
    if not os.path.isdir(missing_directory) : 
        os.mkdir(missing_directory)
    # move file in this directory
    new_path_of_file = os.path.join(missing_directory, os.path.basename(pdf_path))
    shutil.move(pdf_path, new_path_of_file)
