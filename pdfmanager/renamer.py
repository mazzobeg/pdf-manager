from posixpath import dirname
from nltk.tokenize import word_tokenize
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
from dotenv import load_dotenv

import string, random, re, os, logging

def get_pretty_title(title:str, date:str) -> str: 
    """Remake current title in document.

    Args:
        title (str): Current title in metadata
        date (str): Current date in metadate

    Returns:
        str: New title
    """
    
    title = title.replace('\\t', ' ')
    title = title.replace('\\n', ' ')

    new_title = title[2:-1]

    # remove pseudo hexa
    new_title = re.sub('[xX][0-9a-fA-F]+','', new_title) 
    new_title = new_title.replace('\\', '')
    new_title = new_title.replace(':', '')
    new_title = new_title.replace('?', '')

    # remove punctuation
    new_title = new_title.translate(str.maketrans('', '', string.punctuation))

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
    
    new_named = f"[{date[4:8]}]" + stemmed + ".pdf"
    return new_named

def get_new_path(new_title:str, directory:str = None) -> str:
    """Get new path of document.

    Args:
        new_title (str): Title of document.
        directory (str, optional): Directory path of document. Defaults to None.

    Returns:
        str: Full path.
    """
    if directory is None : 
        dotenv_path = os.path.join(os.getcwd(), '.env')
        load_dotenv(dotenv_path)
        directory = os.environ.get("SHELFPATH")
        print(directory)
    return os.path.join(directory, new_title)

def rename_pdf(old_path:str, new_path:str) -> int:
    """Rename pdf.

    Args:
        old_path (str): Old absolute path.
        new_path (str): New absolute path.

    Returns:
        bool: If document was renamed return 1, 0 if title already exist, -1 if missing. 
    """
    # if file already exist
    ans = 1
    if os.path.exists(new_path) :
        logging.info(f"{os.path.basename(new_path)} Filename already exist… I while add an extension")
        ans = 0
        while os.path.exists(new_path) :
            dirpath = os.path.dirname(new_path)
            filename = os.path.basename(new_path)
            new_path = os.path.join(dirpath,increment_filename(filename))
    try :
        os.rename(old_path, new_path)
    except Exception : 
        ans = -1
    return ans

def increment_filename( filename : str ) -> str :
    finded = re.findall('\[\*[\d]+\]', filename)
    if len(finded) == 1 :
        finded = finded[0]
        sub = re.sub('\[\*[\d]+\]','', filename).split('.')[0]
        id_ = int(finded.split('*')[-1][0:-1])
        id_ += 1
        return sub + f'[*{id_}]' + '.pdf'
    # if first extension
    else : 
        filename_without_ext = filename.split('.')[0]
        new_filename = filename_without_ext + '[*1].pdf'
        return new_filename

