import re
import json
import glob

def extract_funing_robust():
    # Tìm file chính xác bằng glob để tránh ký tự đặc biệt
    files = glob.glob("The-Mun-Language-of-Funing-CountyIts-Classified-Lexicon*.txt")
    if not files:
        print("Không tìm thấy file Funing.")
        return []
    
    file_path = files[0]
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    segments = re.split(r'(\d{6}\.)', content)
    entries = []
    
    for i in range(1, len(segments), 2):
        entry_id = segments[i].replace('.', '').strip()
        body = segments[i+1]
        
        # Tiếng Dao (Mun) và phiên âm /.../
        mun_match = re.search(r'([A-Za-z\s][A-Za-z\s]+\s+/[^/]+/)', body)
        mun_text = mun_match.group(1).strip() if mun_match else ""
        
        # Nghĩa tiếng Anh
        en_match = re.search(r'/\s+([^0-9\n>]{3,})', body)
        meaning_en = en_match.group(1).split('\n')[0].strip() if en_match else ""
        
        if not mun_text:
            lines = [l for l in body.split('\n') if '/' in l]
            if lines: mun_text = lines[0].strip()
            
        entries.append({
            "entry_id": entry_id,
            "raw_text": mun_text,
            "meaning_en": meaning_en,
            "source": "Shintani (2008)"
        })
        
    with open("funing_repaired_data.json", "w", encoding="utf-8") as f:
        json.dump(entries, f, ensure_ascii=False, indent=4)
        
    return entries

if __name__ == "__main__":
    results = extract_funing_robust()
    print(f"Extracted {len(results)} Funing entries.")
