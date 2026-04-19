import sqlite3

def migrate_db():
    conn = sqlite3.connect("kim_mun_dict_v2.db")
    cursor = conn.cursor()
    
    # Thêm cột entry_id và chinese nếu chưa có
    try:
        cursor.execute("ALTER TABLE dictionary ADD COLUMN entry_id TEXT")
        print("Added column entry_id")
    except sqlite3.OperationalError:
        print("Column entry_id already exists")
        
    try:
        cursor.execute("ALTER TABLE dictionary ADD COLUMN chinese TEXT")
        print("Added column chinese")
    except sqlite3.OperationalError:
        print("Column chinese already exists")
        
    conn.commit()
    conn.close()

if __name__ == "__main__":
    migrate_db()
