import pdfplumber

pdf_path = r"D:\AGENT\KIMM_DOCS\A phonological analysis and comparison of two Kim Mun varieties in Laos and Vietnam.pdf"

def find_appendix():
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages):
            text = page.extract_text()
            if text and "APPENDIX A" in text:
                print(f"Found APPENDIX A on PDF page index {i} (Page {i+1})")
                return i
    return -1

if __name__ == "__main__":
    find_appendix()
