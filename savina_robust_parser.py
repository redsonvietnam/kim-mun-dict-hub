import re
import json

# Tập hợp từ điển Pháp-Việt mở rộng để dịch nghĩa chính xác
FR_VN_MAP = {
    "Arbre": "Cây", "Racine": "Rễ", "Feuille": "Lá", "Ecorce": "Vỏ cây", "Branche": "Cành",
    "Poisson": "Cá", "Buffle": "Trâu", "Tigre": "Hổ", "Chat": "Mèo", "Chien": "Chó",
    "Maison": "Nhà", "Porte": "Cửa", "Ciel": "Bầu trời", "Terre": "Đất", "Eau": "Nước",
    "Feu": "Lửa", "Manger": "Ăn", "Boire": "Uống", "Mourir": "Chết", "Grand": "Lớn",
    "Petit": "Nhỏ", "Vieux": "Già", "Neuf": "Mới", "Fils": "Con trai", "Fille": "Con gái",
    "Arroyo": "Con suối", "Chemin": "Đường đi", "Pierre": "Đá", "Soleil": "Mặt trời",
    "Lune": "Mặt trăng", "Nuit": "Đêm", "Midi": "Trưa", "Homme": "Đàn ông", "Femme": "Đàn bà"
}

def clean_ocr(text):
    if not text: return ""
    # Sửa lỗi OCR: Savina thường dùng A cho các chữ có dấu
    text = text.replace('A', 'é').replace('A', 'à').replace('A', 'á')
    return text.strip()

def extract_savina_final_fixed(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
        
    entries = []
    started = False
    
    for line in lines:
        line = line.strip()
        if not line: continue
        if "Arroyo" in line or "CA'te" in line: started = True
        if not started: continue
        if re.match(r'^- \d+ -$', line) or "FRANAAIS" in line: continue

        # Chiến thuật bóc tách:
        # Tiếng Pháp: Cụm từ đầu tiên bắt đầu bằng chữ HOA.
        # Tiếng Dao: Bắt đầu ngay khi gặp từ viết thường (lower case).
        words = line.split()
        if len(words) < 2: continue
        
        split_idx = -1
        for i, word in enumerate(words):
            # Tìm từ đầu tiên bắt đầu bằng chữ thường (a-z)
            # Mun Dao thường viết thường trong tài liệu Savina
            if i > 0 and word[0].islower() and not word.startswith('('):
                split_idx = i
                break
        
        if split_idx != -1:
            french = " ".join(words[:split_idx]).strip()
            mun_part = " ".join(words[split_idx:]).strip()
            
            # Tách lấy Mun Kim-mun đầu tiên (trước dấu ; hoặc khoảng cách lớn)
            mun_kimm = re.split(r'[;]\s+|\s{2,}', mun_part)[0]
            
            # Chỉ lấy nếu Tiếng Pháp có độ dài hợp lý và không phải rác OCR
            if len(french) > 1 and not french.isdigit():
                vn = FR_VN_MAP.get(french, f"[Dịch từ Pháp: {french}]")
                entries.append({
                    "entry_id": f"SA-{len(entries)+1:04d}",
                    "french": french, # Trường này cực kỳ quan trọng
                    "kimmun": clean_ocr(mun_kimm),
                    "vietnamese": vn,
                    "source": "Savina (1926)"
                })
            
    # Lưu vào JSON
    with open("savina_robust_data.json", "w", encoding="utf-8") as f:
        json.dump(entries, f, ensure_ascii=False, indent=4)
        
    return entries

if __name__ == "__main__":
    results = extract_savina_final_fixed("befeo_0336-1519_1926_num_26_1_3091.pdf_draft.txt")
    print(f"Bóc tách thành công {len(results)} mục từ Savina.")
