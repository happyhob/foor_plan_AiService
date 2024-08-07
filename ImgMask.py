import cv2
import numpy as np


IMAGE_DIR = "image25.jpg"

# 이미지 읽기
image = cv2.imread(IMAGE_DIR)

# 이미지가 정상적으로 읽혔는지 확인
if image is None:
    print("이미지를 읽을 수 없습니다.")
else:
    # 마스크 좌표 (예시)
    x_min, y_min, x_max, y_max = 319,  64, 510, 270
    # 좌표 값 확인
    print(f"x_min: {x_min}, y_min: {y_min}, x_max: {x_max}, y_max: {y_max}")

    # 사각형 그리기
    color = (0, 0, 255)  # BGR 형태의 컬러 (여기서는 초록색)
    thickness = 2  # 선의 두께
    cv2.rectangle(image, (x_min, y_min), (x_max, y_max), color, thickness)

    # 이미지 창에 표시
    cv2.imshow('Image with Rectangle', image)


    # 좌표에 해당하는 부분만 캡처
    captured_region = image[y_min:y_max, x_min:x_max]

    # 캡처한 부분을 새 창에 표시
    cv2.imshow('Captured Region', captured_region)


    # 캡처한 부분을 파일로 저장
    output_filename = "captured_region.jpg"
    cv2.imwrite(output_filename, captured_region)
    print(f"캡처한 부분을 {output_filename}로 저장했습니다.")

    # 키보드 입력 대기
    cv2.waitKey(0)
    cv2.destroyAllWindows()


# # 마스크 좌표 (예시)
# x_min, y_min, x_max, y_max = 319.2942810058594,  64.03502655029297, 510.8223571777344, 270.57537841796875

# # 사각형 그리기
# color = (0, 255, 0)  # BGR 형태의 컬러 (여기서는 초록색)
# thickness = 2  # 선의 두께

# cv2.rectangle(image, (x_min, y_min), (x_max, y_max), color, thickness)

# # 결과 이미지 보여주기
# cv2.imshow('Image with Rectangle', image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()