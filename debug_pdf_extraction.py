import fitz
import sys
import os

def analyze_pdf(file_path):
    print(f"Analyzing: {file_path}")
    if not os.path.exists(file_path):
        print("Error: File not found.")
        return

    try:
        doc = fitz.open(file_path)
        print(f"Page Count: {len(doc)}")
        
        if len(doc) > 0:
            page = doc[0]
            print("\n--- Page 1 Analysis ---")
            
            # 1. Inspect Blocks Raw
            print("Inspecting all blocks...")
            blocks = page.get_text("dict")["blocks"]
            print(f"Found {len(blocks)} blocks.")
            
            for i, block in enumerate(blocks):
                b_type = block["type"]
                type_str = "Text" if b_type == 0 else "Image" if b_type == 1 else "Unknown"
                bbox = block["bbox"]
                print(f"Block {i}: Type={type_str} ({b_type}) | BBox={bbox}")
                
                if b_type == 0: # Text
                    if "lines" in block:
                        for line in block["lines"]:
                            for span in line["spans"]:
                                print(f"  - Span: '{span['text']}' (len={len(span['text'])}) | Font: {span['font']}")
                elif b_type == 1: # Image
                    print(f"  - Image info: {block.get('image', 'N/A')}")
            
            # 2. Check Images List
            print("\nChecking page.get_images()...")
            images = page.get_images()
            print(f"Found {len(images)} images via get_images().")
            
            # 3. Plain Text Check
            print("\nChecking get_text('text')...")
            plain_text = page.get_text("text")
            print(f"Plain text length: {len(plain_text)}")
            print(f"Content preview: {plain_text[:100]!r}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    pdf_path = r"C:\Users\User\OneDrive - ITRI\桌面\AI_Power_War_Avoidance_Design_2026.pdf"
    analyze_pdf(pdf_path)
