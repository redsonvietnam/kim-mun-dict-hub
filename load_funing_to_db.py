#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Load Funing data từ funing_final_master_cleaned.json vào kim_mun_dict_v2.db
"""
import json
import sqlite3
from pathlib import Path

DB_PATH = "kim_mun_dict_v2.db"
FUNING_JSON = "funing_final_master_cleaned.json"

def load_funing_to_db():
    print(f"📖 Đọc file {FUNING_JSON}...")
    with open(FUNING_JSON, 'r', encoding='utf-8') as f:
        funing_data = json.load(f)
    
    print(f"✅ Đã tải {len(funing_data)} entries từ Funing")
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Kiểm tra schema
    c.execute("PRAGMA table_info(dictionary)")
    columns = [row[1] for row in c.fetchall()]
    print(f"\n📋 Database columns: {columns}")
    
    # Map Funing JSON fields -> DB columns
    inserted = 0
    skipped = 0
    
    for item in funing_data:
        try:
            # Ensure all required fields
            entry_id = item.get('entry_id', '').strip()
            chinese = item.get('chinese', '').strip()
            pinyin = item.get('pinyin', '').strip()
            kimmun = item.get('kimmun', '').strip()
            vietnamese = item.get('vietnamese', '').strip()
            meaning_en = item.get('meaning_en', '').strip()
            source = item.get('source', 'Shintani (2008)').strip()
            category = item.get('category', '').strip()
            
            if not entry_id or not chinese:
                skipped += 1
                continue
            
            # Check if entry already exists
            c.execute("SELECT COUNT(*) FROM dictionary WHERE entry_id = ?", (entry_id,))
            if c.fetchone()[0] > 0:
                skipped += 1
                continue
            
            # Insert into DB
            c.execute("""
                INSERT INTO dictionary 
                (entry_id, chinese, pinyin, kimmun, vietnamese, meaning_en, source, category, subcategory, page_ref, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                entry_id,
                chinese,
                pinyin,
                kimmun,
                vietnamese,
                meaning_en,
                source,
                category,
                '',  # subcategory
                '',  # page_ref
                ''   # notes
            ))
            inserted += 1
            
        except Exception as e:
            print(f"❌ Lỗi khi xử lý entry {item.get('entry_id', '?')}: {e}")
            skipped += 1
    
    conn.commit()
    conn.close()
    
    print(f"\n✅ Hoàn thành!")
    print(f"   Inserted: {inserted}")
    print(f"   Skipped: {skipped}")
    
    # Verify
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM dictionary")
    total = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM dictionary WHERE source = ?", ("Shintani (2008)",))
    shintani_count = c.fetchone()[0]
    conn.close()
    
    print(f"\n📊 Verification:")
    print(f"   Total entries in DB: {total}")
    print(f"   Shintani (2008) entries: {shintani_count}")

if __name__ == "__main__":
    load_funing_to_db()
