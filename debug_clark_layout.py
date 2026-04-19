import pdfplumber
import os

pdf_path = r"D:\AGENT\KIMM_DOCS\A phonological analysis and comparison of two Kim Mun varieties in Laos and Vietnam.pdf"

def debug_appendix():
    with pdfplumber.open(pdf_path) as pdf:
        # Appendix A starts on page 156 (index 155)
        # Check page 158
        page = pdf.pages[157]
        words = page.extract_words()
        for w in words[:100]:
            print(f"{w['text']} ({w['x0']:.1f}, {w['top']:.1f})")

if __name__ == "__main__":
    debug_appendix()
