import sqlite3
import json

def get_french_words():
    conn = sqlite3.connect('kim_mun_dict_v2.db')
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT french_orig FROM dictionary WHERE source LIKE 'Savina%'")
    words = [r[0] for r in cursor.fetchall() if r[0]]
    
    with open("savina_french_list.json", "w", encoding="utf-8") as f:
        json.dump(words, f, ensure_ascii=False, indent=4)
    
    print(f"Total unique French words: {len(words)}")
    conn.close()

if __name__ == "__main__":
    get_french_words()
