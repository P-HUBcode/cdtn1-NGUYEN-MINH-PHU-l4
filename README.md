# BÀI TẬP 3: KIỂM THỬ VÀ ĐÓNG GÓI PROTOTYPE (20%)
## HỆ THỐNG SMART CRM - MEKONG MOBILE WARRANTY HUB
### LUỒNG L4: PHÂN CÔNG KỸ THUẬT VIÊN VÀ LỊCH HẸN BẢO HÀNH
**Trọng số học phần:** 20% | **Hình thức:** Làm việc cá nhân 100% | **Chuẩn đầu ra:** CLO3, CLO4, CLO5  
**Phiên bản phát hành chính thức:** Git Release Tag [`v1.0`](https://github.com/P-HUBcode/cdtn1-NGUYEN-MINH-PHU-l4/releases/tag/v1.0)

---

## 👨‍💻 Thông Tin Sinh Viên & Học Phần
- **Họ và tên sinh viên:** Nguyễn Minh Phú
- **Mã số sinh viên (MSSV):** 2374802013447
- **Lớp học phần:** 232_71ITBS40103_01
- **Chuyên ngành (Track):** SE (Software Engineering - Kỹ thuật phần mềm)
- **Giảng viên hướng dẫn:** TS. Nguyễn Trí Hải
- **Repository GitHub (Public):** [https://github.com/P-HUBcode/cdtn1-NGUYEN-MINH-PHU-l4](https://github.com/P-HUBcode/cdtn1-NGUYEN-MINH-PHU-l4)
- **Release Tag v1.0:** [https://github.com/P-HUBcode/cdtn1-NGUYEN-MINH-PHU-l4/releases/tag/v1.0](https://github.com/P-HUBcode/cdtn1-NGUYEN-MINH-PHU-l4/releases/tag/v1.0)
- **Báo cáo đồ án chính thức (PDF):** [`docs/BT3_2374802013447_NguyenMinhPhu.pdf`](./docs/BT3_2374802013447_NguyenMinhPhu.pdf)

---

## ⚡ PHÉP THỬ MÁY TRẮNG — DỰNG HỆ THỐNG VỚI 2 LỆNH DUY NHẤT (CỐT LÕI C1)

Hệ thống được đóng gói container hóa hoàn chỉnh theo chuẩn Docker & Docker Compose. Giảng viên chỉ cần clone repo vào một thư mục trống và thực thi đúng 2 lệnh:

```bash
# Lệnh 1: Khởi tạo biến môi trường từ mẫu
cp .env.example .env

# Lệnh 2: Dựng image và khởi chạy toàn bộ dịch vụ ở chế độ nền
docker compose up -d --build
```

### Kiểm tra hệ thống sau khi khởi chạy:
```bash
# 1. Kiểm tra trạng thái container (phải hiển thị healthy)
docker compose ps

# 2. Kiểm tra Healthcheck REST API
curl -s http://localhost:3000/api
# Kết quả mong đợi: {"name":"Smart CRM Warranty Hub API - Luồng L4","version":"1.0.0","status":"UP",...}
```

### Chạy toàn bộ bộ kiểm thử tự động (CỐT LÕI C3):
```bash
# Chạy bộ 12 ca kiểm thử thực tế của Buổi 14 (Đủ 5 loại, 12/12 PASS):
docker compose exec app npm run test:report
# (Hoặc chạy trên host nếu cài Node.js): npm run test:report

# Chạy toàn bộ 38 Unit & Data Contract Tests:
docker compose exec app npm test
```

---

## 🌐 Đường Dẫn Truy Cập Giao Diện
- **Giao diện Web Platform (M1, M2, M3):** [http://localhost:3000](http://localhost:3000)
- **Bảng điều khiển kiểm thử trực quan (Live Test Dashboard):** [http://localhost:3000/test-dashboard.html](http://localhost:3000/test-dashboard.html)

### Danh sách tài khoản thử nghiệm có sẵn:
| Tên đăng nhập | Mật khẩu | Vai trò | Mô tả thẩm quyền |
| :--- | :--- | :--- | :--- |
| `quanly` | `123456` | `MANAGER` | Quản lý Trung tâm Cần Thơ — Toàn quyền điều phối, phân công & lịch hẹn |
| `ktv_binh` | `123456` | `TECHNICIAN` | Kỹ thuật viên KTV-001 (chuyên Màn hình 5/5, Pin 4/5) — Chỉ sửa phiếu của mình |
| `ktv_cuong` | `123456` | `TECHNICIAN` | Kỹ thuật viên KTV-002 (chuyên Phần mềm 5/5) — Chỉ sửa phiếu của mình |
| `admin` | `123456` | `ADMIN` | Quản trị viên hệ thống Mekong Mobile |

---

## 📂 Danh Mục Tài Liệu Bàn Giao Trong Thư Mục `docs/`

Tuân thủ đầy đủ 6 thành phần bắt buộc của Đề bài Bài tập 3:

| Thành phần | Đường dẫn tệp trong Repo | Mô tả chi tiết |
| :--- | :--- | :--- |
| **Thành phần 1** | [`docs/test-plan.md`](./docs/test-plan.md) | **Test Plan rút gọn** (4 mục chuẩn, trả lời câu hỏi *"Làm sao em biết là đã kiểm thử ĐỦ?"*). |
| **Thành phần 2** | [`docs/test-report.md`](./docs/test-report.md) | **Test Report** (12 test case chạy THẬT đủ 8 cột, bao phủ đủ 5 loại: Happy Path 5, Biên 3, Ngoại lệ 2, Bảo mật 1, Tái lập 1 — Đạt 12/12 PASS 100%). |
| **Thành phần 3** | [`docs/bug-log.md`](./docs/bug-log.md) | **Bug Log** (3 bug thực tế: 1 Critical, 1 Major, 1 Minor; mỗi bug đủ 7 dòng, có commit hash riêng biệt). |
| **Thành phần 4** | [`Dockerfile`](./Dockerfile) & [`docker-compose.yml`](./docker-compose.yml) | **Đóng gói Docker** tái lập được, cấu hình Healthcheck, volume dữ liệu bền vững. |
| **Thành phần 5** | [`docs/deployment-guide.md`](./docs/deployment-guide.md) & [`docs/checklist-bao-mat.md`](./docs/checklist-bao-mat.md) | **Deployment Guide** viết bằng tiếng Anh (5 mục chuẩn) và **Checklist Bảo Mật** 7 mục có minh chứng xác minh thực tế. |
| **Thành phần 6** | [`docs/api-docs.md`](./docs/api-docs.md) | **Tài liệu kỹ thuật Track SE (API Docs)** viết bằng tiếng Anh cho toàn bộ 15 endpoints, mỗi endpoint đủ 7 mục bắt buộc và JSON schema/payload thật. |
| **Phụ lục 1** | [`docs/thay-doi-thiet-ke.md`](./docs/thay-doi-thiet-ke.md) | Nhật ký thay đổi thiết kế tích lũy từ BT2 (TD-01 đến TD-14). |
| **Phụ lục 2** | [`docs/ai-disclosure.md`](./docs/ai-disclosure.md) | Bảng khai báo sử dụng công cụ AI minh bạch cho toàn bộ các giai đoạn (10 mục). |
| **Minh chứng ảnh**| [`docs/screenshots/`](./docs/screenshots/) | Thư mục ảnh chụp chạy test THẬT (`TC-01.png` đến `TC-12.png`) và ảnh nền tảng thật. |

---

## 🎯 Bảng Tự Đánh Giá Tiêu Chí Kỹ Thuật Tối Thiểu (Mục 4.2 Đề BT3)

### Tiêu chí CHUNG (C1 - C9):
- [x] **C1. (CỐT LÕI)** Gói đóng gói dựng lại được từ thư mục trống bằng $\le 2$ lệnh theo Deployment Guide (`cp .env.example .env` && `docker compose up -d --build`).
- [x] **C2. (CỐT LÕI)** Test Report có 12 test case đủ 8 cột, bao phủ đủ 5 loại theo mục 2.2.
- [x] **C3. (CỐT LÕI)** Bộ kiểm thử chạy PASS bằng 1 lệnh (`npm run test:report` hoặc `npm test`); chạy lại ngẫu nhiên tại chỗ đều PASS.
- [x] **C4. (CỐT LÕI)** Bug Log có 3 bug (1 Critical, 1 Major, 1 Minor), mỗi bug đủ 7 dòng, commit link mở được và trỏ đúng commit đơn lẻ.
- [x] **C5.** Deployment Guide viết bằng tiếng Anh đủ 5 mục, có mục cách kiểm tra hệ thống chạy đúng.
- [x] **C6.** Checklist bảo mật 7 mục đã điền đủ, mỗi mục có một dòng minh chứng cụ thể.
- [x] **C7.** Không có secret nào trong repo, file `.env` chưa từng bị commit vào lịch sử Git.
- [x] **C8.** Chạy lại lần 2 (nạp dữ liệu seed / reset demo) không lỗi và không trùng lặp dữ liệu (Idempotent).
- [x] **C9.** Tài liệu kỹ thuật theo track mô tả đúng hệ thống thật, không mô tả tính năng hư cấu.

### Tiêu chí RIÊNG Track SE (S1 - S4):
- [x] **S1.** API docs đầy đủ mọi endpoint (15 endpoints), mỗi endpoint đủ 7 mục, có JSON payload thật.
- [x] **S2.** Có test kiểm tra quyền truy cập theo chủ sở hữu (OWASP A01) và chạy PASS (`TC-11` & Unit Test #26).
- [x] **S3.** Mật khẩu trong CSDL được băm an toàn (SHA-256 + Salt), không lưu plaintext.
- [x] **S4.** Thông báo lỗi không lộ vết ngăn xếp (stack trace), tên bảng hay chuỗi kết nối khi chạy production.
