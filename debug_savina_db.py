import sqlite3

def dump_savina():
    conn = sqlite3.connect('kim_mun_dict_v2.db')
    cursor = conn.cursor()
    cursor.execute("SELECT french_orig, vietnamese, kimmun, meaning_en FROM dictionary WHERE source LIKE 'Savina%' LIMIT 20")
    rows = cursor.fetchall()
    
    with open("savina_debug_dump.txt", "w", encoding="utf-8") as f:
        f.write("FRENCH_ORIG | VIETNAMESE | KIMMUN | MEANING_EN\n")
        f.write("-" * 50 + "\n")
        for r in rows:
            f.write(f"{r[0]} | {r[1]} | {r[2]} | {r[3]}\n")
    conn.close()

if __name__ == "__main__":
    dump_savina()
