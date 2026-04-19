TÓM TẮT NHANH CHO AGENT MỚI

Mục đích: cung cấp overview ngắn, các bước nhanh để bắt đầu và các file cần đọc.

1) Các file quan trọng trong `.ai_context/` (đọc theo thứ tự):
   - `ARCHITECTURE.md` — cấu trúc DB và backend
   - `ROADMAP.md` — kế hoạch dự án
   - `task.md` — việc đã làm / đang làm dở
   - `implementation_plan.md` — kế hoạch triển khai
   - `PAGE_REFERENCES_GUIDE.md` — (Vi) hướng dẫn tham chiếu trang
   - `AI_PROMPT_INIT.md` — hướng dẫn cho agent (bắt buộc)

2) Lệnh khởi tạo nhanh (PowerShell) - thực hiện trong `d:\AGENT\dict_builder`:

```powershell
# Chạy kiểm tra khởi động
python startup_check.py

# Khởi chạy web UI (dev)
cd web_ui; python app.py
```

3) Kiểm tra nhanh khi bắt đầu
   - DB: `kim_mun_dict_v2.db` có tồn tại?
   - Web UI: `web_ui/app.py` có thể start?
   - Mapping trang: `page_reference_mapping.json` có sẵn?

4) Quy trình thay đổi quan trọng
   - Luôn commit thay đổi cục bộ với message rõ ràng
   - Push lên GitHub repo: `https://github.com/redsonvietnam/kim-mun-dict-hub`
   - Nếu thay đổi ảnh hưởng DB, tạo migration note (file `migrations/` nếu cần) và backup DB

5) Nếu bạn là agent khác hoặc IDE mới: đọc các file trên, chạy `startup_check.py`, và tiếp tục công việc.

---

Ghi chú: file này nhằm giúp các phiên làm việc khác nhau (agents/IDE) nối tiếp nhau mượt mà.