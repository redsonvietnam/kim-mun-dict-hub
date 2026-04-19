import sqlite3
import json
import os

def build_final_database(db_path="kim_mun_dict_v2.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Tạo bảng v3 hoàn thiện
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
    
    total_count = 0

    # 1. Nạp từ kim_mun_translated_demo.json (Savina + Funing đã dịch)
    if os.path.exists("kim_mun_translated_demo.json"):
        with open("kim_mun_translated_demo.json", "r", encoding="utf-8") as f:
            data = json.load(f)
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
                total_count += 1
        print(f"Loaded {total_count} entries from demo JSON.")

    # 2. Nạp từ clark_final_data.json (Clark 2008)
    if os.path.exists("clark_final_data.json"):
        clark_count = 0
        with open("clark_final_data.json", "r", encoding="utf-8") as f:
            data = json.load(f)
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
                clark_count += 1
        total_count += clark_count
        print(f"Loaded {clark_count} additional entries from Clark JSON.")
        
    conn.commit()
    conn.close()
    print(f"\n[SUCCESS] Total {total_count} entries integrated into {db_path}")

if __name__ == "__main__":
    build_final_database()
