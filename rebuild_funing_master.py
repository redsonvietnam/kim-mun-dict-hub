import json
import os

def rebuild_funing_master():
    # 1. Load các nguồn dữ liệu chuyên biệt
    try:
        with open('funing_repaired_data.json', 'r', encoding='utf-8') as f:
            repaired_data = json.load(f)
    except:
        print("Error: funing_repaired_data.json missing")
        return

    try:
        with open('id_hanzi_map.json', 'r', encoding='utf-8') as f:
            hanzi_map = json.load(f)
    except:
        print("Error: id_hanzi_map.json missing")
        hanzi_map = {}

    try:
        with open('full_lexicon_translated.json', 'r', encoding='utf-8') as f:
            translated_orig = json.load(f)
            # Chuyển translated_orig thành map theo ID để tra cứu nhanh cho Pinyin và Vietnamese
            trans_map = {item.get('entry_id'): item for item in translated_orig}
    except:
        print("Error: full_lexicon_translated.json missing")
        trans_map = {}

    final_master = []
    
    for item in repaired_data:
        eid = item.get('entry_id')
        
        # Lấy Hán tự
        hanzi = hanzi_map.get(eid, "")
        
        # Lấy Pinyin và nghĩa Tiếng Việt từ bản gốc đã dịch
        orig_info = trans_map.get(eid, {})
        pinyin = orig_info.get('pinyin', "")
        vietnamese = orig_info.get('vietnamese', item.get('meaning_en', ""))
        
        # Ưu tiên tiếng Dao đã sửa lỗi từ repaired_data
        kimmun = item.get('raw_text', orig_info.get('raw_text', ""))
        
        final_master.append({
            "entry_id": eid,
            "chinese": hanzi,
            "pinyin": pinyin,
            "kimmun": kimmun,
            "vietnamese": vietnamese,
            "meaning_en": item.get('meaning_en', orig_info.get('meaning_en', "")),
            "source": "Shintani (2008)",
            "category": orig_info.get('category', "Academic")
        })
        
    with open('funing_final_master.json', 'w', encoding='utf-8') as f:
        json.dump(final_master, f, ensure_ascii=False, indent=4)
    
    print(f"Successfully rebuilt Funing Master with {len(final_master)} entries.")

if __name__ == "__main__":
    rebuild_funing_master()
