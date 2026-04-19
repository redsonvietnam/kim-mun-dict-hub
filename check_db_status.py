#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Check database status"""
import sqlite3
import json
from pathlib import Path

DB_PATH = "kim_mun_dict_v2.db"

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

# Check total entries
c.execute('SELECT COUNT(*) FROM dictionary')
total = c.fetchone()[0]
print(f"✅ Total entries in DB: {total}")

# Check by source
c.execute('SELECT source, COUNT(*) FROM dictionary GROUP BY source ORDER BY COUNT(*) DESC')
print("\n📊 Entries by source:")
for source, count in c.fetchall():
    print(f"   {source}: {count}")

# Check by category
c.execute('SELECT category, COUNT(*) FROM dictionary WHERE category != "" AND category != "General" GROUP BY category ORDER BY COUNT(*) DESC LIMIT 10')
print("\n📚 Top 10 categories:")
for cat, count in c.fetchall():
    print(f"   {cat}: {count}")

# Check if there are Funing entries with Phonology/Topic 1 data
c.execute('SELECT COUNT(*) FROM dictionary WHERE source LIKE "%Funing%"')
funing_count = c.fetchone()[0]
print(f"\n🔤 Funing entries: {funing_count}")

conn.close()

# Check JSON files
print("\n📄 Latest JSON files:")
json_files = [
    "funing_final_master_cleaned.json",
    "savina_robust_data.json",
    "clark_final_data.json"
]

for jf in json_files:
    if Path(jf).exists():
        with open(jf, 'r', encoding='utf-8') as f:
            data = json.load(f)
            print(f"   {jf}: {len(data)} entries")
