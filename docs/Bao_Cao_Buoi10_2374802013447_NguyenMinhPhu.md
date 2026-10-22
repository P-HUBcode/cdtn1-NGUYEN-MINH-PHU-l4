# TRƯỜNG ĐẠI HỌC VĂN LANG — KHOA CÔNG NGHỆ THÔNG TIN
## BÁO CÁO THỰC HÀNH BUỔI 10: WORKSHOP MODULE MỞ RỘNG VÀ GIAO DIỆN (SPRINT 2)
### HỌC PHẦN: CHUYÊN ĐỀ TỐT NGHIỆP 1 (HK261)

---

### THÔNG TIN SINH VIÊN & HỆ THỐNG
- **Họ và tên sinh viên:** Nguyễn Minh Phú
- **Mã số sinh viên (MSSV):** 2374802013447
- **Chuyên ngành (Track):** SE (Software Engineering - Kỹ thuật phần mềm)
- **Tên đề tài / Luồng nghiệp vụ:** Hệ thống Smart CRM Mekong Mobile — **Luồng L4: Phân công kỹ thuật viên và lịch hẹn**
- **Đường dẫn Repository GitHub:** [https://github.com/P-HUBcode/cdtn1-NGUYEN-MINH-PHU-l4](https://github.com/P-HUBcode/cdtn1-NGUYEN-MINH-PHU-l4)
- **Nhánh nộp bài:** `main`
- **Mã Commit băm mới nhất:** `07d2281` (hoặc `HEAD`)
- **Ngày nộp báo cáo:** 22/10/2026

---

### MỤC 1. ĐỐI CHIẾU CHECKLIST 10 MỤC KIỂM CHỨNG BUỔI 10 (SLIDE 9 & 10)

| STT | Mục kiểm chứng bắt buộc theo bài giảng | Kết quả tự đánh giá | Minh chứng cụ thể trong Repository |
| :---: | :--- | :---: | :--- |
| **1** | Module mở rộng theo track đã hiện thực và chạy được | **ĐẠT (PASS)** | Frontend 3 màn hình M1, M2, M3 kết nối API thật tại `src/public/index.html`. |
| **2** | **Luồng chính chạy END-TO-END không lỗi treo** | 🔴 **ĐẠT (PASS)** | Toàn bộ 8 bước chạy tự động qua `npm run test:e2e` không cần can thiệp thủ công. |
| **3** | Đã chạy trên dữ liệu mẫu THẬT, không phải dữ liệu tự gõ | **ĐẠT (PASS)** | Khởi tạo CSDL SQLite và nạp seed data 7 bảng quan hệ 3NF tại `src/config/database.js`. |
| **4** | Đã chụp ảnh kết quả toàn luồng, lưu vào `docs/` | **ĐẠT (PASS)** | Đã lưu ảnh minh chứng tại `docs/screenshots/buoi10_e2e_result.png` và `buoi10_unit_tests.png`. |
| **5** | **$\ge 5$ Unit Tests chạy PASS; hiển thị số test trên màn hình** | 🔴 **ĐẠT (PASS)** | **17/17 Unit Tests PASS 100%** qua lệnh `npm test` trong `tests/ticket.service.test.js`. |
| **6** | Có ít nhất 1 test cho trường hợp BIÊN hoặc luồng ngoại lệ | **ĐẠT (PASS)** | Có 4 test biên: KTV tay nghề đúng bằng 3; lý do đúng 10 ký tự; khung giờ còn đúng 1 slot (4/5); SLA Priority CAO/THAP. |
| **7** | Ba trạng thái (đang tải, rỗng, lỗi) đã xử lý cho ít nhất 1 màn hình | **ĐẠT (PASS)** | Thành phần `src/public/js/components/DataState.js` bao đóng: Loading, Empty, Error kèm nút Thử lại. |
| **8** | README mục 3 đã điền đủ các bước chạy, mỗi bước một lệnh | **ĐẠT (PASS)** | `README.md` Mục 3 trình bày chuẩn 7 bước chạy độc lập, chi tiết từng lệnh. |
| **9** | **ĐÃ THỬ clone repo vào thư mục mới và chạy theo đúng README** | 🔴 **ĐẠT (PASS)** | Đã clone sang thư mục độc lập `D:\temp_clone_verify`, chạy `npm install`, `npm test`, `npm run test:e2e` thành công 100%. |
| **10**| Đã commit theo quy ước; tổng số commit của repo $\ge 8$ | **ĐẠT (PASS)** | Repository đạt **13 commits** sạch theo chuẩn Conventional Commits (`feat:`, `docs:`, `test:`, `chore:`). |

---

### MỤC 2. CHI TIẾT KẾT QUẢ KỸ THUẬT ĐẠT ĐƯỢC (SPRINT 2 - TRACK SE)

#### 2.1 Xây dựng Frontend 3 màn hình gọi API thật (Phục vụ Prototype)
- **Tách riêng tầng HTTP Client:** 
  - Tạo `src/api/client.js` và `src/api/ticket.api.js` đóng gói toàn bộ logic gọi mạng và đính kèm Bearer token.
  - **Quy tắc kiểm tra mã nguồn:** Tìm kiếm từ khóa `fetch(` trong toàn bộ mã nguồn giao diện `src/public/js/app.js` cho kết quả **hoàn toàn bằng 0** (100% gọi qua API Adapter).
- **Hiện thực 3 Màn hình theo đúng Wireframe BT1:**
  - **Màn hình M1 (Danh sách chờ & Tải KTV):** Cho phép lọc theo trung tâm và trạng thái; hiển thị tải công việc hiện hành của từng KTV; có nút *“⚡ Khôi phục mẫu MOI”* và nút *“➕ Tiếp nhận phiếu mới”* màu xanh lá nổi bật trên Toolbar và Header.
  - **Màn hình M2 (Phân công & Chuyển gán Re-assign):** Xem thông tin khách hàng từ bảng `customers` (khắc phục TD-05); gợi ý KTV cùng trung tâm đạt tay nghề $\ge 3$ (QT-07); xác nhận phân công hoặc chuyển gán phiếu sang KTV khác (bắt buộc nhập lý do $\ge 10$ ký tự theo QT-08); bảng Audit Log lưu vết lịch sử.
  - **Màn hình M3 (Đặt & Quản lý lịch hẹn):** Cho phép đặt lịch giao hoặc nhận máy; tự động kiểm soát tải khung giờ 30 phút tối đa 5 lịch hẹn (QT-09).
- **Thành phần DataState đóng gói 3 trạng thái:**
  - *Đang tải (`loading`):* Hiển thị hiệu ứng Spinner xoay tròn.
  - *Dữ liệu rỗng (`empty`):* Hiển thị thông điệp khi danh sách không có phiếu.
  - *Lỗi kết nối (`error`):* Khi tắt server backend, giao diện hiển thị thông báo lỗi mạng màu đỏ kèm nút **"🔄 Thử lại ngay"**.
- **Cấu hình chống lưu Cache:** Máy chủ Express được cấu hình Header `no-cache, no-store` đảm bảo khi F5 trình duyệt luôn tải mã nguồn mới nhất.

#### 2.2 Hệ thống Xác thực & Phân quyền (Auth & 401 Handling)
- Hỗ trợ **4 tài khoản demo** đại diện đầy đủ các vai trò:
  1. `quanly` (Mật khẩu: `123456`) — Quản lý trung tâm bảo hành (Nguyễn Minh Phú).
  2. `ktv_binh` (Mật khẩu: `123456`) — KTV Trần Văn Bình (Chuyên Màn hình 5/5, Pin 4/5).
  3. `ktv_cuong` (Mật khẩu: `123456`) — KTV Lê Văn Cường (Chuyên Phần mềm 5/5, Màn hình 3/5).
  4. `admin` (Mật khẩu: `123456`) — Quản trị viên hệ thống.
- Modal đăng nhập tích hợp sẵn bảng nút bấm **`[Chọn]`** giúp tự động điền thông tin tài khoản nhanh.
- Nút **"⚡ Thử mã 401"** trên header gọi API trả về HTTP 401 để kiểm thử cơ chế tự động xóa token và chuyển về modal đăng nhập lại.

#### 2.3 Bộ 17 Unit Tests kiểm chứng lớp Nghiệp vụ (`npm test`)
Thực thi kiểm thử tự động độc lập qua thư viện chuẩn `node:test` và `node:assert`, bao phủ đầy đủ 5 quy tắc nghiệp vụ:
- **QT-04 (Hạn cam kết SLA):** 5 tests (Happy path: CAO +24h, TRUNG_BINH +48h, THAP +72h; Ngoại lệ: sai priority, thiếu ngày tiếp nhận).
- **QT-06 & QT-07 (Điều kiện KTV):** 5 tests (Happy path: cùng trung tâm và tay nghề 5/5; **Giá trị biên: tay nghề đúng bằng 3**; Ngoại lệ: tay nghề < 3 bị từ chối; khác trung tâm bị từ chối; KTV nghỉ phép bị từ chối).
- **QT-08 (Lý do chuyển gán Re-assign):** 4 tests (Happy path: lý do đầy đủ; **Giá trị biên: lý do có đúng 10 ký tự**; Ngoại lệ: lý do < 10 ký tự hoặc để trống bị từ chối).
- **QT-09 (Tải lịch hẹn 30 phút):** 3 tests (Happy path: còn slot 2/5; **Giá trị biên: còn đúng 1 slot 4/5**; Ngoại lệ: đã đầy 5/5 lịch hẹn bị từ chối).
- **Kết quả:** **17 tests pass 100%**, thời gian chạy 45ms.

#### 2.4 Kiểm thử tích hợp toàn luồng End-to-End (`npm run test:e2e`)
Script `tests/test_end_to_end.js` tự động khởi chạy và kiểm thử thông suốt 8 bước:
1. Đăng nhập hệ thống $\to$ nhận JWT Token hợp lệ (HTTP 200).
2. Lấy danh sách phiếu MOI và Tải KTV tại M1.
3. Lấy danh sách gợi ý KTV tay nghề $\ge 3$ tại M2.
4. Phân công KTV Trần Văn Bình $\to$ Phiếu chuyển sang `DANG_XU_LY`, SLA cập nhật +24h.
5. Chuyển gán (Re-assign) sang KTV Lê Văn Cường với lý do hợp lệ $\ge 10$ ký tự $\to$ Cập nhật thành công.
6. Đặt lịch hẹn giao máy tại M3 $\to$ Khởi tạo thành công (HTTP 201).
7. Kiểm chứng ngoại lệ QT-09: Nạp đầy 5 lịch hẹn vào cùng khung giờ $\to$ Đặt lịch thứ 6 bị hệ thống chặn lỗi HTTP 400.
8. Truy vết toàn vẹn Audit Log $\to$ Ghi nhận đầy đủ 4 sự kiện chuyển trạng thái.

---

### MỤC 3. GHI NHẬN THAY ĐỔI THIẾT KẾ (DESIGN CHANGE LOG - MẪU 4 DÒNG)

#### TD-08: Tích hợp Frontend 3 màn hình, bao đóng DataState, tách API Client và mở rộng bộ Unit Tests
- **Yêu cầu Buổi 10:** Hiện thực Frontend 3 màn hình gọi API thật; tách riêng `client.js` và `ticket.api.js`; bọc 3 trạng thái dữ liệu (đang tải, rỗng, lỗi kèm thử lại); bắt mã lỗi 401; viết $\ge 5$ unit tests cho lớp nghiệp vụ và chạy toàn luồng end-to-end không lỗi treo.
- **Quyết định:** HOÀN THIỆN TOÀN DIỆN
- **Lý do:** Đáp ứng 10 mục kiểm chứng cốt lõi của Buổi 10 (Sprint 2 - Track SE), chuyển đổi từ prototype backend sang hệ thống phần mềm hoàn chỉnh chạy được cục bộ, phục vụ người dùng trải nghiệm thực tế và peer review theo README.
- **Ảnh hưởng:** Xây dựng `src/public/` (3 màn hình M1, M2, M3), `src/api/client.js`, `src/api/ticket.api.js`, `DataState.js`, bộ 17 unit tests tại `tests/ticket.service.test.js`, kịch bản E2E tại `tests/test_end_to_end.js`, ảnh minh chứng tại `docs/screenshots/` và cập nhật Mục 3 `README.md`.

---

### MỤC 4. HƯỚNG DẪN TÁI LẬP HỆ THỐNG TRONG 7 BƯỚC (PEER REVIEW)

```bash
# 1. Clone repository từ GitHub
git clone https://github.com/P-HUBcode/cdtn1-NGUYEN-MINH-PHU-l4.git

# 2. Di chuyển vào thư mục dự án
cd cdtn1-NGUYEN-MINH-PHU-l4

# 3. Cài đặt các gói phụ thuộc
npm install

# 4. Sao chép tệp biến môi trường
cp .env.example .env

# 5. Chạy bộ 17 Unit Tests nghiệp vụ (PASS 100%)
npm test

# 6. Chạy kịch bản tích hợp toàn luồng End-to-End
npm run test:e2e

# 7. Khởi chạy máy chủ Web & REST API
npm start
# Truy cập giao diện tại: http://localhost:3000
```

---

### DÒNG CAM KẾT LIÊM CHÍNH BẮT BUỘC
*Tôi xác nhận đã đọc, hiểu và chịu trách nhiệm về toàn bộ nội dung nộp.*  
*Họ và tên: **Nguyễn Minh Phú** | MSSV: **2374802013447** | Ngày nộp: **22/10/2026***
