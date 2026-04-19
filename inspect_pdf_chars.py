import pdfplumber
import sys

# Set UTF-8 for printing
if sys.stdout.encoding != 'utf-8':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

pdf_path = r"D:\AGENT\KIMM_DOCS\The-Mun-Language-of-Funing-CountyIts-Classified-Lexicon富寧金門語.pdf"

def inspect_chars(page_num):
    print(f"--- Inspecting Chars on Page {page_num+1} ---")
    with pdfplumber.open(pdf_path) as pdf:
        page = pdf.pages[page_num]
        chars = page.chars
        for c in chars[:200]: # Look at first 200 chars
            print(f"Char: '{c['text']}' font: {c['fontname']} size: {c['size']:.1f}")

if __name__ == "__main__":
    inspect_chars(6) # Page 7 roughly has entries 011001...
