from fastapi import FastAPI, UploadFile, HTTPException
from starlette.responses import FileResponse
import os
import subprocess
from ai_model import MyClass
import json

IMAGE_DIR = os.path.abspath(r"C:/Users/user/OneDrive - 우송대학교(WOOSONG UNIVERSITY)/바탕 화면/seg-model/image")
MODEL_DIR = "C:/Users/user/OneDrive - 우송대학교(WOOSONG UNIVERSITY)/바탕 화면/seg-model/best.pt"
RESULT_DIR = os.path.abspath(r"C:/Users/user/OneDrive - 우송대학교(WOOSONG UNIVERSITY)/바탕 화면/seg-model/output")

class Connect2():
    file_total_path = None
    file_name = None
    app = FastAPI()
    image_name = None


    @app.get("/")
    def read_root():
        return {"Hello": "World"}
    

    @app.post("/photo")
    async def upload_photo(file: UploadFile, newname: str):
        #이미지 가져오기
        content = await file.read()
        path = load(content,newname)

        # YOLO 객체 탐지 실행
        polygon_data_json = MyClass.pointdata(MODEL_DIR,path)
        # 3D모델링 파일 전송
        
        
        output_glb_path= blender_run(newname,polygon_data_json)
        return FileResponse(output_glb_path, media_type='application/octet-stream', filename=f"{newname}.glb")
    
        #return image_upload(newname,point)



def load(content,newname):
    file_name = f"{newname}.jpg"
    file_total_path = os.path.join(IMAGE_DIR, file_name)

    with open(file_total_path, "wb") as fp:
        fp.write(content)
    image_p = "C:/Users/user/OneDrive - 우송대학교(WOOSONG UNIVERSITY)/바탕 화면/seg-model/image/"+file_name
    return image_p


def blender_run(newname,point_json):
    output_glb_path = os.path.join(RESULT_DIR, f"{newname}.glb")
    blender_path = "C:/Program Files/Blender Foundation/Blender 4.0/blender.exe"  # Blender 실행 파일 경로
    script_path = "C:/Users/user/OneDrive - 우송대학교(WOOSONG UNIVERSITY)/바탕 화면/seg-model/bpy.py"      # VS Code에서 작성한 스크립트 경로
    subprocess.run([blender_path, "-b", "-P", script_path, "--", point_json, output_glb_path])
    return output_glb_path

