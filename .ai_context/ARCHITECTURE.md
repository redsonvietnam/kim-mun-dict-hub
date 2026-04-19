# Cấu trúc Database
- DB: kim_mun_dict_v2.db (SQLite)
- Table: dictionary (id, entry_id, chinese, kimmun, pinyin, vietnamese, meaning_en, meaning_fr, category, subcategory, source, page_ref, notes)

# Backend
- Flask app tại web_ui/app.py

# Workflow Core Scripts
- unified_ingestor.py: Push json files to DB
- clean_funing_categories.py: Clean OCR garbage using Golden Mapping
- ision_extractor.py: OCR pages using API