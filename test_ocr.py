import os
import sys

# Suppress warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

print("Testing RapidOCR import...")
try:
    from rapidocr_onnxruntime import RapidOCR
    print("Import successful.")
    
    print("Initializing RapidOCR...")
    ocr = RapidOCR()
    print("Initialization successful.")
    
except Exception as e:
    print(f"OCR Test Failed: {e}")
    sys.exit(1)
