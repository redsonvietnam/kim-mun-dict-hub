"# 📚 Kim Mun Dictionary Hub

**Nền tảng từ điển ngôn ngữ Kim Mun toàn diện** - Gộp từ các nguồn học thuật Savina (1926), Shintani (2008), và Clark (2000)

---

## 🚀 Bắt Đầu Nhanh

### 1. **Nếu bạn là AI Agent (Khuyến Nghị Đọc Trước)**
> **Trước khi làm bất cứ điều gì, hãy đọc:**  
> `.ai_context/AI_AGENT_INIT.md`

File này chứa:

## Kim Mun Dictionary Hub — Hướng dẫn nhanh

Khi bạn bắt đầu một phiên làm việc mới (IDE hoặc agent khác), làm theo các bước sau để đảm bảo continuity giữa các session:

1. Mở và đọc các file trong thư mục `.ai_context/` theo thứ tự:
   - `ARCHITECTURE.md`
   - `ROADMAP.md`
   - `task.md`
   - `implementation_plan.md`
   - `AI_PROMPT_INIT.md` (Hướng dẫn khởi tạo cho Agent)
   - `AGENT_SUMMARY.md` (Tóm tắt nhanh)
   - `PAGE_REFERENCES_GUIDE.md` (Hướng dẫn tham chiếu trang, tiếng Việt)

2. Chạy script kiểm tra khởi động để xác nhận môi trường:

```powershell
cd d:\\AGENT\\dict_builder
python startup_check.py
```

3. Nếu có thay đổi quan trọng (code, dữ liệu, DB), commit và push lên GitHub repo chính: https://github.com/redsonvietnam/kim-mun-dict-hub

4. Khởi chạy giao diện web (nếu cần) để kiểm tra trực tiếp:

```powershell
cd d:\\AGENT\\dict_builder\\web_ui
python app.py
```

Ghi chú: Đừng push các API keys hoặc secrets vào repo. Lưu keys trong biến môi trường hoặc secret manager.

---

File này là entrypoint người / agent nhìn đầu tiên khi bắt đầu làm việc trên thư mục `dict_builder`.
```bash
cd web_ui
python app.py
# → Mở http://127.0.0.1:5000 trong browser
```

### 3. **Kiểm Tra Database**
```bash
python check_db_status.py
```

---

## 📖 Các File Context (.ai_context/)

Khi bắt đầu dự án mới, hãy đọc theo thứ tự này:

| File | Mục Đích | Thời Gian |
|------|---------|----------|
| **AI_AGENT_INIT.md** | 🤖 Hướng dẫn cho AI agents (ĐỌC TRƯỚC!) | 5-10 phút |
| **ARCHITECTURE.md** | 🏗️ Cấu trúc DB, Backend | 5-10 phút |
| **ROADMAP.md** | 🗺️ Bức tranh toàn cảnh, milestones | 5 phút |
| **task.md** | 📋 Việc ĐÃ XONG / ĐANG LÀM / CẦN LÀM | 5 phút |
| **implementation_plan.md** | 🛠️ Chiến lược kỹ thuật, các thay đổi | 10 phút |
| **PAGE_REFERENCES_GUIDE.md** | 📖 Tham chiếu trang, cách chỉnh sửa | 5-10 phút |

---

## 📊 Trạng Thái Dự Án

### ✅ Đã Hoàn Thành
- [x] Database merge (12.486 entries từ 3 nguồn)
- [x] Web UI (Card View + Table View)
- [x] Search & Filter
- [x] CSV Export/Import
- [x] Inline Edit Modal
- [x] Page References System (tất cả entries có page_ref)
- [x] Phonology Academic Hub
- [x] Beautiful dark theme UI

### 🔄 Đang Làm Dở
- [ ] Vision extraction từ PDF (cần API key mới)
- [ ] Fine-tune page references

### ⏳ Cần Làm
- [ ] Hoàn thành vision extraction
- [ ] Deploy online
- [ ] Database backup/sync
- [ ] UI/UX optimization

---

## 📁 Cấu Trúc Thư Mục

```
kim_mun_dict_builder/
├── .ai_context/                           ← 🔴 FILE CONTEXT (ĐỌC TRƯỚC!)
│   ├── AI_AGENT_INIT.md                  ← Hướng dẫn agent (BẮT BUỘC)
│   ├── ARCHITECTURE.md
│   ├── ROADMAP.md
│   ├── task.md
│   ├── implementation_plan.md
│   └── PAGE_REFERENCES_GUIDE.md
├── web_ui/
│   ├── app.py                             ← Flask backend
│   ├── static/
│   └── templates/
│       └── index.html                     ← Frontend giao diện
├── kim_mun_dict_v2.db                     ← 🔴 DATABASE CHÍNH
├── page_reference_mapping.json            ← Ánh xạ trang
├── kim_mun_dict_with_pages.csv            ← Export cho review
├── *.json                                 ← Source data files
├── *.py                                   ← Scripts processing
└── README.md                              ← File này

```

---

## 🗄️ Database

**File**: `kim_mun_dict_v2.db` (SQLite)

**Thống kê**:
```
Tổng entries: 12.486
├── Savina (1926):    7.879 entries
├── Shintani (2008):  4.445 entries
└── Clark (2000):     162 entries
```

**Bảng chính**: `dictionary`
- `entry_id` - Mã mục từ
- `source` - Nguồn (Savina, Shintani, Clark)
- `page_ref` - Trang (p.XX)
- `chinese` - Hán tự
- `pinyin` - Pinyin
- `kimmun` - Kim Mun (IPA)
- `vietnamese` - Tiếng Việt
- `meaning_en` - Ý nghĩa Tiếng Anh
- `category` - Chủ đề/Danh mục
- `notes` - Ghi chú

---

## 🌐 Web UI

**Chạy**: `http://127.0.0.1:5000`

**Tính năng**:
- 🔍 **Tìm kiếm** - Search across Vietnamese, Kim Mun, English, Chinese, Pinyin
- 🏷️ **Lọc** - By Source (Savina, Shintani, Clark) & Category
- 🎨 **View Modes** - Card View (mặc định) + Table View
- ✏️ **Chỉnh sửa** - Inline edit modal
- 📤 **Export** - Tải xuống CSV
- 📥 **Import** - Upload CSV để batch update
- 🔬 **Academic Hub** - Xem Phonology (Âm vị học)
- 📖 **Page References** - Mỗi entry hiển thị số trang

---

## 🛠️ Các Lệnh Hữu Ích

### Kiểm Tra
```bash
python check_db_status.py                 # Xem số entries theo nguồn
python show_page_samples.py               # Xem sample entries với pages
```

### Xử Lý Dữ Liệu
```bash
python export_for_page_review.py          # Export tất cả + page refs
python create_page_mapping.py             # Tạo page mapping
python update_db_pages.py                 # Update DB với pages
```

### Web Server
```bash
cd web_ui
python app.py
```

---

## 📝 Hướng Dẫn Chỉnh Sửa Page References

**Phương pháp 1**: Dùng Web UI (đơn giản)
- Click card → Edit → Update `page_ref` → Save

**Phương pháp 2**: CSV bulk edit (nhanh)
1. Export: `python export_for_page_review.py`
2. Mở `kim_mun_dict_with_pages.csv` trong Excel
3. Chỉnh sửa cột `CORRECTED_PAGE`
4. Save CSV
5. Upload qua Web UI → Auto update DB

**Phương pháp 3**: Kiểm chéo PDF
- Savina: `KIMM_DOCS/befeo_0336-1519_1926_num_26_1_3091.pdf`
- Shintani: `KIMM_DOCS/The-Mun-Language-of-Funing-CountyIts-Classified-Lexicon富寧金門語.pdf`

---

## 💾 Đảm Bảo Continuity

**Để dự án không bị đứt đoạn khi chuyển agent/session**:

1. **Luôn update** `.ai_context/task.md` khi có thay đổi
2. **Export dữ liệu** trước khi kết thúc: `python export_for_page_review.py`
3. **Đọc lại** tất cả `.md` files khi bắt đầu session mới
4. **Run** `python check_db_status.py` để xác nhận

---

## 🤖 Cho AI Agents

**Khi bạn bắt đầu:**
1. Đọc `.ai_context/AI_AGENT_INIT.md` TRƯỚC TIÊN
2. Đọc tất cả các file context theo thứ tự
3. Chạy `python check_db_status.py`
4. Chào user với current status
5. Hỏi user: "Chúng ta tiếp tục ở đâu?"

**Important**: Đây là continuity system - agent mới phải đọc các file context để hiểu progress hiện tại!

---

## 🚀 Các Bước Tiếp Theo

1. **Hoàn thành Vision Extraction** (cần API key mới)
   - Trích xuất Phonology pages (13-20)
   - Trích xuất Topic 1 pages (21-34)

2. **Tối ưu Page References**
   - Xác minh page mapping cho Savina
   - Tinh chỉnh category ranges cho Shintani

3. **Nâng cấp UI**
   - Mobile responsive
   - Dark mode toggle
   - Advanced filters

4. **Deployment**
   - Deploy to cloud (Vercel/Render)
   - Setup CI/CD
   - Database backup

---

## 📞 Support

Hỏi user (hoặc hỏi AI lead) nếu:
- Không rõ trạng thái hiện tại
- Cần API keys/credentials
- Cần hướng dẫn business logic
- Gặp lỗi technical

---

## 📜 License

This project is part of Kim Mun linguistic research and documentation.

---

**Last Updated**: April 19, 2026
**Status**: Active Development
**Database**: 12.486 entries
**Web UI**: Running ✅

" 
