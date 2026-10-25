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

---

## Trong Sprint 2 (Buổi 10, ngày 22/10/2026)

### TD-08: Tích hợp Frontend 3 màn hình, bao đóng DataState, tách API Client và mở rộng bộ Unit Tests
- **Yêu cầu Buổi 10:** Hiện thực Frontend 3 màn hình gọi API thật; tách riêng `client.js` và `ticket.api.js`; bọc 3 trạng thái dữ liệu (đang tải, rỗng, lỗi kèm thử lại); bắt mã lỗi 401; viết $\ge 5$ unit tests cho lớp nghiệp vụ và chạy toàn luồng end-to-end không lỗi treo.
- **Quyết định:** HOÀN THIỆN TOÀN DIỆN
- **Lý do:** Đáp ứng 10 mục kiểm chứng cốt lõi của Buổi 10 (Sprint 2 - Track SE), chuyển đổi từ prototype backend sang hệ thống phần mềm hoàn chỉnh chạy được cục bộ, phục vụ người dùng trải nghiệm thực tế và peer review theo README.
- **Ảnh hưởng:**
  - Xây dựng thư mục `src/public/` chứa giao diện 3 màn hình M1 (Danh sách chờ & Tải KTV), M2 (Chi tiết & Phân công / Re-assign), M3 (Đặt & Dời lịch hẹn).
  - Tách riêng `src/api/client.js` và `src/api/ticket.api.js` đóng gói toàn bộ HTTP calls và token; loại bỏ 100% lệnh `fetch(` trong mã giao diện người dùng.
  - Xây dựng thành phần `DataState.js` xử lý chuẩn mực 3 trạng thái: Đang tải (Spinner), Danh sách rỗng, Lỗi kết nối (kèm nút "Thử lại ngay").
  - Cài đặt nút "Thử mã 401" kiểm chứng cơ chế tự động xóa token và chuyển về modal đăng nhập khi nhận lỗi 401 Unauthorized.
  - Viết bộ 17 Unit Tests tự động trong `tests/ticket.service.test.js` kiểm chứng toàn diện 5 quy tắc nghiệp vụ: SLA `due_date` (QT-04), KTV cùng trung tâm (QT-06), tay nghề $\ge 3$ (QT-07), lý do chuyển gán $\ge 10$ ký tự (QT-08), tải khung giờ 30p tối đa 5 lịch hẹn (QT-09).
  - Tạo script kiểm thử toàn luồng `tests/test_end_to_end.js` và chụp ảnh minh chứng lưu tại `docs/screenshots/buoi10_unit_tests.png` và `docs/screenshots/buoi10_e2e_result.png`.
  - Cập nhật Mục 3 README hướng dẫn từng bước chi tiết (mỗi bước 1 lệnh) đã được kiểm chứng bằng việc clone thử sang thư mục mới.

---

## Tích hợp Hệ thống & Đóng gói Container (Buổi 11 & 12, ngày 26/10/2026)

### TD-09: Hệ thống Logging có cấu trúc (Structured Logging) & Xử lý lỗi xuyên lớp (Centralized Error Handler)
- **Yêu cầu Buổi 11 (Slide 19–26):**
  - Logging có cấu trúc: 4 mức log (`DEBUG`, `INFO`, `WARN`, `ERROR`), 3 thành phần bắt buộc (thời điểm ISO, ngữ cảnh requestId/IDs, mô tả hành vi).
  - Khử độc dữ liệu (Data Redaction): Tuyệt đối không log password, token, SĐT, PII. Ghi ID thay vì dữ liệu cá nhân.
  - Xử lý lỗi xuyên lớp: Repository bắt lỗi SQL bọc `LoiTruyCapDuLieu` (503); Service ném `LoiNghiepVu` (400, 404, 409) có mã máy đọc `ma`; Controller chuyển `next(err)`; Middleware lỗi duy nhất ghi log 1 lần và trả format JSON chuẩn `{ error, message, requestId }`.
  - Áp dụng `toTicketView()` bảo toàn Data Contract, xử lý triệt để bug thiếu/null dữ liệu (BUG-004).
- **Quyết định:** HOÀN THIỆN TOÀN DIỆN
- **Lý do:** Loại bỏ các lỗi ngẫu hứng `catch (e) {}` hoặc `console.log()` rải rác; nâng cao năng lực quan sát hệ thống (Observability); che giấu chi tiết kỹ thuật nội bộ (`err.stack`, câu truy vấn SQL) với người dùng cuối; chuẩn hóa Bug Log có hệ thống theo 4 bước.
- **Ảnh hưởng:**
  - Tạo `src/errors.js` định nghĩa phân cấp lỗi `LoiNghiepVu` và `LoiTruyCapDuLieu`.
  - Tạo `src/utils/logger.js` cấu hình Structured JSON logger ra stdout, tích hợp bộ khử độc tự động che giấu `password`, `token`, `phone`, `so_dien_thoai`.
  - Tạo `src/middleware/requestId.js` tự động cấp phát `requestId` cho mỗi HTTP request.
  - Tạo `src/middleware/errorHandler.js` ghi log tập trung và chuẩn hóa phản hồi lỗi.
  - Cập nhật `src/services/ticketService.js` với `toTicketView()` và ném lỗi có mã chuẩn; cập nhật `src/repositories/ticketRepository.js` bọc lỗi kỹ thuật.
  - Bổ sung tài liệu `docs/bug-log.md` ghi nhận 4 bug chuẩn 7 dòng (`BUG-001` đến `BUG-004`).
  - Mở rộng bộ Unit Tests từ 17 lên **22 Unit Tests PASS 100%** (bổ sung nhóm Regression Tests bảo vệ các bug trong Bug Log).

---

### TD-10: Đóng gói và chuẩn hóa môi trường triển khai bằng Docker & Docker Compose
- **Yêu cầu Buổi 11 & 12 (Slide 27–36):**
  - Đóng gói toàn bộ ứng dụng và runtime Node.js 20 LTS vào Docker container, đảm bảo nguyên tắc TÁI LẬP ĐƯỢC từ máy chưa cài đặt môi trường.
  - Sử dụng Dockerfile tối ưu hóa lớp bộ nhớ đệm (Layer Caching) bằng cách sao chép tệp khóa phiên bản và cài đặt bằng `npm ci --omit=dev` trước khi sao chép mã nguồn.
  - Cấu hình file `.dockerignore` bảo mật; cấu hình `docker-compose.yml` có Volume mount bảo lưu dữ liệu CSDL SQLite và cơ chế Healthcheck tự động.
- **Quyết định:** HOÀN THIỆN TOÀN DIỆN
- **Lý do:** Ngăn chặn triệt để 5 nguồn sai lệch môi trường (thư viện, runtime, biến môi trường, dữ liệu cục bộ, cổng mạng). Cho phép giảng viên và đồng môn dựng lại toàn bộ ứng dụng chỉ bằng $\le 2$ lệnh: `cp .env.example .env` và `docker compose up --build`.
- **Ảnh hưởng:**
  - Tạo file `Dockerfile` sử dụng base image `node:20-alpine`, tích hợp lệnh HEALTHCHECK thăm dò endpoint `/api` mỗi 20 giây.
  - Tạo file `.dockerignore` ngăn chặn đưa `node_modules`, `.git`, `.env` vào image Docker.
  - Tạo file `docker-compose.yml` ánh xạ cổng `${PORT:-3000}:3000`, volume mount `./db:/app/db`, thiết lập chính sách khởi động lại `restart: unless-stopped`.
  - Cập nhật tài liệu `README.md` Mục 2 và Mục 3 bổ sung hướng dẫn chạy hệ thống bằng Docker Compose song song với chạy qua Node.js truyền thống.
