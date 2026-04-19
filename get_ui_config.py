import sqlite3
import json

def get_ui_data():
    conn = sqlite3.connect('kim_mun_dict_v2.db')
    cursor = conn.cursor()
    
    # Lấy danh sách nguồn
    cursor.execute("SELECT source, count(*) FROM dictionary GROUP BY source")
    sources = [{"name": r[0], "count": r[1]} for r in cursor.fetchall()]
    
    # Lấy danh sách category
    cursor.execute("SELECT category FROM dictionary WHERE category != 'General' AND category != '' GROUP BY category ORDER BY count(*) DESC")
    categories = [r[0] for r in cursor.fetchall()]
    
    data = {
        "sources": sources,
        "categories": categories
    }
    
    with open("ui_config.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    
    conn.close()

if __name__ == "__main__":
    get_ui_data()
