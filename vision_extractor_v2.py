#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Vision Extraction for Kim Mun Dictionary
Phonology (pages 13-20) and Topic 1 (pages 21-34)
"""
import os
import sys
import json
import time

# Force UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

try:
    import google.generativeai as genai
    from PIL import Image
except ImportError:
    print("ERROR: Install google-generativeai and pillow")
    exit(1)

API_KEY = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY") 

if not API_KEY:
    print("ERROR: No GEMINI_API_KEY found in environment")
    API_KEY = input("Enter Gemini API Key: ").strip()

genai.configure(api_key=API_KEY)

# Try to select best available model
model = None
models_to_try = ['gemini-2.0-flash', 'gemini-1.5-pro', 'gemini-pro-vision']

for model_name in models_to_try:
    try:
        model = genai.GenerativeModel(model_name)
        print(f"[OK] Using model: {model_name}")
        break
    except Exception as e:
        print(f"[SKIP] {model_name}: {str(e)[:50]}")

if not model:
    print("[ERROR] No suitable model found")
    exit(1)

def extract_phonology():
    print("\n[PHONOLOGY] Extracting pages 13-20...")
    phonology_markdown = "# Kim Mun Phonology (Shintani 2008)\n\n"
    
    try:
        import fitz
    except:
        print("[ERROR] Install PyMuPDF: pip install pymupdf")
        return
    
    pdf_path = 'D:/AGENT/KIMM_DOCS/The-Mun-Language-of-Funing-CountyIts-Classified-Lexicon富寧金門語.pdf'
    
    if not os.path.exists(pdf_path):
        print(f"[ERROR] PDF not found: {pdf_path}")
        return
    
    doc = fitz.open(pdf_path)
    print(f"[OK] Opened PDF with {len(doc)} pages")
    
    for i in range(12, 20):  # PDF indices 12-19 = pages 13-20
        img_filename = f"phonology_p{i}.png"
        
        if not os.path.exists(img_filename):
            print(f"[RENDER] Creating {img_filename}...")
            try:
                doc[i].get_pixmap(dpi=150).save(img_filename)
            except Exception as e:
                print(f"[ERROR] Failed to render page {i}: {e}")
                continue
        
        print(f"[VISION] Processing {img_filename}...")
        try:
            img = Image.open(img_filename)
            
            prompt = """Extract all text from this phonology page accurately. 
Preserve linguistic symbols, IPA phonetics, and tables if any. 
Format the output elegantly in Markdown. 
Output ONLY the markdown text without any conversational filler."""
            
            response = model.generate_content([prompt, img])
            phonology_markdown += f"## Page {i-11}\n\n{response.text}\n\n"
            print(f"[OK] Extracted page {i-11}")
            time.sleep(2)
            
        except Exception as e:
            print(f"[ERROR] Vision API failed for {img_filename}: {e}")
            time.sleep(3)
    
    output_file = "kim_mun_phonology.md"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(phonology_markdown)
    print(f"\n[DONE] Phonology extraction saved to {output_file}")

def extract_topic_1():
    print("\n[TOPIC1] Extracting vocabulary pages 21-34...")
    topic_words = []
    
    for i in range(20, 34):  # PDF indices 20-33 = pages 21-34
        img_filename = f"topic1_p{i}.png"
        
        if not os.path.exists(img_filename):
            print(f"[SKIP] {img_filename} not found")
            continue
        
        print(f"[VISION] Processing {img_filename}...")
        try:
            img = Image.open(img_filename)
            
            prompt = """You are an expert OCR and linguist for Kim Mun Dao language.
Extract all vocabulary entries from this dictionary page into a JSON array.
Each object MUST have: id, hanzi, pinyin, kimmun, vietnamese, english, subcategory
Output ONLY valid JSON (no markdown, no explanation).
If extraction fails, output an empty array: []"""
            
            response = model.generate_content([prompt, img])
            json_text = response.text.strip()
            
            # Clean JSON if wrapped in markdown
            if json_text.startswith("```"):
                json_text = json_text.split('\n', 1)[1].rsplit('\n', 1)[0]
            
            page_data = json.loads(json_text)
            topic_words.extend(page_data)
            print(f"[OK] Extracted {len(page_data)} entries from page {i+1}")
            time.sleep(3)
            
        except json.JSONDecodeError as e:
            print(f"[ERROR] JSON parse failed for {img_filename}: {e}")
        except Exception as e:
            print(f"[ERROR] Vision API failed for {img_filename}: {e}")
            time.sleep(3)
    
    output_file = "funing_topic1_vision.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(topic_words, f, ensure_ascii=False, indent=2)
    print(f"\n[DONE] Topic 1 extraction saved to {output_file}")
    print(f"[STATS] Total entries: {len(topic_words)}")

if __name__ == "__main__":
    extract_phonology()
    extract_topic_1()
    print("\n[COMPLETE] Vision extraction finished!")
