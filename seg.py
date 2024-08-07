import ultralytics
from ultralytics import YOLO
from glob import glob
import numpy as np
import json
import cv2

# IMAGE_DIR = "C:/Users/user/OneDrive - 우송대학교(WOOSONG UNIVERSITY)/바탕 화면/structure/image25.jpg"
IMAGE_DIR = "enhanced_contrast_image.jpg"
MODEL_DIR ="C:/ai_test/best.pt"


model = YOLO(MODEL_DIR)


result = model.predict(source=IMAGE_DIR, save=True)
mask = result[0].masks
xy_data = mask.xy

print(xy_data)


