# cv_tools

傳統 cv 工具集

## 專案結構

```
cv_tool/
├─ .gitignore                  # Git 忽略配置文件
├─ calibrate/                  # 相機標定相關程式與資料
│  ├─ script/                    # 腳本目錄
│  │  ├─ calibrate.py             # 相機標定主程式（OpenCV 應用）
│  │  └─ calibrate2mm.py          # 標定結果單位轉換/校正（mm）
│  │
│  ├─ run/
│  │  └─ calibration.yaml      # 標定設定或輸出（YAML）
│  │
│  └─ data/
│     ├─ 133_calibrate(0)/     # 標定影像集（範例）
│     │  └─ DFK_33UX252_0.jpg
│     └─ 135_calibrate(handup_72.8)/
│        ├─ INTEL_435I_RGB.jpg
│        ├─ INTEL_435I_RGB (2).jpg
│        └─ INTEL_435I_RGB (3).jpg
│
├─ depth/                      # 深度與點雲處理
│  ├─ script/                    # 腳本目錄
│  │  ├─ point_cloud.py           # 生成/處理點雲
│  │  └─ txt2depth.py             # 將深度文字檔轉成深度圖
│  │
│  └─ data/
│     ├─ INTEL_435I_RGB_354.jpg
│     └─ intel_435i_depth.txt
│
├─ traditional_cv/             # 傳統影像處理範例
│  ├─ script/                    # 腳本目錄
│  │  ├─ canny.py                 # Canny 邊緣檢測示例
│  │  ├─ HSV.py                   # HSV 顏色分割示例
│  │  └─ HSV_cap.py               # 從攝影機擷取並以 HSV 處理
│  │
│  └─ data/
│     └─ 774250875.052961.mp4  # 範例影片
│
└─ README.md（本檔）            # 專案說明與使用指引（請參閱檔案內容）
```