#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Display sample entries with page references
Hiển thị sample entries với page references
"""
import sqlite3

DB_PATH = "kim_mun_dict_v2.db"

def show_samples():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    print("\n" + "="*80)
    print("📚 SAMPLE ENTRIES WITH PAGE REFERENCES")
    print("="*80)
    
    # Show Savina samples
    print("\n🔸 SAVINA (1926) - Samples:")
    c.execute("""
        SELECT entry_id, page_ref, vietnamese, kimmun
        FROM dictionary
        WHERE source = 'Savina (1926)'
        LIMIT 5
    """)
    for row in c.fetchall():
        print(f"  {row[0]:10} {row[1]:8}  {row[2]:20}  {row[3][:30]}")
    
    # Show Shintani samples
    print("\n🔹 SHINTANI (2008) - Samples:")
    c.execute("""
        SELECT entry_id, page_ref, vietnamese, category
        FROM dictionary
        WHERE source = 'Shintani (2008)'
        LIMIT 5
    """)
    for row in c.fetchall():
        print(f"  {row[0]:10} {row[1]:8}  {row[2]:20}  {row[3][:30]}")
    
    # Show Clark samples
    print("\n🔺 CLARK (2000) - Samples:")
    c.execute("""
        SELECT entry_id, page_ref, vietnamese, meaning_en
        FROM dictionary
        WHERE source = 'Clark (2000)'
        LIMIT 5
    """)
    for row in c.fetchall():
        print(f"  {row[0]:10} {row[1]:8}  {row[2]:20}  {row[3][:30]}")
    
    conn.close()
    
    print("\n" + "="*80)
    print("✅ All entries now display with page references in:")
    print("   • Web UI Card View: 📖 p.XX displayed in header")
    print("   • Web UI Table View: Dedicated 'Trang' column")
    print("   • Edit Modal: Can update page_ref directly")
    print("   • CSV Export: page_ref included for offline review")
    print("="*80 + "\n")

if __name__ == "__main__":
    show_samples()
