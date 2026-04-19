import pdfplumber
import os

pdf_path = r"D:\AGENT\KIMM_DOCS\A phonological analysis and comparison of two Kim Mun varieties in Laos and Vietnam.pdf"

def examine_page(page_num):
    print(f"--- Examining Page {page_num+1} ---")
    with pdfplumber.open(pdf_path) as pdf:
        page = pdf.pages[page_num]
        words = page.extract_words()
        # Sort words by top (y) then x
        sorted_words = sorted(words, key=lambda w: (w['top'], w['x0']))
        
        # Group words by line (approximate y-coordinate)
        lines = []
        if sorted_words:
            current_line = [sorted_words[0]]
            for w in sorted_words[1:]:
                if abs(w['top'] - current_line[0]['top']) < 5:
                    current_line.append(w)
                else:
                    lines.append(current_line)
                    current_line = [w]
            lines.append(current_line)
            
        for line_words in lines[:50]:
            line_str = " | ".join([f"{w['text']} ({w['x0']:.0f})" for w in line_words])
            print(line_str)

if __name__ == "__main__":
    examine_page(156) # Page 157 (Appendix A roughly starts here)
    examine_page(160) # A middle wordlist page
