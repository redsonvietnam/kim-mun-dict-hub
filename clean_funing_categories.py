import json
import os
import re

GOLDEN_MAPPING = {
    "Nature, Natural Phenomena": {"vi": "Tự nhiên, Hiện tượng", "group": "01"},
    "Sky, weather, light": {"vi": "Bầu trời, Thời tiết", "group": "011"},
    "Earth, fire": {"vi": "Đất, Lửa", "group": "012"},
    "Man and nature": {"vi": "Con người và Tự nhiên", "group": "013"},
    "Animals": {"vi": "Động vật", "group": "02"},
    "Beasts": {"vi": "Thú", "group": "021"},
    "Fowls": {"vi": "Gia cầm, Chim", "group": "022"},
    "Domestic animals": {"vi": "Vật nuôi", "group": "023"},
    "Insects": {"vi": "Côn trùng", "group": "024"},
    "Fish": {"vi": "Cá", "group": "025"},
    "Man and animals": {"vi": "Người và Động vật", "group": "026"},
    "Plants": {"vi": "Thực vật", "group": "03"},
    "Food and Drink": {"vi": "Ẩm thực", "group": "04"},
    "Clothing": {"vi": "Trang phục", "group": "05"},
    "Dwelling": {"vi": "Nhà cửa", "group": "06"},
    "Furniture, Tools": {"vi": "Đồ đạc, Công cụ", "group": "07"},
    "Community": {"vi": "Cộng đồng", "group": "08"},
    "Commerce, Trade": {"vi": "Thương mại", "group": "09"},
    "Communication, Transportation": {"vi": "Giao thông", "group": "10"},
    "Culture, Entertainment": {"vi": "Văn hóa, Giải trí", "group": "11"},
    "Cults, Customs, Socializing": {"vi": "Phong tục, Giao tế", "group": "12"},
    "Human Body": {"vi": "Cơ thể người", "group": "13"},
    "Life, Sickness, and Death": {"vi": "Sinh, Bệnh, Tử", "group": "14"},
    "Human Relationships": {"vi": "Các mối quan hệ", "group": "15"},
    "Types of People": {"vi": "Các kiểu người", "group": "16"},
    "Occupation": {"vi": "Nghề nghiệp", "group": "17"},
    "Activities": {"vi": "Hoạt động", "group": "18"},
    "Mental Activities": {"vi": "Hoạt động tinh thần", "group": "19"},
    "Sensations": {"vi": "Cảm giác", "group": "20"},
    "State, Quality": {"vi": "Trạng thái, Tình trạng", "group": "21"},
    "Character, Temperament, Manner, Behavior": {"vi": "Tính cách, Hành vi", "group": "22"},
    "Time": {"vi": "Thời gian", "group": "23"},
    "Location, Movement": {"vi": "Vị trí, Di chuyển", "group": "24"},
    "Copula, Existential": {"vi": "Hệ từ, Tồn tại", "group": "25"},
    "Quantity, Numbers": {"vi": "Số lượng", "group": "26"},
    "Pro-words, Indefinite Words": {"vi": "Đại từ", "group": "27"},
    "Adverbs": {"vi": "Phó từ", "group": "28"},
    "Aspects": {"vi": "Thể (Ngữ pháp)", "group": "29"},
    "Negation": {"vi": "Phủ định", "group": "30"},
    "Particles": {"vi": "Trợ từ", "group": "31"},
    "Connectives": {"vi": "Liên từ", "group": "32"},
    "Classifiers": {"vi": "Lượng từ", "group": "33"}
}

def clean_category_string(raw_cat):
    if not raw_cat:
        return "Tất cả mục từ"
    
    # Check simple substring match since raw_cat usually has English keywords safely
    for eng_key, val in GOLDEN_MAPPING.items():
        # Match only if the exact english keyword is in the noise string
        # Taking care to ignore case for robustness, though title case is standard
        if eng_key.lower() in raw_cat.lower() or raw_cat.lower() in eng_key.lower():
            # Trả về cả tiếng Việt và mã nhóm
            return f"{val['group']}. {val['vi']}"
            
    # Some special hardcoded fixes based on fuzzy OCR errors
    if "aft human body" in raw_cat.lower():
        return "13. Cơ thể người"
    if "ann types of people" in raw_cat.lower():
        return "16. Các kiểu người"
        
    return "Khác"

def main():
    with open("funing_final_master.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        
    for item in data:
        raw_cat = item.get("category", "")
        clean_cat = clean_category_string(raw_cat)
        item["category"] = clean_cat

    with open("funing_final_master_cleaned.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        
    print(f"Cleaned {len(data)} Funing entries to 'funing_final_master_cleaned.json'.")

if __name__ == "__main__":
    main()
