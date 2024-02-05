import bpy
import bmesh
import os
import sys


blender_onefloor_path = os.path.abspath("C:/teamProject_AiServer/blender_file/building_1.blend")
blender_file_path = os.path.abspath("C:/teamProject_AiServer/blender_file/building_2.blend")

#블랜더 건물 층별 객체 확인목적
output_blend_path = os.path.abspath("C:/teamProject_AiServer/blender_file/blederTest.blend")

def buildBuilding(floor_glbs, output_gltf_path):

    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

    current_z_offset = 0
    z_gap = 300  # 오브젝트 간 Z축 간격
    object_counter = 1  # 오브젝트 카운터


    # 병합된 GLB 파일들을 가져와서 층별로 쌓기
    for file_path in floor_glbs:
        # GLB 파일 가져오기
        bpy.ops.import_scene.gltf(filepath=file_path)

        # 가져온 오브젝트들을 선택
        bpy.ops.object.select_all(action='DESELECT')
        for obj in bpy.context.scene.objects:
            if obj.type == 'MESH':
                obj.select_set(True)

        # 병합된 오브젝트의 이름을 숫자로 설정
        bpy.context.object.name = str(object_counter)
        object_counter += 1  # 오브젝트 카운터 증가

        # 병합된 오브젝트의 위치를 조정
        bpy.context.object.location.z = current_z_offset

        # 다음 오브젝트의 Z 위치를 계산
        current_z_offset += z_gap

    # 최종 GLB 파일 저장

    bpy.ops.export_scene.gltf(filepath=output_gltf_path, export_format='GLB', use_selection=False)


def join_and_replace_glbs(floor_glbs):
    print(f"{floor_glbs}**************************************************")
    for glb_path in floor_glbs:
        # GLB 파일 가져오기
        bpy.ops.import_scene.gltf(filepath=glb_path)

        # 가져온 오브젝트들을 선택
        bpy.ops.object.select_all(action='DESELECT')
        for obj in bpy.context.scene.objects:
            if obj.type == 'MESH':
                obj.select_set(True)

        # 선택된 오브젝트가 있다면 병합
        if bpy.context.selected_objects:
            # 액티브 오브젝트를 설정
            bpy.context.view_layer.objects.active = bpy.context.selected_objects[0]
            # 선택된 오브젝트를 병합
            bpy.ops.object.join()

            # 병합된 오브젝트를 GLB 파일로 내보내기
            bpy.ops.export_scene.gltf(filepath=glb_path, export_format='GLB', use_selection=True)

        # 다음 파일을 처리하기 전에 씬을 클리어
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete()






if __name__ == "__main__":
    if len(sys.argv) < 4:  # JSON 데이터와 GLTF 파일 경로
        print("Not enough arguments provided.")
        sys.exit(1)
    argv = sys.argv[sys.argv.index("--") + 1:]  # "--" 이후의 인자들만 추출
    glb_paths = argv[:-1]  # 마지막 인자 전까지가 GLB 파일 경로들
    output_gltf_path = argv[-1]  # 마지막 인자가 출력 GLB 파일 경로

    join_and_replace_glbs(glb_paths)

    buildBuilding(glb_paths, output_gltf_path)


