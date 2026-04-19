import os
import fitz  # PyMuPDF
import pdfplumber
import pytesseract
from PIL import Image
import io

# Cấu hình đường dẫn Tesseract (mặc định Windows). Thay đổi nếu cài ở chỗ khác.
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_text_from_pdf(pdf_path):
    """
    Trích xuất văn bản từ PDF.
    Kết hợp việc đọc text phẳng và OCR nếu trang là dạng ảnh scan.
    """
    print(f"Đang xử lý tài liệu: {pdf_path}")
    text_result = ""
    
    # Cách 1: Đọc text phẳng bằng pdfplumber
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text_result += page_text + "\n"
    except Exception as e:
        print(f"pdfplumber không thể đọc: {e}")

    # Nếu file PDF không chứa text, chạy OCR
    if not text_result.strip():
        print("Tài liệu dạng Scan, tiến hành OCR toàn bộ sách...")
        doc = fitz.open(pdf_path)
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            image_list = page.get_images(full=True)
            for image_index, img in enumerate(image_list, start=1):
                xref = img[0]
                base_image = doc.extract_image(xref)
                image_bytes = base_image["image"]
                
                image = Image.open(io.BytesIO(image_bytes))
                try:
                    ocr_text = pytesseract.image_to_string(image, lang='eng+vie')
                    text_result += ocr_text + "\n"
                except pytesseract.pytesseract.TesseractNotFoundError:
                    print("LỖI: Tesseract OCR chưa lưu trên máy tính. Bạn chưa cài đặt Tesseract nên không thể đọc dạng sách ảnh được.")
                    return text_result
                except Exception as e:
                    print(f"Lỗi OCR OCR: {e}")
                
    return text_result

def process_all_docs(docs_dir):
    all_extracted_text = {}
    for filename in os.listdir(docs_dir):
        if filename.lower().endswith(".pdf"):
            full_path = os.path.join(docs_dir, filename)
            extracted = extract_text_from_pdf(full_path)
            all_extracted_text[filename] = extracted
            
            # Ghi nháp ra file text để bộ NLP xử lý sau
            with open(f"{filename}_draft.txt", "w", encoding="utf-8") as f:
                f.write(extracted)
    return all_extracted_text

if __name__ == "__main__":
    docs_directory = r"D:\AGENT\KIMM_DOCS"
    if os.path.exists(docs_directory) and os.listdir(docs_directory):
        process_all_docs(docs_directory)
    else:
        print(f"Thư mục {docs_directory} trống hoặc không tồn tại. Vui lòng cho PDF vào đây.")
