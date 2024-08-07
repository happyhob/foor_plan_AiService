import ultralytics
from ultralytics import YOLO
from glob import glob
import numpy as np
import json
import cv2

# IMAGE_DIR = "C:/Users/user/OneDrive - 우송대학교(WOOSONG UNIVERSITY)/바탕 화면/structure/image25.jpg"
IMAGE_DIR = "test.jpg"
MODEL_DIR ="C:/ai_test/best.pt"


model = YOLO(MODEL_DIR)


result = model.predict(source=IMAGE_DIR, save=True)


#-----------------------------------seg info---------------------------------
# plots = result[0].plot()


# cv2.imshow("plot", plots)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

#-----------------------------------box info---------------------------------

boxes = result[0].boxes

for box in boxes :
    print(box.xyxy.cpu().detach().numpy().tolist())
    # print(box.conf.cpu().detach().numpy().tolist())
    # print(box.cls.cpu().detach().numpy().tolist())

#print(xy)