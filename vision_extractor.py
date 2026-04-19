import os
import json
import time

try:
    import google.generativeai as genai
    from PIL import Image
except ImportError:
    print("Vui lòng cài đặt google-generativeai và pillow: pip install google-generativeai pillow")
    exit(1)

API_KEY = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY") 

if not API_KEY:
    print("CHÚ Ý: Không tìm thấy GEMINI_API_KEY trong biến môi trường.")
    API_KEY = input("Vui lòng nhập Gemini API Key của bạn để tiếp tục: ").strip()

genai.configure(api_key=API_KEY)
# Sử dụng model có khả năng Vision
model = genai.GenerativeModel('gemini-1.5-flash')

def extract_phonology():
    print("Bắt đầu trích xuất phần Âm vị học (Phonology) - Trang 13 đến 20...")
    phonology_markdown = "# Kim Mun Phonology (Shintani 2008)\n\n"
    # Giả sử ta đã sinh các ảnh toc_p... hoặc ta gọi gen ảnh từ trang 13-20.
    # Trong môi trường hiện hành ta chưa crop trang 13-19, nên code sample này sẽ crop nếu file chưa tồn tại.
    import fitz
    pdf_path = 'D:/AGENT/KIMM_DOCS/The-Mun-Language-of-Funing-CountyIts-Classified-Lexicon富寧金門語.pdf'
    
    doc = fitz.open(pdf_path)
    
    for i in range(12, 20): # PDF index 12 to 19 tương ứng trang đánh số 13-20
        img_filename = f"phonology_p{i}.png"
        if not os.path.exists(img_filename):
            print(f"Đang tạo ảnh {img_filename}...")
            doc[i].get_pixmap(dpi=150).save(img_filename)
        
        print(f"Đang gửi {img_filename} lên AI Vision...")
        img = Image.open(img_filename)
        
        prompt = "Extract all text from this phonology page accurately. Preserve linguistic symbols, IPA phonetics, and tables if any. Format the output elegantly in Markdown. Output ONLY the markdown text without any conversational filler."
        response = model.generate_content([prompt, img])
        
        phonology_markdown += f"## Page {i-11}\n\n" + response.text + "\n\n"
        time.sleep(2) # Tránh rate limit
        
    with open("kim_mun_phonology.md", "w", encoding="utf-8") as f:
        f.write(phonology_markdown)
    print("✅ Đã trích xuất xong Âm vị học!")

def extract_topic_1():
    print("\nBắt đầu trích xuất từ vựng Topic 1 (Trang 21 đến 34)...")
    topic_words = []
    
    for i in range(20, 34): # PDF index 20 to 33, ta đã crop topic1_p20.png đến topic1_p33.png
        img_filename = f"topic1_p{i}.png"
        if not os.path.exists(img_filename):
            print(f"Không tìm thấy {img_filename}, bỏ qua.")
            continue
            
        print(f"Đang phân tích bảng từ vựng từ {img_filename}...")
        img = Image.open(img_filename)
        
        prompt = """
        You are an expert OCR and linguist assistant for Kim Mun Dao language.
        Extract all vocabulary entries from this dictionary page image into a JSON array of objects.
        Each object should strictly follow this schema:
        {
          "id": "e.g., 011001",
          "hanzi": "Extract the traditional Chinese character",
          "pinyin": "Extract the pinyin if present",
          "kimmun": "Extract the Kim Mun word including IPA phonetics like /ts/ or tone letters",
          "vietnamese": "Extract Vietnamese meaning if present. If there is only English, put the English meaning here or translate to Vietnamese briefly",
          "english": "Extract English meaning if present",
          "subcategory": "The subtopic context, e.g. '011. Sky, weather, light'"
        }
        Only output valid JSON starting with [ and ending with ]. Make sure to escape quotes inside strings. Do not output anything else.
        If the page has a subcategory header (e.g. 011. Sky, weather, light), figure out the current subcategory and apply it to the words.
        """
        response = model.generate_content([prompt, img])
        try:
           json_text = response.text.strip()
           if json_text.startswith("```json"):
               json_text = json_text[7:-3]
           page_data = json.loads(json_text)
           topic_words.extend(page_data)
           print(f"   -> Đã lấy được {len(page_data)} từ.")
        except Exception as e:
           print(f"   -> Lỗi parse JSON ở trang {i}: {e}")
        time.sleep(3)
        
    with open("funing_topic1_vision.json", "w", encoding="utf-8") as f:
        json.dump(topic_words, f, ensure_ascii=False, indent=2)
    print("✅ Đã trích xuất xong Từ vựng Topic 1!")

if __name__ == "__main__":
    extract_phonology()
    extract_topic_1()
