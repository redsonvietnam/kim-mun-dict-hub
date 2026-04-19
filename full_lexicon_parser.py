import re
import json
import os

def parse_full_lexicon(draft_path, hanzi_map_path):
    with open(draft_path, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()
        
    with open(hanzi_map_path, 'r', encoding='utf-8') as f:
        hanzi_map = json.load(f)
        
    entries = []
    current_category = ""
    current_subcategory = ""
    
    # Regex cho ID (6 chữ số)
    id_pattern = re.compile(r'^(\d{6})\.')
    # Regex cho Category (vd: 01. Nature)
    cat_pattern = re.compile(r'^(\d{2})\.\s+(.*)')
    # Regex cho Subcategory (vd: 011. Sky)
    subcat_pattern = re.compile(r'^(\d{3})\.\s+(.*)')
    
    for line in lines:
        line = line.strip()
        if not line: continue
        
        # Cập nhật Category
        cat_match = cat_pattern.match(line)
        if cat_match:
            current_category = cat_match.group(2)
            continue
            
        subcat_match = subcat_pattern.match(line)
        if subcat_match:
            current_subcategory = subcat_match.group(2)
            continue
            
        # Tìm mục từ
        id_match = id_pattern.match(line)
        if id_match:
            eid = id_match.group(1)
            # Tách nội dung còn lại
            content = line[id_match.end():].strip()
            
            # Cấu trúc thường là: [Pinyin] [English] [Phonetic]
            # Lưu ý: Pinyin thường chữ thường, English có thể hoa/thường, Phonetic trong //
            
            item = {
                "entry_id": eid,
                "chinese": hanzi_map.get(eid, ""),
                "category": current_category,
                "subcategory": current_subcategory,
                "raw_text": content
            }
            
            # Phân tách sơ bộ Pinyin và English (English thường đứng ở giữa hoặc cuối)
            # Đây là logic demo, cần tinh chỉnh sau
            parts = content.split('  ') # Nhiều khoảng trắng thường phân tách các trường
            parts = [p.strip() for p in parts if p.strip()]
            
            if len(parts) >= 2:
                item["pinyin"] = parts[0]
                item["meaning_en"] = parts[1]
                if len(parts) > 2:
                    item["phonetic"] = parts[2]
            else:
                item["meaning_en"] = content
                
            entries.append(item)
            
    return entries

if __name__ == "__main__":
    draft = r"D:\AGENT\dict_builder\The-Mun-Language-of-Funing-CountyIts-Classified-Lexicon富寧金門語.pdf_draft.txt"
    hmap = r"D:\AGENT\dict_builder\id_hanzi_map.json"
    
    print("Parsing full lexicon...")
    all_entries = parse_full_lexicon(draft, hmap)
    
    with open("full_lexicon_data.json", "w", encoding="utf-8") as f:
        json.dump(all_entries, f, ensure_ascii=False, indent=4)
        
    print(f"Extracted {len(all_entries)} entries with categories.")
