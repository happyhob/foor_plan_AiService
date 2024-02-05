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

def create_polygon(coordinates, height, thickness, polygon_name):
    #---------------------------------------------floor ------------------------------------------------------------------------------------------------
    mesh = bpy.data.meshes.new(name="PolygonMesh")
    obj = bpy.data.objects.new(polygon_name, mesh)
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

    # Calculate the average x and y coordinates
    avg_x = sum(vert.co.x for vert in face_verts) / len(face_verts)
    avg_y = sum(vert.co.y for vert in face_verts) / len(face_verts)

    bm.faces.new(face_verts)

    # Extrude the face to create the height
    for face in bm.faces:
        face.select_set(True)

    extruded = bmesh.ops.extrude_face_region(bm, geom=bm.faces)
    vertices = [e for e in extruded['geom'] if isinstance(e, bmesh.types.BMVert)]
    bmesh.ops.translate(bm, vec=(0, 0, height), verts=vertices)  # 30m 높이로 이동

    obj.location = (avg_x/3.5, avg_y/3.5, height / 2.0)
    #-----------------------------------------------------------------------------------------------------------------------------------------

    # Update mesh with BMesh data
    bm.to_mesh(mesh)
    bm.free()

    # # 폴리곤의 중앙 계산
    # center_x = sum((coord[0] for coord in coordinates)) / len(coordinates)
    # center_y = sum((coord[1] for coord in coordinates)) / len(coordinates)

    # korean_font_path = "C:/Windows/Fonts/H2HDRM.TTF"  # D2Coding 폰트의 실제 경로로 변경

    # # 폴리곤 중앙에 텍스트 추가
    # bpy.ops.object.text_add(location=(center_x-2, -(center_y), height+3))
    # text_obj = bpy.context.active_object
    # text_obj.data.body = text_content

    # # 기존 폰트를 지우지 않고, 새로운 폰트를 적용
    # text_obj.data.font = bpy.data.fonts.load(korean_font_path)

    # # 한글 텍스트 설정
    # text_obj.data.body = text_content

    # # 텍스트 크기 조절
    # text_obj.scale = (10, 10, 0)

    # # Create Solidify modifier
    # solidify_modifier = obj.modifiers.new(name="Solidify", type='SOLIDIFY')
    # solidify_modifier.thickness = thickness

    bpy.context.view_layer.update()  # 시각적 업데이트 수행

    mesh.update()

def add_polygon_data(polygon_data, height):
    for polygon_name, coordinates in polygon_data.items():
        # korean_text = txt_data[polygon_name]
        # txt = korean_text["name"]
        # if(txt =='' or  txt=='\n'):
        #     txt = '텍스트를 \n읽을 수 없습니다'

        create_polygon(coordinates, height, 1.5, polygon_name)



# 초기 설정 및 삭제 함수 호출
#delete_setup()



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
            solidify_mod.thickness = 1  # 두께를 2로 설정
            bpy.context.view_layer.objects.active = obj
            bpy.ops.object.modifier_apply(modifier=solidify_mod.name)


def add_plane(w,h):
    bpy.ops.mesh.primitive_plane_add(size=2, enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(0, 0, 0))
    bpy.context.object.scale[0] = (int(w)/1.2 )
    bpy.context.object.scale[1] = (int(h)/1.2 )
    bpy.context.object.location[0] = (int(w) ) -285
    bpy.context.object.location[1] = -(int(h) )+200
    return bpy.context.object.location

def move_all_objects(x, y):
    # 씬의 모든 오브젝트를 순회합니다.
    for obj in bpy.data.objects:
        # 오브젝트의 위치를 현재 위치에서 주어진 x, y 값만큼 이동합니다.
        obj.location.x -= x
        obj.location.y += -y





'''
매개변수 추가 부분
'''
if __name__ == "__main__":
    if len(sys.argv) < 7:  # JSON 데이터와 GLTF 파일 경로
        print("Not enough arguments provided.")
        sys.exit(1)

    # JSON 파일 경로에서 데이터를 읽어와 polygon_data에 저장
    polygon_data_file = sys.argv[-2]  # JSON 데이터 파일 경로
    with open(polygon_data_file, 'r') as json_file:
        polygon_data = json.load(json_file)

    h = sys.argv[-3]
    w = sys.argv[-4]
    location = add_plane(w, h)
    x_coord = location.x
    y_coord = location.y

    # list_data_file = sys.argv[-5]
    # with open(list_data_file, 'r') as json_file2:
    #     list_data = json.load(json_file2)

    add_polygon_data(polygon_data, 30)

    apply_solidify_modifier()

    for obj in bpy.context.scene.objects:
        obj.select_set(True)

    move_all_objects(x_coord, y_coord)

    output_gltf_path = sys.argv[-1]  # GLTF 파일 경로
    # path ="C:/teamProject_AiServer/memory/floor_result/test1.glb"
    # bpy.ops.objects.select_all(action='SELECT')
    bpy.ops.export_scene.gltf(filepath=output_gltf_path, export_format='GLB', use_selection=True)  # GLTF 파일 저장
