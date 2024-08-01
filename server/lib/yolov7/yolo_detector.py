import sys
import os

__dir__ = os.path.dirname(os.path.abspath(__file__))
sys.path.append(__dir__)
sys.path.insert(0, os.path.abspath(os.path.join(__dir__, '..')))

import math
import cv2
import argparse
import time
import torch
import torch.backends.cudnn as cudnn
import numpy as np
import torchvision.transforms as transforms
import torch.nn as nn

from models.experimental import attempt_load
from torchvision.ops import nms
from pathlib import Path
from PIL import Image, ImageOps #Install pillow instead of PIL
from numpy import random
from django.conf import settings

from utils.general import non_max_suppression


def readYoloClassNames(file_path):
        with open(file_path, 'r') as file:
            class_names = file.read().strip().split('\n')
        return class_names

####################################################################################################

class YOLODetector():

    #reduce using VRAM
    np.set_printoptions(suppress=True)

    cuda = torch.cuda.is_available()

    #device = torch.device('cuda:0' if cuda else 'cpu')
    device = torch.device('cpu')

    currentDir = os.path.dirname(os.path.abspath(__file__))
    modelPath = os.path.join(currentDir, "yolov7.pt")
    classNamePath = os.path.join(currentDir, 'coco.names')
    conf_thres = settings.CONF_THRES
    iou_thres = settings.IOU_THRES


    model = attempt_load(modelPath, map_location=device)

    classes = readYoloClassNames(file_path=classNamePath)

    ####################################################################################################

    def check_img_size(self, img_size, s=32):
        # Verify img_size is a multiple of stride s
        s = int(s)
        new_size = math.ceil(img_size / s) * s  # ceil gs-multiple
        if new_size != img_size:
            print('WARNING: --img-size %g must be multiple of max stride %g, updating to %g' % (img_size, s, new_size))
        return new_size

    ####################################################################################################

    def ConvertMatToPil(self, mat):
        # You may need to convert the color.
        mat = cv2.cvtColor(mat, cv2.COLOR_BGR2RGB)
        im_pil = Image.fromarray(mat)
        return im_pil

    ####################################################################################################

    

    def detect(self, mat):
        class_names = []

        half = self.device.type != 'cpu' # half precision only supported on CUDA
        # stride = int(self.model.stride.max())
        # imgsz = self.check_img_size(imgsz, s=stride)  # check img_size

        imgsz = 224

        # if half:
        #     self.model.half()  # to FP16

        transform = transforms.Compose([
        transforms.Resize((imgsz, imgsz)),
        transforms.ToTensor(),
    ])
        img = transform(self.ConvertMatToPil(mat)).unsqueeze(0)

        # if self.cuda:
        #     img = img.cuda()

        with torch.no_grad():
            pred = self.model(img)[0]
        
        # Apply NMS
        pred = non_max_suppression(pred, self.conf_thres, self.iou_thres)
        
        for i, det in enumerate(pred):
            for i, res in enumerate(det):
                class_names.append(self.classes[int(res.cpu().numpy()[-1])])

        return class_names
        




