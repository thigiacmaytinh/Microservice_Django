
import os
import face_recognition
import json
from api.apps import *
from api.models import Appear

####################################################################################################

def TriggerCuda():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    imagePathAbs = os.path.join(BASE_DIR, "..", "lib", "dlib", "do_not_delete_this_file.jpg")
    image = face_recognition.load_image_file(imagePathAbs)
    landmarks = face_recognition.face_encodings(image)    

####################################################################################################

def ScheduleJob():
    lastAppear = Appear.objects(isDeleted=False).order_by("-timeAppear").limit(1).first()
    if(lastAppear != None):
        numSecondFromLastTimeAppear = int((utcnow() - lastAppear.timeAppear).total_seconds())   
        if(numSecondFromLastTimeAppear > 60):
            TriggerCuda()