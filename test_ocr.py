import os
import sys

# Suppress warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

print("Testing PaddleOCR import...")
try:
    from paddleocr import PaddleOCR
    print("Import successful.")
    
    print("Initializing PaddleOCR...")
    ocr = PaddleOCR(use_angle_cls=True, lang='ch', show_log=False)
    print("Initialization successful.")
    
except Exception as e:
    print(f"OCR Test Failed: {e}")
    sys.exit(1)
