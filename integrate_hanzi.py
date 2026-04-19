import sqlite3
import json
import os

def integrate_hanzi(json_path="id_hanzi_map.json", db_path="kim_mun_dict_v2.db"):
    if not os.path.exists(json_path):
        print(f"File {json_path} chưa tồn tại. Đang đợi OCR hoàn tất...")
        return
        
    with open(json_path, "r", encoding="utf-8") as f:
        hanzi_map = json.load(f)
        
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    update_count = 0
    for eid, hanzi in hanzi_map.items():
        # Cập nhật Hán tự dựa trên mã ID (vd: 011001)
        cursor.execute('''
            UPDATE dictionary 
            SET chinese = ? 
            WHERE entry_id = ?
        ''', (hanzi, eid))
        
        if cursor.rowcount > 0:
            update_count += 1
            
    conn.commit()
    conn.close()
    print(f"Đã cập nhật Hán tự cho {update_count} mục từ trong Database.")

if __name__ == "__main__":
    integrate_hanzi()
