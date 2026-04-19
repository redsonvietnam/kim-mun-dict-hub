import json

FR_VN_CORE = {
    "Arbre": "Cây/Cây cối", "Racine": "Rễ", "Feuille": "Lá", "Ecorce": "Vỏ cây", "Branche": "Cành",
    "Poisson": "Cá", "Buffle": "Trâu", "Tigre": "Hổ", "Chat": "Mèo", "Chien": "Chó",
    "Maison": "Nhà", "Porte": "Cửa", "Ciel": "Bầu trời", "Terre": "Đất", "Eau": "Nước",
    "Feu": "Lửa", "Manger": "Ăn", "Boire": "Uống", "Mourir": "Chết", "Grand": "Lớn",
    "Petit": "Nhỏ", "Vieux": "Già/Cũ", "Neuf": "Mới", "Fils": "Con trai", "Fille": "Con gái",
    "Arroyo": "Con suối", "Côté": "Phía/Bên/Sườn", "pente": "Dốc", "Dire": "Nói", "vérité": "Sự thật",
}

def bulk_translate_savina():
    try:
        with open("savina_tri_lingual_raw.json", "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        print("Error: savina_tri_lingual_raw.json missing")
        return

    unique_french = sorted(list(set([i['french'] for i in data])))
    
    final_map = {}
    for fr in unique_french:
        if fr in FR_VN_CORE:
            final_map[fr] = FR_VN_CORE[fr]
        else:
            final_map[fr] = f"{fr}" # Fallback to original French if no Viet mapping yet
            
    # Apply map
    for item in data:
        fr = item['french']
        item['vietnamese'] = final_map.get(fr, fr)
        item['meaning_en'] = f"(Source 1926) {fr}"
        
    with open("savina_tri_lingual_final.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    
    print(f"Successfully processed {len(data)} entries.")

if __name__ == "__main__":
    bulk_translate_savina()
