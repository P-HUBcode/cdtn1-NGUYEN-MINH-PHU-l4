# BÀI TẬP 1 & BÀI TẬP 2: HỆ THỐNG SMART CRM - MEKONG MOBILE
## LUỒNG L4: PHÂN CÔNG KỸ THUẬT VIÊN VÀ LỊCH HẸN

**Thông tin sinh viên:**
- **Họ và tên:** Nguyễn Minh Phú
- **Mã số sinh viên:** 2374802013447
- **Chuyên ngành (Track):** SE (Software Engineering)
- **Học phần:** Chuyên đề tốt nghiệp 1 (HK261 - Trường Đại học Văn Lang)

---

## 📌 MỤC 1. PHẠM VI NGHIỆP VỤ LUỒNG L4
> **Phạm vi diễn đạt bằng 1 câu:** Hệ thống hỗ trợ Quản lý trung tâm bảo hành phân công phiếu bảo hành cho kỹ thuật viên phù hợp dựa trên tay nghề, trung tâm làm việc và khối lượng công việc hiện tại; cho phép đặt và quản lý lịch hẹn giao – nhận máy với khách hàng, đồng thời tự động theo dõi hạn cam kết (SLA) và lịch sử chuyển trạng thái.

---

## 📌 MỤC 2. YÊU CẦU MÔI TRƯỜNG & HƯỚNG DẪN CÀI ĐẶT
### 2.1 Yêu cầu môi trường:
- **Node.js**: v20 LTS hoặc v22 trở lên, `npm` v10+
- **Cơ sở dữ liệu**: SQLite 3 (dùng engine CSDL quan hệ tích hợp sẵn theo quyết định dự phòng hợp lệ của Buổi 8 để đảm bảo 100% tái lập, không phụ thuộc dịch vụ ngoài) hoặc PostgreSQL 16.
- **Biến môi trường**: Tham khảo `.env.example` (`PORT=3000`, `DATABASE_URL=db/warranty.sqlite`).

### 2.2 Hướng dẫn cài đặt và chạy ứng dụng:
```bash
# 1. Cài đặt các thư viện cần thiết
npm install

# 2. Khởi chạy máy chủ API (tự động khởi tạo schema CSDL và seed data)
node src/app.js
# Máy chủ lắng nghe tại: http://localhost:3000

# 3. Chạy script kiểm thử tự động các endpoints
node tests/test_api.js
```

---

## 📌 MỤC 3. CẤU TRÚC THƯ MỤC DỰ ÁN (THEO SƠ ĐỒ KIẾN TRÚC 3 LỚP)
```text
.
├── docs/                      # Hồ sơ phân tích & thiết kế hệ thống
│   ├── srs.md                 # Bản đặc tả SRS rút gọn (7 User Stories)
│   ├── thay-doi-thiet-ke.md   # Nhật ký điều chỉnh thiết kế theo phản hồi BT1 (TD-01 -> TD-07)
│   ├── api-contract.md        # Hợp đồng API chuẩn RESTful
│   ├── ai-disclosure.md       # Bảng khai báo liêm chính sử dụng công cụ AI
│   ├── usecase.drawio         # File gốc sơ đồ Use Case (có chú thích ký hiệu)
│   ├── architecture.drawio    # File gốc sơ đồ Kiến trúc 4 lớp (có chú thích)
│   ├── erd.drawio             # File gốc ERD chuẩn 3NF (7 bảng, có customers)
│   ├── wireframe.drawio       # File gốc Wireframe 3 màn hình
│   ├── screenshots/           # Ảnh chụp bằng chứng kiểm thử API Sprint 1
│   └── BT1_2374802013447_NguyenMinhPhu.pdf # Bản PDF nộp bài (đã chèn hình ảnh)
├── src/                       # Mã nguồn hệ thống (Ánh xạ 1-1 theo Kiến trúc 3-4 Lớp)
│   ├── config/
│   │   └── database.js        # Cấu hình CSDL SQLite/PostgreSQL & Migration
│   ├── presentation/
│   │   └── controllers/
│   │       └── ticketController.js # Lớp Trình bày: Tiếp nhận request & trả JSON
│   ├── services/
│   │   └── ticketService.js   # Lớp Nghiệp vụ: Chứa 100% Business Rules (QT-04, QT-06, QT-07)
│   ├── repositories/
│   │   └── ticketRepository.js# Lớp Truy cập Dữ liệu: Che giấu chi tiết SQL
│   └── app.js                 # Entry point khởi chạy server Express
├── db/
│   ├── schema.sql             # SQL DDL Skeleton chuẩn 3NF (7 bảng có customers)
│   └── seed.sql               # Dữ liệu mẫu ban đầu từ case study
├── tests/
│   └── test_api.js            # Script kiểm thử tự động API CRUD & Error
├── .env.example               # Mẫu cấu hình biến môi trường
├── .gitignore                 # Loại bỏ file rác, node_modules, sqlite
├── package.json
└── README.md
```

---

## 📌 MỤC 6. TRẠNG THÁI HIỆN TẠI (BUỔI 8 - SPRINT 1)
- [x] **Xử lý phản hồi BT1:** Đã ghi nhận toàn bộ 7 mục thay đổi thiết kế vào `docs/thay-doi-thiet-ke.md`.
- [x] **Tài liệu & Sơ đồ:** Đã xuất ảnh 4 sơ đồ (Use Case, Kiến trúc, ERD, Wireframe) và chèn trực tiếp vào bản Word/PDF; chuẩn hóa còn 7 User Story; bổ sung bảng `customers`; chỉnh sửa bước UC2 9 bước; bổ sung cam kết AI.
- [x] **CSDL & Migration:** Đã tạo bảng CSDL quan hệ chuẩn 3NF và nạp seed data thành công (`customers`, `service_centers`, `technicians`, `technician_skills`, `tickets`, `ticket_status_log`).
- [x] **Core Module CRUD:** Đã hoàn thiện Entity chính `tickets` qua 3 lớp (Controller $\rightarrow$ Service $\rightarrow$ Repository).
- [x] **Business Rules:** Đã cài đặt logic tự động tính hạn SLA due_date (`QT-04`), kiểm tra KTV cùng trung tâm (`QT-06`), lọc theo tay nghề $\ge 3$ (`QT-07`) và ghi log trạng thái tự động (`ticket_status_log`).
- [x] **API Test:** Đã gọi thử nghiệm thành công 4 kịch bản (Lấy danh sách phiếu, Gợi ý KTV, Phân công KTV 200 OK, Kiểm tra lỗi dữ liệu 400 Bad Request). Ảnh kết quả lưu tại `docs/screenshots/api_test_result.png`.
- [ ] **Lịch hẹn giao - nhận máy (US3 / QT-09):** Đang thiết kế service, sẽ hoàn thiện ở Sprint 2 (Buổi 9).
- [ ] **Unit Tests tự động:** Sẽ bổ sung bộ test Jest cho lớp Service trước Buổi 10.
- **Ghi chú kỹ thuật:** Sử dụng SQLite theo phương án dự phòng chính thức của Buổi 8 để đảm bảo tính tái lập 100% trên mọi máy chấm.
