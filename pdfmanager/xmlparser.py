import time
from googletrans import Translator
from string import printable
import xml.etree.ElementTree as ET
import numpy as np

from .calculator import centroid, compareBbox, bboxWithWH

def getBboxFromElement(element) :
    """ Getter of bbox with element of xml tag.

    Args:
        element (ElementTree.Element): element of xml tree.

    Returns:
        list : [xBottomLeft, yBottomLeft, w, h]
    """
    if not 'bbox' in element.attrib.keys() : return -1
    return [float(x) for x in element.attrib['bbox'].split(',')]

def textBoxToText(textbox) :
    """_summary_

    Args:
        textbox (_type_): _description_

    Returns:
        _type_: _description_
    """
    translator = Translator()
    words = []
    for textline in textbox :
        if textline.tag == 'textline' :
            for text in textline :
                if text.tag == 'text' :
                    words.append(str(text.text))
    text = ''.join(words)
    text = text.replace('\n', '')
    text = text.replace('None', '[~]')
    # try :
    #     text = translator.translate(text, 'fr', 'en').text
    # except :
    #     time.sleep(2)
    #     text = translator.translate(text, 'fr', 'en').text
    #text = ''.join(char for char in text if char in printable)
    return text

def wellFormatXml(xmlPath:str) :
    with open(xmlPath, 'r') as f :
        xmlDatas = f.read()
    xmlDatasWellFormat = ''.join(char for char in xmlDatas if char in printable)
    with open(xmlPath, 'w') as f :
        f.write(xmlDatasWellFormat)

def mergeAllTextBox(path) :
    tree = ET.parse(path)
    root = tree.getroot()
    for page in root :
        mergeTextboxes(page)
    tree.write(path)

def removeNoTextBox(tmpXmlPath) :
    tree = ET.parse(tmpXmlPath)
    root = tree.getroot()
    for page in root :
        to_remove = []
        for element in page:
            if element.tag != "textbox" :
                to_remove.append(element)
        for element in to_remove :
            page.remove(element)
    tree.write(tmpXmlPath)

def mergeTextbox(src, dest) :
    yDest = np.array([centroid(getBboxFromElement(x))[1] for x in dest])
    # foreach textline src
    for textline in src :
        # find textline dest
        ySrc = centroid(getBboxFromElement(textline))[1]
        idTextline = np.argmin(abs(yDest - ySrc))
        destTextline = dest[idTextline]
        # foreach word src 
        for word in textline : 
            # find previous word in textline dest
            try :
                xDest = np.array([getBboxFromElement(x)[0] for x in destTextline])
                xSrc = getBboxFromElement(word)[0]
                idPreviousWord = np.argmin(abs(yDest - ySrc))
                # insert word
                destTextline.insert(idPreviousWord+1, word)
            except : 
                pass

def mergeTextboxes(textboxes:list) :
    toMerge = {}
    for textbox1 in textboxes :
        for textbox2 in textboxes : 
            if textbox1.attrib['id'] != textbox2.attrib['id'] :
                comparaison = compareBbox(getBboxFromElement(textbox1), getBboxFromElement(textbox2))
                if comparaison == 1 :
                    toMerge[int(textbox1.attrib['id'])] = int(textbox2.attrib['id'])
                else :
                    pass
    for key, value in toMerge.items() :
        mergeTextbox(textboxes[key], textboxes[value])
    for key in list(toMerge.keys())[::-1] :
        textboxes.remove(textboxes[key])
    return textboxes

def isValidTextBox(textbox, format) :
    bbox = getBboxFromElement(textbox)
    bbox = bboxWithWH(bbox)
    if bbox[2] > (((format[0])/2) - 100):
        return True
    else :
        return False

def getDictFromXml(xmlPath) : 
    dic = {}
    # fetch modeled xml
    tree = ET.parse(xmlPath)
    root = tree.getroot()
    # fetch document dimensions
    bboxFirstPage = ([float(x) for x in root.find('page').attrib['bbox'].split(',')])
    format = (bboxFirstPage[2], bboxFirstPage[3])
    dic['docInfo'] = {
        'width' : format[0],
        'height' : format[1]
    }
    dic['pages'] = {}
    for page_id in range(len(root)) :
        dic['pages'][str(page_id)] = {}
        # fetch textbox
        textboxes = [x for x in root[page_id] if x.tag == 'textbox']
        for textbox_id in range(len(textboxes)) : 
            dic['pages'][str(page_id)][str(textbox_id)] = {}
            # check if is valid
            if isValidTextBox(textboxes[textbox_id], format) :
                # get bbox from tag
                bbox = getBboxFromElement(textboxes[textbox_id])
                # convert xyxy to xywh
                bbox = bboxWithWH(bbox)
                # get text of textbox
                text = textBoxToText(textboxes[textbox_id])
                dic['pages'][str(page_id)][str(textbox_id)]['bbox'] = bbox
                dic['pages'][str(page_id)][str(textbox_id)]['text'] = text  
    return dic