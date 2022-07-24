from googletrans import Translator, LANGUAGES
from string import printable
import time

from regex import T

def traduct(text, language) :
    # parse language
    parseLanguage = language.split('2')
    fromLanguage = parseLanguage[0]
    toLanguage = parseLanguage[1]
    if not fromLanguage in LANGUAGES.keys() or not toLanguage in LANGUAGES.keys() :
        raise Exception('Language not supported.')
    
    textSplitted : list[str] = text.split('.')
    translator = Translator()
    textSplittedTraducted = []
    for t in textSplitted :
        if len(t) > 1 :
            t = t.capitalize()
            try :
                traducted = translator.translate(t, toLanguage, fromLanguage).text
            except :
                time.sleep(2)
                traducted = translator.translate(t, toLanguage, fromLanguage).text
            textSplittedTraducted.append(traducted)
    traductedText = '.'.join(textSplittedTraducted)
    #traductedText = ''.join(char for char in traductedText if char in printable)
    return traductedText

