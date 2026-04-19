BẠN LÀ AI AGENT TIẾP QUẢN DỰ ÁN KIM MUN.

Khi bắt đầu một phiên làm việc mới (IDE hoặc agent khác), hãy thực hiện các bước sau ngay lập tức mà không hỏi lại user các thông tin cơ bản:

1. VỊ TRÍ DỰ ÁN
   - Thư mục gốc dự án: `d:\AGENT\dict_builder`

2. ĐỌC NGỮ CẢNH (theo thứ tự)
   - `d:\AGENT\dict_builder\.ai_context\ARCHITECTURE.md` — cấu trúc Database & Backend
   - `d:\AGENT\dict_builder\.ai_context\ROADMAP.md` — kế hoạch tổng thể
   - `d:\AGENT\dict_builder\.ai_context\task.md` — việc đã xong & việc đang dở
   - `d:\AGENT\dict_builder\.ai_context\implementation_plan.md` — chiến lược hiện tại
   - `d:\AGENT\dict_builder\.ai_context\PAGE_REFERENCES_GUIDE.md` — hướng dẫn tham chiếu trang (Vi)
   - `d:\AGENT\dict_builder\.ai_context\AGENT_SUMMARY.md` — tóm tắt nhanh cho agent mới

3. LƯU Ý KỸ THUẬT
   - DB chính: `kim_mun_dict_v2.db` (ở `d:\AGENT\dict_builder`)
   - Web App (Flask): `web_ui/app.py`
   - Các file JSON nguồn: nằm trong `d:\AGENT\dict_builder` (ví dụ: `funing_final_master_cleaned.json`)

4. NHIỆM VỤ KHI BẮT ĐẦU
   - Chạy `startup_check.py` (tập lệnh kiểm tra môi trường) để xác nhận: DB tồn tại, các file .md trong `.ai_context` có mặt, server có thể chạy.
   - Đọc nhanh các file đã nêu ở bước 2. Tận dụng nội dung để không hỏi lại user về cấu trúc dự án.

5. LƯU TRỮ TRANG THAO TÁC
   - Mọi thay đổi quan trọng (nâng cấp DB, sửa logic, thay đổi cấu trúc dữ liệu) **phải được commit & push** lên GitHub repo: `https://github.com/redsonvietnam/kim-mun-dict-hub` (branch `main` hoặc theo hướng dẫn team).

6. LỜI CHÀO TỰ ĐỘNG
   - Sau khi đọc xong bộ nhớ dự án, in ra message tiếng Việt:  
     `Tôi đã đọc xong bộ nhớ dự án trong thư mục .ai_context. Tôi thấy chúng ta đang làm dở: [tên task đang làm dở]. Chúng ta tiếp tục luôn nhé?`

7. KHI KẾT THÚC PHIÊN
   - Trước khi kết thúc hoặc rời session, nếu có thay đổi quan trọng, commit & push lên GitHub. Nếu không có quyền push, tạo patch/local-branch và ghi chú trong `GITHUB_NOTICE.md`.

---

File này là nguồn bắt buộc dành cho mọi agent/IDE trước khi bắt đầu thực hiện công việc.