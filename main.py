import cv2
import numpy as np

video_path = 'videos/blackpink.mp4'
cap = cv2.VideoCapture(video_path)

# 사이즈 조절하기
output_size = (187, 333) # (width, height)

# writing video Initialization
# mp4 코덱으로 저장
fourcc = cv2.VideoWriter_fourcc("m", "p", "4", "v")
# videowrite 함수에서는 파일이름, 코덱, FPS, output_size
out = cv2.VideoWriter("%s_output.mp4" %(video_path.split(".")[0]), fourcc, cap.get(cv2.CAP_PROP_FPS), output_size)

# 비디오가 잘 열렸는지 확인
if not cap.isOpened():
    print("exit")
    exit()

# Opencv에서 제공하는 CSRT tracker 사용
tracker = cv2.TrackerCSRT_create()

# 첫번째 프레임에서 ROI를 설정 (ROI = Region of Interest)
ret, img = cap.read(20)

# 해당 윈도우에서 ROI를 설정해준다고 선언
cv2.namedWindow("Select Window")
# Select Window에 첫번째 프레임인 img을 보여주겠다
cv2.imshow("Select Window", img)

# setting ROI  ### 직접 설정
# Select Window에서 ROI를 설정해라. img에 센터에서 시작하지말고 중심점을 보이기
rect = cv2.selectROI('Select Window', img, fromCenter=False, showCrosshair=True)
# Select Window를 닫는다
cv2.destroyWindow("Select Window")

# tracker initialize
# 첫번째 프레임의 rect(직접 설정한 사각형)를 따라다니게 설정
tracker.init(img, rect)

while True:
    ret, img = cap.read()

    if not ret:
        exit()

    # image 갱신마다 tracker를 update시키기
    # success는 성공했냐 아니냐(boolean)
    # box는 rect 형태의 박스
    success, box = tracker.update(img)

    # box 속의 각각의 값을 받아오기
    left, top, w, h = [int(v) for v in box]

    # 저장할 동영상의 크기는 동일해야하므로 사이즈 조절해주기
    center_x = left + w / 2
    center_y = top + h / 2

    # 조절한 좌표값 구해내기
    result_top = int(center_y - output_size[1] / 2)
    result_bottom = int(center_y + output_size[1] / 2)
    result_left = int(center_x - output_size[0] / 2)
    result_right = int(center_x + output_size[0] / 2)

    # image crop
    # rect box를 안나오게끔 copy()
    result_img = img[result_top:result_bottom, result_left:result_right].copy()

    out.write(result_img)

    cv2.rectangle(img, pt1=(left, top), pt2 = (left+w, top + h), color = (255, 255, 255), thickness = 2)

    cv2.imshow("result_img", result_img)
    cv2.imshow("img", img)

    if cv2.waitKey(1) == ord('q'):
        break
