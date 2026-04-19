import json
import os
import sqlite3

# Bản dịch mẫu chất lượng cao cho cả Savina (Pháp) và Funing (Anh)
demo_translations = {
    # Từ Savina (Pháp)
    "Moi": "Tôi", "Toi": "Bạn / Anh / Chị", "Lui": "Hắn / Anh ta / Nó",
    "Avoir": "Có", "Pouvoir": "Có thể", "Froid": "Lạnh", "Chaud": "Nóng",
    "Tête": "Đầu", "Habit": "Áo / Quần áo", "Pantalon": "Quần",
    "Champ": "Ruộng / Nương", "Bon": "Tốt / Ngon", "Nez": "Mũi",
    "Œil": "Mắt", "Souffrir": "Đau khổ / Chịu đựng", "Voir": "Nhìn / Thấy",
    
    # Từ Funing (Anh)
    "sky": "Bầu trời",
    "thedaybreaks": "Rạng đông / Bình minh",
    "nightfalls": "Trời tối / Hoàng hôn",
    "horizon": "Chân trời",
    "sun": "Mặt trời",
    "thesun rises": "Mặt trời mọc",
    "thesunsets": "Mặt trời lặn",
    "tosun": "Phơi nắng",
    "toshine": "Chiếu sáng",
    "solareclipse": "Nhật thực",
    "moon": "Mặt trăng",
    "crescentmoon": "Trăng khuyết",
    "fullmoon": "Trăng tròn",
    "lunareclipse": "Nguyệt thực",
    "moonlight": "Ánh trăng",
    "star": "Ngôi sao",
    "comet": "Sao chổi",
    "meteor": "Sao băng",
    "rain": "Mưa",
    "it rams": "Trời mưa",
    "heavyrain": "Mưa to",
    "drizzle": "Mưa lâm thâm"
}

def translate_demo():
    json_path = "kim_mun_parsed.json"
    if not os.path.exists(json_path):
        print("Không tìm thấy file JSON dữ liệu.")
        return

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    translated_data = []
    for entry in data:
        # Làm sạch key tìm kiếm (lowercase cho tiếng Anh của Funing)
        original_word = entry["word"].strip()
        search_key = original_word.lower() if entry["pos"] == "Funing" else original_word
        
        found_translation = None
        # Thử khớp chính xác
        if original_word in demo_translations:
            found_translation = demo_translations[original_word]
        elif search_key in demo_translations:
            found_translation = demo_translations[search_key]
        else:
            # Thử khớp một phần (substring) cho các từ trong demo (như "nightfalls" trong "tian hei le nightfalls")
            for key in demo_translations:
                if key.lower() in search_key:
                    found_translation = demo_translations[key]
                    break

        if found_translation:
            new_entry = {
                "entry_id": entry.get("entry_id", ""),
                "chinese": entry.get("chinese", ""),
                "kimmun": entry["meaning"],
                "vietnamese": found_translation,
                "original": f"{original_word} ({entry['pos']})",
                "phonetic": entry["phonetic"],
                "pos": entry["pos"]
            }
            translated_data.append(new_entry)
            
    with open("kim_mun_translated_demo.json", "w", encoding="utf-8") as f:
        json.dump(translated_data, f, ensure_ascii=False, indent=4)
    
    print(f"Đã dịch thành công {len(translated_data)} từ kết hợp cả 2 nguồn tài liệu.")

if __name__ == "__main__":
    translate_demo()
