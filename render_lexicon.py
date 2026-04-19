import fitz
import os

pdf_path = r"D:\AGENT\KIMM_DOCS\The-Mun-Language-of-Funing-CountyIts-Classified-Lexicon富寧金門語.pdf"
output_dir = "lexicon_pages"

import argparse

def render_pages(start_page=21, end_page=50):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    doc = fitz.open(pdf_path)
    total_pages = len(doc)
    print(f"Total PDF pages: {total_pages}")
    
    end_page = min(end_page, total_pages)
    
    for page_num in range(start_page - 1, end_page):
        page = doc[page_num]
        pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
        img_path = os.path.join(output_dir, f"page_{page_num + 1}.png")
        pix.save(img_path)
        print(f"Saved {img_path}")
        
    doc.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--start", type=int, default=21)
    parser.add_argument("--end", type=int, default=472)
    args = parser.parse_args()
    render_pages(args.start, args.end)
