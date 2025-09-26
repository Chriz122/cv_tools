import cv2
import numpy as np

# 從影片中讀取第一幀
video_path = r'traditional_cv\data\774250875.052961.mp4'
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print("無法開啟影片")
    exit()
for i in range(6):  # 跳過前~幀
    ret, img = cap.read()
    if not ret:
        print("無法讀取影片的前幀")
        exit()

# # 讀取輸入圖像
# img = cv2.imread(r"your_pic.png")

# 空
def empty(v):
    pass

cv2.namedWindow("Track Bar", cv2.WINDOW_NORMAL)

cv2.createTrackbar('Hue MIN', "Track Bar", 0, 179, empty)
cv2.createTrackbar('Hue MAX', "Track Bar", 179, 179, empty)
cv2.createTrackbar('Sat MIN', "Track Bar", 0, 255, empty)
cv2.createTrackbar('Sat MAX', "Track Bar", 255, 255, empty)
cv2.createTrackbar('Val MIN', "Track Bar", 0, 255, empty)
cv2.createTrackbar('Val MAX', "Track Bar", 255, 255, empty)

# 動態調整HSV過濾範圍
while True:
    h_min = cv2.getTrackbarPos('Hue MIN', "Track Bar")
    h_max = cv2.getTrackbarPos('Hue MAX', "Track Bar")
    s_min = cv2.getTrackbarPos('Sat MIN', "Track Bar")
    s_max = cv2.getTrackbarPos('Sat MAX', "Track Bar")
    v_min = cv2.getTrackbarPos('Val MIN', "Track Bar")
    v_max = cv2.getTrackbarPos('Val MAX', "Track Bar")

    lower = np.array([h_min, s_min, v_min])
    upper = np.array([h_max, s_max, v_max])

    mask2 = cv2.inRange(cv2.cvtColor(img, cv2.COLOR_BGR2HSV), lower, upper)
    r = cv2.bitwise_and(img, img, mask=mask2)  # 使用原始BGR影像

    cv2.imshow("result Image", r)

    if cv2.waitKey(1) & 0xFF == 27:  # 按ESC退出
        break

cv2.destroyAllWindows()
cap.release()