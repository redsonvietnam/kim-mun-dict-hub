import sqlite3
conn = sqlite3.connect('kim_mun_dict_v2.db')
cols_to_add = [
    ('meaning_fr', 'TEXT'),
    ('notes', 'TEXT'),
    ('page_ref', 'TEXT'),
]
for col, typ in cols_to_add:
    try:
        conn.execute(f'ALTER TABLE dictionary ADD COLUMN {col} {typ} DEFAULT ""')
        print(f'Added column: {col}')
    except Exception as e:
        print(f'Skip {col}: {e}')
conn.commit()
conn.close()
print('Done!')
