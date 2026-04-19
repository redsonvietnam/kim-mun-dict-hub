#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Create page reference mapping for each source
Tạo ánh xạ entry_id → page number cho mỗi nguồn
"""
import json
from pathlib import Path

# Define source metadata
SOURCES = {
    "Savina (1926)": {
        "pdf": "D:/AGENT/KIMM_DOCS/befeo_0336-1519_1926_num_26_1_3091.pdf",
        "json": "savina_robust_data.json",
        "total_pages": 42,  # Estimated
        "entries_per_page": 50,  # Rough average
        "page_offset": 0
    },
    "Shintani (2008)": {
        "pdf": "D:/AGENT/KIMM_DOCS/The-Mun-Language-of-Funing-CountyIts-Classified-Lexicon富寧金門語.pdf",
        "json": "funing_final_master_cleaned.json",
        "total_pages": 250,  # Total pages in book
        "category_pages": {
            "01": 20,      # Nature starts page 20
            "02": 50,      # Animals
            "03": 70,      # Plants
            # ... akan tính từ category sections
        }
    },
    "Clark (2000)": {
        "pdf": None,  # Clark data từ paper nhỏ
        "json": "clark_final_data.json",
        "total_pages": 2,
        "entries_per_page": 100,
        "page_offset": 0
    }
}

def create_page_mapping():
    """Create mapping of entry_id to page references"""
    mapping = {}
    
    # 1. SAVINA - Simple sequential estimate
    with open(SOURCES["Savina (1926)"]["json"], 'r', encoding='utf-8') as f:
        savina_data = json.load(f)
    
    mapping["Savina (1926)"] = {}
    for i, entry in enumerate(savina_data):
        entry_id = entry['entry_id']
        # Estimate page: ~50 entries per page
        estimated_page = (i // 50) + 1
        mapping["Savina (1926)"][entry_id] = {
            "page": estimated_page,
            "pdf": SOURCES["Savina (1926)"]["pdf"],
            "note": "Estimated from sequential order"
        }
    
    # 2. SHINTANI - By category
    with open(SOURCES["Shintani (2008)"]["json"], 'r', encoding='utf-8') as f:
        shintani_data = json.load(f)
    
    # Define category page ranges (you can refine this)
    category_page_map = {
        "01": (20, 49),      # 01. Nature, Natural Phenomena
        "02": (50, 80),      # 02. Animals
        "03": (81, 110),     # 03. Plants
        "04": (111, 140),    # 04. Food and Drink
        "05": (141, 160),    # 05. Clothing
        "06": (161, 180),    # 06. Life, Sickness, Death
        "07": (181, 200),    # 07. Customs, Socializing
        "08": (201, 220),    # 08. Culture, Entertainment
        "09": (221, 240),    # 09. Furniture, Tools
        "10": (241, 260),    # 10. Commerce, Trade
        "11": (261, 280),    # 11. Activities
        "12": (281, 300),    # 12. Quantity, Numbers
        "13": (301, 330),    # 13. Dwelling
        "14": (331, 350),    # 14. Sensations
        "15": (351, 370),    # 15. State, Quality
        "16": (371, 390),    # 16. Occupation
        "17": (391, 410),    # 17. Relationships
        "18": (411, 430),    # 18. Communication, Transportation
        "19": (431, 450),    # 19. Character, Temperament, Behavior
        "20": (451, 470),    # 20. Mental Activities
        "21": (471, 490),    # 21. Adverbs
        "22": (491, 510),    # 22. Time
        "23": (511, 520),    # 23. Types of People
        "24": (521, 540),    # 24. Location, Movement
        "25": (541, 550),    # 25. Community
        "26": (551, 560),    # 26. Classifiers
        "27": (561, 570),    # 27. Connectives
        "28": (571, 580),    # 28. Aspects
        "29": (581, 590),    # 29. Particles
        "30": (591, 600),    # 30. Negation
        "31": (601, 610),    # 31. Copula, Existential
        "32": (611, 620),    # 32. Classifiers (continuation)
        "33": (621, 630),    # 33. Special topics
    }
    
    mapping["Shintani (2008)"] = {}
    for entry in shintani_data:
        entry_id = entry['entry_id']
        cat_code = str(entry_id)[:2]
        
        if cat_code in category_page_map:
            page_range = category_page_map[cat_code]
            # Estimate within category (rough)
            seq_num = int(str(entry_id)[2:]) if len(entry_id) > 2 else 1
            page = page_range[0] + (seq_num % (page_range[1] - page_range[0]))
        else:
            page = 630  # Default end
        
        mapping["Shintani (2008)"][entry_id] = {
            "page": page,
            "pdf": SOURCES["Shintani (2008)"]["pdf"],
            "category": entry.get('category', ''),
            "note": "Estimated from category ranges"
        }
    
    # 3. CLARK - Sequential
    with open(SOURCES["Clark (2000)"]["json"], 'r', encoding='utf-8') as f:
        clark_data = json.load(f)
    
    mapping["Clark (2000)"] = {}
    for i, entry in enumerate(clark_data):
        entry_id = entry['entry_id']
        # Clark is short, roughly 2 pages
        page = 1 if i < 100 else 2
        mapping["Clark (2000)"][entry_id] = {
            "page": page,
            "pdf": SOURCES["Clark (2000)"]["pdf"],
            "note": "Clark (2000) - small paper"
        }
    
    # Save mapping to JSON
    output_file = "page_reference_mapping.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(mapping, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Page reference mapping created: {output_file}")
    print(f"\nSummary:")
    for source, entries in mapping.items():
        print(f"  {source}: {len(entries)} entries mapped")
    
    return mapping

if __name__ == "__main__":
    create_page_mapping()
