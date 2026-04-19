import os
import sqlite3
import unicodedata
from flask import Flask, render_template, request, jsonify

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

if __name__ == '__main__':
    print("Khởi chạy máy chủ Web Giao diện Từ Điển tại http://127.0.0.1:5000")
    app.run(debug=True, port=5000)
