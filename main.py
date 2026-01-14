import argparse
import os
from src.processor import PDFProcessor
from src.config import Config

def main():
    parser = argparse.ArgumentParser(description="NotebookLM PDF Enhancer")
    parser.add_argument("input_file", help="Path to the input PDF file")
    parser.add_argument("--format", choices=["pdf", "pptx", "all"], default="all", help="Output format")
    parser.add_argument("--font", help="Path to custom font file", default=None)
    
    args = parser.parse_args()
    
    input_path = args.input_file
    if not os.path.isabs(input_path):
        input_path = os.path.abspath(input_path)
        
    if not os.path.exists(input_path):
        print(f"Error: Input file '{input_path}' not found.")
        return

    print(f"Processing: {input_path}")
    
    processor = PDFProcessor(input_path, font_path=args.font)
    
    if args.format in ["pdf", "all"]:
        print("Generating Enhanced PDF...")
        processor.render_new_pdf()
        
    if args.format in ["pptx", "all"]:
        print("Generating PPTX...")
        processor.convert_to_pptx()
        
    print("Done!")

if __name__ == "__main__":
    main()
