import easyocr
import os
import re
import json

def is_chinese(text):
    """Kiểm tra xem chuỗi có chứa ký tự Hán không."""
    return any('\u4e00' <= char <= '\u9fff' for char in text)

def extract_hanzi_from_page(reader, image_path):
    print(f"Reading {image_path}...")
    results = reader.readtext(image_path)
    
    # Sắp xếp theo trục Y (dòng), rồi trục X (từ trái qua phải)
    results.sort(key=lambda x: (x[0][0][1], x[0][0][0]))
    
    id_map = {}
    current_id = None
    
    for bbox, text, conf in results:
        text = text.strip()
        # Tìm mã ID (6 chữ số + dấu chấm)
        match = re.search(r'(\d{6})\.', text)
        if match:
            current_id = match.group(1)
            # Chỉ lấy các ký tự thuộc dải Unicode của chữ Hán
            hanzi_only = "".join([c for c in text if '\u4e00' <= c <= '\u9fff'])
            if hanzi_only:
                id_map[current_id] = hanzi_only
            continue
            
        # Nếu đã có current_id mà chưa có Hán tự, kiểm tra block tiếp theo
        if current_id and current_id not in id_map:
            hanzi_only = "".join([c for c in text if '\u4e00' <= c <= '\u9fff'])
            if hanzi_only:
                id_map[current_id] = hanzi_only
            # Nếu gặp một text block có vẻ là Pinyin hoặc tiếng Anh dài quá thì dừng tìm Hán tự cho ID này
            elif len(text) > 20: 
                # Có thể Hán tự bị thiếu cho ID này
                pass

    return id_map

def bulk_process(img_dir="lexicon_pages"):
    reader = easyocr.Reader(['ch_sim', 'en'])
    all_mappings = {}
    
    files = sorted([f for f in os.listdir(img_dir) if f.endswith(".png")], 
                   key=lambda x: int(re.search(r'(\d+)', x).group(1)))
    
    for filename in files:
        img_path = os.path.join(img_dir, filename)
        page_map = extract_hanzi_from_page(reader, img_path)
        all_mappings.update(page_map)
        print(f" -> Extracted {len(page_map)} IDs from {filename}")
        
    with open("id_hanzi_map.json", "w", encoding="utf-8") as f:
        json.dump(all_mappings, f, ensure_ascii=False, indent=4)
        
    print(f"\n[DONE] Total {len(all_mappings)} IDs mapped to Hanzi.")

if __name__ == "__main__":
    bulk_process()
