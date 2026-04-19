import sqlite3
import sys

# Set UTF-8 for printing
if sys.stdout.encoding != 'utf-8':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def verify_db():
    conn = sqlite3.connect("kim_mun_dict_v2.db")
    cursor = conn.cursor()
    
    print("Checking Funing entries...")
    cursor.execute("SELECT entry_id, chinese, kimmun, vietnamese FROM dictionary WHERE pos = 'Funing' LIMIT 5")
    for row in cursor.fetchall():
        print(f"ID: {row[0]} | Hanzi: {row[1]} | Mun: {row[2]} | Viet: {row[3]}")
        
    print("\nChecking Clark entries...")
    cursor.execute("SELECT entry_id, kimmun, vietnamese FROM dictionary WHERE pos = 'Clark 2008' LIMIT 5")
    for row in cursor.fetchall():
        print(f"ID: {row[0]} | Mun: {row[1]} | Viet: {row[2]}")
        
    conn.close()

if __name__ == "__main__":
    verify_db()
