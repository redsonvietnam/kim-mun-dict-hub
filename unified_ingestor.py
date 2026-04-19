import sqlite3
import json
import os

def unified_ingestion_v4():
    db_path = "kim_mun_dict_v2.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute('DROP TABLE IF EXISTS dictionary_new')
    cursor.execute('''
        CREATE TABLE dictionary_new (
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
            source TEXT,
            pos TEXT,
            french_orig TEXT
        )
    ''')
    
    all_records = []
    
    # --- 1. FUNING (FINAL MASTER - CONTAINS HANZI & PINYIN) ---
    funing_path = "funing_final_master_cleaned.json"
    if os.path.exists(funing_path):
        with open(funing_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            for item in data:
                all_records.append((
                    item.get("entry_id"),
                    item.get("chinese"), # KHÔI PHỤC HÁN TỰ
                    item.get("kimmun"),
                    item.get("pinyin"),  # KHÔI PHỤC PINYIN
                    item.get("vietnamese"),
                    item.get("meaning_en"),
                    "",
                    item.get("category", "Academic"),
                    "",
                    "Shintani (2008)",
                    "", ""
                ))
        print(f"Loaded {len(data)} from Funing (Final Master with Hanzi).")

    # --- 2. SAVINA (TRI-LINGUAL FINAL) ---
    savina_path = "savina_tri_lingual_final.json"
    if os.path.exists(savina_path):
        with open(savina_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            for item in data:
                all_records.append((
                    item.get("entry_id"), "", item.get("kimmun"), "",
                    item.get("vietnamese"), item.get("meaning_en"), "",
                    "Savina Dictionary", "", "Savina (1926)",
                    "Savina", item.get("french")
                ))
        print(f"Loaded {len(data)} from Savina (Tri-lingual).")

    # --- 3. CLARK (STABLE) ---
    clark_path = "clark_final_data.json"
    if os.path.exists(clark_path):
        with open(clark_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            for item in data:
                all_records.append((
                    item.get("entry_id"), item.get("chinese"), item.get("kimmun"), "",
                    item.get("vietnamese"), item.get("original"), item.get("phonetic"),
                    "General", "", "Clark (2000)", item.get("pos"), ""
                ))
        print(f"Loaded {len(data)} from Clark.")

    cursor.executemany('''
        INSERT INTO dictionary_new (entry_id, chinese, kimmun, pinyin, vietnamese, meaning_en, phonetic, category, subcategory, source, pos, french_orig)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', all_records)
    
    cursor.execute('DROP TABLE IF EXISTS dictionary')
    cursor.execute('ALTER TABLE dictionary_new RENAME TO dictionary')
    
    conn.commit()
    conn.close()
    print("Unified Database V4 Overhaul Complete (Hanzi/Pinyin Restored)!")

if __name__ == "__main__":
    unified_ingestion_v4()
