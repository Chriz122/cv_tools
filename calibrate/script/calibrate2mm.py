import cv2
import numpy as np

# === 已知相機內參矩陣 ===
def parse_K(K_raw):
    K_raw = np.array(K_raw)
    if K_raw.ndim == 2 and K_raw.shape == (3, 3):
        return K_raw
    elif K_raw.ndim == 2 and K_raw.shape[1] == 9:
        # 1x9 展平成 3x3
        return K_raw.reshape(3, 3)
    elif K_raw.ndim == 1 and K_raw.size == 9:
        return K_raw.reshape(3, 3)
    else:
        raise ValueError("K shape not supported")

def parse_RT(RT_raw):
    RT_raw = np.array(RT_raw)
    if RT_raw.ndim == 2 and RT_raw.shape == (3, 4):
        return RT_raw
    elif RT_raw.ndim == 1 and RT_raw.size == 12:
        # 1x12 展平成 3x4
        return RT_raw.reshape(3, 4)
    else:
        raise ValueError("RT shape not supported")
    
K = parse_K([ 3.2219600767051470e+03, 0., 1.0705947459383449e+03, 0.,
       3.1351289962110445e+03, 8.5726899265126053e+02, 0., 0., 1. ])

RT = parse_RT([ -9.7517585936018703e-01, 1.6931457405460697e-02,
       2.2078353442059054e-01, 5.6748511292256801e+01,
       -3.5234020381309968e-02, -9.9623385394993191e-01,
       -7.9225450783415724e-02, -3.7336348687532897e+01,
       2.1861062903914449e-01, -8.5037838602548349e-02,
       9.7209976796464503e-01, 9.0313591105202295e+02 ])

# 從 RT 中提取 R 和 T
R = RT[:3, :3]
T = RT[:3, 3].reshape(3, 1)

# === 載入影像 ===
# img = cv2.imread('calibrate\data\135_calibrate(handup_72.8)\INTEL_435I_RGB (3).jpg')
img = cv2.imread(r'calibrate\data\133_calibrate(0)\DFK_33UX252_0.jpg')
clone = img.copy()
points = []

K_inv = np.linalg.inv(K)

# === 計算 3D 交點 ===
def intersect_plane(ray):
    R_inv = R.T
    n = np.array([0, 0, 1])  # 平面法向量 (棋盤格 Z=0)
    top = n @ (R_inv @ T).reshape(-1)
    bottom = n @ (R_inv @ ray)
    s = top / bottom
    X_cam = s * ray
    X_world = R_inv @ (X_cam - T.reshape(-1))
    return X_world

# === 滑鼠事件 ===
def click_event(event, x, y, flags, param):
    global points, img
    if event == cv2.EVENT_LBUTTONDOWN:
        # 繪製十字標記
        cross_size = 5
        cv2.line(img, (x-cross_size, y), (x+cross_size, y), (0, 0, 255), 2)  # 水平線
        cv2.line(img, (x, y-cross_size), (x, y+cross_size), (0, 0, 255), 2)  # 垂直線
        cv2.imshow('image', img)
        points.append([x, y, 1])

        if len(points) == 2:
            p1 = np.array(points[0])
            p2 = np.array(points[1])

            cv2.line(img, (points[0][0], points[0][1]), (points[1][0], points[1][1]), (255, 0, 0), 2)
            cv2.imshow('image', img)

            # 反投影到 3D
            ray1 = K_inv @ p1
            ray2 = K_inv @ p2

            P1_world = intersect_plane(ray1)
            P2_world = intersect_plane(ray2)

            dist = np.linalg.norm(P1_world - P2_world)
            print(f"真實 3D 距離: {dist:.2f} mm")

            cv2.putText(img, f"Matrix: {dist:.2f} mm",
                        (min(points[0][0], points[1][0]), min(points[0][1], points[1][1])-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.imshow('image', img)

cv2.imshow('image', img)
cv2.setMouseCallback('image', click_event)
cv2.waitKey(0)
cv2.destroyAllWindows()
