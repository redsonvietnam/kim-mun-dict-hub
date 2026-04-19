"""
Kiểm tra xem kimmun data có sẵn trong file JSON gốc không.
Nếu có, ta chỉ cần map lại — KHÔNG cần dùng API Vision.
"""
import json, sqlite3

# Đọc file JSON gốc (trước khi clean)
with open('funing_final_master.json', encoding='utf-8') as f:
    raw = json.load(f)

# Đọc DB để lấy danh sách entry_id bị mất kimmun
conn = sqlite3.connect('kim_mun_dict_v2.db')
missing = conn.execute(
    "SELECT entry_id FROM dictionary WHERE source='Shintani (2008)' AND (kimmun='' OR kimmun IS NULL)"
).fetchall()
conn.close()

missing_ids = {r[0] for r in missing}
print(f'Tổng entry bị mất kimmun trong DB: {len(missing_ids)}')

# Kiểm tra trong file JSON gốc có kimmun không
raw_has_kimmun = 0
raw_can_fix = 0
for entry in raw:
    eid = str(entry.get('entry_id', '')).strip()
    if eid in missing_ids:
        km = str(entry.get('kimmun', '')).strip()
        raw_has_kimmun += 1
        if km and km not in ('', 'None', 'nan'):
            raw_can_fix += 1

print(f'Trong số đó, có trong file JSON gốc: {raw_has_kimmun}')
print(f'Trong dó, JSON gốc có kimmun có giá trị: {raw_can_fix}')

# Hiển thị mẫu
print('\n--- VÍ DỤ MẪU CÁC ENTRY BỊ MẤT KIMMUN TRONG DB ---')
for entry in raw:
    eid = str(entry.get('entry_id', '')).strip()
    if eid in missing_ids:
        km = str(entry.get('kimmun', '')).strip()
        vi = str(entry.get('vietnamese', '')).strip()[:30]
        print(f'  {eid} | kimmun="{km}" | vi="{vi}"')
        break  # chỉ xem 1 mẫu
