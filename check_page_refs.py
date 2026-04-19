#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Check page_ref availability in JSON sources"""
import json
from pathlib import Path

files_to_check = [
    ("savina_robust_data.json", "Savina (1926)"),
    ("funing_final_master_cleaned.json", "Shintani (2008)"),
    ("clark_final_data.json", "Clark (2000)"),
]

for filename, source_name in files_to_check:
    if not Path(filename).exists():
        print(f"[SKIP] {filename} not found")
        continue
    
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    if not isinstance(data, list) or len(data) == 0:
        print(f"[ERROR] {filename} is empty")
        continue
    
    print(f"\n{'='*60}")
    print(f"SOURCE: {source_name}")
    print(f"Total entries: {len(data)}")
    print(f"Sample keys: {list(data[0].keys())}")
    
    # Check if page info exists
    has_page_info = any('page' in str(k).lower() for k in data[0].keys())
    print(f"Has page info: {'YES' if has_page_info else 'NO'}")
    
    if has_page_info:
        # Find page-related keys
        page_keys = [k for k in data[0].keys() if 'page' in str(k).lower()]
        print(f"Page-related keys: {page_keys}")
        
        # Show first 3 entries with page info
        print(f"\nFirst 3 entries with page info:")
        for i, entry in enumerate(data[:3]):
            print(f"  [{i}] id={entry.get('entry_id', '?')} page={entry.get('page', entry.get('page_ref', '?'))}")
    
    print(f"\nSample entry:")
    print(json.dumps(data[0], ensure_ascii=False, indent=2)[:400])
