import sqlite3

def check_savina():
    conn = sqlite3.connect('kim_mun_dict_v2.db')
    cursor = conn.cursor()
    cursor.execute("SELECT french_orig, vietnamese, kimmun FROM dictionary WHERE source LIKE 'Savina%' LIMIT 10")
    rows = cursor.fetchall()
    
    print("--- Savina Data Check ---")
    for r in rows:
        print(f"French: {r[0]} | Viet: {r[1]} | Dao: {r[2]}")
    
    conn.close()

if __name__ == "__main__":
    check_savina()
