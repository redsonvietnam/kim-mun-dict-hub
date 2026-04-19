import re
import json
import os

def decode_reversed(s):
    """Đảo ngược chuỗi và xử lý các ký tự đặc biệt."""
    if not s: return ""
    # Đảo ngược chuỗi
    rev = s[::-1].strip()
    return rev

def clean_repeated(s):
    """Xử lý các ký tự lặp 4 lần (mã hóa lạ của PDF)."""
    # Ví dụ: mmmmaaaa -> ma
    result = ""
    i = 0
    while i < len(s):
        char = s[i]
        count = 1
        while i + 1 < len(s) and s[i+1] == char:
            count += 1
            i += 1
        # Nếu lặp 4 lần (hoặc bội số), lấy 1
        if count >= 3:
            result += char
        else:
            result += char * count
        i += 1
    return result

def parse_clark():
    input_file = r"D:\AGENT\dict_builder\A phonological analysis and comparison of two Kim Mun varieties in Laos and Vietnam.pdf_draft.txt"
    if not os.path.exists(input_file):
        print("Không tìm thấy file draft.")
        return

    with open(input_file, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f.readlines()]

    entries = []
    
    # Logic: Tìm các dòng có định dạng Index (.100, .200, .a300, .140...)
    # Sau đó lấy 1-2 dòng phía trên làm English và Phonetic.
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # Nhận diện dòng Index (vd: .100)
        index_match = re.match(r'^\.([a-z0-9]+)$', line)
        if index_match:
            index_rev = index_match.group(1)
            index_proper = index_rev[::-1] # .100 -> 001
            
            # Lấy English (dòng ngay trên)
            english_raw = lines[i-1] if i > 0 else ""
            # Lấy Phonetic (dòng trên nữa)
            phonetic_raw = lines[i-2] if i > 1 else ""
            
            # Đôi khi English chiếm 2 dòng (vd: the sun rises)
            if i > 2 and not re.match(r'^\.|^#|^---', lines[i-2]) and len(lines[i-2]) < 20 and not any(c.isdigit() for c in lines[i-2]):
                # Thử kiểm tra xem có phải English đa dòng không
                # Nhưng tạm thời cứ lấy logic đơn giản trước
                pass

            english = decode_reversed(english_raw)
            phonetic = decode_reversed(phonetic_raw)
            
            # Lọc bỏ các dòng rác
            if len(english) > 1 and len(phonetic) > 1:
                entries.append({
                    "id": index_proper,
                    "english": english,
                    "phonetic": phonetic,
                    "source_raw": line
                })
        i += 1

    # Gom nhóm theo ID vì mỗi ID sẽ có 2 biến thể (Lào và Việt Nam)
    grouped = {}
    for e in entries:
        eid = e["id"]
        if eid not in grouped:
            grouped[eid] = []
        grouped[eid].append(e)

    # Xuất kết quả
    output_data = []
    for eid, variants in grouped.items():
        # Thường thì variant đầu tiên là Lào, thứ hai là Việt Nam (hoặc ngược lại)
        # Dựa trên draft: Vietnam liệt kê trước, Lào sau? 
        # Cần kiểm tra kỹ header.
        if len(variants) >= 2:
            output_data.append({
                "id": eid,
                "english": variants[0]["english"],
                "kimmun_v1": variants[0]["phonetic"], # Vietnam?
                "kimmun_v2": variants[1]["phonetic"], # Laos?
                "source": "Clark 2008"
            })
        else:
            output_data.append({
                "id": eid,
                "english": variants[0]["english"],
                "kimmun_v1": variants[0]["phonetic"],
                "source": "Clark 2008"
            })

    with open("clark_decoded.json", "w", encoding="utf-8") as f:
        json.dump(output_data, f, ensure_ascii=False, indent=4)
    
    # Sử dụng ascii-safe print cho log
    print(f"Decoded {len(output_data)} entries from Clark 2008.")

if __name__ == "__main__":
    parse_clark()
