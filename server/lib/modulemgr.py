from django.conf import settings
 
if(settings.ENABLE_CHECK_YOLO):
    from lib.yolov7.yolo_detector import YOLODetector
     
yoloDetectors = []
yoloDetectorAvailables = []

def GetAvailableYoloDetector():
    for (i, yoloDetectorAvailable) in enumerate(yoloDetectorAvailables):
        if(yoloDetectorAvailable):
            return i
    
    if(len(yoloDetectors) < settings.NUM_THREAD):
        yoloDetectors.append(YOLODetector())
        yoloDetectorAvailables.append(True)
        return len(yoloDetectors) - 1

    return -1