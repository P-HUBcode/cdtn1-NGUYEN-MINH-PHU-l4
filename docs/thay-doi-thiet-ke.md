# NHẬT KÝ THAY ĐỔI THIẾT KẾ (DESIGN CHANGE LOG)

**Tên học phần:** Chuyên đề tốt nghiệp 1 (HK261)  
**Sinh viên thực hiện:** Nguyễn Minh Phú - MSSV: 2374802013447  
**Track:** SE (Software Engineering) | **Luồng:** L4 - Phân công kỹ thuật viên và lịch hẹn  

---

## Sau phản hồi Bài tập 1 (Buổi 8, ngày 15/10/2026)

### TD-01: Bổ sung hình ảnh sơ đồ và wireframe trực tiếp vào bản tài liệu PDF
- **Phản hồi của GV:** File PDF không có hình nào: thiếu Use Case Diagram, sơ đồ kiến trúc, ERD và wireframe 3 màn hình (mục 2.1, 3.1, 4.1, 5 chỉ có chữ). Sơ đồ phải dán vào PDF, không chỉ để trong repo. Trang 14 bị trắng.
- **Quyết định:** SỬA
- **Lý do:** Bản nộp PDF là tài liệu chính để chấm bài và lưu trữ hồ sơ, việc chỉ dẫn link file `.drawio` khiến người đọc không thể theo dõi trực quan các mô hình thiết kế độc lập.
- **Ảnh hưởng:** 
  - Xuất ảnh PNG độ phân giải cao cho: Use Case Diagram, Sơ đồ Kiến trúc 4 lớp, Mô hình ERD chuẩn 3NF, Wireframe 3 màn hình (M1, M2, M3).
  - Chèn trực tiếp ảnh vào các mục tương ứng trong file Word và xuất lại file PDF chuẩn, loại bỏ hoàn toàn các trang trắng.

---

### TD-02: Bổ sung khung chú thích ký hiệu (Legend) vào file sơ đồ gốc
- **Phản hồi của GV:** `usecase.drawio` và `erd.drawio` không có chú thích ký hiệu.
- **Quyết định:** SỬA
- **Lý do:** Tiêu chí kỹ thuật bắt buộc mọi sơ đồ phải đọc được độc lập mà không cần tác giả giải thích thêm; thiếu chú thích khiến người xem khó phân biệt ranh giới hệ thống, quan hệ `<<include>>`, `<<extend>>` và các ký hiệu quan hệ thực thể.
- **Ảnh hưởng:** Cập nhật file `docs/usecase.drawio` và `docs/erd.drawio`, bổ sung bảng chú giải ký hiệu (Actor, System boundary, Include/Extend, Primary Key, Foreign Key, Cardinality 1:N, Composite Index).

---

### TD-03: Rút gọn danh sách User Story về phạm vi 5–7 story
- **Phản hồi của GV:** Có 8 User Story, đề yêu cầu 5–7.
- **Quyết định:** SỬA
- **Lý do:** Tuân thủ chặt chẽ yêu cầu phạm vi của đề bài (tối đa 7 User Story) nhằm tập trung vào các chức năng cốt lõi của prototype cá nhân, tránh mở rộng phân tán.
- **Ảnh hưởng:** 
  - Gộp US3 (Đặt lịch hẹn giao - nhận máy) và US8 (Cập nhật và dời lịch hẹn) thành một User Story duy nhất: **US3 - Đặt và quản lý lịch hẹn giao – nhận máy với khách hàng**.
  - Tổng số User Story giảm từ 8 xuống đúng **7 User Story** (gồm 5 MUST và 2 SHOULD).
  - Cập nhật lại Bảng User Story ở Mục 1.6 và Bảng truy vết ma trận Mục 1.9 trong `docs/srs.md` và file báo cáo.

---

### TD-04: Đồng bộ số bước giữa Luồng chính và Luồng ngoại lệ của Use Case UC2
- **Phản hồi của GV:** Luồng ngoại lệ 9a của UC2 tham chiếu bước 9, nhưng luồng chính chỉ có 7 bước.
- **Quyết định:** SỬA
- **Lý do:** Lỗi không nhất quán giữa bản nháp phân tích chi tiết (9 bước) và bản rút gọn đưa vào bảng Word (7 bước), gây sai lệch trong truy vết kiểm thử (Traceability).
- **Ảnh hưởng:** 
  - Chuẩn hóa lại bảng Luồng chính của UC2 (Gợi ý và phân công KTV) gồm đủ **9 bước tuần tự**:
    1. Quản lý chọn phiếu bảo hành chờ phân công.
    2. Quản lý nhấn "Gợi ý KTV phù hợp".
    3. Hệ thống xác định nhóm sự cố và trung tâm tiếp nhận.
    4. Hệ thống truy vấn KTV cùng trung tâm có `proficiency >= 3`.
    5. Hệ thống tính số phiếu đang xử lý của từng KTV.
    6. Hệ thống hiển thị danh sách KTV gợi ý xếp tăng dần theo tải.
    7. Quản lý chọn 1 KTV phù hợp.
    8. Hệ thống tính hạn cam kết SLA `due_date` theo quy tắc QT-04.
    9. Quản lý bấm "Xác nhận phân công", hệ thống lưu CSDL và ghi log lịch sử.
  - Các luồng ngoại lệ: `4a` (Không tìm thấy KTV đạt tay nghề), `7a` (KTV được chọn bị quá tải > 10 phiếu), `9a` (Lỗi kết nối CSDL khi lưu) khớp chính xác 100% với các bước của luồng chính.

---

### TD-05: Bổ sung bảng thực thể `customers` và liên kết khóa ngoại với `tickets`
- **Phản hồi của GV:** `tickets.customer_id` không nối tới bảng nào; wireframe M2 hiện tên và SĐT khách nhưng ERD không có cột này.
- **Quyết định:** SỬA
- **Lý do:** Thiết kế ban đầu thiếu bảng `customers`, dẫn đến việc trường `tickets.customer_id` bị cô lập (vi phạm nguyên tắc toàn vẹn khóa ngoại) và không khớp dữ liệu hiển thị thông tin khách hàng trên màn hình giao diện M1/M2.
- **Ảnh hưởng:**
  - Bổ sung bảng `customers` vào DDL và ERD gồm các thuộc tính: `customer_id` (PK), `customer_code` (UNIQUE), `full_name`, `phone` (UNIQUE), `address`, `created_at`.
  - Thiết lập ràng buộc khóa ngoại: `tickets.customer_id REFERENCES customers(customer_id) ON DELETE RESTRICT`.
  - Cập nhật sơ đồ `docs/erd.drawio` và file mã nguồn `db/schema.sql`.

---

### TD-06: Bổ sung đầy đủ thông tin định danh vào Dòng cam kết Liêm chính AI
- **Phản hồi của GV:** Dòng cam kết AI thiếu họ tên, MSSV, ngày.
- **Quyết định:** SỬA
- **Lý do:** Đáp ứng quy chuẩn liêm chính học thuật bắt buộc của Trường ĐH Văn Lang theo hướng dẫn của Buổi 1 và Đề bài BT1.
- **Ảnh hưởng:** Bổ sung rõ ràng ở cuối Bảng khai báo AI trong mọi tài liệu:  
  *“Tôi xác nhận đã đọc, hiểu và chịu trách nhiệm về toàn bộ nội dung nộp.  
  Họ và tên: Nguyễn Minh Phú | MSSV: 2374802013447 | Ngày nộp: 15/10/2026”*.

---

### TD-07: Chuẩn hóa cấu trúc Repository Git và quy ước Commit
- **Phản hồi của GV:** Repo: tài liệu nằm lồng trong `bai-tap-1-buoi6/`, thiếu `.gitignore`, `.env.example`, README gần như trống; commit toàn "Add files via upload".
- **Quyết định:** SỬA
- **Lý do:** Việc upload thủ công bằng web làm mất cấu trúc chuẩn của dự án, vi phạm tiêu chí đánh giá quy trình làm việc chuyên nghiệp (CLO6) của học phần.
- **Ảnh hưởng:**
  - Đưa toàn bộ nội dung ra thư mục gốc repo: `docs/`, `src/`, `db/`, `tests/`.
  - Thêm file `.gitignore` loại bỏ `node_modules/`, `*.log`, `.env`, `__pycache__/`.
  - Thêm file `.env.example` cấu hình cổng `PORT` và chuỗi kết nối `DATABASE_URL`.
  - Viết lại `README.md` đầy đủ Mục 2 (Yêu cầu môi trường & hướng dẫn chạy) và Mục 6 (Trạng thái hiện tại Sprint 1).
  - Áp dụng lệnh Git dòng lệnh với quy ước Conventional Commits (`docs: ...`, `chore: ...`, `feat: ...`).
