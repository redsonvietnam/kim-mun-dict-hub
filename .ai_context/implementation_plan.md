# Roadmap Dự án Từ điển Kim Mun (Giai đoạn Kế tiếp)

Dưới đây là lộ trình tiếp theo, bao gồm cả hệ thống "sang số" chuyển giao trí nhớ (AI Handover) để giải quyết dứt điểm vấn đề giới hạn API của bạn.

## 0. Chuyển Giao Trí Nhớ (AI Handover System) ⭐ MỚI
**Vấn đề:** Đổi/hết tài khoản API, nhảy sang VS Code dùng Copilot dẫn đến việc AI mới bị "mất trí nhớ", không biết dự án đang làm tới đâu, quy chuẩn ra sao.
**Giải pháp:** Đóng gói toàn bộ trí nhớ của AI vào chính bên trong cấp thư mục dự án (không lưu ở thư mục cục bộ của app).
**Kế hoạch thực thi:**
- Khởi tạo cấu trúc file `.ai_context/` ngay trong `d:\AGENT\dict_builder`.
- Bao gồm các file: 
  - `ARCHITECTURE.md` (Ghi rõ cấu trúc DB, code frontend Flask chạy sao, script ingest hoạt động thế nào).
  - `ROADMAP.md` (Nhật ký các mốc đã xong và việc cần làm).
  - `PROMPT_INIT.txt` (Kịch bản mồi). Khi bạn sang một Account mới hay bật VS Code, bạn chỉ cần ném cái file này vào bảo: "Đọc file kia rồi làm tiếp" là AI mới sẽ bắt nhịp được 100%.

## 1. Lưu trữ & Phiên bản hóa (Backup & Version Control)
- Khởi tạo Git Repo (`git init`).
- Đẩy source code (Flask App, Logic Script, Mẫu dữ liệu) lên một **GitHub** (kết hợp với nhánh 0 ở trên, Github sẽ giữ luôn trí nhớ của AI).

## 2. Tổng hợp Phân tích Ngôn ngữ (Linguistic Synthesis)
- Sử dụng AI để tổng hợp tài liệu Âm vị học của **Shintani (Funing)**, hệ thống phiên âm tiếng Pháp cổ của **Savina**, ngữ pháp **Clark**.
- Xây dựng Hub "Tài liệu học thuật" chuyên sâu ngay trên giao diện Web.

## 3. Cải tiến Trải nghiệm Giao diện (Thị giác & Tương tác)
- Bổ sung nút Toggle chuyển đổi thiết kế hiển thị giữa **Dạng Thẻ (Card View)** và **Dạng Bảng (Table View)**.
- Phân trang (Pagination) hoặc Cuộn Vô Cực (Infinite Scroll) để tải mượt hơn.

## 4. Công cụ Hiệu đính Thủ công (Fix OCR Workflow)
- Tính năng Export CSV.
- Tính năng Import & Merge từ CSV, xử lý cơ chế map id đè dữ liệu.

---

> [!IMPORTANT]
> Với hoàn cảnh của bạn, **Bước 0 & Bước 1 (AI Handover + Github)** trở nên cực kỳ cấp bách! Nếu đồng ý, tôi sẽ tạo luôn bộ nhớ lưu trữ đó ngay bây giờ và thực hiện Git Init ngay lập tức cho bạn nhé!
