from dotenv import load_dotenv
import os, shutil, pathlib

def store_in_missing(pdf_path:str) :
    dotenv_path = os.path.join(pathlib.Path(__file__).parent.parent.absolute(), '.env')
    load_dotenv(dotenv_path)
    directory = os.environ.get("SHELFPATH")
    missing_directory = os.path.join( directory,  "missing")
    # check if missing folder exist 
    if not os.path.isdir(missing_directory) : 
        os.mkdir(missing_directory)
    # move file in this directory
    new_path_of_file = os.path.join(missing_directory, os.path.basename(pdf_path))
    shutil.move(pdf_path, new_path_of_file)
