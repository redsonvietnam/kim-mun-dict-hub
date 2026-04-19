# Kế hoạch: Xây dựng Trung tâm Học thuật & Nâng cấp Giao diện Hệ thống

Dựa trên yêu cầu của bạn, chúng ta sẽ biến KIMM HUB thành một công cụ nghiên cứu thực thụ. Kế hoạch này tập trung vào 3 trụ cột: Phân tích Âm vị học, Linh hoạt hiển thị và Công cụ dữ liệu.

## 1. Trung tâm Học thuật (Academic Hub)
Chúng ta sẽ tích hợp các phát hiện từ Shintani (2008) về cấu trúc âm tiết tiếng Mun.
- **Nội dung:**
  - Cấu trúc âm tiết: `C1V(C2) / T`.
  - Bảng hệ thống Phụ âm đầu (pj, bj, θ, ð...), Nguyên âm và 7 Thanh điệu.
  - So sánh sơ lược với hệ thống của Savina (nếu có thể).
- **Giao diện:** Thêm một tab hoặc nút "Học thuật" mở ra một Modal (cửa sổ nổi) hoặc Drawer (ngăn kéo) chứa các phân tích này dưới dạng Markdown trình bày đẹp mắt.

## 2. Linh hoạt hiển thị (View Toggle)
Bổ sung khả năng chuyển đổi giữa Card View (hiện tại) và Table View (dạng bảng nghiên cứu).
- **Tính năng:**
  - Nút chuyển đổi tại Header.
  - **Table View:** Hiển thị dữ liệu cô đọng hơn, cho phép cuộn xem nhanh hàng trăm từ cùng lúc.
  - Các cột: ID, Hán tự, Pinyin, IPA Dạo, Tiếng Việt, Nguồn.

## 3. Công cụ Dữ liệu (CSV Import/Export)
Giúp bạn làm chủ dữ liệu OCR và sửa lỗi nhanh chóng.
- **Export:** Cho phép tải xuống bộ lọc hiện tại (ví dụ: tất cả từ Funing Topic 1) dưới dạng file CSV.
- **Import:** Bạn có thể sửa file CSV này (bằng Excel) và tải ngược lên để cập nhật Database.

---

## Các thay đổi dự kiến

### [Component] Backend (Flask)
#### [MODIFY] [app.py](file:///d:/AGENT/dict_builder/web_ui/app.py)
- Thêm endpoint `/export_csv` để sinh file CSV từ query search.
- Thêm endpoint `/import_csv` (POST) để nhận file và update DB (sử dụng `entry_id` làm khóa).
- Thêm endpoint `/phonology` để trả về nội dung Markdown nghiên cứu.

### [Component] Frontend (HTML/CSS/JS)
#### [MODIFY] [index.html](file:///d:/AGENT/dict_builder/web_ui/templates/index.html)
- **CSS:** Thêm style cho `.data-table` và các hiệu ứng chuyển đổi View.
- **HTML:** 
  - Thêm nút "View Mode: Card/Table" vào header-bar.
  - Thêm nút "Học thuật" và "Export CSV".
  - Thêm Modal popup cho Academic Hub.
- **JS:** 
  - Viết logic render bảng (`renderTableMode`).
  - Viết logic gửi yêu cầu Export/Import.

---

## Open Questions
> [!IMPORTANT]
> 1. **Vị trí Academic Hub:** Bạn muốn phần phân tích Âm vị học hiện ra như một **Trang mới** hay một **Cửa sổ Modal** khi nhấn nút?
> 2. **Cấu trúc Table:** Ngoài các cột cơ bản (Hán, Pinyin, Dạo, Việt, Nguồn), bạn có muốn hiển thị thêm cột **Nghĩa tiếng Pháp** hay **Số trang PDF** không?
> 3. **Import CSV:** Bạn có muốn hệ thống tự động lưu bản backup dữ liệu cũ trước khi thực hiện "Ghi đè" từ file CSV không?

## Kế hoạch Xác minh
- Kiểm thử tính năng chuyển View xem có bị nhảy layout không.
- Xuất thử 1 file CSV, sửa 1 từ và Import lại để xem Database có cập nhật đúng không.
- Kiểm tra hiển thị các ký tự đặc biệt (IPA, Hán tự) trên dạng bảng.
