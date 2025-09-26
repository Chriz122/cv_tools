import matplotlib.pyplot as plt
import numpy as np

# 從指定路徑讀取深度數據
depth_array = np.loadtxt(r'depth\data\intel_435i_depth.txt')

# 顯示深度圖
plt.imshow(depth_array, cmap='jet')
plt.axis('off')  # 移除軸線
plt.colorbar()
plt.show()
