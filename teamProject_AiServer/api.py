'''
실질적인 통신의 파일(FastAPI)

POST로 요청이 들어오면
    1. controller.py의 controller() 클래스를 통해 클라이언트가 넘겨준 파일명과 파일을 불러온다.
    2. 받은 이미지 파일을 ai_model.py에 MyClass로 넘겨서 추출한 좌표값을 json형식으로 얻어온다.
    3. 추출한 좌표값을 controller.py의 controller() 을 통해 bpy.py를 실행시킨다
    4. 3을 통해 3D모델링 된 .glb파일을 클라이언트에게 넘겨준다


'''
from fastapi import FastAPI, UploadFile, Form, File, Request
from fastapi.responses import Response
from control import Control
from ai_model import async_pointdata
from fastapi.middleware.cors import CORSMiddleware
#from request import Request
import os
import json


from typing import List
import base64
import io
import asyncio
###################################################

MODEL_DIR = "best5.pt"
#POINT_JSON_DIR = "C:/Users/wjdtj/OneDrive/바탕 화면/teamProject_AiServer/teamProject_AiServer/point.json"
#TEXT_JSON_DIR = "C:/Users/wjdtj/OneDrive/바탕 화면/teamProject_AiServer/teamProject_AiServer/text.json"

class Api():
    app = FastAPI()

    app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 도메인 허용 (운영 환경에서는 수정 필요)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    )


    @app.post("/model")
    async def upload_photo(floors: List[UploadFile] = File(...)): #스프링 서버로부터 파일을 받음
        # 만들어진 glb파일들의 경로들을 담음
        floor_glbs=[]

        # 바이트로 변환한 glb를 담는 딕셔너리
        floor_byes = {}

        # json 메타데이터를 담는 딕셔너리
        meta_datas = {}

        # 좌표값을 저장하는 임시파일 생성
        POINT_JSON_DIR = Control.point_file()

        # 텍스트를 저장하는 임시파일 생성
        TEXT_JSON_DIR = Control.text_file()

        # 업로드된 파일 리스트를 순회하면서, 각 파일과 그 인덱스를 반환합니다.
        for index, floor in enumerate(floors):
            content = await floor.read()
            # 업로드 받은 이미지 파일을 읽어 임시파일에 저장
            image_path = Control.load(content)
            # 비동기로 ai모델을 이용해 좌표값,텍스트를 임시파일에 저장
            await async_pointdata(MODEL_DIR,image_path,POINT_JSON_DIR,TEXT_JSON_DIR)
            # 임시파일의 좌표값을 이용해 블랜더를 사용/  결과물은 생성된 이미지의 파일경로
            output_glb_path = await Control.run_floor_blender(POINT_JSON_DIR, image_path)

            # 임시파일에 들어있는 json을 리스트에 담음
            with open(TEXT_JSON_DIR, 'r') as json_file2:
                json_data = json.load(json_file2)
                meta_json = json.dumps(json_data)
                meta_datas[index+1] = meta_json

            # 이미지를 저장했던 임시파일을 제거 *** 사용이 끝남 (content = await floor.read()여기서 만들어짐)
            if os.path.exists(image_path):
                os.remove(image_path)

            # 생성된 glb파일을 읽어 바이트로 딕셔너리에 저장
            with open(output_glb_path, "rb") as glb_file:
                floor_byte: bytes = glb_file.read()
                floor_byes[index + 1] = floor_byte

            # 건물을 만들기 위해 생성된 glb 파일을 보관
            floor_glbs.append(output_glb_path)

        # 건물생성 블랜더로 보관된 glb파일을 넘김
        building_glb_path = await Control.run_building_blender(floor_glbs) #👍👍👍👍👍👍👍👍👍👍👍👍👍👍👍👍👍👍👍👍👍👍👍👍
        with open(building_glb_path, "rb") as building_file:
            building_glb = building_file.read()

        # ✌✌✌✌✌ 스프링 서버로 보내는 응답하는 부분 ✌✌✌✌✌
        # 바이트를 json형태로 스프링서버로 응답하기위해 utf-8로 변환
        encoded_building_glb = base64.b64encode(building_glb).decode('utf-8').rstrip('=')
        encoded_glb_paths = {key: base64.b64encode(value).decode('utf-8').rstrip('=') for key, value in floor_byes.items()}
        encoded_metadata = {key:  base64.b64encode(str(value).encode('utf-8')) for key, value in meta_datas.items()}

        # 층의glb파일, 빌딩glb파일을 저장하는임시 파일 삭제
        Control.delete_temp_file(output_glb_path)
        Control.delete_temp_file(building_glb_path)
        Control.delete_temp_file(POINT_JSON_DIR)
        Control.delete_temp_file(TEXT_JSON_DIR)

        # 인코딩된 데이터를 json형태로 반환
        return {

            "buildingData": encoded_building_glb,
            "floorData": encoded_glb_paths,
            "metaData": encoded_metadata
        }
    


    @app.post("/model/addPartial")
    async def update_floor(floor: UploadFile = File(...)):

        content = await floor.read()

        image_path = Control.load(content)
        POINT_JSON_DIR = Control.point_file()
        TEXT_JSON_DIR = Control.text_file()

        # 받은 이미지 정보를 통해 AI 모델에 넘겨 좌표값 추출
        await async_pointdata(MODEL_DIR,image_path,POINT_JSON_DIR,TEXT_JSON_DIR)

        # output_glb_path = Controller.blender_run(buildingName, polygon_data_json,image)
        output_glb_path = await Control.run_floor_blender(POINT_JSON_DIR, TEXT_JSON_DIR, image_path)



        #✌✌✌✌✌ 스프링 서버로 보내는 응답하는 부분 ✌✌✌✌✌ 
        with open(output_glb_path, "rb") as glb_file:
            building_glb = glb_file.read()  # base64.b64decode(glb_file.read())

        if os.path.exists(image_path):
            os.remove(image_path)
            os.path.exists(image_path)



        # 응답 반환
        encoded_building_glb = base64.b64encode(building_glb).decode('utf-8')

        Control.delete_temp_file(output_glb_path)
        Control.delete_temp_file(POINT_JSON_DIR)
        Control.delete_temp_file(TEXT_JSON_DIR)

        return {
            "floorData": encoded_building_glb
        }