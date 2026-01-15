# NotebookLM Enhancer 🚀

**NotebookLM Enhancer** 是一個專為優化 Google NotebookLM 生成的簡報 (Slides) 而設計的工具。它解決了原始 PDF 解析度不足、浮水印干擾以及無法編輯的問題，並提供高品質的 OCR 文字辨識與 PPTX 轉換功能。

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.10-3776AB?style=for-the-badge&logo=python&logoColor=white)
![RapidOCR](https://img.shields.io/badge/OCR-RapidOCR-green?style=for-the-badge)

## ✨ 主要功能 (Key Features)

### 1. PDF 畫質增強與浮水印移除
*   **高解析度重繪**：將模糊的 PDF 頁面轉換為高解析度圖片。
*   **智慧去浮水印**：自動偵測並移除 NotebookLM 的浮水印，支援「鏡像修補」與「純色遮蓋」模式。

### 2. 強大的 OCR 文字辨識
*   **RapidOCR 引擎**：採用輕量級且高效的 `rapidocr_onnxruntime`，支援中文與英文辨識。
*   **雲端友善**：使用 ONNX Runtime，完美解決 Streamlit Cloud 等雲端環境的 AVX 指令集相容性問題 (不再有 `Illegal instruction` 錯誤)。
*   **自動 fallback**：當 PDF 內嵌文字無法提取時，自動切換至 OCR 模式。

### 3. 轉換為可編輯的 PPTX
*   **保留排版**：將 PDF 頁面轉換為 PowerPoint 投影片。
*   **文字可編輯**：提取的文字會轉換為 PPTX 文字方塊，而非單純的背景圖片。
*   **原圖背景**：保留原始設計風格，同時去除浮水印。

### 4. 即時預覽與編輯
*   **全頁面預覽**：上傳後立即檢視所有頁面的縮圖。
*   **文字編輯器**：內建表格編輯器，可在轉換前修正 OCR 辨識錯誤的文字。

## 🛠️ 安裝與執行 (Installation)

### 本地端執行

1.  **複製專案**
    ```bash
    git clone https://github.com/您的帳號/notebooklm-enhancer.git
    cd notebooklm-enhancer
    ```

2.  **建立虛擬環境 (建議)**
    ```bash
    python -m venv venv
    # Windows
    .\venv\Scripts\activate
    # Mac/Linux
    source venv/bin/activate
    ```

3.  **安裝套件**
    ```bash
    pip install -r requirements.txt
    ```

4.  **啟動應用程式**
    ```bash
    streamlit run app.py
    ```

## ☁️ 雲端部署 (Deployment)

本專案已針對 **Streamlit Community Cloud** 進行優化。

### 部署設定
*   **Python 版本**：建議使用 `3.10` (已在 `.python-version` 指定)。
*   **系統套件**：專案包含 `packages.txt`，會自動安裝所需的 Linux 函式庫 (如 `libgl1`, `libxrender1` 等)。
*   **OCR 引擎**：使用 `rapidocr_onnxruntime`，無需額外安裝 PaddlePaddle，部署速度快且穩定。

詳細部署指南請參考 [DEPLOYMENT.md](DEPLOYMENT.md)。

## 📂 專案結構

```
notebooklm-enhancer/
├── app.py              # Streamlit 主程式
├── requirements.txt    # Python 套件清單
├── packages.txt        # Linux 系統套件清單
├── src/
│   ├── processor.py    # PDF 處理與 OCR 核心邏輯
│   └── config.py       # 設定檔
├── fonts/              # 字型檔案 (建議放入微軟正黑體 msjh.ttc)
└── output/             # 處理後的檔案輸出目錄
```

## 📝 注意事項

*   **字型**：為了讓 PPTX 顯示正確的中文，建議在 `fonts/` 資料夾下放入 `msjh.ttc` (微軟正黑體)。如果找不到，程式會嘗試使用系統預設字型。
*   **記憶體**：處理大型 PDF 時可能會消耗較多記憶體，建議分批處理或使用較小的檔案。

---
Developed with ❤️ for NotebookLM users.
