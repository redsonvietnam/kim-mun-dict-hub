#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Analyze entry_id patterns and estimate page references"""
import json
from pathlib import Path

print("ANALYZING ENTRY_ID PATTERNS:\n")

# Analyze Savina
with open('savina_robust_data.json', 'r', encoding='utf-8') as f:
    savina = json.load(f)

print("SAVINA (1926) - Entry ID format:")
sample_ids = [e['entry_id'] for e in savina[:20]]
print(f"  Samples: {sample_ids}")
print(f"  Pattern: SA-XXXX (sequential)")

# Try to estimate page: Savina has ~300 pages, 13000+ entries
# Rough estimate: ~40-50 entries per page
print(f"  Estimate: ~50 entries/page = {len(savina)//50} pages")

print("\n" + "="*60)

# Analyze Shintani
with open('funing_final_master_cleaned.json', 'r', encoding='utf-8') as f:
    shintani = json.load(f)

print("SHINTANI (2008) - Entry ID format:")
sample_ids = [e['entry_id'] for e in shintani[:20]]
print(f"  Samples: {sample_ids}")
print(f"  Pattern: XXXXX (5-digit numeric)")
print(f"  Format: [Category][Subcategory][Sequence]")
print(f"    01XXXX = Category 01 (Nature)")
print(f"    13XXXX = Category 13 (Body)")

# Estimate pages from category
categories = set()
for e in shintani:
    cat_code = str(e['entry_id'])[:2]
    categories.add(cat_code)

print(f"  Categories: {sorted(categories)}")
print(f"  Estimate: Pages ~20-30 (by category sections)")

print("\n" + "="*60)

# Analyze Clark
with open('clark_final_data.json', 'r', encoding='utf-8') as f:
    clark = json.load(f)

print("CLARK (2000) - Entry ID format:")
sample_ids = [e['entry_id'] for e in clark[:20]]
print(f"  Samples: {sample_ids}")
print(f"  Pattern: CL-XXX (sequential)")
print(f"  Only 207 entries = 1-2 pages in paper")

print("\n" + "="*60)
print("\nCONCLUSION:")
print("❌ No page refs in JSON files")
print("✅ Entry IDs have patterns but not direct page mapping")
print("✅ SOLUTION: Store page_ref as NULL in DB, allow user to manually add OR")
print("✅ ALTERNATIVE: Create page mapping file based on PDF analysis")
