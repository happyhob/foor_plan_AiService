'''
fastAPT 실행부에서 사용하는 매서드!
    -load(content,newname) 함수를 통해서 이미지 파일을 저장하고, 이미지 경로를 넘겨줌

    -blender_run(newname,point_json) 모델을 통해 얻은 좌표를 실질적으로 처리하는 부분
        -> 최종 .glb 파일을 얻을 수 있다
'''

import subprocess
import os

IMAGE_DIR = os.path.abspath(r"C:/Users/user/OneDrive - 우송대학교(WOOSONG UNIVERSITY)/바탕 화면/seg-model/image")
RESULT_DIR = os.path.abspath(r"C:/Users/user/OneDrive - 우송대학교(WOOSONG UNIVERSITY)/바탕 화면/seg-model/output")

class Controller:
    def load(content,newname):
        #저장할 파일 이름과, 저장할 경로
        file_name = f"{newname}.jpg"
        file_total_path = os.path.join(IMAGE_DIR, file_name)

        #원본 사진 저장
        with open(file_total_path, "wb") as fp:
            fp.write(content)

        #AI_MODEL에 넘겨줄 형식으로 경로 변환
        image_p = "C:/Users/user/OneDrive - 우송대학교(WOOSONG UNIVERSITY)/바탕 화면/seg-model/image/"+file_name
        return image_p


    def blender_run(newname,point_json):
        #.glb파일 경로 설정
        output_glb_path = os.path.join(RESULT_DIR, f"{newname}.glb")
        # Blender 실행 파일 경로
        blender_path = "C:/Program Files/Blender Foundation/Blender 4.0/blender.exe" 
        # 블랜더에서 실행할 Script
        script_path = "C:/Users/user/OneDrive - 우송대학교(WOOSONG UNIVERSITY)/바탕 화면/seg-model/bpy.py"
        #Blender 실행      
        subprocess.run([blender_path, "-b", "-P", script_path, "--", point_json, output_glb_path])
        
        #.glb파일의 경로를 넘겨준다
        return output_glb_path