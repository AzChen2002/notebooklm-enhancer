import streamlit as st
import os
import tempfile
import traceback
from src.processor import PDFProcessor
from src.config import Config
from PIL import Image

# Page Config
st.set_page_config(
    page_title="NotebookLM Enhancer",
    page_icon="📄",
    layout="wide"
)

# Title and Description
# Custom CSS for Hero Section
st.markdown("""
<style>
    .hero-container {
        text-align: center;
        padding: 2rem 0;
    }
    .hero-title {
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        background: -webkit-linear-gradient(45deg, #FF4B4B, #FF914D);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .hero-subtitle {
        font-size: 1.2rem;
        color: #666;
        margin-bottom: 2rem;
    }
    .feature-card {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
        height: 100%;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: transform 0.2s;
    }
    .feature-card:hover {
        transform: translateY(-5px);
    }
    .feature-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
    }
    .feature-title {
        font-weight: 600;
        font-size: 1.1rem;
        margin-bottom: 0.5rem;
    }
    .feature-desc {
        font-size: 0.9rem;
        color: #555;
    }
</style>
""", unsafe_allow_html=True)

# Main Area - File Uploader
uploaded_file = st.file_uploader("上傳 NotebookLM PDF", type=["pdf"])

# Show Hero Section only if no file is uploaded
if uploaded_file is None:
    st.markdown("""
        <div class="hero-container">
            <div class="hero-title">NotebookLM Enhancer</div>
            <div class="hero-subtitle">將您的 AI 簡報升級為專業、清晰、可編輯的 PPTX</div>
        </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
            <div class="feature-card">
                <div class="feature-icon">🎨</div>
                <div class="feature-title">畫質增強 (Enhance)</div>
                <div class="feature-desc">使用 Noto Sans TC 字型重新渲染，將模糊的 PDF 轉為高解析度影像。</div>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
            <div class="feature-card">
                <div class="feature-icon">✏️</div>
                <div class="feature-title">完全可編輯 (Editable)</div>
                <div class="feature-desc">轉換為 PPTX 格式，文字不再是圖片，而是真正的可編輯文字方塊。</div>
            </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
            <div class="feature-card">
                <div class="feature-icon">💧</div>
                <div class="feature-title">智慧去浮水印 (Clean)</div>
                <div class="feature-desc">自動偵測並移除右下角浮水印，還原乾淨的版面設計。</div>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.info("👆 請在上方拖曳或選擇您的 PDF 檔案以開始使用。")

# Sidebar - Settings
# Logo
logo_path = os.path.join(os.path.dirname(__file__), "assets", "sidebar_logo.png")
if os.path.exists(logo_path):
    st.sidebar.image(logo_path, use_container_width=True)

st.sidebar.header("⚙️ 設定 (Settings)")

# Font Selection (Disabled for now as per user request)
# fonts_dir = Config.FONTS_DIR
# available_fonts = {}
# ... (Font loading logic commented out)
selected_font_path = None

# Debug Options
# st.sidebar.markdown("---")
# debug_mode = st.sidebar.checkbox("🐞 測試模式 (強制紅字)", value=False, help="將所有文字轉為紅色，用於確認字型是否正確套用。")
debug_mode = False

# Text Settings (Disabled)
# st.sidebar.markdown("---")
# st.sidebar.subheader("📝 文字設定 (Text)")
# text_bg = st.sidebar.checkbox("使用文字底色遮蓋 (Cover Old Text)", value=True, help="在文字下方繪製白色方塊，以遮蓋原本模糊的文字。")
text_bg = False # Default to False since we are not rendering text

# Watermark Settings
st.sidebar.markdown("---")
st.sidebar.subheader("💧 浮水印設定 (Watermark)")
st.sidebar.subheader("💧 浮水印設定 (Watermark)")
remove_watermark = st.sidebar.checkbox("去除浮水印 (Remove Watermark)", value=True)

if remove_watermark:
    col_wm1, col_wm2 = st.sidebar.columns(2)
    with col_wm1:
        wm_x_start = st.slider("目標 X (Target X)", 0.0, 1.0, 0.89, 0.01)
        wm_width = st.slider("寬度 (Width)", 0.0, 0.3, 0.11, 0.01)
    with col_wm2:
        wm_y_start = st.slider("目標 Y (Target Y)", 0.0, 1.0, 0.95, 0.01)
        wm_height = st.slider("高度 (Height)", 0.0, 0.2, 0.04, 0.01)
    
    use_mirror_patch = st.sidebar.checkbox("使用鏡像修補 (Use Mirror Patching)", value=True)
    
    if not use_mirror_patch:
        use_patch = st.sidebar.checkbox("使用手動背景修補 (Manual Patching)", value=False)
        if use_patch:
            st.sidebar.markdown("---")
            st.sidebar.markdown("**修補來源 (Patch Source)**")
            col_src1, col_src2 = st.sidebar.columns(2)
            with col_src1:
                src_x = st.slider("來源 X (Source X)", 0.0, 1.0, 0.5, 0.01)
            with col_src2:
                src_y = st.slider("來源 Y (Source Y)", 0.0, 1.0, 0.92, 0.01)
        else:
            src_x = 0
            src_y = 0
    else:
        use_patch = False
        src_x = 0
        src_y = 0

    wm_settings = {
        "x_start": wm_x_start,
        "y_start": wm_y_start,
        "width": wm_width,
        "height": wm_height,
        "use_mirror_patch": use_mirror_patch,
        "use_patch": use_patch,
        "src_x": src_x,
        "src_y": src_y,
        "text_bg": text_bg
    }
else:
    wm_settings = {"text_bg": text_bg}

# Main Area - File Uploader (Moved to top)
# uploaded_file = st.file_uploader("上傳 NotebookLM PDF", type=["pdf"])

if uploaded_file is not None:
    # Save uploaded file to temp
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(uploaded_file.getvalue())
        tmp_path = tmp_file.name

    st.success(f"檔案已上傳: {uploaded_file.name}")

    # Initialize Processor
    processor = PDFProcessor(tmp_path, font_path=selected_font_path)

    # Preview Section
    st.subheader("👀 預覽 (Preview - Page 1)")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**原始頁面 (Original)**")
        # Render original first page
        page1 = processor.doc[0]
        pix = page1.get_pixmap(dpi=150)
        img_original = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        st.image(img_original, width="stretch")
        
        # Debug Info: Check text blocks
        text_blocks = page1.get_text("blocks")
        num_blocks = len(text_blocks)
        st.caption(f"🔍 偵測到的文字區塊數: {num_blocks}")
        
        if num_blocks > 0:
            with st.expander("查看提取的文字數據 (Debug Data)"):
                # Extract using our method to see exactly what we are getting
                elements = processor.extract_elements(0)
                for i, elem in enumerate(elements[:5]):
                    st.text(f"Text: {elem['text'][:20]}...")
                    st.text(f"Size: {elem['size']:.2f} | Color: {elem['color']}")
                    st.text(f"BBox: {elem['bbox']}")
                    st.markdown("---")
        else:
            st.error("⚠️ 警告：未偵測到文字！這可能是純圖片 PDF 或向量文字。")
            st.info("建議：我們可能需要加入 OCR 功能來處理此檔案。")

    with col2:
        st.markdown("**處理後背景 (Cleaned Background)**")
        # Show what the background looks like (cleaned)
        if remove_watermark:
            img_cleaned = processor.clean_page_image(0, dpi=150, wm_settings=wm_settings)
            
            # Draw visualization boxes for UI feedback (only on preview, not on result)
            # We need a copy to draw on
            img_preview = img_cleaned.copy()
            from PIL import ImageDraw
            draw = ImageDraw.Draw(img_preview)
            w, h = img_preview.size
            
            # Draw Target Box (Red)
            tx = int(w * wm_settings["x_start"])
            ty = int(h * wm_settings["y_start"])
            tw = int(w * wm_settings["width"])
            th = int(h * wm_settings["height"])
            draw.rectangle([tx, ty, tx+tw, ty+th], outline="red", width=3)
            
            # Draw Source Box
            if wm_settings.get("use_mirror_patch"):
                # Calculate symmetric source
                sx = w - (tx + tw)
                sy = ty
                draw.rectangle([sx, sy, sx+tw, sy+th], outline="blue", width=3)
                caption = "紅框: 消除區域 | 藍框: 鏡像來源 (自動計算)"
            elif wm_settings.get("use_patch"):
                sx = int(w * wm_settings["src_x"])
                sy = int(h * wm_settings["src_y"])
                draw.rectangle([sx, sy, sx+tw, sy+th], outline="#00ff00", width=3)
                caption = "紅框: 消除區域 | 綠框: 手動來源"
            else:
                caption = "紅框: 消除區域 (白色遮蓋)"
                
            st.image(img_preview, width="stretch", caption=caption)
        else:
            st.info("浮水印去除已關閉")
            st.image(img_original, width="stretch")
            
    # Full Page Preview Expander
    with st.expander("👀 預覽所有頁面 (Preview All Pages)"):
        if "thumbnails" not in st.session_state or st.session_state.get("thumb_file") != uploaded_file.name:
             with st.spinner("正在生成頁面預覽 (Generating Previews)..."):
                 st.session_state.thumbnails = processor.get_page_thumbnails()
                 st.session_state.thumb_file = uploaded_file.name
        
        # Grid Layout for Thumbnails
        cols = st.columns(4)
        pages_to_remove = []
        for i, (page_num, img) in enumerate(st.session_state.thumbnails):
            with cols[i % 4]:
                st.image(img, caption=f"Page {page_num}", width="stretch")
                # Checkbox for deletion
                # Use a unique key for each checkbox
                del_key = f"del_page_{page_num}"
                if st.checkbox("🗑️ 刪除 (Delete)", key=del_key):
                    pages_to_remove.append(page_num - 1) # Store 0-based index

        if pages_to_remove:
            st.warning(f"⚠️ 將刪除 {len(pages_to_remove)} 頁: {[p+1 for p in pages_to_remove]}")

    # Action Buttons
    # Create tabs for different functions
    tab_enhance, tab_edit, tab_pptx = st.tabs(["✨ 增強 PDF (Enhance)", "✏️ 編輯文字 (Edit Text)", "📊 轉為 PPTX"])

    with tab_enhance:
        if st.button("🚀 生成增強版 PDF", type="primary", width="stretch"):
            if not uploaded_file:
                st.warning("請先上傳 PDF 檔案。")
            else:
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                def update_progress(progress, message):
                    progress_bar.progress(progress)
                    status_text.text(message)

                try:
                    output_path = processor.render_new_pdf(
                        wm_settings=wm_settings, 
                        debug_mode=debug_mode, 
                        enable_ocr=False,
                        progress_callback=update_progress,
                        pages_to_remove=pages_to_remove
                    )
                    st.success("PDF 生成成功！")
                    with open(output_path, "rb") as f:
                        st.download_button(
                            label="📥 下載增強版 PDF",
                            data=f,
                            file_name=f"{processor.filename}_enhanced.pdf",
                            mime="application/pdf"
                        )
                except Exception as e:
                    st.error(f"發生錯誤: {e}")
                    import traceback
                    st.code(traceback.format_exc())
                finally:
                    progress_bar.empty()
                    status_text.empty()

    with tab_edit:
        st.info("在此頁籤中，您可以直接修改 PDF 內的文字內容。")
        
        if "text_data" not in st.session_state or st.session_state.get("file_name") != uploaded_file.name:
            st.markdown("### 1. 選擇要分析的頁面 (Select Pages)")
            st.info("請勾選需要編輯文字的頁面。未勾選的頁面將保持原樣。")
            
            if "thumbnails" not in st.session_state or st.session_state.get("thumb_file") != uploaded_file.name:
                 with st.spinner("正在生成頁面預覽 (Generating Previews)..."):
                     st.session_state.thumbnails = processor.get_page_thumbnails()
                     st.session_state.thumb_file = uploaded_file.name
            
            # Select All / Deselect All Buttons
            col_btn1, col_btn2, _ = st.columns([1, 1, 4])
            with col_btn1:
                if st.button("✅ 全選 (Select All)"):
                    for page_num, _ in st.session_state.thumbnails:
                        st.session_state[f"pg_select_{page_num}"] = True
                    st.rerun()
            with col_btn2:
                if st.button("❌ 全不選 (Deselect All)"):
                    for page_num, _ in st.session_state.thumbnails:
                        st.session_state[f"pg_select_{page_num}"] = False
                    st.rerun()

            # Grid Layout for Thumbnails
            selected_pages = []
            cols = st.columns(4)
            for i, (page_num, img) in enumerate(st.session_state.thumbnails):
                with cols[i % 4]:
                    st.image(img, width="stretch")
                    # Use a unique key for each checkbox
                    # Initialize key in session state if not present (default True)
                    key = f"pg_select_{page_num}"
                    if key not in st.session_state:
                        st.session_state[key] = True
                        
                    if st.checkbox(f"第 {page_num} 頁", key=key):
                        selected_pages.append(page_num)
            
            st.divider()
            
            if st.button("🔍 讀取選定頁面 (Read Selected Pages)", type="primary"):
                if not selected_pages:
                    st.warning("請至少選擇一頁！ (Please select at least one page)")
                else:
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    def update_progress(progress, message):
                        progress_bar.progress(progress)
                        status_text.text(message)

                    try:
                        st.session_state.text_data = processor.extract_text_data(
                            pages=selected_pages,
                            progress_callback=update_progress
                        )
                        st.session_state.file_name = uploaded_file.name
                        st.rerun()
                    except Exception as e:
                        st.error(f"發生錯誤: {e}")
                        st.code(traceback.format_exc())
                    finally:
                        progress_bar.empty()
                        status_text.empty()
        
        if "text_data" in st.session_state:
            # Display data editor
            edited_data = st.data_editor(
                st.session_state.text_data,
                column_config={
                    "page": st.column_config.NumberColumn("頁碼", disabled=True),
                    "original_text": st.column_config.TextColumn("原始文字", disabled=True),
                    "new_text": st.column_config.TextColumn("新文字 (可編輯)"),
                    "size": st.column_config.NumberColumn("字體大小"),
                    "color": st.column_config.TextColumn("顏色 (Hex)", help="請輸入 Hex 色碼，例如 #FF0000", validate="^#[0-9a-fA-F]{6}$"),
                    "id": None, # Hide ID
                    "bbox": None, # Hide bbox
                    "origin": None # Hide origin
                },
                hide_index=True,
                width="stretch",
                height=500
            )
            
            st.divider()
            
            col_opts, col_btn = st.columns([2, 1])
            
            with col_opts:
                bg_mode = st.selectbox(
                    "背景處理模式 (Background Mode)",
                    ["Blur (高斯模糊)", "Smart Fill (周圍底色)", "White (固定白色)"],
                    index=0,
                    help="選擇如何處理被修改文字的背景區域"
                )
            
            with col_btn:
                st.write("") # Spacer
                st.write("") # Spacer
                generate_clicked = st.button("💾 生成編輯後的 PDF", type="primary", width="stretch")

            if generate_clicked:
                with st.spinner("正在生成 PDF (Processing)..."):
                    try:
                        # Map UI selection to internal mode string
                        mode_map = {
                            "Blur (高斯模糊)": "Blur",
                            "Smart Fill (周圍底色)": "Smart Fill",
                            "White (固定白色)": "White"
                        }
                        selected_mode = mode_map[bg_mode]
                        
                        output_path = processor.apply_text_edits(
                            edited_data, 
                            font_path=selected_font_path, 
                            wm_settings=wm_settings,
                            bg_mode=selected_mode
                        )
                        st.success("編輯完成！")
                        with open(output_path, "rb") as f:
                            st.download_button(
                                label="📥 下載編輯後的 PDF",
                                data=f,
                                file_name=f"{processor.filename}_edited.pdf",
                                mime="application/pdf",
                                type="primary"
                            )
                    except Exception as e:
                        st.error(f"發生錯誤: {e}")
                        st.code(traceback.format_exc())

    with tab_pptx:
        st.info("將 PDF 轉換為 PowerPoint 投影片。")
        
        pptx_mode = st.radio(
            "文字模式 (Text Mode)",
            ["Re-render (重繪模式)", "Overlay (疊加模式)"],
            index=0,
            help="Re-render: 重新繪製清晰文字 (適合模糊文件)\nOverlay: 保留原始背景，疊加隱形文字 (適合保留原始排版)"
        )
        
        enable_ocr_pptx = st.checkbox(
            "啟用 OCR (Enable OCR)", 
            value=False, 
            help="若 PDF 為純圖片或掃描檔，請勾選此項。若為一般 PDF (已有文字)，請取消勾選以大幅提升轉換速度。"
        )
        
        if st.button("📊 轉為 PPTX", width="stretch"):
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            def update_progress(progress, message):
                progress_bar.progress(progress)
                status_text.text(message)

            try:
                # Map UI selection to internal mode string
                mode_map = {
                    "Re-render (重繪模式)": "re-render",
                    "Overlay (疊加模式)": "overlay"
                }
                selected_mode = mode_map[pptx_mode]
                
                pptx_path = processor.convert_to_pptx(
                    wm_settings=wm_settings, 
                    text_mode=selected_mode,
                    enable_ocr=enable_ocr_pptx,
                    progress_callback=update_progress,
                    pages_to_remove=pages_to_remove
                )
                st.success("PPTX 轉換成功！")
                with open(pptx_path, "rb") as f:
                    st.download_button(
                        label="📥 下載 PPTX",
                        data=f,
                        file_name=f"{processor.filename}.pptx",
                        mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
                    )
            except Exception as e:
                st.error(f"發生錯誤: {e}")
                import traceback
                st.code(traceback.format_exc())
            finally:
                progress_bar.empty()
                status_text.empty()
