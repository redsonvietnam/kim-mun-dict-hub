import json
import re

# Từ điển ánh xạ từ vựng học thuật Kim Mun (Anh -> Việt linh hoạt Hán-Việt)
VOCAB_MAP = {
    # 01. Nature
    "sky": "bầu trời", "sun": "mặt trời/thái dương", "moon": "mặt trăng/thái âm", "star": "nhôi sao/tinh tú",
    "cloud": "mây", "rain": "mưa", "wind": "gió", "fire": "lửa/hỏa", "water": "nước/thủy",
    "mountain": "núi/sơn", "river": "sông/hà", "sea": "biển/hải", "earth": "đất/thổ", "dust": "bụi",
    "lightning": "sét", "thunder": "sấm", "snow": "tuyết", "ice": "băng", "rainbow": "cầu vồng",
    
    # 02. Animals
    "animal": "động vật", "beast": "thú rừng", "tiger": "hổ/cọp", "lion": "sư tử", "leopard": "báo",
    "wolf": "chó sói", "fox": "cáo/hồ ly", "elephant": "voi", "deer": "hươu/nai", "pig": "lợn/heo",
    "boar": "lợn rừng", "bear": "gấu", "monkey": "khỉ", "rabbit": "thỏ", "rat": "chuột",
    "bird": "chim/cầm", "eagle": "đại bàng", "crow": "quạ", "chicken": "gà", "duck": "vịt",
    "snake": "rắn/xà", "dragon": "rồng/long", "fish": "cá/ngư", "shrimp": "tôm", "crab": "cua",
    
    # 03. Plants
    "plant": "thực vật", "tree": "cây/mộc", "flower": "hoa", "grass": "cỏ/thảo", "leaf": "lá/diệp",
    "root": "rễ/căn", "seed": "hạt/chủng", "bamboo": "tre/trúc", "pine": "thông", "fruit": "trái cây/quả",
    "rice": "lúa/gạo", "corn": "ngô/bắp", "vegetable": "rau/thái", "medicine": "thuốc/dược",
    
    # 13. Human Body
    "human": "người/nhân", "body": "cơ thể/thân", "head": "đầu", "face": "mặt/diện", "eye": "mắt/mục",
    "ear": "tai/nhĩ", "nose": "mũi/tị", "mouth": "miệng/khẩu", "tooth": "răng/nha", "hair": "tóc",
    "neck": "cổ/hạng", "shoulder": "vai", "hand": "tay/thủ", "finger": "ngón tay", "arm": "cánh tay",
    "heart": "tim/tâm", "blood": "máu/huyết", "bone": "xương/cốt", "skin": "da", "meat": "thịt/nhục",
    
    # 15. Relationships
    "father": "cha/phụ", "mother": "mẹ/mẫu", "son": "con trai", "daughter": "con gái",
    "brother": "anh em", "sister": "chị em", "friend": "bạn bè/bằng hữu", "husband": "chồng/phu",
    "wife": "vợ/thê", "child": "trẻ con/nhi đồng", "people": "người/dân",
    
    # 05. Clothing
    "clothing": "trang phục", "garment": "quần áo", "fabric": "vải", "cotton": "bông/miên",
    "silk": "lụa/tơ", "needle": "kim", "thread": "chỉ", "button": "khuy/cúc", "shoe": "giày",
    "hat": "mũ/nón", "skirt": "váy", "trousers": "quần", "shirt": "áo",
    
    # 06. Dwelling
    "house": "nhà", "dwelling": "nơi ở/trú sở", "wall": "tường", "roof": "mái nhà",
    "door": "cửa", "window": "cửa sổ", "floor": "sàn nhà", "room": "phòng", "kitchen": "bếp",
    
    # 07. Furniture, Tools
    "furniture": "đồ gia dụng", "tool": "công cụ", "table": "bàn", "chair": "ghế",
    "bed": "giường", "lamp": "đèn", "bowl": "bát/chén", "chopsticks": "đũa",
    "knife": "dao", "axe": "rìu", "hammer": "búa", "saw": "cưa",
    
    # Colors
    "red": "đỏ/xích", "white": "trắng/bạch", "black": "đen/huyền", "blue": "xanh", "yellow": "vàng/hoàng",
    "green": "xanh lá"
}

def clean_english(text):
    # Loại bỏ phần phonetic /.../
    text = re.split(r'[/\\(\[]', text)[0]
    # Loại bỏ các từ pinyin nếu nó trùng với pinyin field (nếu có thể)
    # Ở đây đơn giản là xóa các từ không phải tiếng Anh nếu chúng đứng đầu
    text = text.strip().lower()
    return text

def translate_entry(item):
    en_raw = item.get("meaning_en", "")
    en_clean = clean_english(en_raw)
    
    # Chiến thuật: Tìm bất kỳ từ khóa nào trong VOCAB_MAP xuất hiện trong en_clean
    # Ưu tiên các từ dài hơn để tránh match nhầm
    sorted_keys = sorted(VOCAB_MAP.keys(), key=len, reverse=True)
    
    for key in sorted_keys:
        # Kiểm tra xem từ khóa có tồn tại như một từ độc lập trong chuỗi không
        if re.search(r'\b' + re.escape(key) + r'\b', en_clean):
            return VOCAB_MAP[key]
            
    # Fallback: Trả về chuỗi gốc đã làm sạch thay vì thêm [VN]
    return en_clean.capitalize()

def run_translation():
    with open("full_lexicon_data.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        
    count = 0
    for item in data:
        vi = translate_entry(item)
        item["vietnamese"] = vi
        if vi and not vi.startswith(item.get("meaning_en", "").lower()[:2]):
            count += 1
            
    with open("full_lexicon_translated.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
        
    print(f"Processed {len(data)} entries. Found quality translations for {count} items.")

if __name__ == "__main__":
    run_translation()
