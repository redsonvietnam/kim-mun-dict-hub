import os
import io
import csv
import sqlite3
import unicodedata
from flask import Flask, render_template, request, jsonify, Response, stream_with_context

app = Flask(__name__)
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "kim_mun_dict_v2.db")

def remove_accents(input_str):
    if not input_str:
        return ""
    input_str = input_str.replace('đ', 'd').replace('Đ', 'D')
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return "".join([c for c in nfkd_form if not unicodedata.combining(c)]).lower()

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search')
def search():
    query = request.args.get('q', '').strip()
    source_filter = request.args.get('source', 'All').strip()
    category_filter = request.args.get('category', '').strip()
    
    conn = get_db_connection()
    
    sql = "SELECT * FROM dictionary WHERE 1=1"
    params = []
    
    # Ưu tiên Category trước nếu có lọc theo chủ đề
    if category_filter:
        sql += " AND category = ?"
        params.append(category_filter)

    if query:
        search_term = f"%{query}%"
        sql += """ AND (
            vietnamese LIKE ? 
            OR kimmun LIKE ? 
            OR meaning_en LIKE ? 
            OR entry_id LIKE ? 
            OR chinese LIKE ? 
            OR pinyin LIKE ?
        )"""
        params.extend([search_term] * 6)
    
    if source_filter != 'All':
        sql += " AND source = ?"
        params.append(source_filter)
        
    sql += " LIMIT 200"
    
    words = [dict(w) for w in conn.execute(sql, params).fetchall()]
    conn.close()
    
    # Sort and refine matching for Vietnamese if querying
    if query:
        query_clean = remove_accents(query)
        for word in words:
            vi_clean = remove_accents(word.get('vietnamese', ''))
            word['match_score'] = 1 if query_clean in vi_clean else 0
        words.sort(key=lambda x: x.get('match_score', 0), reverse=True)

    return jsonify(words[:100])

@app.route('/stats')
def stats():
    conn = get_db_connection()
    total = conn.execute("SELECT count(*) FROM dictionary").fetchone()[0]
    sources = conn.execute("SELECT source, count(*) FROM dictionary GROUP BY source").fetchall()
    categories = conn.execute("SELECT category, count(*) FROM dictionary WHERE category != 'General' AND category != '' GROUP BY category ORDER BY count(*) DESC").fetchall()
    conn.close()
    
    return jsonify({
        "total": total,
        "sources": [dict(s) for s in sources],
        "categories": [dict(c) for c in categories]
    })


@app.route('/entry/<entry_id>')
def get_entry(entry_id):
    """Lấy chi tiết một mục từ để chỉnh sửa."""
    conn = get_db_connection()
    row = conn.execute("SELECT * FROM dictionary WHERE entry_id = ? LIMIT 1", (entry_id,)).fetchone()
    conn.close()
    if row:
        return jsonify(dict(row))
    return jsonify({"error": "Không tìm thấy mục từ."}), 404

@app.route('/update_entry', methods=['POST'])
def update_entry():
    """Cập nhật trực tiếp một mục từ vào DB."""
    data = request.get_json()
    entry_id = data.get('entry_id', '').strip()
    if not entry_id:
        return jsonify({"error": "Thiếu entry_id."}), 400
    
    conn = get_db_connection()
    conn.execute("""
        UPDATE dictionary SET
            chinese = ?, pinyin = ?, kimmun = ?, vietnamese = ?,
            meaning_en = ?, meaning_fr = ?, category = ?, subcategory = ?, notes = ?
        WHERE entry_id = ?
    """, (
        data.get('chinese', ''), data.get('pinyin', ''), data.get('kimmun', ''),
        data.get('vietnamese', ''), data.get('meaning_en', ''), data.get('meaning_fr', ''),
        data.get('category', ''), data.get('subcategory', ''), data.get('notes', ''),
        entry_id
    ))
    conn.commit()
    changes = conn.execute("SELECT changes()").fetchone()[0]
    conn.close()
    return jsonify({"success": True, "updated": changes})

@app.route('/phonology')
def phonology():
    """Trả về nội dung Markdown về Âm vị học Kim Mun."""
    phono_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".ai_context", "kim_mun_phonology.md")
    if os.path.exists(phono_path):
        with open(phono_path, encoding="utf-8") as f:
            return jsonify({"content": f.read()})
    return jsonify({"content": "# Chưa có dữ liệu Âm vị học."})

@app.route('/export_csv')
def export_csv():
    """Xuất dữ liệu hiện tại ra file CSV."""
    source_filter = request.args.get('source', 'All').strip()
    category_filter = request.args.get('category', '').strip()
    
    conn = get_db_connection()
    sql = "SELECT entry_id, chinese, pinyin, kimmun, vietnamese, meaning_en, meaning_fr, category, subcategory, source, page_ref FROM dictionary WHERE 1=1"
    params = []
    if category_filter:
        sql += " AND category = ?"
        params.append(category_filter)
    if source_filter != 'All':
        sql += " AND source = ?"
        params.append(source_filter)
    
    rows = conn.execute(sql, params).fetchall()
    conn.close()
    
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['entry_id', 'chinese', 'pinyin', 'kimmun', 'vietnamese', 'meaning_en', 'meaning_fr', 'category', 'subcategory', 'source', 'page_ref'])
    for row in rows:
        writer.writerow(list(row))
    
    filename = f"kimmun_export_{source_filter}_{category_filter or 'all'}.csv".replace(' ', '_').replace('(', '').replace(')', '')
    return Response(
        '\ufeff' + output.getvalue(),  # BOM for Excel UTF-8 compatibility
        mimetype='text/csv; charset=utf-8',
        headers={'Content-Disposition': f'attachment; filename="{filename}"'}
    )

@app.route('/import_csv', methods=['POST'])
def import_csv():
    """Nhận file CSV và cập nhật DB theo entry_id."""
    if 'file' not in request.files:
        return jsonify({"error": "Không có file được tải lên."}), 400
    
    file = request.files['file']
    content = file.read().decode('utf-8-sig')  # Xử lý BOM
    
    reader = csv.DictReader(io.StringIO(content))
    conn = get_db_connection()
    updated = 0
    errors = []
    
    for row in reader:
        entry_id = row.get('entry_id', '').strip()
        if not entry_id:
            continue
        try:
            conn.execute("""
                UPDATE dictionary SET
                    chinese = ?, pinyin = ?, kimmun = ?, vietnamese = ?,
                    meaning_en = ?, meaning_fr = ?, category = ?, subcategory = ?, page_ref = ?
                WHERE entry_id = ?
            """, (
                row.get('chinese',''), row.get('pinyin',''), row.get('kimmun',''),
                row.get('vietnamese',''), row.get('meaning_en',''), row.get('meaning_fr',''),
                row.get('category',''), row.get('subcategory',''), row.get('page_ref',''),
                entry_id
            ))
            updated += conn.execute("SELECT changes()").fetchone()[0]
        except Exception as e:
            errors.append(str(e))
    
    conn.commit()
    conn.close()
    return jsonify({"updated": updated, "errors": errors})

if __name__ == '__main__':
    print("Khởi chạy máy chủ Web Giao diện Từ Điển tại http://127.0.0.1:5000")
    app.run(debug=True, port=5000)
