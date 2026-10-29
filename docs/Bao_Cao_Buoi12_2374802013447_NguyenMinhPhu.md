# BÁO CÁO THỰC HÀNH BUỔI 12: WORKSHOP TÍCH HỢP HỆ THỐNG, DEMO NHANH VÀ NỘP BÀI TẬP 2
**Môn học:** Chuyên đề tốt nghiệp 1 (232_71ITBS40103_01 — HK261)  
**Trường Đại học Văn Lang — Khoa Công nghệ Thông tin**  
**Sinh viên thực hiện:** Nguyễn Minh Phú — MSSV: 2374802013447  
**Chuyên ngành (Track):** Kỹ thuật phần mềm (Software Engineering - SE)  
**Luồng nghiệp vụ:** Luồng L4 — Phân công kỹ thuật viên và lịch hẹn bảo hành (Smart CRM Mekong Mobile)  
**Repository GitHub:** [https://github.com/P-HUBcode/cdtn1-NGUYEN-MINH-PHU-l4](https://github.com/P-HUBcode/cdtn1-NGUYEN-MINH-PHU-l4)  
**Phiên bản phát hành (Tag nộp bài):** [`v0.2`](https://github.com/P-HUBcode/cdtn1-NGUYEN-MINH-PHU-l4/releases/tag/v0.2)  
**Tệp báo cáo chính thức:** `docs/BT2_2374802013447_NguyenMinhPhu.pdf` (Đã xuất bản 7 trang chuẩn A4)  

---

## 1. TỔNG QUAN NỘI DUNG VÀ MỤC TIÊU BUỔI 12 (SLIDE 1–3)

Buổi 12 là buổi thực hành đánh giá trực tiếp kết thúc Giai đoạn 2 của học phần Chuyên đề tốt nghiệp 1: **Workshop tích hợp hệ thống và Nộp Bài tập 2 (chiếm 20% tổng điểm học phần)**.

### Ba mục tiêu cốt lõi của buổi học:
1. **HOÀN THIỆN tích hợp:** Luồng nghiệp vụ chính chạy thông suốt End-to-End từ đầu đến cuối, không gặp lỗi treo hoặc sập dịch vụ (Server crash).
2. **DEMO nhanh 3 phút và kiểm chứng tại lớp:** Trực tiếp trình diễn trước Giảng viên và lớp học; Giảng viên clone repository theo tag `v0.2` về máy sạch và chạy thử theo đúng `README.md`.
3. **★ NỘP BÀI TẬP 2 qua VLU E-learning:** Nộp đúng hạn trước khi kết thúc buổi 12 gồm:
   - 01 file PDF duy nhất: `BT2_2374802013447_NguyenMinhPhu.pdf` (tuyệt đối không nộp file `.docx`).
   - Đường link GitHub repository công khai (Public) có gắn Release Tag `v0.2`.

---

## 2. BẢY VIỆC DỌN REPO TRƯỚC KHI NỘP BÀI (SLIDE 5)

Hệ thống đã thực hiện đầy đủ và nghiêm ngặt toàn bộ 7 việc dọn dẹp kho mã nguồn trước khi xuất bản bản nộp cuối:

| Việc | Nội dung quy định | Hiện trạng thực tế trong repo của sinh viên | Kết quả đối soát |
| :---: | :--- | :--- | :---: |
| **1** | **`git status` sạch:** Không commit `node_modules/`, `.env`, file log hay dữ liệu lớn. | Tệp `.gitignore` đã chặn triệt để: `node_modules/`, `*.log`, `.env`, `__pycache__/`, `.DS_Store`. Lệnh `git status` sạch hoàn toàn. | **ĐẠT** |
| **2** | **Tìm Secret:** Quét không có mật khẩu, token, chuỗi kết nối thật trong mã nguồn. | Quét sạch sẽ `src/`. Mọi biến nhạy cảm đều lấy qua `process.env` với fallback an toàn cho môi trường test/local. | **ĐẠT** |
| **3** | **Tệp khóa đã commit:** Commit `package-lock.json` ghi chính xác từng phiên bản. | `package-lock.json` đã được commit vào Git repo; cài đặt bằng `npm ci`. | **ĐẠT** |
| **4** | **`.env.example` đầy đủ:** Liệt kê đầy đủ tên biến, giá trị mẫu, không lộ secret. | Có `.env.example` cấu hình cổng `PORT=3000`, `DATABASE_URL=./db/warranty.sqlite`, `LOG_LEVEL=info`. | **ĐẠT** |
| **5** | **`README.md` chuẩn:** Đủ runtime, mỗi bước một lệnh sao chép được, có lệnh chạy test. | `README.md` Mục 2 khai báo `Node.js >= 20 LTS`; Mục 3 hướng dẫn 7 bước (mỗi bước 1 lệnh); có lệnh `npm test` và `npm run test:e2e`. | **ĐẠT** |
| **6** | **Clone vào thư mục mới và chạy thử (Phép thử máy sạch):** Không phụ thuộc máy cũ. | Đã clone thử vào thư mục trống, chạy `npm ci`, `npm run setup`, `npm test` (38/38 pass), `npm start` thành công 100%. | **ĐẠT** |
| **7** | **Gắn Tag và đẩy GitHub:** Gắn tag `v0.2` trỏ commit mới nhất, đẩy cả `main` và `v0.2`. | Tag `v0.2` đã được push lên GitHub remote, mở công khai tại `/releases/tag/v0.2`. | **ĐẠT** |
| **+** | **Dọn mã & Bug Log:** Xóa console.log thừa, xóa catch rỗng (Slide 25), có `docs/bug-log.md`. | Đã dọn sạch catch rỗng (commit `49b8ad8`), `docs/bug-log.md` có đủ 6 bugs (BUG-001 -> BUG-006) kèm link commit mở được. | **ĐẠT** |

---

## 3. KỊCH BẢN DEMO NHANH 3 PHÚT (SLIDE 7)

Dưới đây là kịch bản trình diễn 3 phút được thiết kế chuẩn xác theo 4 chặng của Slide 7:

```
[00:00 - 01:15] CHẶNG 1: LUỒNG CHÍNH CHẠY END-TO-END (9 BƯỚC)
- Mở Terminal và chạy: npm run test:e2e
- Minh chứng toàn bộ 9 bước chạy mượt mà:
  1. Đăng nhập Quản lý (POST /api/v1/auth/login) -> cấp JWT demo token.
  2. M1: Tải danh sách 9 phiếu và trạng thái làm việc của 3 KTV.
  3. M2: Gọi thuật toán gợi ý KTV cho phiếu #1 (chọn ra 2 KTV tay nghề >= 3 theo QT-07).
  4. M2: Phân công KTV Trần Văn Bình -> Chuyển trạng thái DANG_XU_LY, tự tính hạn SLA (QT-04).
  5. M2: Chuyển gán (Re-assign) sang KTV Lê Văn Cường với lý do hợp lệ >= 10 ký tự (QT-08).
  6. M2: KTV cập nhật tiến độ (FR6/US5): DANG_XU_LY -> CHO_LINH_KIEN -> HOAN_TAT.
  7. Khóa vĩnh viễn: Thử cập nhật tiếp phiếu HOAN_TAT -> Bị chặn với mã lỗi PHIEU_DA_HOAN_TAT.
  8. M3: Đặt lịch hẹn giao máy -> Giao máy thành công, cấp ID lịch hẹn.
  9. Audit Log: Đọc 60 bản ghi nhật ký kiểm toán lưu vết chi tiết từng thay đổi.

[01:15 - 01:50] CHẶNG 2: XỬ LÝ LỖI ĐÚNG VÀ SUY GIẢM CÓ KIỂM SOÁT (C7 & S4)
- Trình diễn xử lý dữ liệu sai:
  + Đặt lịch hẹn vào khung giờ đã đủ 5/5 lịch: Hệ thống từ chối với mã LICH_HEN_QUA_TAI (HTTP 409 theo QT-09).
  + Thử nhập lý do chuyển gán < 10 ký tự: Bị từ chối với LY_DO_QUA_NGAN (HTTP 400 theo QT-08).
- Trình diễn suy giảm có kiểm soát trên UI:
  + Mở giao diện Web tại http://localhost:3000.
  + Nhấn nút "Thử mã 401": Client tự động xóa token và chuyển về modal đăng nhập, không treo web.
  + Thử tải dữ liệu lỗi: Thành phần DataState hiển thị banner đỏ kèm mã requestId và nút Thử lại (tối đa 3 lần theo Slide 25).

[01:50 - 02:25] CHẶNG 3: BỘ KIỂM THỬ TỰ ĐỘNG PASS 100% (C4)
- Chạy lệnh: npm test
- Kết quả: 38/38 Tests PASS 100% trong ~124ms:
  + 6 tests Data Contract (Buổi 09: ISO 8601, Che SĐT QT-15, null fallback).
  + 5 tests SLA due_date (QT-04).
  + 5 tests Phân công KTV (QT-06 & QT-07).
  + 4 tests Lý do chuyển gán (QT-08).
  + 3 tests Khung giờ lịch hẹn (QT-09).
  + 5 tests Hồi quy cho Bug Log (BUG-001 -> BUG-004).
  + 10 tests Cập nhật tiến độ & Khóa hoàn tất (FR6, US5, BUG-006).

[02:25 - 03:00] CHẶNG 4: MỘT LỖI ĐÃ GẶP VÀ CÁCH GỠ THEO 4 BƯỚC (BUG LOG)
- Mở file docs/bug-log.md, thuyết minh về BUG-006 (Khóa vĩnh viễn phiếu HOAN_TAT):
  1. Tái lập: KTV chuyển phiếu sang HOAN_TAT nhưng vẫn gọi được API chuyển ngược về DANG_XU_LY; trên M1 phiếu đã xong vẫn nằm chung với phiếu cần làm.
  2. Khoanh vùng: Thiếu kiểm tra status === 'HOAN_TAT' trong ticketService.js và M1 thiếu bộ lọc tách biệt.
  3. Sửa nguyên nhân: Bổ sung ràng buộc ném PHIEU_DA_HOAN_TAT (HTTP 400); Frontend M2 ẩn form sửa; Frontend M1 thêm checkbox "Ẩn phiếu đã hoàn tất" (mặc định bật).
  4. Xác nhận: Viết Unit Test 31 & 32 kiểm chứng; commit 8ea5ec4 có link mở được trên GitHub.
```

---

## 4. BỘ BA CÂU HỎI CHUẨN CỦA GIẢNG VIÊN (SLIDE 10)

Sinh viên chuẩn bị sẵn câu trả lời tự tin, bám sát trực tiếp vào từng dòng mã nguồn của dự án:

### Câu 1: "Vì sao em chọn cách này mà không phải cách kia?"
* **Phương án đã chọn:** Sử dụng SQLite tích hợp (`node:sqlite`) với cơ chế Migration & Seed tự động dạng **Idempotent** (`CREATE TABLE IF NOT EXISTS`, `INSERT OR IGNORE`).
* **Lý do chọn:** 
  1. Đáp ứng tiêu chí CỐT LÕI C5 của học phần: Khi chạy lại ứng dụng lần thứ hai hoặc nhiều lần, hệ thống không bị lỗi trùng khóa chính và không nhân đôi dữ liệu.
  2. Không cần cài đặt máy chủ CSDL cồng kềnh (PostgreSQL/MySQL), giúp Giảng viên clone về là chạy ngay lập tức qua `npm start` hoặc `docker compose up`.
* **Phương án khác đã cân nhắc và lý do không chọn:** Cách "Xóa bảng rồi nạp lại" (`DROP TABLE IF EXISTS`) cũng chạy lại được nhưng làm mất toàn bộ dữ liệu lịch sử và Audit Log đã thao tác trước đó; không phù hợp với luồng nghiệp vụ cần truy vết kiểm toán như Mekong Mobile.

### Câu 2: "Nếu dữ liệu tăng gấp mười thì chỗ nào hỏng trước?"
* **Điểm nghẽn (Bottleneck) cụ thể:** 
  1. **Màn hình danh sách M1:** Hiện tại hàm `getTickets()` đang truy vấn toàn bộ danh sách phiếu (`SELECT * FROM tickets`) và chuyển toàn bộ sang client. Nếu số lượng phiếu tăng lên 10.000 phiếu, ứng dụng sẽ bị nghẽn băng thông mạng và trình duyệt bị chậm khi render DOM.
  2. **Kiểm tra tải khung giờ 30 phút (QT-09):** Câu truy vấn `countAppointmentsInSlot()` quét bảng `appointments` theo khoảng thời gian `appointment_time >= ? AND appointment_time < ?`. Khi hàng trăm nghìn lịch hẹn được tạo, truy vấn Full Table Scan sẽ gây nghẽn CPU.
* **Giải pháp kỹ thuật khắc phục:**
  1. Bổ sung phân trang Server-side qua `LIMIT ? OFFSET ?` và lazy loading trên UI.
  2. Đánh chỉ mục hỗn hợp (Composite Index) trên bảng `appointments`: `CREATE INDEX idx_appointments_slot ON appointments(center_id, appointment_time, status)`.

### Câu 3: "Chỉ cho thầy dòng mã chịu trách nhiệm cho việc này"
* **Quy tắc tính SLA due_date (QT-04):** Mở tệp [`src/services/ticketService.js`](file:///d:/CDTN%201/src/services/ticketService.js#L26-L45) tại hàm `calculateSlaDueDate(receivedDate, priority)`. Chỉ dòng tính toán cộng `+24h`, `+48h`, `+72h` và ném lỗi `LoiNghiepVu('MUC_UU_TIEN_KHONG_HOP_LE')`.
* **Quy tắc tay nghề KTV $\ge 3$ (QT-07):** Mở tệp [`src/services/ticketService.js`](file:///d:/CDTN%201/src/services/ticketService.js#L68-L82) tại hàm `checkTechnicianEligibility(tech, ticket)`. Chỉ dòng `tech.proficiency < 3` ném `TAY_NGHE_KHONG_DAT`.
* **Quy tắc khóa hoàn tất HOAN_TAT (BUG-006):** Mở tệp [`src/services/ticketService.js`](file:///d:/CDTN%201/src/services/ticketService.js#L125-L135) tại hàm `validateStatusTransition(ticket, newStatus, user)`. Chỉ dòng `if (ticket.status === 'HOAN_TAT') throw new LoiNghiepVu('PHIEU_DA_HOAN_TAT', ...)`.
* **Test kiểm chứng tương ứng:** Mở tệp [`tests/ticket.service.test.js`](file:///d:/CDTN%201/tests/ticket.service.test.js) chỉ Test 31 & 32.

---

## 5. BẢNG CHECKLIST 10 MỤC NỘP BÀI TẬP 2 (SLIDE 11)

| STT | Tiêu chí kiểm tra | Minh chứng trong dự án | Trạng thái |
| :---: | :--- | :--- | :---: |
| **1** | Một file PDF duy nhất: `BT2_<MSSV>_<Họ tên không dấu>.pdf` | Tệp `docs/BT2_2374802013447_NguyenMinhPhu.pdf` (dung lượng 688 KB, độ dài 7 trang). | **ĐẠT** |
| **2** | Trang bìa đầy đủ thông tin: link repo, tag `v0.2`, track SE, luồng L4 | Trang 1 của PDF ghi rõ link GitHub, tag `v0.2`, SE, Luồng L4, họ tên, MSSV, lớp. | **ĐẠT** |
| **3** | PDF đủ 7 mục theo quy định (Tóm tắt, Kiến trúc, Module, Test, Kết quả, Dựng lại, Thay đổi) | PDF có đủ từ Mục 1 đến Mục 7 và Phụ lục Liêm chính AI. | **ĐẠT** |
| **4** | Ảnh chụp kết quả chạy thật trong PDF (Module chạy, Test PASS, 3 trạng thái giao diện) | Đã chèn 4 ảnh độ nét cao: `api_test_result.png`, `buoi11_unit_tests.png` (38 pass), `buoi11_datastate_3states.png`, `buoi11_docker_compose.png`. | **ĐẠT** |
| **5** | Phụ lục bảng khai báo AI cụ thể (Công cụ, phần áp dụng, SV kiểm chứng) | Bảng khai báo 7 tác vụ có AI hỗ trợ và lời cam kết liêm chính học thuật cuối trang PDF. | **ĐẠT** |
| **6** | Tag `v0.2` đã đẩy và trang releases mở được trên GitHub | Tag `v0.2` trỏ vào commit mới nhất, truy cập công khai tại GitHub. | **ĐẠT** |
| **7** | Repository để chế độ Public | Repo `cdtn1-NGUYEN-MINH-PHU-l4` để Public 100%, không cần cấp quyền truy cập. | **ĐẠT** |
| **8** | Có `docs/thay-doi-thiet-ke.md` và `docs/ai-disclosure.md` | Có đủ 2 tệp tại thư mục `docs/` với 14 thay đổi TD-01 $\to$ TD-13. | **ĐẠT** |
| **9** | Không có `.env` thật và secret trong repo; có `.env.example` đủ biến | `.gitignore` đã chặn `.env`; `.env.example` có đủ tên biến cần thiết. | **ĐẠT** |
| **10** | Sẵn sàng nộp qua VLU E-learning | File PDF và link repo đã sẵn sàng để tải lên hệ thống trước hạn chót. | **ĐẠT** |

---

## 6. KẾT LUẬN VÀ CAM KẾT LIÊM CHÍNH

Hệ thống Smart CRM Warranty Hub — Luồng L4 đã hoàn thành toàn bộ các yêu cầu của Buổi 11 và Buổi 12 với chất lượng kỹ thuật cao nhất:
- Mã nguồn sạch sẽ, không nuốt lỗi, có timeout và giới hạn retry theo chuẩn Slide 25.
- Bộ 38 Unit Tests và 9 bước E2E chạy PASS 100%.
- Hồ sơ Bài tập 2 chuẩn chỉnh 7 trang PDF sẵn sàng nộp và bảo vệ tại Workshop Buổi 12.

**Sinh viên cam kết:**
Tôi xác nhận đã đọc, hiểu và chịu trách nhiệm về toàn bộ nội dung nộp. Mọi dòng mã, cấu hình và báo cáo đều được tôi trực tiếp kiểm chứng, hiểu rõ logic hoạt động và sẵn sàng giải thích chi tiết trước Giảng viên tại buổi đánh giá Workshop Buổi 12.

* **Sinh viên:** Nguyễn Minh Phú  
* **MSSV:** 2374802013447  
* **Ngày hoàn tất:** 26/10/2026 — Cập nhật lần cuối: 29/10/2026  
