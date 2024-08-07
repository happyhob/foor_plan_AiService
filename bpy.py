'''
blender에서 사용할 수 있는 python scprict!
(blender.exe 파일 경로/ 넘겨줄bpy 스크립트 경로 / 좌표.json/  file저장경로)를 매개변수로 받아서 실행가능

'''
import bpy
import bmesh
import sys
import json


def delete_all_objects():
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.object.select_by_type(type='MESH')
    bpy.ops.object.delete()

def delete_camera_and_lights():
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.object.select_by_type(type='CAMERA')
    bpy.ops.object.select_by_type(type='LIGHT')
    bpy.ops.object.delete()

def delete_setup():
    delete_all_objects()
    delete_camera_and_lights()

def create_polygon(coordinates, height, thickness):
    mesh = bpy.data.meshes.new(name="PolygonMesh")
    obj = bpy.data.objects.new("PolygonObject", mesh)
    bpy.context.collection.objects.link(obj)
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj

    # Get BMesh
    bm = bmesh.new()

    # Create vertices
    verts = [bm.verts.new((x, -y, 0)) for x, y in coordinates]

    # Create faces
    face_verts = [verts[i] for i in range(len(verts))]
    bm.faces.new(face_verts)

    # Extrude the face to create the height
    for face in bm.faces:
        face.select_set(True)

    extruded = bmesh.ops.extrude_face_region(bm, geom=bm.faces)
    vertices = [e for e in extruded['geom'] if isinstance(e, bmesh.types.BMVert)]
    bmesh.ops.translate(bm, vec=(0, 0, height), verts=vertices)  # 30m 높이로 이동


    # Update mesh with BMesh data
    bm.to_mesh(mesh)
    bm.free()

    solidify_modifier = obj.modifiers.new(name="Solidify", type='SOLIDIFY')
    solidify_modifier.thickness = 2

    bpy.context.view_layer.update()  # 시각적 업데이트 수행

    mesh.update()

def add_polygon_data(polygon_data, height):
    for polygon_name, coordinates in polygon_data.items():
        create_polygon(coordinates, height, 30)

def save_fbx_file(output_file_path):
    # 모든 오브젝트를 선택합니다 (FBX 내보내기 시 선택된 오브젝트만 내보내집니다)
    bpy.ops.object.select_all(action='SELECT')

    # FBX 파일로 내보내기를 수행합니다
    bpy.ops.export_scene.fbx(filepath=output_file_path, use_selection=True)
def save_gltf_file(output_file_path):
    # 모든 오브젝트를 선택합니다 (GLTF 내보내기 시 선택된 오브젝트만 내보내집니다)
    bpy.ops.object.select_all(action='SELECT')

    # GLTF 파일로 내보내기를 수행합니다
    bpy.ops.export_scene.gltf(filepath=output_file_path, export_format='GLTF_SEPARATE', use_selection=True)

def save_glb_file(output_file_path):
        # 모든 오브젝트를 선택합니다 (GLTF 내보내기 시 선택된 오브젝트만 내보내집니다)
        bpy.ops.object.select_all(action='SELECT')

        # GLTF 파일로 내보내기를 수행합니다
        bpy.ops.export_scene.glb(filepath=output_file_path, export_format='GLB', use_selection=True)

#-------------------------------------

#-------------------------------------
# 초기 설정 및 삭제 함수 호출
delete_setup()



'''
# 주어진 다각형 데이터에 대해 다각형 생성 함수 호출
# 모든 객체에 대한 Solidify modifier 적용
'''
def apply_solidify_modifier():
    for obj in bpy.context.scene.objects:
        if obj.type == 'MESH':
            solidify_mod = next((mod for mod in obj.modifiers if mod.type == 'SOLIDIFY'), None)
            if not solidify_mod:
                solidify_mod = obj.modifiers.new(name="Solidify", type='SOLIDIFY')
            solidify_mod.thickness = 2  # 두께를 2로 설정
            bpy.context.view_layer.objects.active = obj
            bpy.ops.object.modifier_apply(modifier=solidify_mod.name)
'''
매개변수 추가 부분
'''
if __name__ == "__main__":
    if len(sys.argv) < 4:  # JSON 데이터와 GLTF 파일 경로
        print("Not enough arguments provided.")
        sys.exit(1)

    polygon_data_json = sys.argv[-2]
    polygon_data = json.loads(polygon_data_json)
    add_polygon_data(polygon_data, 70)
    apply_solidify_modifier()

    output_gltf_path = sys.argv[-1]  # GLTF 파일 경로
    bpy.ops.export_scene.gltf(filepath=output_gltf_path, export_format='GLB', use_selection=True)  # GLTF 파일 저장
