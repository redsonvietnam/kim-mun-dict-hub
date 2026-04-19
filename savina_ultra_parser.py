import re
import json

FR_VN_MAP = {
    "Arbre": "Cây", "Poisson": "Cá", "Buffle": "Trâu", "Tigre": "Hổ", "Chat": "Mèo", 
    "Chien": "Chó", "Maison": "Nhà", "Ciel": "Bầu trời", "Terre": "Đất", "Eau": "Nước", 
    "Feu": "Lửa", "Manger": "Ăn", "Boire": "Uống", "Mourir": "Chết",
    "Arroyo": "Con suối", "CA'te (pente)": "Sườn (dốc)", "Dire la vAcritAc": "Nói thật", "Mentir": "Nói dối"
}

def clean_ocr(text):
    if not text: return ""
    return text.replace('A', 'é').strip()

def extract_savina_split_logic(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
        
    entries = []
    started = False
    
    for line in lines:
        line = line.strip()
        if not line: continue
        if "Arroyo" in line or "CA'te" in line: started = True
        if not started: continue
        if re.match(r'^- \d+ -$', line) or "FRANAAIS" in line or "TAl-PAN" in line: continue

        # Tìm ranh giới giữa Tiếng Pháp và Tiếng Dao
        # Tiếng Pháp thường bắt đầu bằng chữ HOA (Upper)
        # Tiếng Dao thường bắt đầu bằng chữ thường (lower)
        words = line.split()
        if len(words) < 2: continue
        
        # Tìm vị trí của từ đầu tiên bắt đầu bằng chữ thường
        split_idx = -1
        for i, word in enumerate(words):
            # Nếu từ bắt đầu bằng chữ thường (a-z) và không phải là một vệt rác số
            if word[0].islower() and i > 0:
                split_idx = i
                break
        
        if split_idx != -1:
            french = " ".join(words[:split_idx])
            mun = " ".join(words[split_idx:])
            
            # Tách lấy Kim-mun (bỏ qua phần Tal-pan nếu có dấu chấm phẩy)
            kimm = re.split(r'[; ]\s+', mun)[0]
            
            entries.append({
                "entry_id": f"SA-{len(entries)+1:04d}",
                "french": french,
                "kimmun": clean_ocr(kimm),
                "vietnamese": FR_VN_MAP.get(french, f"[Dịch Pháp: {french}]"),
                "source": "Savina (1926)"
            })
            
    return entries

if __name__ == "__main__":
    data = extract_savina_split_logic("befeo_0336-1519_1926_num_26_1_3091.pdf_draft.txt")
    print(f"Total extracted: {len(data)}")
    with open("savina_robust_data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
