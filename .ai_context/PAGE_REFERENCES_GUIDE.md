# 📚 Hướng Dẫn Tham Chiếu Trang - Kim Mun Dictionary Hub

## ✅ Những Gì Đã Hoàn Thành

### 1. **Hệ Thống Tham Chiếu Trang Được Triển Khai**
- ✅ Tất cả **12.486 mục từ** giờ đều có **tham chiếu trang được ước tính** trong cơ sở dữ liệu
- ✅ Số trang được hiển thị trên mọi card và hàng bảng
- ✅ Định dạng: `📖 p.XX` trên card, `p.XX` trên bảng

### 2. **Logic Ước Tính Trang**

#### **Savina (1926)** - 13.139 mục từ
- Tổng số trang: ~262 trang (ước tính)
- Phương pháp: Sắp xếp tuần tự (~50 mục từ mỗi trang)
- Lưu ý: Đây là những ước tính sơ khai dựa trên mật độ

#### **Shintani (2008)** - 4.445 mục từ  
- Tổng số trang: ~630 trang (Từ Điển Funing)
- Phương pháp: Theo **phạm vi danh mục** (01-33 danh mục)
  - Danh mục 01 (Tự nhiên): trang 20-49
  - Danh mục 02 (Động vật): trang 50-80
  - Danh mục 03 (Thực vật): trang 81-110
  - ... v.v. (xem `create_page_mapping.py` để chi tiết)

#### **Clark (2000)** - 162 mục từ
- Tổng số trang: ~2 trang (bài báo nhỏ)
- Phương pháp: Chia tuần tự đơn giản

### 3. **Các File Được Tạo**

```
page_reference_mapping.json         ← JSON ánh xạ entry_id → trang
kim_mun_dict_with_pages.csv         ← Export với trang ước tính để review
create_page_mapping.py              ← Script đã tạo ánh xạ
update_db_pages.py                  ← Script đã update DB
export_for_page_review.py           ← Script để export để chỉnh sửa
```

---

## 🎯 Cách Sử Dụng & Chỉnh Sửa Trang

### **Phương Pháp 1: Review Trực Tuyến (Được Khuyến Nghị)**

1. **Mở Giao Diện Web**: http://127.0.0.1:5000
2. **Tìm Kiếm** các mục từ bạn muốn kiểm tra
3. **Xem Tham Chiếu Trang** được hiển thị trên mỗi card/hàng
4. **Nhấp Để Chỉnh Sửa** → Cập nhật trường `page_ref` → Lưu
5. Các thay đổi được **lưu ngay lập tức vào DB**

### **Phương Pháp 2: Review CSV Hàng Loạt**

1. **File**: `kim_mun_dict_with_pages.csv` (trong thư mục dự án)
2. **Mở trong Excel**:
   - Cột A: `entry_id`
   - Cột B: `source` (Savina, Shintani, Clark)
   - Cột C: `page_ref` (trang ước tính - có thể sai!)
   - ...dữ liệu khác...
   - **Cột J: `CORRECTED_PAGE`** ← Viết số trang chính xác ở đây

3. **Đánh Dấu Chỉnh Sửa**:
   ```
   entry_id    source        page_ref    ...    CORRECTED_PAGE
   SA-0001     Savina(1926)  p.1         ...    p.3
   011001      Shintani(2008) p.35       ...    p.28
   CL-001      Clark(2000)   p.1        ...    p.1
   ```

4. **Lưu** file Excel dưới dạng CSV

5. **Import Lại** qua Giao Diện Web:
   - Nút "⬆ Import" 
   - Chọn file CSV
   - Hệ thống tự động update DB

### **Phương Pháp 3: Kiểm Chéo PDF**

Nếu bạn muốn tự xác minh các trang:

**Cho Savina (1926)**:
- File: `D:\AGENT\KIMM_DOCS\befeo_0336-1519_1926_num_26_1_3091.pdf`
- Entry ID: SA-0001, SA-0002, ... v.v.
- Tìm kiếm theo entry_id trong PDF

**Cho Shintani (2008) - Từ Điển Funing**:
- File: `D:\AGENT\KIMM_DOCS\The-Mun-Language-of-Funing-CountyIts-Classified-Lexicon富寧金門語.pdf`
- Trang được sắp xếp theo danh mục (01-33)
- Entry ID mã hóa danh mục + chuỗi

**Cho Clark (2000)**:
- Bài báo ngắn, chỉ 2 trang
- Entry: CL-001 đến CL-207

---

## 📊 Trạng Thái Tham Chiếu Trang Hiện Tại

```
Tổng mục từ được ánh xạ:     12.486
├── Savina (1926):           7.879 mục từ   (ước tính)
├── Shintani (2008):         4.445 mục từ   (theo danh mục)
└── Clark (2000):            162 mục từ     (tuần tự)

Mức Độ Tự Tin:
├── Savina:             ⭐⭐⭐ Trung bình (mật độ thay đổi)
├── Shintani:           ⭐⭐⭐⭐ Cao (có cấu trúc theo danh mục)
└── Clark:              ⭐⭐⭐⭐⭐ Rất cao (chỉ 2 trang)
```

---

## 🔧 Nâng Cao: Điều Chỉnh Ánh Xạ Trang Thủ Công

Nếu bạn cần điều chỉnh **phạm vi trang danh mục** cho Shintani:

1. **Chỉnh sửa file**: `create_page_mapping.py`
2. **Tìm phần**: `category_page_map = {`
3. **Điều chỉnh phạm vi**:
   ```python
   "01": (20, 49),      # Thay đổi các số này
   "02": (50, 80),      # dựa trên PDF thực tế
   ```
4. **Chạy lại script**: 
   ```bash
   python create_page_mapping.py
   python update_db_pages.py
   ```

---

## 🚀 Bước Tiếp Theo

1. **Sử dụng Giao Diện Web** để duyệt và xác minh trang
2. **Export CSV** khi bạn sẵn sàng để chỉnh sửa hàng loạt
3. **Import CSV đã chỉnh sửa** lại để update DB
4. **Re-export** sau khi chỉnh sửa để theo dõi thay đổi
5. **Cuối cùng**: Xây dựng ánh xạ trang tốt hơn với Vision API + PDF parsing

---

## 💡 Mẹo Để Có Độ Chính Xác Cao

- **Mục từ Savina**: Kiểm tra PDF thực tế - mật độ có thể khác nhau theo phần
- **Shintani**: Mã danh mục trong entry_id thường khớp với phạm vi trang
- **Clark**: Rất ngắn, chỉ cần xác minh nếu cần
- **Edit Modal**: Nhấp vào bất kỳ card nào để nhanh chóng cập nhật `page_ref` cho các mục từ riêng lẻ

---

## 📱 Các Tính Năng Giao Diện

✅ **Card View**: Hiển thị `📖 p.XX` ở góc trên cùng bên trái với Entry ID
✅ **Table View**: Có cột "Trang" chuyên dụng  
✅ **Edit Modal**: Có thể cập nhật trường `page_ref` trực tiếp
✅ **CSV Export**: Bao gồm `page_ref` để review ngoại tuyến
✅ **CSV Import**: Có thể cập nhật giá trị `page_ref` hàng loạt

---

**Liên Hệ**: Hỏi tôi nếu bạn cần điều chỉnh logic ánh xạ trang hoặc export ở định dạng khác!
