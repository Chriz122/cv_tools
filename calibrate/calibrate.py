import cv2
import numpy as np
import glob
from scipy.spatial.transform import Rotation
import os
import sys

# === 設定參數 ===
# # 內角點數：以你的棋盤格推測 12 x 11
# chessboard_size = (12, 11)
# square_size = 25.0  # mm (2.0 cm)

chessboard_size = (10, 7)
square_size = 23.5  # mm (2.35 cm)

# === 建立棋盤格 3D 世界座標 ===
objp = np.zeros((chessboard_size[0]*chessboard_size[1], 3), np.float32)
objp[:, :2] = np.mgrid[0:chessboard_size[0],
                       0:chessboard_size[1]].T.reshape(-1, 2)
objp = objp * square_size

objpoints = []  # 3D 世界座標
imgpoints = []  # 2D 影像座標

# === 讀取圖片 ===
# 把多張圖片放到 INTEL_435I_RGB/ 目錄
# images = glob.glob(r'calibrate\data\135_calibrate(handup_72.8)\INTEL_435I_RGB*.jpg')
images = [r'calibrate\data\133_calibrate(0)\DFK_33UX252_0.jpg']

for i, fname in enumerate(images):
    img = cv2.imread(fname)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 找棋盤格角點
    ret, corners = cv2.findChessboardCorners(gray, chessboard_size, None)

    if ret:
        objpoints.append(objp)

        # 亞像素優化
        criteria = (cv2.TERM_CRITERIA_EPS +
                    cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
        corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
        imgpoints.append(corners2)

        # 畫出角點
        cv2.drawChessboardCorners(img, chessboard_size, corners2, ret)
        cv2.imshow(f'img_{i}', img)
        cv2.waitKey(0)
    else:
        print(f"找不到角點：{fname}")

cv2.destroyAllWindows()

# 在 calibrate 前檢查是否有找到角點
if len(objpoints) == 0 or len(imgpoints) == 0:
    print("找不到任何角點資料，請確認影像路徑與棋盤格參數是否正確。")
    sys.exit(1)

# === 執行校正 ===
ret, cameraMatrix, distCoeffs, rvecs, tvecs = cv2.calibrateCamera(
    objpoints, imgpoints, gray.shape[::-1], None, None)

if not ret:
    print("相機校正失敗 (calibrateCamera 回傳 False)。")
    sys.exit(1)

# 收集所有轉移矩陣
all_R = []
all_T = []
for rvec, tvec in zip(rvecs, tvecs):
    R, _ = cv2.Rodrigues(rvec)
    all_R.append(R)
    # 確保 tvec 形狀為 (3,1)
    all_T.append(np.array(tvec).reshape(3, 1))

# 計算平均平移向量
all_T_arr = np.array(all_T)  # shape: (N, 3, 1)
mean_T = np.mean(all_T_arr, axis=0).reshape(3, 1)  # shape: (3,1)

# 計算平均旋轉矩陣
# 使用四元數平均方法
rotations = [Rotation.from_matrix(R) for R in all_R]
quats = np.array([r.as_quat() for r in rotations])
mean_quat = np.mean(quats, axis=0)
mean_quat = mean_quat / np.linalg.norm(mean_quat)  # 正規化
mean_R = Rotation.from_quat(mean_quat).as_matrix()

# 組合平均轉移矩陣
mean_RT = np.hstack((mean_R, mean_T))
print("\n平均 [R|T] 轉移矩陣:")
print(mean_RT)

# === 輸出到 YAML（確保目錄存在並以絕對路徑開啟） ===
base_dir = os.path.dirname(os.path.abspath(__file__))
out_dir = os.path.join(base_dir, 'run')
os.makedirs(out_dir, exist_ok=True)
out_path = os.path.join(out_dir, 'calibration.yaml')

fs = cv2.FileStorage(out_path, cv2.FILE_STORAGE_WRITE)
if not fs.isOpened():
    print(f"無法開啟輸出檔案：{out_path}")
    sys.exit(1)

fs.write('camera_matrix', cameraMatrix)
fs.write('dist_coeffs', distCoeffs)
fs.write('mean_RT', mean_RT)
fs.release()

print(f"\n已輸出 {out_path} ✔️")
