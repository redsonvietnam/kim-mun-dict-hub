import sqlite3

def check_sources():
    conn = sqlite3.connect('kim_mun_dict_v2.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT count(*) FROM dictionary WHERE entry_id LIKE 'CL-%'")
    clark = cursor.fetchone()[0]
    
    cursor.execute("SELECT count(*) FROM dictionary WHERE entry_id LIKE 'SA-%'")
    savina = cursor.fetchone()[0]
    
    # Những cái không có tiền tố CL hay SA thường là Funing (numeric)
    cursor.execute("SELECT count(*) FROM dictionary WHERE entry_id NOT LIKE 'CL-%' AND entry_id NOT LIKE 'SA-%'")
    funing = cursor.fetchone()[0]
    
    print(f"Clark entries: {clark}")
    print(f"Savina entries: {savina}")
    print(f"Funing entries: {funing}")
    
    # Check if we have a 'source' column
    cursor.execute("PRAGMA table_info(dictionary)")
    cols = [c[1] for c in cursor.fetchall()]
    print(f"Columns: {cols}")
    
    conn.close()

if __name__ == "__main__":
    check_sources()
