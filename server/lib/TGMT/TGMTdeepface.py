import cv2

def DrawRects(mat, boxes):
    for box in boxes:
        box = box["facial_area"]
        cv2.rectangle(mat, (box['x'], box['y']), (box['x'] + box['w'], box['y'] + box['h']), color=(255,0,0))

####################################################################################################

def DrawRect(mat, box):
    print(box)
    cv2.rectangle(mat, (box['x'], box['y']), (box['x'] + box['w'], box['y'] + box['h']), color=(255,0,0))

####################################################################################################

def GetBestRect(boxes):
    result = None
    confidence = 0 
    for box in boxes:
        if(box["confidence"] > confidence):
            confidence = box["confidence"]
            result = box["facial_area"]
    return result

####################################################################################################

def MakeSquare(box):
    if(box['w'] > box['h']):        
        box['y'] -= int((box['w'] - box['h']) /2)
        box['h'] = box['w']
    else:
        box['x'] -= int((box['h'] - box['w']) /2)
        box['w'] = box['h']
    return box