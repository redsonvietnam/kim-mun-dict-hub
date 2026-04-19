# 📚 Tài Liệu AI Context - Hướng Dẫn

**Chào các Agent/Dev tiếp theo! 👋**

Đây là folder chứa tất cả tài liệu context cần thiết để bắt đầu làm việc với dự án Kim Mun Dictionary Hub.

---

## 🚀 BẮT ĐẦU NHANH

### Bước 1: Đọc Các File Chính (5-10 phút)

Bắt đầu từ những file này theo thứ tự:

1. **AI_PROMPT_INIT.md** ⭐ (PHẢI ĐỌC)
   - 7 bước khởi động cho AI agents
   - Quy trình commit/push GitHub
   - Kiểm tra an toàn

2. **QUICK_START.md** (3-5 phút)
   - Tổng quan nhanh về dự án
   - Cấu trúc thư mục chính
   - Câu lệnh cơ bản

3. **task.md** (Review tiến độ)
   - Trạng thái hiện tại: **92.5% hoàn thành**
   - Những gì đã làm
   - Những gì chưa làm

### Bước 2: Chọn Tài Liệu Theo Nhiệm Vụ

#### 🔧 Nếu Bạn Muốn Contributes Code
- Đọc: **GITHUB_NOTICE.md**
  - Git workflow (add → commit → push)
  - Quy tắc đặt tên commit
  - Bảo mật (NO API keys in repo!)

#### 📖 Nếu Bạn Muốn Hiểu Page Reference System
- Đọc: **PAGE_REFERENCES_GUIDE.md**
  - Cách page reference hoạt động
  - CSV workflow cho verification
  - Adjust trang qua UI

#### 🔤 Nếu Bạn Muốn Học Về Phonology Kim Mun
- Đọc: **PHONOLOGY_VI.md** 🇻🇳
  - Phương hệ Kim Mun toàn diện
  - So sánh 3 nguồn (Savina 1926, Shintani 2008, Clark 2008)
  - Ứng dụng cho giáo dục & bảo tồn

---

## 📋 File Tham Khảo

| File | Kích Thước | Mục Đích | Đọc Nếu... |
|------|-----------|---------|-----------|
| **AI_PROMPT_INIT.md** | 2.5 KB | Startup procedure | Bạn là AI agent mới |
| **QUICK_START.md** | 3.2 KB | Getting started | Bạn lần đầu làm việc |
| **task.md** | 7 KB | Project status | Bạn muốn biết progress |
| **GITHUB_NOTICE.md** | 1.1 KB | Git workflow | Bạn muốn push code |
| **PAGE_REFERENCES_GUIDE.md** | 6.1 KB | Page system | Bạn làm việc với pages |
| **PHONOLOGY_VI.md** | 15 KB | Phonology analysis | Bạn muốn hiểu ngôn ngữ |

---

## 🎯 Tính Năng Chính Của Dự Án

```
✅ Database: 12,486 Kim Mun entries từ 3 nguồn (Savina, Shintani, Clark)
✅ Web UI: Card View + Table View + Search + Export/Import
✅ Page References: Mỗi entry có reference đến trang PDF
✅ Phonology Docs: Phân tích chi tiết (tiếng Việt & English)
✅ Infrastructure: Startup check, Git workflow, AI documentation
🔄 Vision Extraction: 30% (chờ API key Gemini mới)
⏳ Deployment: Chưa bắt đầu (sẵn sàng khi hoàn thành)
```

---

## 🛠️ Các Câu Lệnh Thường Dùng

```bash
# Kiểm tra environment startup
python startup_check.py

# Chạy web server
cd web_ui && python app.py

# Commit & push (sau khi thay đổi)
git add -A
git commit -m "feat: Mô tả ngắn thay đổi của bạn"
git push origin main

# Xem trạng thái git
git status
git log --oneline -5
```

---

## 📁 Cấu Trúc Dự Án

```
d:\AGENT\dict_builder\
├── .ai_context/              ← Bạn đang ở đây!
│   ├── README.md             ← File này
│   ├── AI_PROMPT_INIT.md     (Startup guide)
│   ├── QUICK_START.md        (Getting started)
│   ├── task.md               (Progress tracking)
│   ├── GITHUB_NOTICE.md      (Git workflow)
│   ├── PAGE_REFERENCES_GUIDE.md
│   ├── PHONOLOGY_VI.md       ⭐ Phonology analysis (Tiếng Việt)
│   └── AGENT_SUMMARY.md      (Quick reference)
│
├── web_ui/                   ← Flask web application
│   ├── app.py
│   ├── templates/
│   │   └── index.html
│   └── static/
│
├── kim_mun_dict_v2.db        ← SQLite database (12,486 entries)
│
├── extract_phonology_comparative.py
├── enhance_phonology_extraction.py
├── startup_check.py
│
├── README.md                 ← Project README
└── [Other scripts & data files...]
```

---

## ❓ Thường Gặp

### Q: Tôi là AI agent mới, bắt đầu từ đâu?
**A:** 
1. Đọc `AI_PROMPT_INIT.md` (đầu tiên!)
2. Chạy `python startup_check.py` để verify
3. Đọc `task.md` để hiểu progress hiện tại
4. Xem `QUICK_START.md` để biết cấu trúc

### Q: Database có bao nhiêu entry?
**A:** **12,486 entries** từ 3 nguồn:
- Savina (1926): 7,879
- Shintani (2008): 4,445
- Clark (2000): 162

### Q: Làm sao để chạy web app?
**A:** 
```bash
cd web_ui
python app.py
# Mở http://127.0.0.1:5000 trong trình duyệt
```

### Q: Tôi có thể modify database không?
**A:** Có! Có 2 cách:
1. **UI**: Dùng modal Edit trong web interface
2. **CSV**: Export → Edit → Import CSV

### Q: Phonology gì? Tôi cần biết không?
**A:** Nếu bạn:
- Muốn bảo tồn ngôn ngữ → **PHẢI** đọc `PHONOLOGY_VI.md`
- Muốn dạy Kim Mun → **PHẢI** đọc `PHONOLOGY_VI.md`
- Chỉ làm kỹ thuật → Tùy chọn, nhưng hữu ích

### Q: Làm sao để push thay đổi?
**A:** Xem `GITHUB_NOTICE.md` - có 4 bước rõ ràng

---

## 🔐 An Toàn & Quy Tắc

⚠️ **IMPORTANT**: 
- ❌ KHÔNG được commit API keys hoặc passwords
- ❌ KHÔNG được push credentials
- ✅ PHẢI sử dụng git credentials manager hoặc SSH
- ✅ PHẢI write meaningful commit messages

---

## 📞 Hỗ Trợ

Nếu bạn gặp vấn đề:

1. Chạy `python startup_check.py` - nó sẽ bảo bạn vấn đề gì
2. Xem `QUICK_START.md` - phần Troubleshooting
3. Check `task.md` - xem có task nào chưa xong không

---

## 🎓 Học Thêm

### Về Ngôn Ngữ Kim Mun
- **PHONOLOGY_VI.md** - Phương hệ, thanh điệu, hệ chữ
- Các nguồn gốc:
  - Clark (2008) - Master's thesis chi tiết
  - Shintani (2008) - Từ điển phân loại
  - Savina (1926) - Tài liệu lịch sử

### Về Dự Án
- **task.md** - Roadmap & tiến độ
- **PAGE_REFERENCES_GUIDE.md** - Page reference system
- **QUICK_START.md** - Technical overview

---

## ✅ Checklist Khi Bắt Đầu

Khi bạn mới bắt đầu, hãy kiểm tra:

- [ ] Đã đọc `AI_PROMPT_INIT.md` chưa?
- [ ] Đã chạy `python startup_check.py` chưa? (Tất cả PASS?)
- [ ] Có thể truy cập GitHub không?
- [ ] Web server có chạy được không? (`python app.py`)
- [ ] Database có sẵn không? (12,486 entries?)

---

## 🚀 Tiếp Theo

**Bạn đã sẵn sàng!** Chọn một trong:

1. **Tiếp Tục Vision Extraction** (30% hoàn thành)
   - Cần Gemini API key mới
   - Extract Phonology pages (13-20)
   - Extract Topic 1 pages (21-34)

2. **Fine-Tune Page References**
   - Verify trang Savina qua PDF
   - Tinh chỉnh category ranges Shintani
   - Test Clark pages

3. **UI Improvements**
   - Mobile responsive design
   - Keyboard shortcuts
   - Dark/Light mode

4. **Performance Optimization**
   - Database indexing
   - Search caching
   - Lazy loading

---

**Good luck! Chúc bạn làm việc vui! 🎉**

*Last Updated: April 19, 2026*
