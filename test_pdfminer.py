from pdfminer.high_level import extract_text
import sys

# Set UTF-8 for printing
if sys.stdout.encoding != 'utf-8':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

pdf_path = r"D:\AGENT\KIMM_DOCS\The-Mun-Language-of-Funing-CountyIts-Classified-Lexicon富寧金門語.pdf"

def test_pdfminer():
    print("--- Testing pdfminer.six ---")
    try:
        # Extract only page 7 (index 6)
        text = extract_text(pdf_path, page_numbers=[6])
        print(text[:1000])
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_pdfminer()
