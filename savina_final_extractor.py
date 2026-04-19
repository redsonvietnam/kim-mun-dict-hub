import re
import json

def clean_ocr(text):
    # Sửa các lỗi OCR phổ biến trong tài liệu Savina
    text = text.replace('A', 'á').replace('A', 'à').replace('A', 'é').replace('A', 'ê').replace('A', 'ó')
    return text.strip()

def extract_savina_v2(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
        
    entries = []
    started = False
    
    # Một bộ dịch thuật Pháp-Việt cơ bản cho các danh từ trong từ điển cổ
    fr_vn_map = {
        "Arbre": "Cây", "Racine": "Rễ", "Feuille": "Lá", "Ecorce": "Vỏ cây", "Branche": "Cành",
        "Poisson": "Cá", "Buffle": "Trâu", "Tigre": "Hổ", "Chat": "Mèo", "Chien": "Chó",
        "Maison": "Nhà", "Porte": "Cửa", "Ciel": "Bầu trời", "Terre": "Đất", "Eau": "Nước",
        "Feu": "Lửa", "Manger": "Ăn", "Boire": "Uống", "Mourir": "Chết"
    }

    for line in lines:
        line = line.strip()
        if not line: continue
        
        # Nhận diện điểm bắt đầu nội dung từ điển
        if "Arroyo" in line or "CA'te" in line or "Dire la" in line:
            started = True
        
        if not started: continue
        if re.match(r'^- \d+ -$', line) or "FRANAAIS" in line or "K.LM-BI" in line: continue

        # Tách tiếng Pháp và tiếng Dao
        # Giả định: Tiếng Pháp bắt đầu dòng, là cụm từ đầu tiên
        # Tiếng Dao thường viết thường và bắt đầu sau tiếng Pháp
        match = re.search(r'^([A-Z\'][^a-z]*[a-z\']+(?:\s+[a-z\']+)*)\s+([a-z].+)$', line)
        if match:
            french = match.group(1).strip()
            mun_part = match.group(2).strip()
            
            # Chỉ lấy Kim-mun (phần đầu tiên của cụm từ tiếng Dao)
            mun_kimm = re.split(r'[; ]\s+', mun_part)[0]
            
            entries.append({
                "source": "Savina (1926)",
                "entry_id": f"SA-{len(entries)+1:04d}",
                "french": french,
                "meaning_en": f"(French) {french}",
                "vietnamese": fr_vn_map.get(french, f"[VN] {french}"),
                "kimmun": clean_ocr(mun_kimm),
                "category": "Savina Dictionary"
            })
            
    with open("savina_final_clean.json", "w", encoding="utf-8") as f:
        json.dump(entries, f, ensure_ascii=False, indent=4)
    
    return entries

if __name__ == "__main__":
    results = extract_savina_v2("befeo_0336-1519_1926_num_26_1_3091.pdf_draft.txt")
    print(f"Extracted {len(results)} Savina entries.")
