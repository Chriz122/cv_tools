import numpy as np
import open3d as o3d
import cv2

img = cv2.imread(r"depth\data\INTEL_435I_RGB_354.jpg")
depth_data = np.loadtxt(r"depth\data\intel_435i_depth.txt")

height, width = depth_data.shape
x, y = np.meshgrid(np.arange(width), np.arange(height))
z = -depth_data/10  # 調整深度比例
z[z == np.min(z)] = 0

# 將 x, y, z 堆疊成點雲數據
point_cloud = np.dstack((x, -y, z)).reshape(-1, 3)

# 如果影像尺寸與深度圖尺寸不一致，resize 影像
img_h, img_w = img.shape[:2]
if (img_h, img_w) != (height, width):
    img = cv2.resize(img, (width, height), interpolation=cv2.INTER_LINEAR)

img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
color = img_rgb.reshape(-1, 3) / 255.0

# 只保留 z != 0 的點與對應顏色（不顯示 z==0）
mask = (point_cloud[:, 2] != 0)
point_cloud = point_cloud[mask]
color = color[mask]

# 創建 Open3D 點雲物件
pcd = o3d.geometry.PointCloud()
pcd.points = o3d.utility.Vector3dVector(point_cloud)
pcd.colors = o3d.utility.Vector3dVector(color)

# 可視化點雲（側視）
vis = o3d.visualization.Visualizer()
vis.create_window(window_name="3D Point Cloud (Side View)")
vis.add_geometry(pcd)

# 設定側視視角
ctr = vis.get_view_control()
lookat = pcd.get_center()
ctr.set_lookat(lookat)
ctr.set_front((0.0, 1.0, 0.0))
ctr.set_up((0.0, 0.0, 1.0))
ctr.set_zoom(0.1)

vis.run()
vis.destroy_window()

# 將點雲保存為 .ply 格式
# o3d.io.write_point_cloud("point_cloud.ply", pcd)
