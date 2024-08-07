'''
도면 이미지에서 객체를 추출하는 부분!
도면의 이미지를 넣어주면, 도면의 객체를 분류하고 각각 분류된 좌표값을 JSON 형식으로 보내준다.

__init__() : 모델을 불러온다

def get_image(self) : 이미지의 경로를 폴더단위로 넘겼을 때 test_image_list[]에 정렬하여 저장

def predict_image(self): 이미지 파일로 PREDICT 수행, 좌표값을 받는다

def get_point(self): 받은 좌표값을 필터링 하여 Blender에게 넘겨줄 수 있는 딕셔너리 형식으로 추출


class get_polygon: 사용자가 모델의 경로와, 이미지의 경로를 넣어주면 최종적인 json 파일 형식으로 추출 가능

'''


import ultralytics
from ultralytics import YOLO
from glob import glob
import numpy as np
import json
IMG_DIR = "C:/Users/user/OneDrive - 우송대학교(WOOSONG UNIVERSITY)/바탕 화면/structure/image25.jpg"
MODEL_DIR = "C:/Users/user/OneDrive - 우송대학교(WOOSONG UNIVERSITY)/바탕 화면/best.pt"

class MyClass:
    #model
    model = None
    #mask data
    xy_data = None
    #필요한 좌표값 저장
    polygons = {}
    #이미지 경로
    iamge_path = None

    test_image_list = []

    #초기화
    def __init__(self,model_dir,img_path):
        ultralytics.checks()
        self.model = YOLO(model_dir)  # load a pretrained YOLOv8n detection model
        self.iamge_path =img_path

    #이미지가 많을 때 모든 이미지 경로 추출
    def get_image(self):
        self.test_image_list = glob(self.iamge_path)
        print(len(self.test_image_list))
        self.test_image_list.sort()
        for i in range(len(self.test_image_list)):
            print('i = ',i, self.test_image_list[i])

    def predict_image(self):
        results = self.model.predict(source=self.iamge_path, save=True)
        mask = results[0].masks
        self.xy_data = mask.xy
        

    def get_point(self):
        for i in range(0,len(self.xy_data)-1):
            np.set_printoptions(precision=2)
            poligon =self.xy_data[i].tolist()
            self.polygons["polygon{}".format(i)] = poligon
        
        return self.polygons

class get_polygon:
    def pointdata(model, image):
        obj = MyClass(model,image )
        obj.predict_image()
        point = obj.get_point()
        polygon_data_json = json.dumps(point)
        return polygon_data_json


