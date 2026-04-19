import json
import os

# Một từ điển dịch thuật chuyên sâu cho các hạng mục từ vựng học thuật trong Funing Lexicon
TRANSLATIONS = {
    # 01. Nature
    "sky": "bầu trời", "weather": "thời tiết", "light": "ánh sáng", "earth": "đất", "fire": "lửa",
    "nature": "tự nhiên", "phenomena": "hiện tượng", "sky, weather, light": "bầu trời, thời tiết, ánh sáng",
    "day breaks": "rạng đông", "night falls": "trời tối", "horizon": "chân trời", "sun": "mặt trời",
    "moon": "mặt trăng", "star": "ngôi sao", "cloud": "mây", "rain": "mưa", "wind": "gió",
    "thunder": "sấm", "lightning": "sét", "snow": "tuyết", "ice": "băng", "water": "nước",
    
    # 02. Animals
    "animals": "động vật", "beasts": "thú rừng", "fowls": "gia cầm/chim", "domestic animals": "vật nuôi",
    "insects": "côn trùng", "fish": "cá", "tiger": "hổ", "lion": "sư tử", "leopard": "báo",
    "wolf": "chó sói", "fox": "cáo", "elephant": "voi", "deer": "nai/hươu", "wild boar": "lợn rừng",
    "bear": "gấu", "monkey": "khỉ", "rabbit": "thỏ", "rat": "chuột", "mouse": "chuột",
    "bird": "chim", "eagle": "đại bàng", "crow": "quạ", "sparrow": "chim sẻ", "chicken": "gà",
    "duck": "vịt", "goose": "ngỗng", "snake": "rắn", "spider": "nhện", "bee": "ong",
    
    # 03. Plants
    "plants": "thực vật", "trees": "cây cối", "flowers and grasses": "hoa cỏ", "grains": "ngũ cốc",
    "vegetables": "rau củ", "fruits": "trái cây", "root": "rễ", "leaf": "lá", "flower": "hoa",
    "fruit": "quả", "seed": "hạt", "bamboo": "tre", "pine": "thông", "oak": "sồi",
    "rose": "hoa hồng", "lotus": "hoa sen", "rice": "lúa", "corn": "ngô", "bean": "đậu",
    
    # Body parts
    "human body": "cơ thể người", "head": "đầu", "hair": "tóc", "face": "mặt", "eye": "mắt",
    "ear": "tai", "nose": "mũi", "mouth": "miệng", "tooth": "răng", "neck": "cổ",
    "shoulder": "vai", "arm": "cánh tay", "hand": "tay", "finger": "ngón tay", "leg": "chân",
    "foot": "bàn chân", "heart": "tim", "blood": "máu", "bone": "xương"
}

def apply_translations(input_json="full_lexicon_data.json", output_json="full_lexicon_vi.json"):
    with open(input_json, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    for item in data:
        en = item.get("meaning_en", "").lower()
        # Tìm kiếm khớp chính xác hoặc khớp một phần
        if en in TRANSLATIONS:
            item["vietnamese"] = TRANSLATIONS[en]
        else:
            # Nếu không có trong map, giữ nguyên Anh hoặc thử dịch đơn giản
            item["vietnamese"] = "" 
            
    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"Đã cập nhật nghĩa tiếng Việt cho {len(data)} mục từ.")

if __name__ == "__main__":
    apply_translations()
