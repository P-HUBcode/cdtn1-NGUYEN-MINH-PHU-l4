# BÀI TẬP 1 & BÀI TẬP 2: HỆ THỐNG SMART CRM - MEKONG MOBILE
## LUỒNG L4: PHÂN CÔNG KỸ THUẬT VIÊN VÀ LỊCH HẸN

**Thông tin sinh viên:**
- **Họ và tên:** Nguyễn Minh Phú
- **Mã số sinh viên:** 2374802013447
- **Chuyên ngành (Track):** SE (Software Engineering)
- **Học phần:** Chuyên đề tốt nghiệp 1 (HK261 - Trường Đại học Văn Lang)
- **Repository GitHub:** [https://github.com/P-HUBcode/cdtn1-NGUYEN-MINH-PHU-l4](https://github.com/P-HUBcode/cdtn1-NGUYEN-MINH-PHU-l4)

---

## 📌 MỤC 1. PHẠM VI NGHIỆP VỤ LUỒNG L4
> **Phạm vi diễn đạt bằng 1 câu:** Hệ thống hỗ trợ Quản lý trung tâm bảo hành phân công phiếu bảo hành cho kỹ thuật viên phù hợp dựa trên tay nghề (proficiency $\ge 3$), cùng trung tâm và tải công việc hiện tại; cho phép tiếp nhận đặt và quản lý lịch hẹn giao – nhận máy với khách hàng (tối đa 5 lịch/khung giờ 30 phút), đồng thời tự động theo dõi hạn cam kết (SLA) và lưu vết lịch sử chuyển gán.

---

## 📌 MỤC 2. YÊU CẦU MÔI TRƯỜNG
- **Node.js**: Phiên bản v20 LTS hoặc v22 trở lên (Đã kiểm chứng trên Node v22.14.0).
- **Trình quản lý gói**: `npm` v10 trở lên.
- **Cơ sở dữ liệu**: SQLite 3 (dùng engine quan hệ tích hợp sẵn qua `node:sqlite` theo quyết định dự phòng hợp lệ của Buổi 8 để đảm bảo 100% tái lập, tự động migrate 7 bảng 3NF và nạp seed data khi khởi động).
- **Hệ điều hành**: Windows, macOS hoặc Linux.

---

## 📌 MỤC 3. CÁC BƯỚC DỰNG VÀ CHẠY HỆ THỐNG (MỖI BƯỚC MỘT LỆNH - PHỤC VỤ REPRODUCE & PEER REVIEW)
*Thực hiện tuần tự từng lệnh dưới đây trong Terminal / PowerShell:*

```bash
# Bước 1: Clone mã nguồn về máy cục bộ
git clone https://github.com/P-HUBcode/cdtn1-NGUYEN-MINH-PHU-l4.git

# Bước 2: Di chuyển vào thư mục dự án
cd cdtn1-NGUYEN-MINH-PHU-l4

# Bước 3: Cài đặt các thư viện phụ thuộc
npm install

# Bước 4: Khởi tạo tệp biến môi trường từ mẫu
cp .env.example .env
# (Trên Windows PowerShell nếu lệnh cp lỗi, dùng: Copy-Item .env.example .env)

# Bước 5: Chạy bộ kiểm thử Unit Tests nghiệp vụ (17 tests PASS 100%)
npm test

# Bước 6: Chạy kiểm thử tích hợp toàn luồng End-to-End (M1 -> M2 -> Re-assign -> M3)
npm run test:e2e

# Bước 7: Khởi chạy máy chủ Backend & Giao diện Frontend Web
npm start
```
*Sau khi chạy Bước 7, mở trình duyệt tại: **`http://localhost:3000`**.*

---

## 📌 MỤC 4. CẤU TRÚC THƯ MỤC DỰ ÁN (THEO SƠ ĐỒ KIẾN TRÚC 3 LỚP & SPRINT 2)
```text
.
├── .env.example                                      # Mẫu biến môi trường
├── .gitignore                                        # Loại trừ node_modules, *.sqlite, *.docx
├── package.json                                      # Cấu hình scripts test, start, dependencies
├── README.md                                         # Tài liệu hướng dẫn cài đặt & tái lập
├── db/
│   ├── schema.sql                                    # DDL CSDL 7 bảng chuẩn 3NF (có customers)
│   └── seed.sql                                      # Dữ liệu mẫu chuẩn của ca bài toán
├── docs/                                             # Tài liệu phân tích và thiết kế BT1 & BT2
│   ├── srs.md                                        # Bản đặc tả 7 User Stories & kịch bản Use Case 9 bước
│   ├── thay-doi-thiet-ke.md                          # Ghi nhận thay đổi thiết kế TD-01 -> TD-08
│   ├── api-contract.md                               # Đặc tả hợp đồng OpenAPI / RESTful
│   ├── ai-disclosure.md                              # Cam kết liêm chính AI (Nguyễn Minh Phú - 2374802013447)
│   ├── usecase.drawio / usecase.png                  # Sơ đồ Use Case (kèm Bảng chú thích Legend)
│   ├── architecture.drawio / architecture.png        # Sơ đồ Kiến trúc 4 lớp (kèm Chú thích 1 chiều)
│   ├── erd.drawio / erd.png                          # Sơ đồ ERD 7 bảng chuẩn 3NF (kèm Chú thích PK/FK/Index)
│   ├── wireframe.drawio / wireframe.png              # Wireframe 3 màn hình (kèm UI Legend & Ánh xạ)
│   ├── BT1_2374802013447_NguyenMinhPhu.pdf           # File nộp BT1 (12 trang hoàn chỉnh)
│   ├── BT2_2374802013447_NguyenMinhPhu.pdf           # File lưu trữ nộp BT2
│   └── screenshots/
│       ├── api_test_result.png                       # Minh chứng kiểm thử API Sprint 1 (Buổi 8)
│       ├── buoi10_unit_tests.png                     # Minh chứng 17 Unit Tests PASS (Buổi 10)
│       └── buoi10_e2e_result.png                     # Minh chứng luồng chạy End-to-End (Buổi 10)
├── src/                                              # Mã nguồn hệ thống
│   ├── api/
│   │   ├── client.js                                 # HTTP Client dùng chung, xử lý token & mã lỗi 401
│   │   └── ticket.api.js                             # API Adapter đóng gói toàn bộ gọi API nghiệp vụ phiếu
│   ├── config/
│   │   └── database.js                               # Cấu hình SQLite, tự động migrate & nạp seed data
│   ├── presentation/
│   │   └── controllers/
│   │       └── ticketController.js                   # Lớp Trình bày: Tiếp nhận request & trả JSON chuẩn
│   ├── services/
│   │   └── ticketService.js                          # Lớp Nghiệp vụ: Chứa 100% logic QT-04, QT-06, QT-07, QT-08, QT-09
│   ├── repositories/
│   │   └── ticketRepository.js                       # Lớp Truy cập Dữ liệu: Che giấu chi tiết SQL
│   ├── public/                                       # Giao diện Web Frontend (3 Màn hình theo Wireframe BT1)
│   │   ├── index.html                                # Giao diện M1, M2, M3 & Modal đăng nhập
│   │   ├── css/style.css                             # Bố cục hiện đại theo tone màu Navy Văn Lang (#1F4E78)
│   │   └── js/
│   │       ├── api/client.js                         # Client HTTP Frontend tự động bắt 401
│   │       ├── api/ticket.api.js                     # Adapter API Frontend (Không gọi fetch trực tiếp từ view)
│   │       ├── components/DataState.js               # Đóng gói 3 trạng thái: Đang tải, Rỗng, Lỗi kèm Thử lại
│   │       └── app.js                                # Điều phối tương tác giao diện người dùng
│   └── app.js                                        # Express REST API Server & phục vụ static web
└── tests/
    ├── ticket.service.test.js                        # Bộ 17 Unit Tests cho lớp Nghiệp vụ (Buổi 10)
    ├── test_end_to_end.js                            # Script kiểm thử tích hợp toàn luồng End-to-End (Buổi 10)
    └── test_api.js                                   # Script kiểm thử API cơ bản Sprint 1 (Buổi 8)
```

---

## 📌 MỤC 5. HƯỚNG DẪN TRẢI NGHIỆM GIAO DIỆN WEB (3 MÀN HÌNH M1, M2, M3)
Truy cập `http://localhost:3000` trên trình duyệt:
1. **Đăng nhập:**
   - Bấm nút **Đăng nhập** ở góc phải trên cùng.
   - Tài khoản mẫu: `quanly` | Mật khẩu: `123456`.
2. **Màn hình M1 (Danh sách chờ & Tải KTV):**
   - Lọc phiếu theo từng trung tâm bảo hành (Cần Thơ / An Giang).
   - Xem tải công việc hiện hành của từng kỹ thuật viên (số phiếu đang giữ, trạng thái).
   - Bấm nút **"⚡ Gợi ý KTV (M2)"** tại một phiếu bất kỳ để chuyển thẳng sang Màn hình M2.
3. **Màn hình M2 (Phân công & Chuyển gán phiếu):**
   - Xem chi tiết thông tin khách hàng (lấy từ bảng `customers` theo phản hồi TD-05) và hạn SLA (QT-04).
   - Xem bảng gợi ý kỹ thuật viên đạt chuẩn tay nghề ($\ge 3$ theo QT-07) và tải ít nhất.
   - Chọn KTV và bấm **"✅ Xác nhận phân công"**.
   - Nếu cần chuyển phiếu: Bấm **"🔄 Đổi sang Chuyển gán (Re-assign)"** $\to$ Nhập lý do chuyển ($\ge 10$ ký tự theo QT-08) và xác nhận.
   - Theo dõi toàn bộ lịch sử thay đổi ở bảng **Audit Log** bên dưới.
4. **Màn hình M3 (Đặt & Quản lý lịch hẹn):**
   - Chọn phiếu bảo hành cần hẹn.
   - Chọn loại lịch (Tiếp nhận máy / Trả máy), ngày giờ và ghi chú.
   - Bấm **"📅 Xác nhận lưu lịch hẹn"**. Hệ thống kiểm soát tự động quy tắc **QT-09**: Nếu cùng khung giờ 30 phút đã có 5 lịch hẹn, hệ thống sẽ cảnh báo từ chối đặt thêm.
5. **Kiểm thử xử lý mã lỗi 401 (Tiêu chí Buổi 10):**
   - Bấm nút **"⚡ Thử mã 401"** trên thanh tiêu đề: Hệ thống sẽ gọi API giả lập lỗi 401, tự động xóa token phiên làm việc, hiển thị thông báo và mở form đăng nhập lại.
6. **Kiểm thử trạng thái lỗi kèm nút thử lại (`DataState`):**
   - Tắt terminal server (`Ctrl + C`) $\to$ F5 lại trang web $\to$ Màn hình hiện thông báo lỗi mạng màu đỏ kèm nút **"🔄 Thử lại ngay"**.

---

## 📌 MỤC 6. ĐỐI CHIẾU CHECKLIST 10 MỤC KIỂM CHỨNG BUỔI 10 (SPRINT 2)
| STT | Mục kiểm chứng theo Slide Buổi 10 | Trạng thái thực tế | Ghi chú minh chứng |
| :---: | :--- | :---: | :--- |
| **1** | Module mở rộng theo track đã hiện thực và chạy được | **ĐẠT (PASS)** | Frontend 3 màn hình M1, M2, M3 kết nối API thật. |
| **2** | **Luồng chính chạy END-TO-END không lỗi treo** | 🔴 **ĐẠT (PASS)** | Đã kiểm thử tự động toàn bộ 8 bước qua `npm run test:e2e`. |
| **3** | Đã chạy trên dữ liệu mẫu THẬT, không phải dữ liệu tự gõ | **ĐẠT (PASS)** | Dữ liệu khởi tạo từ database SQLite và seed 7 bảng quan hệ 3NF. |
| **4** | Đã chụp ảnh kết quả toàn luồng, lưu vào `docs/` | **ĐẠT (PASS)** | Lưu tại `docs/screenshots/buoi10_e2e_result.png`. |
| **5** | **$\ge 5$ unit test chạy PASS; hiển thị số test trên màn hình** | 🔴 **ĐẠT (PASS)** | **17 Unit Tests PASS 100%** qua `npm test`. |
| **6** | Có ít nhất 1 test cho trường hợp BIÊN hoặc luồng ngoại lệ | **ĐẠT (PASS)** | Có 4 test biên: QT-04, QT-07 (tay nghề đúng bằng 3), QT-08 (lý do đúng 10 ký tự), QT-09 (khung giờ còn đúng 1 slot). |
| **7** | Ba trạng thái (đang tải, rỗng, lỗi) đã xử lý cho ít nhất 1 màn hình | **ĐẠT (PASS)** | Cài đặt trong `DataState.js` và áp dụng cho cả M1, M2, M3. |
| **8** | README mục 3 đã điền đủ các bước chạy, mỗi bước một lệnh | **ĐẠT (PASS)** | Đầy đủ 7 bước, mỗi bước 1 lệnh độc lập tại Mục 3 ở trên. |
| **9** | **ĐÃ THỬ clone repo vào thư mục mới và chạy theo đúng README** | 🔴 **ĐẠT (PASS)** | Đã kiểm chứng clone sang thư mục độc lập và chạy thành công. |
| **10**| Đã commit theo quy ước; tổng số commit của repo $\ge 8$ | **ĐẠT (PASS)** | Lịch sử commit theo chuẩn Conventional Commits (`feat:`, `docs:`, `chore:`). |
