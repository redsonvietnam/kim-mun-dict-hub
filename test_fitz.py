import fitz
import sys

# Set UTF-8 for printing
if sys.stdout.encoding != 'utf-8':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

pdf_path = r"D:\AGENT\KIMM_DOCS\The-Mun-Language-of-Funing-CountyIts-Classified-Lexicon富寧金門語.pdf"

def test_fitz_extraction(page_num):
    doc = fitz.open(pdf_path)
    page = doc[page_num]
    
    print(f"--- FITZ TEXT (raw) ---")
    print(page.get_text("raw")[:500])
    
    print(f"\n--- FITZ TEXT (blocks) ---")
    blocks = page.get_text("blocks")
    for b in blocks[:20]:
        print(f"Block: {b[4][:100]}")

if __name__ == "__main__":
    test_fitz_extraction(6) # Page 7
