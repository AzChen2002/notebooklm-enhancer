import os

class Config:
    # Base paths
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    FONTS_DIR = os.path.join(BASE_DIR, 'fonts')
    INPUT_DIR = os.path.join(BASE_DIR, 'input')
    OUTPUT_DIR = os.path.join(BASE_DIR, 'output')

    # Font settings
    # Default to Microsoft JhengHei if available, otherwise fallback
    DEFAULT_FONT_NAME = "NotoSansTC-Regular.otf" 
    DEFAULT_FONT_PATH = os.path.join(FONTS_DIR, DEFAULT_FONT_NAME)
    
    # Fallback font if the primary one isn't found (e.g., system font)
    SYSTEM_FONT_FALLBACK = "C:\\Windows\\Fonts\\msjh.ttc"

    # PDF Generation settings
    DPI = 300  # High resolution for background images

    # Watermark settings (NotebookLM usually puts it in bottom right)
    # These are relative coordinates (0.0 to 1.0) or absolute points?
    # Better to use a flexible approach or fixed size from bottom-right corner.
    # For now, let's assume a rectangular area in the bottom right.
    # (x_start_percent, y_start_percent, x_end_percent, y_end_percent)
    WATERMARK_AREA_RATIO = (0.8, 0.9, 1.0, 1.0) 
