import os
import glob
import re
import json

def parse_dictionary_text(raw_text):
    entries = []
    lines = raw_text.split('\n')
    
    i = 0
    sa_count = 1
    while i < len(lines):
        line = lines[i].strip()
        i += 1
        
        # 1. Nhận diện cấu trúc Funing Lexicon (mã số 6 chữ số)
        funing_match = re.search(r'^(\d{6})\.\s+(.*?)\s+([a-zA-Z\s\',-]+)(?:\s+/|/|$)', line)
        if funing_match:
            code = funing_match.group(1)
            chinese_raw = funing_match.group(2)
            english = funing_match.group(3).strip()
            
            # Tách Hán tự và Pinyin (Pinyin thường ở cuối và là chữ không dấu Latin)
            # Ví dụ: "ffff ^ qingtian" -> "ffff ^" và "qingtian"
            chinese = ""
            pinyin = chinese_raw
            if " " in chinese_raw:
                parts = chinese_raw.rsplit(" ", 1)
                chinese = parts[0]
                pinyin = parts[1]
                
            # Kiểm tra dòng tiếp theo xem có phải từ tiếng Mun không
            mun_word = ""
            if i < len(lines):
                next_line = lines[i].strip()
                if next_line and not re.match(r'^\d{6}\.', next_line) and len(next_line) < 40:
                    mun_word = next_line
                    i += 1
            
            if mun_word:
                entries.append({
                    "entry_id": code,
                    "chinese": chinese,
                    "word": english,        
                    "meaning": mun_word,    
                    "pos": "Funing",        
                    "phonetic": pinyin 
                })
            continue

        # 2. Nhận diện cấu trúc Savina (Và các tài liệu khác dùng dấu cách)
        if len(line) < 3 or line.isupper() or ":" in line:
            continue
            
        parts = re.split(r'\s{2,}|\t', line)
        if len(parts) >= 2:
            entries.append({
                "entry_id": f"SA-{sa_count:04d}",
                "chinese": "",
                "word": parts[0].strip(),
                "meaning": " | ".join(p.strip() for p in parts[1:] if p.strip()),
                "pos": "Savina",
                "phonetic": ""
            })
            sa_count += 1
        else:
            # Fallback cho Savina/Befeo khi chỉ dùng 1 dấu cách
            words = line.split()
            if 2 <= len(words) <= 5 and not re.search(r'\d', line):
                entries.append({
                    "entry_id": f"SA-{sa_count:04d}",
                    "chinese": "",
                    "word": words[0],
                    "meaning": " ".join(words[1:]),
                    "pos": "Savina",
                    "phonetic": ""
                })
                sa_count += 1
                
    return entries

def process_all_drafts():
    all_entries = []
    for txt_file in glob.glob("*_draft.txt"):
        print(f"Processing draft: {txt_file}")
        with open(txt_file, 'r', encoding='utf-8', errors='ignore') as f:
            text = f.read()
            entries = parse_dictionary_text(text)
            all_entries.extend(entries)
            print(f" -> Extracted {len(entries)} words.")
            
    with open("kim_mun_parsed.json", "w", encoding="utf-8") as f:
        json.dump(all_entries, f, ensure_ascii=False, indent=4)
        print(f"\n[OK] Exported {len(all_entries)} words to kim_mun_parsed.json")

if __name__ == "__main__":
    process_all_drafts()
