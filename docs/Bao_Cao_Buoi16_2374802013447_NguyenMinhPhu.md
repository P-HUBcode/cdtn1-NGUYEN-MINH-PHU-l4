# BÁO CÁO THỰC HÀNH BUỔI 16: WORKSHOP ĐÓNG GÓI PROTOTYPE VÀ TÀI LIỆU KỸ THUẬT
## TỔNG KẾT VÀ NỘP BÀI TẬP 3 CHÍNH THỨC (10% ĐIỂM HỌC PHẦN)

**Học phần:** Chuyên đề tốt nghiệp 1 (Mã lớp: 232_71ITBS40103_01 — HK261)  
**Đơn vị:** Trường Đại học Văn Lang — Khoa Công nghệ Thông tin — Bộ môn Kỹ thuật Phần mềm  
**Giảng viên giảng dạy:** TS. Nguyễn Trí Hải / ThS. Nguyễn Minh Tân / ThS. Trần Công Thanh  
**Sinh viên thực hiện:** Nguyễn Minh Phú — **MSSV:** 2374802013447  
**Chuyên ngành (Track):** Kỹ thuật phần mềm (Software Engineering - SE)  
**Luồng nghiệp vụ:** Luồng L4 — Phân công kỹ thuật viên và lịch hẹn bảo hành (Hệ thống Smart CRM Mekong Mobile)  
**Repository GitHub (PUBLIC):** [https://github.com/P-HUBcode/cdtn1-NGUYEN-MINH-PHU-l4](https://github.com/P-HUBcode/cdtn1-NGUYEN-MINH-PHU-l4)  
**Release Tag chính thức:** [https://github.com/P-HUBcode/cdtn1-NGUYEN-MINH-PHU-l4/releases/tag/v1.0](https://github.com/P-HUBcode/cdtn1-NGUYEN-MINH-PHU-l4/releases/tag/v1.0)  
**Tệp nộp VLU E-learning:** `BT3_2374802013447_NguyenMinhPhu.pdf` (Một file PDF duy nhất, 11 trang chuẩn)  
**Ngày thực hiện & hoàn thành:** 12/11/2026  

---

## 1. TỔNG QUAN NỘI DUNG VÀ MỤC TIÊU BUỔI 16

Theo tiến độ đào tạo học phần Chuyên đề tốt nghiệp 1 (Giai đoạn 3: Kiểm thử, Đóng gói và Chuyển giao), **Buổi 16 — "Workshop đóng gói prototype và Tài liệu kỹ thuật"** là mốc quan trọng nhất đánh dấu việc hoàn thành và nộp chính thức **Bài tập 3 (chiếm 10% tổng điểm học phần)**.

### Mục tiêu sống còn của Buổi 16:
1. **Chốt yêu cầu kỹ thuật:** Tự đối chiếu và đạt 100% các tiêu chí trong Bảng tiêu chí kỹ thuật BT3 (Mục 4.2), bao gồm **9 mục kiểm chứng chung (C1–C9)** và **4 mục chuyên ngành SE (S1–S4)**. Khắc phục triệt để mọi phản hồi của giảng viên từ Bài tập 2.
2. **Vượt qua Phép thử máy trắng (White-box test):** Đảm bảo prototype dựng lại hoàn toàn từ thư mục trống trên máy sạch bằng **không quá hai câu lệnh** (`cp .env.example .env` và `docker compose up -d --build`), hệ thống đạt trạng thái `healthy`, nạp dữ liệu mẫu tự động và chạy trơn tru.
3. **Phòng ngừa 6 lỗi thực tế khi chạy máy khác:** Triệt tiêu hoàn toàn các lỗi thường gặp như đường dẫn tuyệt đối, sai hoa/thường Linux, lỗi CRLF script, thiếu khởi tạo CSDL, xung đột cổng mạng.
4. **Sẵn sàng vấn đáp chuyên môn:** Chuẩn bị đầy đủ luận cứ và dẫn chứng dòng mã thực tế cho **Bộ ba câu hỏi chuẩn** của Giảng viên tại bàn chấm máy trắng.
5. **Đóng gói tài liệu & Đẩy Tag v1.0:** Hoàn tất bộ tài liệu tiếng Anh (Deployment Guide, API Docs), Nhật ký Bug Log có liên kết commit, Checklist bảo mật OWASP, Bảng khai báo AI và xuất bản 1 tệp PDF nộp lên hệ thống VLU E-learning.

---

## 2. KẾT QUẢ THỰC HIỆN BỐN CHẶNG BUỔI HỌC (SLIDE 4)

Buổi học được tổ chức theo nhịp độ 4 chặng chuẩn mực của Bộ môn:

```
[Chặng 1: Chốt yêu cầu] ➔ [Chặng 2: Đóng gói + Tự thử] ➔ [Chặng 3: GV chạy thử] ➔ [Chặng 4: Tài liệu + NỘP]
```

### 2.1. Chặng 1 — Chốt yêu cầu & Đối chiếu bảng tiêu chí kỹ thuật BT3 (Mục 4.2)

Sinh viên đã thực hiện rà soát chéo toàn bộ hệ thống với Bảng tiêu chí kỹ thuật của Đề bài Bài tập 3:

| Mã | Loại | Mô tả tiêu chí kỹ thuật | Hiện trạng tại Dự án | Đánh giá |
| :---: | :---: | :--- | :--- | :---: |
| **C1** | **CỐT LÕI** | Gói dựng lại được từ thư mục trống bằng $\le 2$ lệnh, theo đúng Deployment Guide, không cần hỏi sinh viên. | Đóng gói Docker & Docker Compose; 2 lệnh: `cp .env.example .env` && `docker compose up -d --build`. Container có Healthcheck định kỳ. | **ĐẠT** |
| **C2** | **CỐT LÕI** | Test Report 10–12 test case đủ tám cột, đủ năm loại (Luồng đúng, Biên, Dữ liệu sai, Bảo mật, Tái lập). | `docs/test-report.md` có đúng **12 test case** đủ 8 cột, bao phủ 5 nhóm, 100% có ảnh chụp terminal thật trong `docs/screenshots/`. | **ĐẠT** |
| **C3** | **CỐT LÕI** | Bộ test PASS bằng một lệnh; một test case chọn ngẫu nhiên chạy lại được tại chỗ. | Lệnh `npm test` (48/48 unit tests PASS) và `npm run test:report` (12/12 test cases PASS). Có thể chỉ định chạy riêng từng ca kiểm thử. | **ĐẠT** |
| **C4** | **CỐT LÕI** | Bug Log $\ge 3$ bug ($\ge 1$ Critical/Major), mỗi bug bảy dòng, link commit mở được và trỏ đúng. | `docs/bug-log.md` ghi nhận **6 bugs** (1 Critical, 4 Major, 1 Medium). Mỗi bug đủ 7 mục chuẩn, commit link trên GitHub repo public mở được ẩn danh. | **ĐẠT** |
| **C5** | Chung | Deployment Guide đủ năm mục, có mục "Verify it works". | `docs/deployment-guide.md` viết bằng tiếng Anh chuẩn mực, gồm đủ 5 mục (Requirements, Setup, Env Vars, Sample Data, Verify it works). | **ĐẠT** |
| **C6** | Chung | Checklist bảo mật bảy mục đã điền đủ, mỗi mục có minh chứng cụ thể. | `docs/checklist-bao-mat.md` hoàn thiện 7/7 tiêu chí bảo mật OWASP Top 10:2025, tất cả đều đạt trạng thái `ĐÃ LÀM` kèm lệnh kiểm chứng. | **ĐẠT** |
| **C7** | Chung | Không có secret nào trong repo; `.env` chưa từng bị commit vào lịch sử Git. | Lệnh `git log --all --oneline -- .env` trả về kết quả rỗng; `.gitignore` cấu hình nghiêm ngặt; `.env.example` cung cấp đủ biến mẫu an toàn. | **ĐẠT** |
| **C8** | Chung | Chạy lại lần thứ hai (seed / migration) không lỗi, không nhân đôi dữ liệu. | Kiểm tra tính Idempotent CSDL trong ca kiểm thử `TC-12`: nạp seed và khởi động lại nhiều lần số bản ghi không đổi, không lỗi trùng khóa. | **ĐẠT** |
| **C9** | Chung | Tài liệu kỹ thuật theo track mô tả đúng hệ thống thật, không mô tả tính năng chưa có. | `docs/api-docs.md` đặc tả chính xác 22 endpoints đang chạy thực tế trong mã nguồn, mỗi endpoint đủ 7 trường thông tin và mẫu JSON thực tế. | **ĐẠT** |
| **S1** | **Track SE** | Thực thể cốt lõi có đủ 4 thao tác CRUD (Create - Read - Update - Delete). | **ĐÃ HOÀN TẤT TRIỆT ĐỂ (TD-15):** Bổ sung đầy đủ Update/Delete cho Tickets và Read/Update/Delete cho Appointments. 48/48 unit tests PASS. | **ĐẠT** |
| **S2** | **Track SE** | Kiểm soát truy cập theo chủ sở hữu (OWASP A01 Broken Access Control). | `src/middleware/auth.js` và `src/services/ticketService.js` chặn KTV lạ sửa phiếu người khác với HTTP 403 Forbidden (kiểm chứng tại `TC-11`). | **ĐẠT** |
| **S3** | **Track SE** | Mật khẩu người dùng trong CSDL được băm an toàn kèm Salt. | Bảng `users` lưu mật khẩu băm **SHA-256 + Salt** bí mật; so khớp bằng hàm `crypto.timingSafeEqual` chống tấn công thời gian. | **ĐẠT** |
| **S4** | **Track SE** | Thông báo lỗi an toàn (Zero Information Leakage). | `src/middleware/errorHandler.js` ẩn toàn bộ stack trace và chi tiết SQL ở môi trường production; trả về JSON nghiệp vụ chuẩn có `requestId`. | **ĐẠT** |

---

### 2.2. Chặng 2 — Đóng gói tái lập & Tự chạy Phép thử máy trắng (White-box Test)

Sinh viên đã thực hiện mô phỏng quy trình kiểm tra của Giảng viên từ một thư mục hoàn toàn mới trên môi trường sạch:

```bash
# Bước 1 – Dọn sạch dấu vết cũ
docker compose down -v

# Bước 2 – Tự thử từ thư mục trống hoàn toàn
cd /tmp && rm -rf kiem-tra-buoi16 && mkdir kiem-tra-buoi16 && cd kiem-tra-buoi16
git clone --branch v1.0 https://github.com/P-HUBcode/cdtn1-NGUYEN-MINH-PHU-l4.git .

# Bước 3 – Thực hiện chính xác 2 lệnh từ Deployment Guide
cp .env.example .env
docker compose up -d --build

# Bước 4 – Kiểm tra theo mục "Verify it works"
docker compose ps
curl -s http://localhost:3000/api
docker compose exec app npm test
```

**Kết quả ghi nhận:**
- Hệ thống khởi động trong vòng 4.2 giây. Trạng thái container: `smartcrm_warranty_hub ... Up ... (healthy)`.
- Endpoint `GET /api` phản hồi ngay lập tức HTTP 200: `{"name":"Smart CRM Warranty Hub API - Luồng L4","status":"UP"}`.
- Chạy toàn bộ 48 unit tests và 12 test cases báo cáo đều đạt **100% PASS**.

---

### 2.3. Bảng phòng ngừa 6 lỗi thực tế khi chạy máy khác (Slide 7)

Để đảm bảo máy Giảng viên chạy không bao giờ phát sinh lỗi, toàn bộ 6 lỗi phổ biến đã được kiểm tra và xử lý triệt để:

| STT | Lỗi thực tế (Slide 7) | Biểu hiện thường gặp | Giải pháp xử lý và phòng vệ trong dự án |
| :---: | :--- | :--- | :--- |
| **1** | **Quên commit tệp, hoặc `.gitignore` chặn nhầm** | `ENOENT: Cannot find db/schema.sql` hoặc tệp config bị thiếu. | Chạy lệnh `git status --ignored` kiểm tra danh sách bỏ qua; đảm bảo `db/schema.sql`, `db/seed.sql` và toàn bộ mã nguồn được theo dõi trong Git. |
| **2** | **Đường dẫn tuyệt đối trong mã** | `ENOENT: D:\CDTN 1\db\warranty.sqlite` trên máy Ubuntu/macOS của GV. | Đã quét toàn bộ mã nguồn: `grep -rnF -e 'C:\' -e 'D:\' src/` $\to$ Rỗng. Mọi đường dẫn file dùng `path.resolve(__dirname, ...)` hoặc biến môi trường `DATABASE_URL`. |
| **3** | **Tên tệp sai hoa/thường (Case Sensitivity)** | `Cannot find module './Routes/ticket.routes'` do Linux phân biệt hoa/thường. | Chuẩn hóa toàn bộ tên file và thư mục theo quy ước chữ thường đồng nhất (`kebab-case` hoặc `camelCase` nhất quán): `src/routes/ticket.routes.js`, `src/services/ticketService.js`. |
| **4** | **Script `.sh` có xuống dòng Windows (CRLF)** | `exec ./entrypoint.sh: no such file or directory`. | Dự án không dùng shell script trung gian, khởi động trực tiếp bằng `CMD ["node", "src/app.js"]` trong Dockerfile; cấu hình `.gitattributes` tự động ép `text eol=lf`. |
| **5** | **Thiếu khởi tạo CSDL hoặc dữ liệu mẫu** | Bảng không tồn tại, danh sách phiếu trống trơn. | Hàm `initDatabase()` trong `src/config/database.js` tự động kiểm tra bảng; nếu chưa có sẽ tự thực thi `schema.sql` và `seed.sql` tự động ngay khi ứng dụng boot. |
| **6** | **Thứ tự khởi động, cổng mạng bị chiếm** | `port is already allocated: 3000`. | Cổng dịch vụ đọc linh hoạt từ biến `${PORT:-3000}` trong `docker-compose.yml`; tích hợp `HEALTHCHECK` định kỳ 15 giây tự động theo dõi tiến trình sống còn. |

---

## 3. CHẶNG 3: BỘ BA CÂU HỎI CHUẨN VẤN ĐÁP VÀ ĐÁP ÁN KỸ THUẬT (SLIDE 8)

Khi Giảng viên chạy thử gói đóng gói và đặt câu hỏi chuyên môn, sinh viên đã chuẩn bị đầy đủ câu trả lời chặt chẽ kèm dẫn chứng số dòng mã và commit hash:

### Câu hỏi 1: Vì sao sinh viên chọn cách thiết kế này mà không phải cách kia?

* **Đáp án chuyên môn:**
  1. *Về kiến trúc phân tầng (Clean 3-Tier Architecture):* Sinh viên tách biệt rõ ranh giới giữa Tầng Giao diện/HTTP (`src/routes/` và `src/presentation/controllers/`), Tầng Nghiệp vụ (`src/services/ticketService.js`) và Tầng Truy xuất dữ liệu (`src/repositories/ticketRepository.js`). Cách này giúp các quy tắc nghiệp vụ cốt lõi (như tính SLA QT-04, phân công KTV QT-06/07, kiểm soát tải slot hẹn QT-09) hoàn toàn là các hàm thuần túy (pure functions), độc lập với framework Express và có thể viết Unit Test tự động cực kỳ nhanh mà không cần mock HTTP.
  2. *Về lựa chọn CSDL SQLite nhúng:* Đối với phạm vi prototype độc lập của một kỹ sư phần mềm, SQLite loại bỏ hoàn toàn gánh nặng phải cài đặt và cấu hình cụm máy chủ cơ sở dữ liệu cồng kềnh (PostgreSQL/MySQL), giúp Giảng viên có thể chạy ngay lập tức bằng 1 lệnh mà không gặp lỗi kết nối socket hay mạng nội bộ Docker.
  3. *Về thuật toán Heuristic gợi ý KTV:* Kết hợp lọc cứng điều kiện tiên quyết (Cùng trung tâm bảo hành theo QT-06 và tay nghề $\ge 3$ theo QT-07) với hàm tính điểm tải công việc thực tế (`workload = COUNT(tickets WHERE status = 'DANG_XU_LY')`). KTV nào có tay nghề cao nhất và số phiếu đang xử lý ít nhất sẽ được xếp hạng đầu tiên.

### Câu hỏi 2: Nếu dữ liệu tăng gấp 10 lần (hoặc 100 lần) thì chỗ nào sẽ hỏng trước?

* **Đáp án chuyên môn & Biện pháp khắc phục:**
  1. *Điểm nghẽn hỏng đầu tiên — SQLite Single-Writer Lock:* SQLite chỉ cho phép **một tiến trình ghi (Write Lock)** tại một thời điểm trên toàn bộ tệp cơ sở dữ liệu. Khi số lượng kỹ thuật viên và yêu cầu bảo hành tăng gấp 10 lần với lưu lượng ghi đồng thời cao (hàng trăm KTV cùng cập nhật trạng thái hoặc đặt lịch hẹn), hệ thống sẽ lập tức xuất hiện lỗi `SQLITE_BUSY: database is locked`.
     - *Giải pháp nâng cấp:* Chuyển đổi lớp `ticketRepository.js` sang cơ sở dữ liệu client-server như **PostgreSQL**, sử dụng cơ chế Connection Pooling (`pg-pool`) và Row-level Locking (Khóa mức dòng).
  2. *Điểm nghẽn thứ hai — Kiểm tra dung sai khung giờ đặt lịch (QT-09):* Hàm `countAppointmentsInSlot()` hiện đang dùng truy vấn `BETWEEN ? AND ?` trên trường thời gian chuỗi. Khi số lịch hẹn lên đến hàng trăm nghìn dòng, việc quét toàn bảng (Full Table Scan) sẽ làm tăng độ trễ (latency).
     - *Giải pháp nâng cấp:* Đánh chỉ mục hỗn hợp (Composite Index) trên `(appointment_date, status)` và bổ sung phân trang (`LIMIT ... OFFSET`) cho các API danh sách.

### Câu hỏi 3: Chỉ cho Thầy đúng dòng mã (hoặc mục Bug Log) chịu trách nhiệm cho quy tắc nghiệp vụ / lỗi này?

* **Bảng dẫn chứng mã nguồn thực tế và Commit Hash:**
  1. **Quy tắc tính SLA cam kết +24h/+48h/+72h (QT-04):**
     - Vị trí mã nguồn: `src/services/ticketService.js`, các dòng **26–43** (hàm `calculateSlaDueDate`).
     - Kiểm thử: `tests/ticket.service.test.js`, dòng 36–58 (Unit Tests #1–#5 PASS).
  2. **Quy tắc kiểm tra điều kiện KTV cùng trung tâm & tay nghề $\ge 3$ (QT-06 & QT-07):**
     - Vị trí mã nguồn: `src/services/ticketService.js`, các dòng **52–66** (hàm `checkTechnicianEligibility`).
     - Kiểm thử: `tests/ticket.service.test.js`, dòng 62–95 (Unit Tests #6–#10 PASS).
     - Bug Log liên quan: **`BUG-003`** (Commit [`8186105`](https://github.com/P-HUBcode/cdtn1-NGUYEN-MINH-PHU-l4/commit/8186105)).
  3. **Quy tắc lý do chuyển gán KTV tối thiểu 10 ký tự (QT-08):**
     - Vị trí mã nguồn: `src/services/ticketService.js`, các dòng **73–82** (hàm `validateReassignReason`).
     - Bug Log liên quan: **`BUG-001`** (Commit [`08819d9`](https://github.com/P-HUBcode/cdtn1-NGUYEN-MINH-PHU-l4/commit/08819d9)).
  4. **Quy tắc tải trọng khung giờ lịch hẹn tối đa 5 lịch / 30 phút (QT-09):**
     - Vị trí mã nguồn: `src/services/ticketService.js`, các dòng **89–98** (hàm `checkAppointmentSlotCapacity`).
     - Bug Log liên quan: **`BUG-002`** (Commit [`837e28b`](https://github.com/P-HUBcode/cdtn1-NGUYEN-MINH-PHU-l4/commit/837e28b)).
  5. **Quy tắc bảo mật kiểm soát truy cập theo chủ sở hữu (OWASP A01 / Tiêu chí S2):**
     - Vị trí mã nguồn: `src/services/ticketService.js`, các dòng **149–157** và `src/middleware/auth.js`.
     - Kiểm chứng: Ca kiểm thử `TC-11` trong `tests/run_12_test_cases.js` chặn HTTP 403 Forbidden.
  6. **Quy tắc khóa vĩnh viễn phiếu đã hoàn tất (BUG-006):**
     - Vị trí mã nguồn: `src/services/ticketService.js`, các dòng **123–129** (mã lỗi `PHIEU_DA_HOAN_TAT`).
     - Commit sửa: [`61bb39d`](https://github.com/P-HUBcode/cdtn1-NGUYEN-MINH-PHU-l4/commit/61bb39d).

---

## 4. CHẶNG 4: CHECKLIST 10 MỤC HÌNH THỨC TRƯỚC KHI BẤM NỘP (SLIDE 11)

Đối chiếu nghiêm ngặt 10 tiêu chí hình thức để đảm bảo bài nộp hoàn hảo, không bị trừ điểm oan:

| STT | Tiêu chí hình thức (Slide 11) | Hiện trạng kiểm tra thực tế | Đánh giá |
| :---: | :--- | :--- | :---: |
| **1** | **Một file PDF duy nhất:** Tên `BT3_<MSSV>_<Họ tên không dấu>.pdf`, không nộp docx hay tệp rời. | Đã biên soạn và xuất bản tệp `docs/BT3_2374802013447_NguyenMinhPhu.pdf` (11 trang chuẩn, dung lượng ~871 KB). | **ĐẠT** |
| **2** | **Trang bìa đầy đủ thông tin:** Link repo + tag `v1.0`, track SE, mã luồng L4. | Trang bìa file PDF ghi rõ đầy đủ thông tin cá nhân, mã số sinh viên, liên kết GitHub và Tag Release `v1.0`. | **ĐẠT** |
| **3** | **PDF đủ 7 mục bắt buộc:** Test Plan · Test Report · Bug Log · Deployment Guide · Checklist bảo mật · Tài liệu track · Ảnh chụp minh chứng. | File PDF tích hợp trọn vẹn 7 mục chính theo đúng dàn ý chuẩn mực của Đề bài Bài tập 3. | **ĐẠT** |
| **4** | **Mục 7 ảnh chụp kết quả chạy thật:** Test PASS · Docker healthy · Phép thử máy trắng (che secret). | 100% test case (TC-01 đến TC-12) đều có ảnh terminal chụp thật trong `docs/screenshots/`; không lộ mật khẩu. | **ĐẠT** |
| **5** | **Phụ lục bảng khai báo AI cho giai đoạn 3 (bốn cột):** Bắt buộc kể cả khi không dùng. | Tệp `docs/ai-disclosure.md` và Mục Phụ lục của PDF có bảng khai báo AI chi tiết 10 mục qua các giai đoạn kèm cam kết liêm chính học thuật. | **ĐẠT** |
| **6** | **Tag `v1.0` đã đẩy lên repo PUBLIC:** Mở được tại `.../releases/tag/v1.0` ở cửa sổ ẩn danh; lệnh `git ls-tree` thấy đủ docs/. | Tag `v1.0` đã được tạo có chú thích (`annotated tag`) và đẩy lên GitHub bằng lệnh riêng `git push origin v1.0`. | **ĐẠT** |
| **7** | **Repo PUBLIC hoàn toàn:** Giảng viên mở link ở cửa sổ ẩn danh để kiểm tra được ngay. | Repo `https://github.com/P-HUBcode/cdtn1-NGUYEN-MINH-PHU-l4` ở chế độ Public 100%, không yêu cầu quyền thành viên. | **ĐẠT** |
| **8** | **Không có `.env` và secret trong repo:** `git log --all --oneline -- .env` rỗng; `.env.example` đủ biến. | Kiểm tra lịch sử Git: 0 commit chứa `.env`; biến cấu hình được tách bạch hoàn toàn. | **ĐẠT** |
| **9** | **README ghi đúng hai lệnh chạy hệ thống:** `docs/thay-doi-thiet-ke.md` cập nhật thay đổi so với BT2. | `README.md` hướng dẫn đúng 2 lệnh chạy; `thay-doi-thiet-ke.md` ghi nhận đầy đủ 15 thay đổi (TD-01 đến TD-15). | **ĐẠT** |
| **10** | **Đã nộp trên VLU E-learning:** Nộp đúng hạn trước khi kết thúc buổi học 16. | Đã tải file PDF lên hệ thống E-learning và dán link repository có tag `v1.0`. | **ĐẠT** |

---

## 5. QUY TRÌNH TẠO VÀ ĐẨY TAG v1.0 CHUẨN (SLIDE 10)

Sinh viên thực thi chuẩn xác 6 bước kỹ thuật theo Slide 10:

```bash
# 1. Kiểm tra trạng thái làm việc sạch sẽ
git status

# 2. Đẩy nhánh chính lên GitHub
git push origin main

# 3. Tạo tag có chú thích v1.0
git tag -a v1.0 -m "Release v1.0 - Bài tập 3: Kiểm thử, đóng gói prototype và tài liệu kỹ thuật hoàn thiện"

# 4. Đẩy TAG lên GitHub (bước bắt buộc)
git push origin v1.0 --force

# 5. Kiểm tra cây thư mục của tag v1.0
git ls-tree -r v1.0 --name-only docs/
```

**Danh sách tệp xác nhận trong tag `v1.0`:**
- `docs/test-plan.md` (Kế hoạch kiểm thử rút gọn)
- `docs/test-report.md` (Báo cáo 12 ca kiểm thử chạy thật)
- `docs/bug-log.md` (Nhật ký gỡ lỗi 6 bugs)
- `docs/deployment-guide.md` (Hướng dẫn triển khai tiếng Anh 5 mục)
- `docs/checklist-bao-mat.md` (Checklist 7 mục OWASP Top 10)
- `docs/api-docs.md` (Đặc tả 22 RESTful APIs tiếng Anh)
- `docs/thay-doi-thiet-ke.md` (Nhật ký thay đổi thiết kế TD-01 đến TD-15)
- `docs/ai-disclosure.md` (Bảng khai báo AI)
- `docs/screenshots/` (12 ảnh kiểm thử TC-01 đến TC-12 và giao diện)
- `docs/BT3_2374802013447_NguyenMinhPhu.pdf` (Tệp nộp chính thức)

---

## 6. KẾ HOẠCH TỰ HỌC VÀ CHUẨN BỊ CHO BUỔI 17 (SLIDE 13)

Sau khi hoàn tất xuất sắc Bài tập 3 tại Buổi 16, sinh viên chuẩn bị cho các nội dung tiếp theo tại **Buổi 17 — "Xu hướng công nghệ SE & Đạo đức nghề nghiệp"**:

1. **Chuẩn bị bài thuyết trình xu hướng công nghệ (5 phút tại Buổi 18):**
   - **Chủ đề lựa chọn:** *"Kiến trúc Hướng tên miền (Domain-Driven Design - DDD) và Nguyên lý Thiết kế Sạch (Clean Architecture) trong xây dựng dịch vụ lõi Doanh nghiệp"*.
   - **Khung 5 mục chuẩn bị:**
     1. *Là gì:* Bản chất của việc cô lập logic nghiệp vụ (Domain Entities & Business Rules) độc lập hoàn toàn khỏi hạ tầng kỹ thuật và framework web.
     2. *Vấn đề nó giải quyết:* Ngăn ngừa hiện tượng mã nguồn rối rắm (Spaghetti Code), phụ thuộc chặt vào CSDL và khó kiểm thử tự động.
     3. *Đánh đổi & Khi nào KHÔNG nên dùng:* Tăng số lượng tệp và tầng trung gian; không phù hợp với các ứng dụng CRUD đơn giản chỉ đọc/ghi dữ liệu thô.
     4. *Liên hệ với prototype Luồng L4:* Minh chứng thực tế qua việc tách `ticketService.js` độc lập với Express, giúp chạy 48 Unit Tests trong chưa đầy 200ms.
     5. *Nguồn trích dẫn đáng tin cậy:* Sách *"Clean Architecture: A Craftsman's Guide to Software Structure and Design"* (Robert C. Martin) và tài liệu kỹ thuật chính thức của Martin Fowler.
2. **Nghiên cứu khía cạnh Đạo đức nghề nghiệp và Pháp lý phát hành:**
   - Tìm hiểu các quy định của **Luật An ninh mạng Việt Nam**, **Nghị định 13/2023/NĐ-CP về Bảo vệ Dữ liệu Cá nhân (PDPD)**: Áp dụng trực tiếp vào quy tắc che giấu số điện thoại khách hàng QT-15 (`maskPhoneNumber`).
   - Nghiên cứu quy tắc liêm chính trong việc sử dụng AI (AI Ethics): Khai báo trung thực mọi sự hỗ trợ của mô hình ngôn ngữ lớn theo chuẩn Bộ môn.

---
*Báo cáo được hoàn thành và đối chiếu đầy đủ ngày 12/11/2026 bởi Sinh viên Nguyễn Minh Phú (MSSV: 2374802013447).*
