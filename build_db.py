import sqlite3
import json
import os

def build_database(json_path="kim_mun_parsed.json", db_path="kim_mun_dict.db"):
    if not os.path.exists(json_path):
        print(f"Không tìm thấy file {json_path}")
        return
        
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Tạo bảng nếu chưa có
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS dictionary (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            word TEXT NOT NULL,
            phonetic TEXT,
            pos TEXT,
            meaning TEXT NOT NULL
        )
    ''')
    
    # Xoá dữ liệu cũ nếu muốn làm mới (tuỳ chọn)
    # cursor.execute('DELETE FROM dictionary')
    
    # Nạp dữ liệu
    count = 0
    for entry in data:
        # Nếu từ đã tồn tại thì bỏ qua hoặc cập nhật (ở đây insert mới)
        cursor.execute('''
            INSERT INTO dictionary (word, phonetic, pos, meaning)
            VALUES (?, ?, ?, ?)
        ''', (entry["word"], entry["phonetic"], entry["pos"], entry["meaning"]))
        count += 1
        
    conn.commit()
    conn.close()
    print(f"Đã nạp thành công {count} từ vựng vào Database: {db_path}")

if __name__ == "__main__":
    build_database()
