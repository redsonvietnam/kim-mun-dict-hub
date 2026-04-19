#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Update database with page references from mapping
"""
import json
import sqlite3

DB_PATH = "kim_mun_dict_v2.db"
MAPPING_FILE = "page_reference_mapping.json"

def update_db_with_page_refs():
    """Load page mapping and update DB"""
    
    with open(MAPPING_FILE, 'r', encoding='utf-8') as f:
        mapping = json.load(f)
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    updated_count = 0
    
    # Iterate through each source
    for source_name, entries_map in mapping.items():
        print(f"\n[{source_name}] Updating {len(entries_map)} entries...")
        
        for entry_id, page_info in entries_map.items():
            page_num = page_info.get('page', '')
            page_ref = f"p.{page_num}" if page_num else ""
            
            c.execute("""
                UPDATE dictionary 
                SET page_ref = ?
                WHERE entry_id = ? AND source = ?
            """, (page_ref, entry_id, source_name))
            
            updated = c.rowcount
            if updated > 0:
                updated_count += updated
    
    conn.commit()
    conn.close()
    
    print(f"\n✅ Updated {updated_count} entries with page references")

def verify_updates():
    """Verify that updates were successful"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    print("\n📊 Verification:")
    
    # Count entries WITH page_ref
    c.execute("SELECT source, COUNT(*) FROM dictionary WHERE page_ref != '' AND page_ref IS NOT NULL GROUP BY source")
    results = c.fetchall()
    for source, count in results:
        print(f"  {source}: {count} entries have page_ref")
    
    # Show sample entries with page_ref
    print("\n📋 Sample entries with page references:")
    c.execute("""
        SELECT entry_id, source, page_ref, vietnamese 
        FROM dictionary 
        WHERE page_ref != '' AND page_ref IS NOT NULL 
        LIMIT 5
    """)
    for row in c.fetchall():
        print(f"  {row[0]:10} {row[1]:20} {row[2]:10} {row[3][:30]}")
    
    conn.close()

if __name__ == "__main__":
    update_db_with_page_refs()
    verify_updates()
