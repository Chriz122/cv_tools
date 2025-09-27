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

# 建立 Canny 閾值 TrackBar
cv2.createTrackbar('Threshold1', "Track Bar", 0, 500, empty)
cv2.createTrackbar('Threshold2', "Track Bar", 500, 1000, empty)

while True:
    threshold1 = cv2.getTrackbarPos('Threshold1', "Track Bar")
    threshold2 = cv2.getTrackbarPos('Threshold2', "Track Bar")

    # 轉灰階
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Canny 邊緣偵測
    edges = cv2.Canny(gray, threshold1, threshold2)

    cv2.imshow("Canny Edge", edges)

    if cv2.waitKey(1) & 0xFF == 27:  # 按ESC退出
        break

cv2.destroyAllWindows()
