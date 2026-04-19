import sqlite3
import json
import os

def rebuild_full_database(json_path="full_lexicon_translated.json", db_path="kim_mun_dict_v2.db"):
    if not os.path.exists(json_path):
        print(f"File {json_path} chưa tồn tại.")
        return
        
    with open(json_path, "r", encoding="utf-8") as f:
        lexicon_data = json.load(f)
        
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Tạo bảng mới với cấu trúc hoàn thiện hơn
    cursor.execute('DROP TABLE IF EXISTS dictionary_temp')
    cursor.execute('''
        CREATE TABLE dictionary_temp (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            entry_id TEXT,
            chinese TEXT,
            kimmun TEXT,
            pinyin TEXT,
            vietnamese TEXT,
            meaning_en TEXT,
            phonetic TEXT,
            category TEXT,
            subcategory TEXT,
            pos TEXT
        )
    ''')
    
    # Một bảng tra cứu nghĩa tiếng Việt cho các từ thông dụng để demo 4000 từ
    # (Trong thực tế nên dùng API dịch thuật, đây là bản demo tích hợp sẵn một số từ)
    trans_map = {
        "sky": "bầu trời", "sun": "mặt trời", "moon": "mặt trăng", "star": "ngôi sao",
        "cloud": "mây", "rain": "mưa", "wind": "gió", "fire": "lửa", "water": "nước",
        "earth": "đất", "mountain": "núi", "river": "sông", "sea": "biển",
        "animal": "động vật", "tiger": "hổ", "lion": "sư tử", "bird": "chim",
        "tree": "cây", "flower": "hoa", "grass": "cỏ", "fruit": "trái cây",
        "meat": "thịt", "fish": "cá", "man": "đàn ông", "woman": "phụ nữ"
    }
    
    insert_data = []
    for item in lexicon_data:
        # Sử dụng nghĩa tiếng Việt đã được dịch từ script translator
        viet = item.get("vietnamese", "")
        if not viet and item.get("meaning_en"):
            viet = item["meaning_en"].capitalize()
            
        insert_data.append((
            item.get("entry_id"),
            item.get("chinese"),
            item.get("raw_text"), # kimmun field
            item.get("pinyin"),
            viet,
            item.get("meaning_en"),
            item.get("phonetic"),
            item.get("category"),
            item.get("subcategory"),
            "" # pos
        ))
        
    cursor.executemany('''
        INSERT INTO dictionary_temp (entry_id, chinese, kimmun, pinyin, vietnamese, meaning_en, phonetic, category, subcategory, pos)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', insert_data)
    
    # Thay thế bảng cũ
    cursor.execute('DROP TABLE IF EXISTS dictionary')
    cursor.execute('ALTER TABLE dictionary_temp RENAME TO dictionary')
    
    conn.commit()
    conn.close()
    print(f"Đã tái cấu trúc Database thành công với {len(insert_data)} mục từ.")

if __name__ == "__main__":
    rebuild_full_database()
