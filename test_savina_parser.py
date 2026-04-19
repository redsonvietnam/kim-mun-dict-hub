import re
import json

def extract_savina_clean(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
        
    entries = []
    # Bắt đầu từ dòng có chứa dữ liệu từ điển thực tế (bỏ qua header hành chính)
    started = False
    
    for line in lines:
        line = line.strip()
        if not line: continue
        
        # Nhận diện khi nào bắt đầu danh sách từ (thường sau trang 17-18)
        if "Arroyo" in line or "CA'te" in line:
            started = True
        
        if not started: continue
        
        # Bỏ qua các dòng tiêu đề trang hoặc số trang
        if re.match(r'^- \d+ -$', line) or "FRANAAIS" in line or "K.LM-BI" in line or "TAl-PAN" in line:
            continue
            
        # Cấu trúc Savina thường là: [Tiếng Pháp] [Kim-Mun] [Tal-pan]
        # Tuy nhiên do OCR, chúng dính vào nhau. 
        # Một đặc điểm là Tiếng Pháp thường bắt đầu bằng chữ hoa hoặc là cụm từ đầu tiên.
        
        # Thử nghiệm bóc tách bằng AI-logic đơn giản:
        # Tách theo khoảng trắng lớn hoặc dấu phân cách
        parts = re.split(r'\s{2,}', line)
        
        if len(parts) >= 2:
            french = parts[0]
            mun_kimm = parts[1]
            # Tal-pan là phần còn lại nếu có
            entries.append({
                "source": "Savina (1926)",
                "french": french,
                "kimmun": mun_kimm,
                "vietnamese": "" # Sẽ dịch từ French
            })
            
    return entries

if __name__ == "__main__":
    sample = extract_savina_clean("befeo_0336-1519_1926_num_26_1_3091.pdf_draft.txt")
    print(f"Extracted {len(sample)} sample entries.")
    for e in sample[:10]:
        print(e)
