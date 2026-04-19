import sqlite3
import unicodedata

def remove_accents(input_str):
    if not input_str:
        return ""
    # Đặc biệt cho tiếng Việt: 'đ' không được normalize bằng NFKD một cách đơn thuần
    input_str = input_str.replace('đ', 'd').replace('Đ', 'D')
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return "".join([c for c in nfkd_form if not unicodedata.combining(c)]).lower()

def test_db_content():
    conn = sqlite3.connect('kim_mun_dict_v2.db')
    cursor = conn.cursor()
    
    # Kiểm tra xem có dữ liệu tiếng Việt không
    cursor.execute("SELECT entry_id, vietnamese, meaning_en FROM dictionary WHERE vietnamese != '' LIMIT 10")
    results = cursor.fetchall()
    print("--- Sample results with Vietnamese ---")
    for r in results:
        print(f"ID: {r[0]} | VN: {r[1]} | EN: {r[2]}")
        print(f"  Normalized VN: {remove_accents(r[1])}")
    
    # Kiểm tra riêng từ 'Mặt trời' (ID 011005)
    cursor.execute("SELECT vietnamese FROM dictionary WHERE entry_id = '011005'")
    row = cursor.fetchone()
    print(f"\nTarget 011005 (Sun) VN: {row[0] if row else 'NOT FOUND'}")
    
    conn.close()

if __name__ == "__main__":
    test_db_content()
