import subprocess
import os
import tempfile
from PIL import Image

import asyncio
import sys
from concurrent.futures import ThreadPoolExecutor


class Control:
    @staticmethod
    def load(content):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp_file:
            tempimage = tmp_file.name
            tmp_file.write(content)
        return tempimage
        #좌표를 저장하는 임시파일 생성
    @staticmethod
    def point_file():
        with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as tmp_file:
            tempimage = tmp_file.name
        return tempimage

    #텍스트를 저장하는 임시파일 생성
    @staticmethod
    def text_file():
        with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as tmp_file:
            tempimage = tmp_file.name
        return tempimage

    
    @staticmethod
    async def run_floor_blender(json_data, list_data, image):
        blender_exe = "C:/Program Files/Blender Foundation/Blender 4.0/blender.exe"
        script_path = "floor_bpy2.py"

        with tempfile.NamedTemporaryFile(delete=False, suffix=".glb") as tmp_floor_file:
            tempfloor = tmp_floor_file.name

        img = Image.open(image)
        width, height = img.size

        print("json_data:",json_data,"\nlist_data:",list_data)

        def run_process():
            process = subprocess.run(
                [blender_exe, "-b", "-P", script_path, "--", list_data, str(width), str(height), json_data, tempfloor],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            return process.stdout, process.stderr, process.returncode

        with ThreadPoolExecutor() as executor:
            future = executor.submit(run_process)
            stdout, stderr, returncode = await asyncio.wrap_future(future)

        if returncode == 0:
            print(f"Blender finished with output: {stdout.decode()}")
        else:
            print(f"Blender finished with errors: {stderr.decode()}", file=sys.stderr)

        return tempfloor
    
    @staticmethod
    async def run_building_blender(count):
        blender_exe = "C:/Program Files/Blender Foundation/Blender 4.0/blender.exe"
        script_path = "building_bpy.py"

        with tempfile.NamedTemporaryFile(delete=False, suffix=".glb") as tmp_building_file:
            tempbuilding = tmp_building_file.name

        def run_process():
            process = subprocess.run(
                [blender_exe, "-b", "-P", script_path, "--", count, tempbuilding],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            return process.stdout, process.stderr, process.returncode

        with ThreadPoolExecutor() as executor:
            future = executor.submit(run_process)
            stdout, stderr, returncode = await asyncio.wrap_future(future)

        if returncode == 0:
            print(f"Blender finished with output: {stdout.decode()}")
        else:
            print(f"Blender finished with errors: {stderr.decode()}", file=sys.stderr)

        return tempbuilding

    @staticmethod
    def delete_temp_file(temp_path):
        # 임시 파일 삭제
        if os.path.exists(temp_path):
            os.remove(temp_path)
