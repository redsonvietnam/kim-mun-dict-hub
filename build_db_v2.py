import sqlite3
import json
import os

def build_database(json_path="kim_mun_translated_demo.json", db_path="kim_mun_dict_v2.db"):
    if not os.path.exists(json_path):
        print(f"Không tìm thấy file {json_path}")
        return
        
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Tạo bảng v3 với cấu trúc mới (hỗ trợ ID và Hán tự)
    cursor.execute('DROP TABLE IF EXISTS dictionary')
    cursor.execute('''
        CREATE TABLE dictionary (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            entry_id TEXT,
            chinese TEXT,
            kimmun TEXT NOT NULL,
            vietnamese TEXT NOT NULL,
            original TEXT,
            phonetic TEXT,
            pos TEXT
        )
    ''')
    
    count = 0
    for entry in data:
        cursor.execute('''
            INSERT INTO dictionary (entry_id, chinese, kimmun, vietnamese, original, phonetic, pos)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            entry.get("entry_id", ""), 
            entry.get("chinese", ""), 
            entry["kimmun"], 
            entry["vietnamese"], 
            entry["original"], 
            entry["phonetic"], 
            entry["pos"]
        ))
        count += 1
        
    conn.commit()
    conn.close()
    print(f"Đã nạp thành công {count} từ vựng vào Database V2: {db_path}")

if __name__ == "__main__":
    build_database()
