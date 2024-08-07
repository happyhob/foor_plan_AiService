'''
//대비 조절
import cv2
import numpy as np

# 이미지 로드
image = cv2.imread('image25.jpg')

# 이미지를 그레이스케일로 변환
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# CLAHE 객체 생성
clahe = cv2.createCLAHE(clipLimit=10.0, tileGridSize=(8, 8))

# 대비 향상을 위해 CLAHE를 적용
clahed_image = clahe.apply(gray)

# 결과 이미지를 원본 이미지와 비교하여 보기
cv2.imshow('Original Image', image)
cv2.imshow('Enhanced Contrast Image', clahed_image)

# 결과 이미지 저장
cv2.imwrite('enhanced_contrast_image.jpg', clahed_image)

cv2.waitKey(0)
cv2.destroyAllWindows()
'''

