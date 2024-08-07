import matplotlib.pyplot as plt
import matplotlib.patches as patches

def draw_rectangle(center_x, center_y, width, height):
    # 그림 생성
    fig, ax = plt.subplots(1)

    # 중심 좌표를 사용하여 좌측 상단 꼭지점 좌표 계산
    x_min = center_x - width / 2
    y_min = center_y - height / 2

    # Rectangle 객체 생성
    rect = patches.Rectangle((x_min, y_min), width, height, linewidth=1, edgecolor='r', facecolor='none')

    # 그림에 Rectangle 객체 추가
    ax.add_patch(rect)

    # 그림 출력
    plt.show()

# 예제 좌표와 크기
center_x = 319.2942810058594
center_y = 64.03502655029297
width = 510.8223571777344
height = 270.57537841796875

# 함수 호출하여 사각형 그리기
draw_rectangle(center_x, center_y, width, height)