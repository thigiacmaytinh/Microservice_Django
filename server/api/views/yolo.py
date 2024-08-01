from rest_framework.decorators import api_view
from dateutil.parser import parse
from api.apps import *

from lib.TGMT.TGMTimage import *
from lib.TGMT.TGMTfile import *
from lib.TGMT.TGMTmat import IsMatEmpty
from lib.TGMT.TGMTpaging import Paging
import time
import cv2

from lib.modulemgr import GetAvailableYoloDetector, yoloDetectors, yoloDetectorAvailables
from django.conf import settings


####################################################################################################

@api_view(["POST"])           
def DetectYOLO(request):
    try:
        startTime = time.time()
        now = utcnow()
        folder = "temp"
        _randFilename = GenerateRandFileName(".jpg")
        uploaded_file_abs = os.path.join(settings.MEDIA_ROOT, folder, _randFilename)
        imgPaths = SaveImageFromRequest(request, folder, _randFilename)

        if (imgPaths==[]):
            raise Exception("Không đọc được ảnh")
        frame = cv2.imread(os.path.join(settings.MEDIA_ROOT, imgPaths[0]))
               
        #detect images
        
        if(IsMatEmpty(frame)):
            return ErrorResponse("Không đọc được ảnh")
            
        yoloDetector = GetAvailableYoloDetector()
        while(yoloDetector == -1):
            time.sleep(0.5)
            yoloDetector = GetAvailableYoloDetector()

        yoloDetectorAvailables[yoloDetector] = False    
        ret = yoloDetectors[yoloDetector].detect(frame)
        yoloDetectorAvailables[yoloDetector] = True

        
    
        return ObjResponse({"ret": ret})
    except Exception as e:     
        return ErrorResponse(str(e))        

####################################################################################################

