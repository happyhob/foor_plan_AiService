import ultralytics
from ultralytics import YOLO
from glob import glob
import numpy as np
import json
import cv2
import torch
from PIL import Image


# IMAGE_DIR = "C:/Users/user/OneDrive - 우송대학교(WOOSONG UNIVERSITY)/바탕 화면/structure/image25.jpg"
IMAGE_DIR = "test.jpg"
MODEL_DIR ="C:/ai_test/best.pt"

image = Image.open(IMAGE_DIR)

# 이미지의 높이와 너비 가져오기
width, height = image.size

print("Width:", width)
print("Height:", height)
print("--------------------------------------------------------------------")

model = YOLO(MODEL_DIR)


result = model.predict(source=IMAGE_DIR, save=True)
points = result[0].masks.xy

#추출한 좌표를 리스트 형태로 만듬
seg =[]
for point in points:
    if isinstance(point, torch.Tensor):
        point = point.cpu().detach().numpy()
    seg.append(point.tolist())

#리스트를 딕셔너리 형로 만듬
point ={}
for i in range(0,len(seg)-1):
    point["points{}".format(i)]=seg[i]

dic1 = {
    "label":"room",
}
for i in range(0,len(seg)-1):
    dic1["points{}".format(i)]=seg[i]

with open('output.json', 'w') as json_file:
    json.dump(dic1, json_file)

print(dic1)

#print(point)
# for point in points :
#     print(point.cpu().detach().numpy().tolist())



