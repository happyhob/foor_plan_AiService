import bpy
import bmesh
import sys
import json

output_gltf_path1 = "C:/Users/wjdtj/OneDrive/바탕 화면/안내도/building/test.glb"

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
    
def create_material(name, color):
    # 새로운 재질 생성
    mat = bpy.data.materials.new(name)
    mat.diffuse_color = color  # 재질의 색상 설정 (RGBA)
    return mat

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
    verts = [bm.verts.new((x, -y, 10)) for x, y in coordinates]

    # 에지 생성
    for i in range(len(verts)):
        bm.edges.new((verts[i], verts[(i + 1) % len(verts)]))
    #Create faces
    face_verts = [verts[i] for i in range(len(verts))]
    bm.faces.new(face_verts)
    color_material = create_material("ColorMat", (0.5, 0.75, 0.4, 1))  # 빨간색 재질 생성
    mesh.materials.append(color_material)

    avg_x = sum(vert.co.x for vert in face_verts) / len(face_verts)
    avg_y = sum(vert.co.y for vert in face_verts) / len(face_verts)



    # 에지 extrude
    edges_to_extrude = [edge for edge in bm.edges]
    geom_extrude = bmesh.ops.extrude_edge_only(bm, edges=edges_to_extrude)
    verts_extruded = [e for e in geom_extrude['geom'] if isinstance(e, bmesh.types.BMVert)]
    bmesh.ops.translate(bm, vec=(0, 0, height), verts=verts_extruded)

    #-----------------------------------------------------------------------------------------------------------------------------------------
    obj.location = (avg_x / 4, avg_y / 4, height / 2.0)

    # Update mesh with BMesh data
    bm.to_mesh(mesh)
    bm.free()

    # 폴리곤의 중앙 계산
    center_x = sum((coord[0] for coord in coordinates)) / len(coordinates)
    center_y = sum((coord[1] for coord in coordinates)) / len(coordinates)

    bpy.context.view_layer.update()  # 시각적 업데이트 수행

    mesh.update()

def add_polygon_data(polygon_data,height):
    for polygon_name, coordinates in polygon_data.items():
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
            solidify_mod.thickness = 2  # 두께를 2로 설정
            bpy.context.view_layer.objects.active = obj
            bpy.ops.object.modifier_apply(modifier=solidify_mod.name)


def add_plane(json_data, extrude_height ):
    all_coords = []
    for key in json_data:
        all_coords.extend(json_data[key])

    # x, y 좌표의 최대, 최소값 찾기
    min_x = min(coord[0] for coord in all_coords)-200
    max_x = max(coord[0] for coord in all_coords)+200
    min_y = min(coord[1] for coord in all_coords)-150
    max_y = max(coord[1] for coord in all_coords)+150


    list = [[min_x, min_y], [min_x, max_y], [max_x, max_y], [max_x, min_y]]

    return list







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

    delete_setup()

    # JSON 파일 경로에서 데이터를 읽어와 polygon_data에 저장
    polygon_data_file = sys.argv[-2]  # JSON 데이터 파일 경로
    with open(polygon_data_file, 'r') as json_file:
        polygon_data = json.load(json_file)


    h = sys.argv[-3]
    w = sys.argv[-4]



    add_polygon_data(polygon_data, 30)

    list = add_plane(polygon_data,33)
    create_polygon(list, 25, 1.5, "plan")
    #x_coord = location.x
    #y_coord = location.y
    #move_all_objects(x_coord, y_coord)
    apply_solidify_modifier()

    output_gltf_path = sys.argv[-1]  # GLTF 파일 경로
    #save_path = "C:/Users/wjdtj/OneDrive/바탕 화면/teamProject_AiServer/teamProject_AiServer/memory/floor_result/test.blend"
    #bpy.ops.wm.save_as_mainfile(filepath=save_path)
    bpy.ops.export_scene.gltf(filepath=output_gltf_path, export_format='GLB', use_selection=False)  # GLTF 파일 저장