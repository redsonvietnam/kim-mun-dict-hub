import re
import json

def clean_ocr_savina(text):
    if not text: return ""
    # Sửa một số lỗi OCR phổ biến của ký tự Pháp/Dao trong tài liệu 1926
    # Thay thế các ký tự đại diện cho dấu tiếng Pháp/Việt cổ
    text = text.replace('A', 'é').replace('A', 'à').replace('A', 'á').replace('A', 'ô').replace('A', 'ù')
    return text.strip()

def is_likely_french(text):
    text = text.strip()
    if not text: return False
    # Tiếng Pháp bắt đầu bằng chữ hoa hoặc mạo từ
    if text[0].isupper(): return True
    if text.split()[0].lower() in ["le", "la", "les", "un", "une", "du", "de", "se", "ne"]: return True
    return False

def extract_savina_tri_lingual(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
        
    entries = []
    started = False
    
    for line in lines:
        line = line.strip()
        if not line: continue
        
        # Mốc nhận diện nội dung bắt đầu từ trang từ điển
        if "Arroyo" in line or "CA'te" in line or "Dire la" in line or "Langue" in line:
            started = True
        if not started: continue
        
        # Bỏ qua rác metadata
        if re.match(r'^- \d+ -$', line) or "FRANAAIS" in line or "K.LM-BI" in line or "TAl-PAN" in line:
            continue

        # Logic bóc tách dùng ranh giới HOA - thường
        words = line.split()
        if len(words) < 2: continue
        
        split_idx = -1
        for i, word in enumerate(words):
            # Từ bắt đầu bằng chữ thường là tiếng Dao (Mun)
            if i > 0 and word[0].islower() and not word.startswith('('):
                split_idx = i
                break
        
        if split_idx != -1:
            french = " ".join(words[:split_idx]).strip()
            mun_part = " ".join(words[split_idx:]).strip()
            
            # Chỉ lấy nếu phần Pháp có vẻ hợp lệ
            if is_likely_french(french):
                # Lấy Kim-mun (bỏ qua Tal-pan sau dấu ;)
                mun_kimm = re.split(r'[;]\s+|\s{2,}', mun_part)[0]
                
                entries.append({
                    "entry_id": f"SA-{len(entries)+1:04d}",
                    "french": clean_ocr_savina(french),
                    "kimmun": clean_ocr_savina(mun_kimm),
                    "source": "Savina (1926)"
                })
                
    # Ghi file QUAN TRỌNG
    with open("savina_tri_lingual_raw.json", "w", encoding="utf-8") as f:
        json.dump(entries, f, ensure_ascii=False, indent=4)
        
    return len(entries)

if __name__ == "__main__":
    count = extract_savina_tri_lingual("befeo_0336-1519_1926_num_26_1_3091.pdf_draft.txt")
    print(f"DONE: Extracted {count} entries.")
