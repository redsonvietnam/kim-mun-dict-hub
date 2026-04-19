#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Export entries WITH page references for easy manual review and correction
Xuất entries với page_ref để bạn review và chỉnh sửa
"""
import sqlite3
import csv
from pathlib import Path

DB_PATH = "kim_mun_dict_v2.db"

def export_for_page_review():
    """Export all entries with page_ref for review and correction"""
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Get all entries with page info, grouped by source
    c.execute("""
        SELECT entry_id, source, page_ref, chinese, pinyin, kimmun, vietnamese, 
               meaning_en, category, notes
        FROM dictionary
        ORDER BY source, page_ref
    """)
    
    rows = c.fetchall()
    conn.close()
    
    # Export to CSV
    output_file = "kim_mun_dict_with_pages.csv"
    
    with open(output_file, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        writer.writerow([
            'entry_id', 'source', 'page_ref', 'chinese', 'pinyin', 'kimmun', 
            'vietnamese', 'meaning_en', 'category', 'notes', 'CORRECTED_PAGE'
        ])
        for row in rows:
            # Add empty column for corrections
            writer.writerow(list(row) + [''])
    
    print(f"✅ Exported {len(rows)} entries to {output_file}")
    print(f"\nFile bây giờ có thể:")
    print(f"  1. Mở bằng Excel")
    print(f"  2. Review cột 'page_ref'")
    print(f"  3. Viết lại page numbers chính xác vào cột 'CORRECTED_PAGE'")
    print(f"  4. Save file")
    print(f"  5. Upload lại qua Web UI để update DB")

if __name__ == "__main__":
    export_for_page_review()
