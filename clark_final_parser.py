import re
import json
import os
import sqlite3

def decode_mirror(s):
    """Đảo ngược chuỗi (ví dụ: 'yvaeh' -> 'heavy')."""
    if not s: return ""
    return s[::-1].strip()

# Bản dịch mẫu cho các concept phổ biến trong Swadesh/Comparative list của Clark
clark_translations = {
    "ant": "Con kiến", "sky": "Bầu trời", "bat": "Con dơi", "sun": "Mặt trời",
    "bee": "Con ong", "the sun rises": "Mặt trời mọc", "bird": "Con chim",
    "the sun sets": "Mặt trời lặn", "buffalo": "Con trâu", "cat": "Con mèo",
    "caterpillar": "Sâu bướm", "star": "Ngôi sao", "centipede": "Con rết",
    "light": "Ánh sáng", "cock": "Con gà trống", "shadow": "Bóng tối / Bóng râm",
    "hen": "Con gà mái", "twinkle": "Lấp lánh", "chicken": "Con gà",
    "bright": "Sáng sủa", "ox/cow": "Con bò / Bò đực", "dark": "Tối tăm",
    "crab": "Con cua", "cloud": "Đám mây", "cricket": "Con dế",
    "rain": "Mưa", "crow": "Con quạ", "rainbow": "Cầu vồng",
    "barking deer": "Con mang (hoẵng)", "lightning": "Tia chớp",
    "sambar deer": "Nai", "thunder": "Sấm sét", "dog": "Con chó",
    "wind": "Gió", "dragon": "Con rồng", "storm": "Bão",
    "dragonfly": "Chuồn chuồn", "snow": "Tuyết", "duck": "Con vịt",
    "melt": "Tan chảy", "hail": "Mưa đá", "eagle": "Đại bàng",
    "weather": "Thời tiết", "fish": "Con cá", "fine day": "Ngày đẹp trời",
    "flea": "Con bọ chét", "cloudy day": "Ngày nhiều mây", "fly": "Con ruồi",
    "drought": "Hạn hán", "frog": "Con ếch", "night": "Ban đêm",
    "goat": "Con dê", "day": "Ban ngày", "grasshopper": "Châu chấu",
    "morning": "Buổi sáng", "horse": "Con ngựa", "noon": "Buổi trưa",
    "insect": "Côn trùng", "yesterday": "Hôm qua", "leech": "Con đỉa",
    "tomorrow": "Ngày mai", "year": "Năm", "lizard": "Con thằn lằn",
    "east": "Hướng Đông", "head louse": "Con chí (chấy)", "west": "Hướng Tây",
    "monkey": "Con khỉ", "north": "Hướng Bắc", "mosquito": "Con muỗi",
    "south": "Hướng Nam", "pig": "Con lợn", "horizon": "Chân trời",
    "boar": "Lợn rừng", "water": "Nước", "piglet": "Lợn con",
    "snail": "Con ốc", "river": "Con sông", "sow": "Lợn nái",
    "rat": "Con chuột", "shrimp": "Con tôm", "stream": "Suối",
    "snake": "Con rắn", "sea": "Biển", "spider": "Con nhện",
    "earth": "Đất / Trái đất", "tiger": "Con hổ", "mud": "Bùn",
    "turtle": "Con rùa", "dust": "Bụi", "wasp": "Ong vò vẽ",
    "stone": "Đá", "weasel": "Con chồn", "pebble": "Đá cuội",
    "earthworm": "Giun đất", "sand": "Cát", "goose": "Con ngỗng",
    "gold": "Vàng", "silver": "Bạc", "arm": "Cánh tay", "iron": "Sắt",
    "back": "Lưng", "steel": "Thép", "beard": "Râu", "mountain": "Núi",
    "belly": "Bụng", "cave": "Hang động", "blood": "Máu", "earthquake": "Động đất",
    "body": "Cơ thể", "swamp": "Đầm lầy", "bone": "Xương", "cliff": "Vách đá",
    "brain": "Não", "valley": "Thung lũng", "butt": "Mông", "hole": "Hố / Lỗ",
    "chest": "Ngực", "ice": "Băng", "cockcomb": "Mào gà", "flow": "Chảy",
    "corpse": "Xác chết", "flood": "Lũ lụt", "ears": "Tai", "egg": "Quả trứng",
    "sink": "Chìm", "eye": "Mắt", "waterfall": "Thác nước", "eyebrows": "Lông mày",
    "island": "Hòn đảo", "face": "Khuôn mặt", "lake": "Hồ", "excrement": "Phân",
    "finger": "Ngón tay", "forest": "Rừng", "fiber": "Sợi", "leaf": "Lá",
    "flower": "Hoa", "foot": "Bàn chân", "fruit": "Quả / Trái", "heart": "Trái tim",
    "seed": "Hạt", "hoof": "Móng guốc", "horn": "Sừng", "intestine": "Ruột",
    "bamboo": "Tre", "leg": "Chân", "liver": "Gan", "lungs": "Phổi",
    "mouth": "Miệng", "mucus": "Dịch nhầy", "neck": "Cổ", "nest": "Tổ",
    "head": "Đầu"
}

def parse_clark_final():
    draft_path = r"D:\AGENT\dict_builder\A phonological analysis and comparison of two Kim Mun varieties in Laos and Vietnam.pdf_draft.txt"
    if not os.path.exists(draft_path):
        return

    with open(draft_path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f.readlines()]

    # Tìm vị trí bắt đầu Appendix A
    start_idx = 0
    for i, line in enumerate(lines):
        if "APPENDIX A" in line:
            start_idx = i
            break
    
    # Duyệt từ Appendix A trở đi, tìm các cụm 3 dòng (Phonetic, English, Index)
    raw_entries = []
    i = start_idx
    while i < len(lines):
        line = lines[i]
        # Nhận diện dòng Index (vd: .100, .a310)
        if re.match(r'^\.([a-z0-9]+)$', line) and i >= 2:
            index_val = line[1:][::-1] # .100 -> 001
            english_rev = lines[i-1]
            phonetic_rev = lines[i-2]
            
            raw_entries.append({
                "index": index_val,
                "english": decode_mirror(english_rev),
                "phonetic": decode_mirror(phonetic_rev)
            })
        i += 1

    # Phân tách 2 danh sách dựa trên quy luật xen kẽ (Interleaved)
    # Tùy vào page header, nhưng thường là Lào trướcc, Việt Nam sau hoặc ngược lại.
    # Thử ghép theo cặp index.
    final_data = []
    i = 0
    while i < len(raw_entries):
        curr = raw_entries[i]
        # Kiểm tra xem dòng tiếp có cùng index không (nghĩa là biến thể so sánh)
        if i + 1 < len(raw_entries) and raw_entries[i+1]["index"] == curr["index"]:
            v1 = curr
            v2 = raw_entries[i+1]
            i += 2
        else:
            v1 = curr
            v2 = None
            i += 1
            
        # Dịch nghĩa
        en = v1["english"].lower()
        viet = clark_translations.get(en, "")
        
        if v2:
            # Ghi nhận cả 2 biến thể
            final_data.append({
                "entry_id": f"CL-{v1['index']}",
                "chinese": "",
                "kimmun": f"{v1['phonetic']} (Laos) | {v2['phonetic']} (Vietnam)",
                "vietnamese": viet,
                "original": f"{v1['english']} (Clark 2008)",
                "phonetic": f"Lao: {v1['phonetic']}, VN: {v2['phonetic']}",
                "pos": "Clark 2008"
            })
        else:
            final_data.append({
                "entry_id": f"CL-{v1['index']}",
                "chinese": "",
                "kimmun": v1['phonetic'],
                "vietnamese": viet,
                "original": f"{v1['english']} (Clark 2008)",
                "phonetic": v1['phonetic'],
                "pos": "Clark 2008"
            })

    # Chỉ lấy những từ có dịch nghĩa (để demo chất lượng)
    final_filtered = [item for item in final_data if item["vietnamese"]]
    
    with open("clark_final_data.json", "w", encoding="utf-8") as f:
        json.dump(final_filtered, f, ensure_ascii=False, indent=4)
        
    print(f"Parsed {len(final_data)} entries, translated {len(final_filtered)} high-quality entries.")

    # Cập nhật vào DB v2
    conn = sqlite3.connect("kim_mun_dict_v2.db")
    cursor = conn.cursor()
    
    for item in final_filtered:
        cursor.execute('''
            INSERT INTO dictionary (entry_id, chinese, kimmun, vietnamese, original, phonetic, pos)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            item.get("entry_id", ""), 
            item.get("chinese", ""), 
            item["kimmun"], 
            item["vietnamese"], 
            item["original"], 
            item["phonetic"], 
            item["pos"]
        ))
    
    conn.commit()
    conn.close()
    print("Database updated with Clark 2008 data.")

if __name__ == "__main__":
    parse_clark_final()
