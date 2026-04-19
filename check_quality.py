import sqlite3
conn = sqlite3.connect('kim_mun_dict_v2.db')

total = conn.execute('SELECT count(*) FROM dictionary').fetchone()[0]
print(f'Tong entries: {total}')

dupes = conn.execute('SELECT entry_id, count(*) as c FROM dictionary GROUP BY entry_id HAVING c > 1 ORDER BY c DESC LIMIT 5').fetchall()
print(f'\nEntry_id bi trung lap: {len(dupes)} nhom')
for d in dupes[:5]:
    print(f'  {d[0]}: {d[1]} lan')

empty_kimmun = conn.execute("SELECT count(*) FROM dictionary WHERE source='Shintani (2008)' AND (kimmun='' OR kimmun IS NULL)").fetchone()[0]
print(f'\nFuning - kimmun trong/NULL: {empty_kimmun}')

empty_vi = conn.execute("SELECT count(*) FROM dictionary WHERE source='Shintani (2008)' AND (vietnamese='' OR vietnamese IS NULL)").fetchone()[0]
print(f'Funing - vietnamese trong/NULL: {empty_vi}')

savina_cat = conn.execute("SELECT count(*) FROM dictionary WHERE source='Savina (1926)' AND category != '' AND category IS NOT NULL").fetchone()[0]
savina_total = conn.execute("SELECT count(*) FROM dictionary WHERE source='Savina (1926)'").fetchone()[0]
print(f'\nSavina - co category: {savina_cat}/{savina_total}')

clark_total = conn.execute("SELECT count(*) FROM dictionary WHERE source='Clark (2000)'").fetchone()[0]
print(f'Clark - tong: {clark_total}')

conn.close()
