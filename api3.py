'''
실질적인 통신의 파일(FastAPI)

POST로 요청이 들어오면
    1. controller.py의 controller() 클래스를 통해 클라이언트가 넘겨준 파일명과 파일을 불러온다.
    2. 받은 이미지 파일을 ai_model.py에 MyClass로 넘겨서 추출한 좌표값을 json형식으로 얻어온다.
    3. 추출한 좌표값을 controller.py의 controller() 을 통해 bpy.py를 실행시킨다
    4. 3을 통해 3D모델링 된 .glb파일을 클라이언트에게 넘겨준다


'''
from fastapi import FastAPI, UploadFile, HTTPException
from starlette.responses import FileResponse
from controller import Controller
from ai_model import get_polygon
from fastapi.middleware.cors import CORSMiddleware

MODEL_DIR = "C:/Users/user/OneDrive - 우송대학교(WOOSONG UNIVERSITY)/바탕 화면/seg-model/model113.pt"

class Connect3():
    app = FastAPI()
    # CORS 설정을 추가합니다.
    app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 도메인 허용 (운영 환경에서는 수정 필요)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


    @app.get("/")
    def read_root():
        return {"Hello": "World"}
    

    @app.post("/photo")
    async def upload_photo(file: UploadFile, newname: str):

        #1.클라 요청파일 받는 부분
        content = await file.read()
        path = Controller.load(content,newname)

        #2. 받은 이미지 정보를 통해 ai 모델에 넘겨 좌표값 추출
        polygon_data_json = get_polygon.pointdata(MODEL_DIR,path)

        
        #3. 받은 좌표값을 controller로 넘겨 bpy.py파일 실행 하여 .glb 파일 저장
        output_glb_path= Controller.blender_run(newname,polygon_data_json)

        #4. glb 파일을 클라이언트에게 리턴
        return FileResponse(output_glb_path, media_type='application/octet-stream', filename=f"{newname}.glb")
    





