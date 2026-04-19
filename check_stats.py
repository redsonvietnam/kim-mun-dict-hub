import sqlite3

def check_db_stats():
    conn = sqlite3.connect('kim_mun_dict_v2.db')
    cursor = conn.cursor()
    
    # 1. Tổng số bản ghi
    cursor.execute('SELECT count(*) FROM dictionary')
    total = cursor.fetchone()[0]
    
    # 2. Số bản ghi có tiếng Việt "thật" (không có tiền tố [VN])
    cursor.execute("SELECT count(*) FROM dictionary WHERE vietnamese IS NOT NULL AND vietnamese != '' AND vietnamese NOT LIKE '[VN]%'")
    real_vn = cursor.fetchone()[0]
    
    # 3. Số bản ghi có tiền tố [VN]
    cursor.execute("SELECT count(*) FROM dictionary WHERE vietnamese LIKE '[VN]%'")
    mock_vn = cursor.fetchone()[0]
    
    # 4. Kiểm tra một từ cụ thể
    cursor.execute("SELECT entry_id, vietnamese, meaning_en FROM dictionary WHERE entry_id='011005'")
    sample = cursor.fetchone()
    
    print(f"Total entries: {total}")
    print(f"Real Vietnamese entries: {real_vn}")
    print(f"Mock [VN] entries: {mock_vn}")
    print(f"Sample 011005: {sample}")
    
    conn.close()

if __name__ == "__main__":
    check_db_stats()
