# BÁO CÁO THỰC HÀNH BUỔI 11: TÍCH HỢP HỆ THỐNG VÀ XỬ LÝ LỖI XUYÊN LỚP
**Môn học:** Chuyên đề tốt nghiệp 1 (232_71ITBS40103_01 — HK261)  
**Trường Đại học Văn Lang — Khoa Công nghệ Thông tin**  
**Sinh viên thực hiện:** Nguyễn Minh Phú — MSSV: 2374802013447  
**Chuyên ngành (Track):** Kỹ thuật phần mềm (Software Engineering - SE)  
**Luồng nghiệp vụ:** L4 — Phân công kỹ thuật viên và lịch hẹn bảo hành (Smart CRM Mekong Mobile)  
**Repository GitHub:** [https://github.com/P-HUBcode/cdtn1-NGUYEN-MINH-PHU-l4](https://github.com/P-HUBcode/cdtn1-NGUYEN-MINH-PHU-l4) (Tag `v0.2`)  
**Ngày thực hiện:** 26/10/2026  

---

## 1. TỔNG QUAN NỘI DUNG VÀ MỤC TIÊU BUỔI 11

Theo đề cương và tài liệu bài giảng Buổi 11 (*"Tích hợp hệ thống và Xử lý lỗi"*), đây là buổi học lý thuyết và hoàn thiện kỹ thuật cuối cùng trước khi bước vào buổi Workshop đánh giá trực tiếp (Buổi 12). Mục tiêu cốt lõi của buổi học là giải quyết vấn đề muôn thuở trong phát triển phần mềm: **"Trên máy em chạy được nhưng máy người khác không chạy được"** và chuyển đổi ứng dụng từ prototype cục bộ thành một hệ thống có tính ổn định cao, có thể quan sát (Observability), tự gỡ lỗi có phương pháp và tái lập được từ máy sạch.

### Các mục tiêu cụ thể đã đạt được:
1. **Quản lý phụ thuộc và khóa phiên bản:** Loại bỏ 5 nguồn sai lệch môi trường, cam kết `package-lock.json` và quy chuẩn cài đặt bằng `npm ci`.
2. **Debug có hệ thống theo 4 bước:** Xây dựng tài liệu `docs/bug-log.md` ghi nhận 5 lỗi thực tế (`BUG-001` đến `BUG-005`) theo mẫu chuẩn 7 dòng, mỗi lỗi được xác nhận bằng một Unit Test hồi quy.
3. **Logging có cấu trúc & Khử độc dữ liệu (Data Redaction):** Hiện thực logger JSON ra `stdout` có cấp phát `requestId`, tự động che giấu mật khẩu, token và số điện thoại khách hàng (QT-15).
4. **Xử lý lỗi tập trung xuyên lớp (Centralized Error Handler):** Xóa bỏ các lệnh bắt lỗi ngẫu hứng rải rác; phân biệt rành mạch giữa `LoiNghiepVu` và `LoiTruyCapDuLieu`.
5. **Đóng gói Docker & Docker Compose:** Cấu hình Dockerfile tối ưu Layer Caching và docker-compose có volume mount bảo lưu CSDL SQLite.
6. **Mở rộng bộ kiểm thử:** Đạt **36/36 Unit Tests PASS 100%** (bao gồm 8 test cases chuyên biệt cho FR6/US5 kiểm chứng KTV cập nhật tiến độ) và kịch bản End-to-End 9 bước toàn luồng chạy thành công trơn tru, sẵn sàng cho buổi Workshop đánh giá tại Buổi 12.

---

## 2. PHẦN 1: QUẢN LÝ PHỤ THUỘC VÀ TÍNH TÁI LẬP (REPRODUCIBILITY)

### 2.1. Nhận diện 5 nguồn khác biệt môi trường (Slide 6–7)
Khi đưa sản phẩm từ máy cá nhân của sinh viên sang máy của Giảng viên chấm bài, hệ thống dễ phát sinh lỗi do:
1. **Khác biệt phiên bản thư viện con (Transitive Dependencies):** Khi dùng `npm install`, các gói thư viện có dấu mũ (`^`) sẽ tự tải phiên bản mới nhất, dẫn đến xung đột API.
2. **Khác biệt Runtime Node.js:** Các hàm mới của `node:sqlite` hoặc `node:test` chỉ chạy chuẩn xác từ Node.js v20 LTS trở lên.
3. **Thiếu biến môi trường:** Máy người chấm chưa có file `.env`, nếu không có `.env.example` và fallback mặc định thì server sẽ sập ngay lúc khởi động.
4. **Dữ liệu cục bộ bị cô lập:** CSDL SQLite nằm ở đường dẫn cố định tuyệt đối hoặc thiếu seed data khiến bảng rỗng.
5. **Xung đột cổng mạng (Port collision):** Cổng 3000 bị chiếm dụng nếu không cho phép ghi đè qua biến môi trường `PORT`.

### 2.2. Giải pháp kỹ thuật đã áp dụng
* **Khóa phiên bản bằng `package-lock.json`:** Xóa bỏ `package-lock.json` khỏi `.gitignore`. Toàn bộ 67 gói phụ thuộc cùng mã băm toàn vẹn (integrity hash) được commit cố định vào Git repository.
* **Quy ước cài đặt bằng `npm ci`:** Thay thế hoàn toàn `npm install` bằng `npm ci` trong hướng dẫn `README.md`. Lệnh này xóa sạch `node_modules` và cài đặt chính xác từng byte theo lockfile, không bao giờ tự ý nâng cấp phiên bản.
* **Tính Idempotent của CSDL (Tiêu chí C5):** Tệp `db/init_db.js` và `db/schema.sql` sử dụng câu lệnh `CREATE TABLE IF NOT EXISTS` và `INSERT OR IGNORE`. Khi chạy lại lần thứ hai hoặc nhiều lần, hệ thống không bị lỗi trùng khóa chính và không nhân đôi dữ liệu.

---

## 3. PHẦN 2: DEBUG CÓ HỆ THỐNG VÀ NHẬT KÝ LỖI (BUG LOG)

### 3.1. Quy trình 4 bước chuẩn (Slide 12–16)
Thay vì "thử sai ngẫu hứng" (trial-and-error) hoặc "chỉ sửa triệu chứng bên ngoài", toàn bộ các lỗi phát sinh trong quá trình tích hợp Luồng L4 đều được xử lý theo 4 bước:
1. **Bước 1 — Tái lập (Reproduce):** Viết một đoạn mã kiểm thử hoặc kịch bản gọi API tối thiểu gây ra lỗi một cách tất định (100% tái hiện).
2. **Bước 2 — Khoanh vùng (Isolate):** Đặt breakpoint hoặc đọc log có `requestId` để xác định chính xác dòng mã, hàm, và tầng kiến trúc gây lỗi.
3. **Bước 3 — Sửa nguyên nhân (Fix Root Cause):** Sửa tận gốc tại tầng chịu trách nhiệm (không vá tạm ở tầng khác).
4. **Bước 4 — Xác nhận (Verify):** Chạy lại test case ở Bước 1 để chứng minh lỗi đã biến mất và bổ sung test này vào bộ Unit Tests hồi quy (`Regression Tests`) để lỗi vĩnh viễn không quay lại.

### 3.2. Bảng tổng hợp 5 lỗi thực tế trong `docs/bug-log.md` (Slide 18)

| Mã lỗi | Triệu chứng & Ranh giới | Nguyên nhân cốt lõi | Cách sửa tận gốc & Test xác nhận |
| :---: | :--- | :--- | :--- |
| **BUG-001** | Quản lý nhập lý do chuyển gán 4 ký tự `"bận"` nhưng hệ thống vẫn cho phép đổi KTV | Service chỉ kiểm tra `if (!reason)` mà quên ràng buộc độ dài tối thiểu của quy tắc QT-08 | Bổ sung hàm `validateReassignReason(reason)` kiểm tra `cleanReason.length >= 10`, ném `LoiNghiepVu('LY_DO_QUA_NGAN')`. Xác nhận bằng Unit Test #18. |
| **BUG-002** | Khung giờ 30 phút đã có 5 lịch hẹn nhưng khách hàng vẫn đặt thêm được lịch thứ 6 | Câu truy vấn SQL đếm lịch hẹn thiếu điều kiện khung giờ `window_start <= appointment_time < window_end` | Viết lại hàm `countAppointmentsInSlot()` truy vấn chính xác khung giờ 30 phút; Service ném `LoiNghiepVu('LICH_HEN_QUA_TAI')` khi count >= 5. Xác nhận bằng Unit Test #19. |
| **BUG-003** | Kỹ thuật viên ở Cần Thơ lại được phân công phiếu bảo hành tiếp nhận tại Trung tâm Mỹ Tho | Quản lý có thể chọn mã KTV bất kỳ gửi lên API mà Backend không xác thực chéo chi nhánh | Bổ sung hàm `checkTechnicianEligibility()` kiểm tra `tech.center_id === ticket.center_id`, ném `LoiNghiepVu('KTV_KHAC_TRUNG_TAM')`. Xác nhận bằng Unit Test #20. |
| **BUG-004** | Giao diện M1/M2 bị trắng xoá với lỗi `TypeError: Cannot read properties of undefined (reading 'full_name')` | Câu lệnh SQL `LEFT JOIN customers` trả về `NULL` khi khách hàng cũ chưa được cập nhật họ tên; View đọc trực tiếp thuộc tính CSDL | Xây dựng Hợp đồng Dữ liệu Ranh giới qua hàm `toTicketView(rawTicket)` trong `src/services/ticket.contract.js`, fallback an toàn `customer_name: '(không rõ họ tên)'` và `technician_name: 'Chưa phân công'`. Xác nhận bằng Unit Test #21 & #22. |
| **BUG-005** | KTV nhấn *"Chỉ xem phiếu của tôi"* trên M1 không thấy phiếu nào dù CSDL đã phân công phiếu | Dropdown trạng thái M1 ghim `MOI` và hàm tìm kiếm `filter()` trên view bỏ sót trường `technician_name` | Đặt dropdown mặc định về `-- Tất cả trạng thái --`, lọc trực tiếp theo `technician_id === currentUser.technicianId` (toggle), thêm `t.technician_name` vào tìm kiếm text. Xác nhận bằng Unit Test #26 & kịch bản E2E. |

---

## 4. PHẦN 3: LOGGING CÓ CẤU TRÚC VÀ XỬ LÝ LỖI XUYÊN LỚP

### 4.1. Structured Logging chuẩn JSON ra `stdout` (Slide 19–24)
Hệ thống không sử dụng các lệnh `console.log()` đơn giản rải rác mà xây dựng module ghi log tập trung tại `src/utils/logger.js`:
* **Định dạng:** Mỗi dòng log là một đối tượng JSON độc lập, dễ dàng được phân tích bởi các hệ thống giám sát log (Docker logs, ELK, Datadog).
* **Bốn mức log chuẩn:**
  * `DEBUG`: Dành cho thông tin chi tiết nội bộ trong lúc phát triển.
  * `INFO`: Ghi nhận các sự kiện nghiệp vụ quan trọng (Khởi động server, Đăng nhập, Tạo phiếu, Gán KTV, Đặt lịch hẹn).
  * `WARN`: Cảnh báo các hành vi vi phạm nghiệp vụ (Nhập lý do quá ngắn, Đặt lịch quá tải slot).
  * `ERROR`: Ghi nhận các sự cố kỹ thuật hạ tầng (Lỗi CSDL 503, Exception chưa lường trước).
* **Mã định danh `requestId`:** Middleware `src/middleware/requestId.js` tự động sinh mã UUID cho mỗi yêu cầu HTTP (`req-xxxxxx`) và truyền vào HTTP Response Header `X-Request-Id`. Giúp truy vết toàn bộ luồng xử lý từ lúc vào đến khi phản hồi.
* **Cơ chế Khử độc Dữ liệu (Data Redaction):**
  * Tự động quét và che giấu các trường nhạy cảm: `password`, `token`, `secret`.
  * Thực thi quy tắc bảo vệ dữ liệu PII và **QT-15**: Số điện thoại khách hàng tự động được che giấu tại ranh giới (ví dụ: `0901234567` $\to$ `090****567`).

```json
{
  "timestamp": "2026-10-25T18:39:35.534Z",
  "level": "INFO",
  "module": "SmartCRM:Server",
  "requestId": "req-37efc3ab",
  "username": "quanly",
  "role": "MANAGER",
  "message": "Người dùng đăng nhập thành công"
}
```

### 4.2. Xử lý lỗi xuyên lớp (Centralized Error Handler — Slide 25–26)
Hệ thống loại bỏ hoàn toàn các cấu trúc `try-catch` nuốt lỗi ngẫu hứng hoặc tự trả HTTP status rải rác trong Repository:
1. **Lớp Repository:** Tuyệt đối không chứa mã trạng thái HTTP. Khi SQLite xảy ra lỗi, bọc lại và ném `LoiTruyCapDuLieu` (mang thông điệp kỹ thuật nội bộ).
2. **Lớp Service:** Kiểm tra logic nghiệp vụ. Khi phát hiện dữ liệu sai hoặc vi phạm quy tắc (QT-04, QT-06, QT-07, QT-08, QT-09), ném `LoiNghiepVu` mang mã lỗi máy đọc (`ma`) và thông điệp tiếng Việt thân thiện.
3. **Lớp Controller:** Bắt ngoại lệ và chuyển trực tiếp cho Express qua hàm `next(err)`.
4. **Middleware Xử lý lỗi tập trung (`src/middleware/errorHandler.js`):** Nơi DUY NHẤT ghi log lỗi và quyết định mã HTTP Status trả về cho Client:
   * `LoiNghiepVu` $\to$ HTTP 400, 404, hoặc 409 (Conflict).
   * `LoiTruyCapDuLieu` $\to$ HTTP 503 Service Unavailable (che giấu câu truy vấn SQL thô, chỉ trả thông điệp an toàn cho người dùng).
   * Chuẩn hóa cấu trúc JSON trả về đồng nhất:
     ```json
     {
       "error": "LICH_HEN_QUA_TAI",
       "message": "Vi phạm quy tắc nghiệp vụ: Khung giờ đã đầy (5/5 lịch hẹn). Vui lòng chọn khung giờ khác theo QT-09",
       "requestId": "req-f0802372"
     }
     ```

---

## 5. PHẦN 4: ĐÓNG GÓI MÔI TRƯỜNG DOCKER & DOCKER COMPOSE (SLIDE 27–36)

Để đảm bảo nguyên tắc TÁI LẬP ĐƯỢC từ bất kỳ máy tính nào chưa cài đặt Node.js hay môi trường phát triển, hệ thống đã được đóng gói container hoàn chỉnh:

### 5.1. Dockerfile tối ưu bộ nhớ đệm (Layer Caching)
```dockerfile
FROM node:20-alpine
WORKDIR /app
# Sao chép tệp khai báo và tệp khóa phiên bản trước
COPY package*.json ./
# Cài đặt chính xác các phụ thuộc production từ tệp khóa (tối ưu cache)
RUN npm ci --omit=dev
# Sao chép toàn bộ mã nguồn
COPY . .
EXPOSE 3000
HEALTHCHECK --interval=20s --timeout=5s --retries=3 CMD wget -qO- http://localhost:3000/api || exit 1
CMD ["npm", "start"]
```

### 5.2. File `.dockerignore` bảo mật
Ngăn chặn không đưa thư mục `node_modules`, file `.env`, file nhật ký `*.log` và thư mục `.git` vào Docker Image, giảm dung lượng image và bảo đảm an toàn thông tin.

### 5.3. Docker Compose (`docker-compose.yml`)
* Khởi chạy hệ thống chỉ bằng 2 lệnh:
  ```bash
  cp .env.example .env
  docker compose up -d --build
  ```
* Thiết lập `volumes: - ./db:/app/db` để cơ sở dữ liệu SQLite được lưu trữ bền vững trên máy chủ chủ quản (Host Machine), không bị mất dữ liệu khi container khởi động lại.
* Tích hợp cơ chế tự kiểm tra sức khỏe `HEALTHCHECK` thăm dò cổng 3000.

---

## 6. PHẦN 5: KẾT QUẢ KIỂM CHỨNG & CHUẨN BỊ CHO BUỔI 12

### 6.1. Kết quả kiểm thử tự động
1. **Bộ 36 Unit Tests (Node.js Test Runner):**
   * Luồng đúng (Happy Path): 6 tests.
   * Trường hợp Biên (Boundary): 4 tests.
   * Dữ liệu sai & Ngoại lệ (Exceptions): 7 tests.
   * Kiểm thử Hồi quy Bug Log: 5 tests (`BUG-001` $\to$ `BUG-004`).
   * Hợp đồng Dữ liệu Ranh giới (Buổi 09): 6 tests (ISO 8601, Che SĐT QT-15, null fallback).
   * Cập nhật tiến độ KTV (FR6, US5): 8 tests (Đổi `DANG_XU_LY` sang `CHO_LINH_KIEN`/`HOAN_TAT`, AC5.2 chặn phiếu MOI, chặn KTV khác, Quản lý cập nhật, chặn trùng trạng thái, chặn thiếu ghi chú).
   * **Kết quả: 36/36 tests PASS 100% trong 139ms.**
2. **Kiểm thử tích hợp toàn luồng End-to-End (`npm run test:e2e`):**
   * Kịch bản 9 bước tuần tự từ M1 (Xem danh sách, kiểm tra tải KTV) $\to$ M2 (Gợi ý phân công, chuyển gán) $\to$ M2 (KTV cập nhật tiến độ FR6/US5: `DANG_XU_LY` $\to$ `CHO_LINH_KIEN` $\to$ `HOAN_TAT`) $\to$ M3 (Đặt lịch hẹn, kiểm tra chặn vượt tải 5/5 theo QT-09) $\to$ Kiểm tra Audit Log.
   * **Kết quả: 100% thành công, không gặp bất kỳ lỗi treo hay sập server.**

### 6.2. Kế hoạch chuẩn bị cho Buổi 12 (Workshop tích hợp & Nộp Bài tập 2)
Sinh viên đã hoàn tất mọi tài liệu và mã nguồn, sẵn sàng bước vào Buổi 12:
* **Khung Demo nhanh 3 phút:** Đã chuẩn bị sẵn sàng 4 chặng: (1) Chạy luồng chính End-to-End 9 bước và demo trên giao diện web; (2) Chứng minh xử lý dữ liệu sai và bắt lỗi 401 không sập; (3) Chạy `npm test` chứng minh 36 tests PASS; (4) Thuyết minh gỡ lỗi `BUG-004` & `BUG-005` trong `docs/bug-log.md` theo 4 bước.
* **Bộ ba câu hỏi vấn đáp chuẩn:** Đã chuẩn bị sẵn sàng lập luận kỹ thuật cho 3 câu hỏi (Vì sao chọn SQLite/Idempotent, Điểm nghẽn khi dữ liệu tăng gấp 10, Chỉ đúng dòng mã chịu trách nhiệm kiểm tra quy tắc).
* **Hồ sơ nộp bài:** File báo cáo PDF [BT2_2374802013447_NguyenMinhPhu.pdf](file:///d:/CDTN%201/docs/BT2_2374802013447_NguyenMinhPhu.pdf) chuẩn 7 trang, link GitHub tag `v0.2` đã kiểm chứng clean clone thành công.

---

## 7. CAM KẾT LIÊM CHÍNH HỌC THUẬT

Tôi xác nhận đã đọc, hiểu và chịu trách nhiệm về toàn bộ nội dung nộp. Mọi dòng mã, cấu hình và báo cáo đều được tôi trực tiếp kiểm chứng, hiểu rõ logic hoạt động và sẵn sàng giải thích chi tiết trước Giảng viên tại buổi đánh giá Workshop Buổi 12.

* **Họ và tên sinh viên:** Nguyễn Minh Phú  
* **Mã số sinh viên (MSSV):** 2374802013447  
* **Lớp học phần:** 232_71ITBS40103_01 — HK261  
* **Ngày hoàn thành báo cáo:** 26/10/2026  
