import pdfplumber
import sys

if sys.stdout.encoding != 'utf-8':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

pdf_path = r"D:\AGENT\KIMM_DOCS\A phonological analysis and comparison of two Kim Mun varieties in Laos and Vietnam.pdf"

def analyze_wordlist_layout(page_num):
    with pdfplumber.open(pdf_path) as pdf:
        page = pdf.pages[page_num]
        words = page.extract_words()
        
        # Look for 'ant' and 'sky' or their reversed forms
        for w in words:
            # Check for words near the top
            if w['top'] < 200:
                print(f"[{w['text']}] x={w['x0']:.1f} y={w['top']:.1f}")

if __name__ == "__main__":
    # The draft said TOC Appendix A is 156. 
    # Draft line 3824 is Appendix A. 
    # Let's try page 171 (156 + ~15 offset) or search for Appendix A page.
    analyze_wordlist_layout(170) 
