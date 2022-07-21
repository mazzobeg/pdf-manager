import numpy as np

def centroid(bbox) :
    """ Get centroid from bbox.

    Args:
        bbox (list): [xBottomLeft,yBottomLeft,w,h]

    Returns:
        tuple: (mean of with, mean of height)
    """
    return (np.mean([bbox[0],bbox[2]]), np.mean([bbox[1],bbox[3]]))

def compareBbox(bbox1, bbox2) :
    """ Check if bbox is included in bbox2.

    Args:
        bbox1 (list): [xBottomLeft,yBottomLeft,w,h]
        bbox2 (list): [xBottomLeft,yBottomLeft,w,h]

    Returns:
        int : 1 if is included 0 otherwise
    """
    if (bbox1[0] >= bbox2[0] -5 
    and bbox1[1] >= bbox2[1] -5
    and bbox1[2] <= bbox2[2] +5
    and bbox1[3] <= bbox2[3] +5) :
        return 1
    else :
        return 0


#
def bboxFromBLtoTL(bbox, gridHeight, wh=False) : 
    """_summary_

    Args:
        bbox (list): _description_
        gridHeight (float): _description_
        wh (bool, optional): _description_. Defaults to False.

    Returns:
        _type_: _description_
    """
    if wh :
        return [bbox[0], gridHeight-bbox[1], bbox[2], -bbox[3]]
    else :
        return [bbox[0], gridHeight-bbox[1], bbox[2], gridHeight-bbox[3]]

def bboxWithWH(bbox) :
    return [bbox[0], bbox[1], bbox[2]-bbox[0], bbox[3]-bbox[1]]
