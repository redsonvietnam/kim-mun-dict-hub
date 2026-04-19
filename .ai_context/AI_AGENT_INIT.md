# 🤖 Hướng Dẫn Cho AI Agent - Kim Mun Dictionary Hub

> **Đây là tài liệu KIM MUN PROJECT CONTEXT**
> Khi bạn (AI Agent) bắt đầu một phiên làm việc mới, hãy bắt đầu bằng việc đọc file này trước tiên!

---

## 🎯 Tóm Tắt Nhanh

**Dự Án**: Kim Mun Dictionary Hub - Nền tảng từ điển ngôn ngữ Kim Mun đầy đủ
**Vị Trí**: `d:\AGENT\dict_builder`
**Ngôn Ngữ Chính**: Python 3.13, Flask, SQLite
**Database**: `kim_mun_dict_v2.db` (12.486 entries)
**Web App**: http://127.0.0.1:5000 (Flask)

---

## 📚 Các File Context Bạn PHẢI Đọc (Theo Thứ Tự)

### 1️⃣ **ARCHITECTURE.md** 
📄 *Hiểu cấu trúc dự án*
- Cấu trúc Database
- Các bảng chính (dictionary table)
- Backend workflow
- **Thời gian đọc**: 5-10 phút

### 2️⃣ **ROADMAP.md**
📄 *Bức tranh toàn cảnh*
- Trạng thái hiện tại
- Kế hoạch tương lai
- Các milestone đã hoàn thành
- **Thời gian đọc**: 5 phút

### 3️⃣ **task.md**
📄 **⭐ QUAN TRỌNG NHẤT** - Nhiệm vụ hiện tại
- ✅ Những việc ĐÃ XONG
- 🔄 Việc ĐANG LÀM DỞ
- ⏳ Việc CẦN LÀM
- **Thời gian đọc**: 5 phút

### 4️⃣ **implementation_plan.md**
📄 *Chiến lược kỹ thuật*
- Các thay đổi dự kiến
- Component cần phát triển
- Open questions để hỏi user
- **Thời gian đọc**: 10 phút

### 5️⃣ **PAGE_REFERENCES_GUIDE.md**
📄 *Tham chiếu trang*
- Cách hiển thị page references
- Cách chỉnh sửa page references
- Dữ liệu mapping
- **Thời gian đọc**: 5-10 phút

---

## 🚀 Quy Trình Khởi Động Agent Mới

### Khi Bạn Bắt Đầu:

1. **Đọc Toàn Bộ** các file `.md` ở trên (theo thứ tự)
   ```bash
   # Vị trí: d:\AGENT\dict_builder\.ai_context\
   - ARCHITECTURE.md
   - ROADMAP.md
   - task.md
   - implementation_plan.md
   - PAGE_REFERENCES_GUIDE.md
   ```

2. **Chạy Script Kiểm Tra**:
   ```bash
   cd d:\AGENT\dict_builder
   python check_db_status.py
   ```
   → Này sẽ cho bạn biết DB hiện tại có bao nhiêu entries

3. **Chào User** với thông tin này:
   ```
   "✅ Tôi đã đọc xong các tài liệu context:
   - ARCHITECTURE.md ✓
   - ROADMAP.md ✓
   - task.md ✓
   - implementation_plan.md ✓
   - PAGE_REFERENCES_GUIDE.md ✓
   
   📊 Trạng thái DB hiện tại:
   - Tổng entries: 12.486
   - Savina (1926): 7.879
   - Shintani (2008): 4.445
   - Clark (2000): 162
   
   Chúng ta tiếp tục ở đâu?"
   ```

4. **Kiểm tra Web Server** (nếu cần):
   ```bash
   cd d:\AGENT\dict_builder\web_ui
   python app.py
   # → http://127.0.0.1:5000
   ```

---

## 🔧 Các Lệnh Hữu Ích

### Kiểm Tra Database
```bash
python check_db_status.py       # Xem số lượng entries theo nguồn
python show_page_samples.py     # Xem sample entries với page refs
```

### Export / Import Dữ Liệu
```bash
python export_for_page_review.py        # Export tất cả entries cho review
python create_page_mapping.py           # Tạo page mapping mới
python update_db_pages.py               # Update DB với pages mới
```

### Chạy Web Server
```bash
cd web_ui
python app.py
# → Mở http://127.0.0.1:5000 trong browser
```

---

## 📂 Cấu Trúc Thư Mục

```
d:\AGENT\dict_builder\
├── .ai_context/                    ← 🔴 CÁC FILE CONTEXT (READ FIRST!)
│   ├── ARCHITECTURE.md
│   ├── ROADMAP.md
│   ├── task.md
│   ├── implementation_plan.md
│   └── PAGE_REFERENCES_GUIDE.md
├── web_ui/                         ← Flask web app
│   ├── app.py
│   └── templates/index.html
├── kim_mun_dict_v2.db              ← 🔴 DATABASE CHÍNH (12.486 entries)
├── *.json                          ← Source data files
├── *.py                            ← Scripts để process dữ liệu
└── README.md                       ← Project README
```

---

## 🔑 Thông Tin Kỹ Thuật Quan Trọng

### Database
- **File**: `kim_mun_dict_v2.db`
- **Bảng chính**: `dictionary`
- **Các cột chính**: 
  - `entry_id` - ID mục từ
  - `source` - Nguồn (Savina, Shintani, Clark)
  - `page_ref` - Tham chiếu trang (p.XX)
  - `chinese` - Hán tự
  - `pinyin` - Pinyin
  - `kimmun` - Kim Mun (IPA)
  - `vietnamese` - Tiếng Việt
  - `meaning_en` - Ý nghĩa Tiếng Anh
  - `category` - Chủ đề/Danh mục
  - `source` - Nguồn

### Web App (Flask)
- **Port**: 5000
- **File**: `web_ui/app.py`
- **Routes chính**:
  - `GET /` - Giao diện chính
  - `GET /search` - Tìm kiếm
  - `GET /stats` - Thống kê
  - `GET /export_csv` - Export CSV
  - `POST /import_csv` - Import CSV
  - `POST /update_entry` - Cập nhật entry

### Sources (Nguồn)
- **Savina (1926)**: 7.879 entries (file PDF trong KIMM_DOCS)
- **Shintani (2008)**: 4.445 entries (Funing Lexicon)
- **Clark (2000)**: 162 entries (bài báo)

---

## 🎯 Các Trạng Thái Task (Xem task.md Để Chi Tiết)

✅ **Đã Hoàn Thành**:
- Database merge từ 3 nguồn
- Web UI (Card View + Table View)
- CSV Export/Import
- Inline Edit Modal
- Page References System
- Phonology Academic Hub

🔄 **Đang Làm Dở**:
- Vision extraction từ PDF (cần Gemini API key mới)

⏳ **Cần Làm**:
- Hoàn thành vision extraction cho tất cả pages
- Tối ưu UI
- Deploy online
- Backup/Sync database

---

## 🆘 Troubleshooting

### Web Server không chạy?
```bash
cd d:\AGENT\dict_builder\web_ui
python app.py
# Nếu lỗi, check: Python 3.13, Flask installed
```

### CSV import không hoạt động?
- Đảm bảo file CSV có UTF-8 BOM
- Check cấu trúc cột: entry_id, source, page_ref, ...

### Database lock?
```bash
# Đóng tất cả Python processes
taskkill /F /IM python.exe
```

---

## 💾 Continuity & Backup

**Để đảm bảo không bị đứt đoạn**:

1. **Trước khi kết thúc phiên**:
   - Run: `python export_for_page_review.py` (backup dữ liệu hiện tại)
   - Commit changes vào Git nếu có
   - Update `task.md` với trạng thái mới

2. **Khi bắt đầu phiên mới**:
   - Đọc lại `task.md` để biết ở đâu
   - Run `python check_db_status.py` để xác nhận dữ liệu
   - Tiếp tục từ điểm để dở

3. **Giữ `.ai_context/` được cập nhật**:
   - Luôn update `task.md` khi có thay đổi
   - Ghi chú lại progress vào comment
   - Lưu reference PDFs trong thư mục

---

## 📞 Khi Cần Hỗ Trợ

**Hỏi User** nếu:
- Bạn không rõ trạng thái hiện tại
- Cần thêm dữ liệu/API keys
- Cần hướng dẫn về business logic
- Không chắc chuyển hướng tiếp theo

**Lệnh hữu ích**:
```bash
# Xem trạng thái hiện tại
python check_db_status.py
python show_page_samples.py

# Xem các file context
cat .ai_context/task.md
cat .ai_context/ARCHITECTURE.md

# Check git history
git log --oneline -10
```

---

## ✨ Final Checklist Cho Agent Mới

Trước khi bắt tay vào làm việc:

- [ ] Đã đọc ARCHITECTURE.md?
- [ ] Đã đọc ROADMAP.md?
- [ ] Đã đọc task.md?
- [ ] Đã đọc implementation_plan.md?
- [ ] Đã đọc PAGE_REFERENCES_GUIDE.md?
- [ ] Đã chạy `python check_db_status.py`?
- [ ] Biết current task là gì?
- [ ] Web server chạy ok không?
- [ ] Ready to continue? ✅

---

**Chúc bạn làm việc vui vẻ! Nếu có vấn đề gì, hãy hỏi!** 🚀
