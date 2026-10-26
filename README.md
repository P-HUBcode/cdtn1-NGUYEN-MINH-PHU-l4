# BÀI TẬP 2: HỆ THỐNG SMART CRM - MEKONG MOBILE
## LUỒNG L4: PHÂN CÔNG KỸ THUẬT VIÊN VÀ LỊCH HẸN BẢO HÀNH
### Tiến độ: Hoàn thành đến Buổi 11 (Tích hợp hệ thống, Xử lý lỗi xuyên lớp & Đóng gói Docker) — Sẵn sàng cho Workshop Buổi 12

**Thông tin sinh viên:**
- **Họ và tên:** Nguyễn Minh Phú
- **Mã số sinh viên (MSSV):** 2374802013447
- **Lớp học phần:** 232_71ITBS40103_01
- **Chuyên ngành (Track):** SE (Software Engineering - Kỹ thuật phần mềm)
- **Giảng viên hướng dẫn:** TS. Nguyễn Trí Hải / ThS. Nguyễn Minh Tân / ThS. Trần Công Thanh
- **Repository GitHub:** [https://github.com/P-HUBcode/cdtn1-NGUYEN-MINH-PHU-l4](https://github.com/P-HUBcode/cdtn1-NGUYEN-MINH-PHU-l4)
- **Phiên bản phát hành (Tag):** [`v0.2`](https://github.com/P-HUBcode/cdtn1-NGUYEN-MINH-PHU-l4/releases/tag/v0.2)

---

## 📌 MỤC 1. PHẠM VI NGHIỆP VỤ LUỒNG L4 (1 CÂU TÓM TẮT)
> **Phạm vi diễn đạt bằng 1 câu:** Hệ thống hỗ trợ Quản lý trung tâm bảo hành phân công phiếu bảo hành cho kỹ thuật viên phù hợp dựa trên tay nghề (proficiency $\ge 3$), cùng trung tâm và tải công việc hiện tại; cho phép tiếp nhận đặt và quản lý lịch hẹn giao – nhận máy với khách hàng (tối đa 5 lịch/khung giờ 30 phút), đồng thời tự động tính toán hạn cam kết SLA và lưu vết toàn diện nhật ký thay đổi trạng thái (Audit Log).

---

## 📌 MỤC 2. YÊU CẦU MÔI TRƯỜNG & PHIÊN BẢN RUNTIME
Để đảm bảo nguyên tắc **TÁI LẬP ĐƯỢC (Reproducibility)** theo chuẩn Buổi 11:
- **Runtime:** Node.js version **20 LTS** (hoặc v22.x LTS). Đã kiểm chứng tương thích 100% trên cả Windows, Linux và macOS.
- **Package Manager:** `npm` v10.x trở lên. Tệp khóa phiên bản `package-lock.json` được commit bắt buộc để phục vụ lệnh `npm ci`.
- **Cơ sở dữ liệu:** SQLite 3 với engine tích hợp sẵn `node:sqlite` (tự động khởi tạo schema 7 bảng chuẩn 3NF và nạp seed data khi máy chủ khởi động — Idempotent C5).
- **Docker (Tùy chọn nâng cao):** Docker Desktop hoặc Docker Engine version 24+ / Docker Compose v2.

---

## 📌 MỤC 3. CÁC BƯỚC DỰNG VÀ CHẠY HỆ THỐNG (MỖI BƯỚC MỘT LỆNH)

### Cách 1: Chạy trực tiếp trên máy cục bộ (Node.js)
```bash
# Bước 1: Clone mã nguồn với đúng tag v0.2
git clone --branch v0.2 https://github.com/P-HUBcode/cdtn1-NGUYEN-MINH-PHU-l4.git

# Bước 2: Di chuyển vào thư mục dự án
cd cdtn1-NGUYEN-MINH-PHU-l4

# Bước 3: Cài đặt chính xác các phụ thuộc theo tệp khóa package-lock.json
npm ci

# Bước 4: Khởi tạo tệp cấu hình môi trường .env (chạy được trên mọi hệ điều hành Windows/macOS/Linux)
npm run setup

# Bước 5: Chạy bộ kiểm thử tự động (38 Unit Tests PASS 100%)
npm test

# Bước 6: Chạy kiểm thử tích hợp toàn luồng End-to-End (M1 -> M2 -> KTV Update -> M3)
npm run test:e2e

# Bước 7: Khởi chạy máy chủ ứng dụng
npm start
```
*Mở trình duyệt tại: **`http://localhost:3000`**.*

> **💡 Ghi chú Bước 4:** Bạn cũng có thể dùng lệnh sao chép của hệ điều hành thay cho `npm run setup`:
> - Trên Linux / macOS / PowerShell: `cp .env.example .env`
> - Trên Windows CMD thông thường: `copy .env.example .env`

### Cách 2: Chạy bằng Docker Compose (≤ 2 lệnh từ máy chưa cài gì — Chuẩn Buổi 11)
```bash
# Bước 1: Khởi tạo biến môi trường
cp .env.example .env

# Bước 2: Dựng image và chạy container ở chế độ nền
docker compose up -d --build
```
- Xem log JSON thời gian thực: `docker compose logs -f app --tail 50`
- Kiểm tra trạng thái healthcheck: `docker compose ps`
- Dừng hệ thống: `docker compose down`

---

## 📌 MỤC 4. KIẾN TRÚC HỆ THỐNG & TÁCH LỚP (C2 & CỐT LÕI)
Hệ thống tuân thủ mô hình kiến trúc 3 lớp phân tách ranh giới rõ ràng:
1. **Lớp Trình bày (Presentation Layer):**
   - Web UI tĩnh tại `src/public/` (M1, M2, M3) giao tiếp với API qua `src/public/js/api/client.js` và `src/public/js/api/ticket.api.js`. Hoàn toàn không có lệnh `fetch(` trong view logic.
   - Thành phần `DataState.js` xử lý chuẩn 3 trạng thái: Đang tải (Spinner), Rỗng, và Lỗi (kèm nút Thử lại).
   - Controller tại `src/presentation/controllers/ticketController.js`: tiếp nhận request, chuyển dữ liệu vào Service và phản hồi JSON. Không chứa logic nghiệp vụ.
   - Hợp đồng Dữ liệu Ranh giới (`src/services/ticket.contract.js`): Chuẩn hóa dữ liệu trả về cho lớp giao diện bằng `toTicketView(rawTicket)`, triệt tiêu phụ thuộc ngầm CSDL, format chuẩn ISO 8601 và che số điện thoại khách hàng theo quy tắc QT-15 (`maskPhoneNumber`).
2. **Lớp Nghiệp vụ (Business Service Layer):**
   - `src/services/ticketService.js`: Độc lập hoàn toàn với HTTP (không có `req`, `res`, HTTP status). Chứa 100% logic của các quy tắc:
     - **QT-04:** Tính hạn cam kết SLA `due_date` dựa trên độ ưu tiên (CAO +24h, TRUNG_BINH +48h, THAP +72h).
     - **QT-06 & QT-07:** Ràng buộc KTV cùng trung tâm tiếp nhận, trạng thái hoạt động và tay nghề $\ge 3$.
     - **QT-08:** Ràng buộc lý do chuyển gán (Re-assign) tối thiểu 10 ký tự.
     - **QT-09:** Khống chế tải lịch hẹn tối đa 5 lịch trong khung giờ 30 phút.
     - **FR6 & US5:** Quy tắc chuyển đổi trạng thái tiến độ KTV (`validateStatusTransition` và `updateTicketStatus`).
     - **toTicketView:** Bảo vệ hợp đồng dữ liệu hiển thị, fallback an toàn khi khách hàng thiếu họ tên hoặc KTV chưa gán.
   - Khi vi phạm nghiệp vụ: ném `LoiNghiepVu` mang mã lỗi máy đọc (`ma`) và thông điệp tiếng Việt.
3. **Lớp Truy cập Dữ liệu (Repository Layer):**
   - `src/repositories/ticketRepository.js`: Đóng gói 100% câu lệnh SQL đối với SQLite 3. Bọc lỗi kỹ thuật CSDL thành `LoiTruyCapDuLieu`. Không biết HTTP status, không ghi log tại đây.
4. **Hạ tầng Xử lý lỗi & Logging tập trung (Buổi 11):**
   - `src/errors.js`: Phân cấp lỗi ứng dụng (`LoiNghiepVu`, `LoiTruyCapDuLieu`).
   - `src/utils/logger.js`: Logger cấu trúc JSON ra `stdout`, tự động khử độc dữ liệu nhạy cảm (Data Redaction: password, token, SĐT).
   - `src/middleware/requestId.js`: Cấp phát `requestId` duy nhất theo dõi xuyên suốt request.
   - `src/middleware/errorHandler.js`: Nơi duy nhất ánh xạ lỗi sang HTTP Status và ghi log đúng 1 lần tại đỉnh hệ thống.

---

## 📌 MỤC 5. BỘ KIỂM THỬ TỰ ĐỘNG (38 TESTS PASS 100% — C4)
Hệ thống tích hợp bộ 38 unit tests chạy qua lệnh `npm test` (kết hợp `tests/ticket.service.test.js` và `tests/ticket.contract.test.js`) với độ bao phủ đầy đủ các nhóm ca kiểm thử:
1. **Luồng đúng (Happy Path):** SLA CAO (+24h), SLA TRUNG_BINH (+48h), SLA THAP (+72h), KTV tay nghề 5/5 cùng trung tâm, Lý do chuyển gán hợp lệ, Slot lịch hẹn còn chỗ (2/5).
2. **Trường hợp Biên (Boundary):**
   - KTV có tay nghề đúng bằng 3 (ngưỡng tối thiểu của QT-07).
   - Lý do chuyển gán đúng 10 ký tự (ngưỡng tối thiểu của QT-08).
   - Khung giờ hẹn đã có đúng 4 lịch (còn đúng 1 slot cuối cùng của QT-09).
3. **Dữ liệu sai & Ngoại lệ (Exceptions):**
   - Mức ưu tiên không hợp lệ hoặc ngày tiếp nhận rỗng.
   - KTV có tay nghề $< 3$ (bị từ chối theo QT-07).
   - KTV khác trung tâm (bị từ chối theo QT-06).
   - KTV đang nghỉ phép `NGHI_PHEP`.
   - Lý do chuyển gán $< 10$ ký tự hoặc để trống.
   - Khung giờ đã đầy 5/5 lịch hẹn (bị từ chối theo QT-09).
4. **Kiểm thử hồi quy (Regression Tests cho `docs/bug-log.md`):**
   - Test hồi quy `BUG-001`: Mã lỗi `LY_DO_QUA_NGAN`.
   - Test hồi quy `BUG-002`: Mã lỗi `LICH_HEN_QUA_TAI`.
   - Test hồi quy `BUG-003`: Mã lỗi `KTV_KHAC_TRUNG_TAM`.
   - Test hồi quy `BUG-004`: `toTicketView` bảo toàn hợp đồng hiển thị khi khách hàng thiếu tên hoặc null.
5. **Kiểm thử Hợp đồng Ranh giới (Boundary Contract Tests — Buổi 09):**
   - Đảm bảo 100% các khóa bắt buộc của View (`ticket_code`, `status`, `technician_name`, `customer_phone`...).
   - Định dạng ngày tháng chuẩn ISO 8601 (`YYYY-MM-DDTHH:mm:ssZ`).
   - Quy tắc bảo mật dữ liệu cá nhân QT-15: Che giấu số điện thoại 10 số (ví dụ: `0901234567` $\to$ `090****567`).
   - Xử lý giá trị mặc định cho KTV chưa phân công (`"Chưa phân công"`).
   - Xử lý an toàn khi đầu vào null mà không làm crash ứng dụng.
6. **Kiểm thử Tiến độ Kỹ thuật viên & Khóa hoàn tất (FR6, US5, BUG-006):**
   - KTV chuyển `DANG_XU_LY` $\to$ `CHO_LINH_KIEN` thành công kèm ghi chú.
   - KTV chuyển `DANG_XU_LY` $\to$ `HOAN_TAT` thành công.
   - AC5.2: Chặn cập nhật khi phiếu còn ở trạng thái `MOI` với mã lỗi `PHIEU_CHUA_PHAN_CONG`.
   - Phân quyền: Chặn KTV khác cập nhật phiếu không thuộc về mình với mã lỗi `FORBIDDEN`.
   - Phân quyền: Quản lý được phép cập nhật nghiệm thu tiến độ.
   - Chặn trạng thái không hợp lệ (`TRANG_THAI_KHONG_HOP_LE`).
   - Chặn cập nhật trùng trạng thái (`TRANG_THAI_TRUNG_LAP`).
   - Chặn ghi chú rỗng hoặc $< 3$ ký tự (`THIEU_GHI_CHU_TIEN_DO`).
   - Khóa vĩnh viễn (BUG-006): Chặn KTV cập nhật khi phiếu đã `HOAN_TAT` với mã lỗi `PHIEU_DA_HOAN_TAT`.
   - Khóa vĩnh viễn (BUG-006): Kể cả Quản lý cũng không được đổi trạng thái khi phiếu đã `HOAN_TAT`.

---

## 📌 MỤC 6. KỊCH BẢN DEMO NHANH 3 PHÚT (CHUẨN BỊ CHO WORKSHOP BUỔI 12)
Tại buổi Workshop chấm điểm Buổi 12 sắp tới, sinh viên chuẩn bị sẵn sàng 4 nội dung đúng khung 3 phút:
1. **Chặng 1 (60s) — Luồng chính End-to-End:**
   - Mở giao diện `http://localhost:3000`, đăng nhập bằng tài khoản `quanly`.
   - Tại **M1**: Xem danh sách phiếu, thử các nút sắp xếp mức ưu tiên và tìm kiếm tức thời theo tên khách hàng / SĐT / KTV.
   - Tại **M2**: Xem danh sách KTV gợi ý (sắp xếp tăng dần theo tải), chọn KTV tay nghề 5/5 và bấm "Xác nhận phân công". Bấm "Đổi sang Chuyển gán", nhập lý do $\ge 10$ ký tự và chuyển cho KTV khác.
   - Đăng nhập tài khoản `ktv_binh`: Bấm *"🔍 Chỉ xem phiếu của tôi"* $\to$ M1 lọc đúng phiếu được gán $\to$ Bấm *"🛠️ Xử lý phiếu"* $\to$ Tại M2 cập nhật tiến độ sang `CHO_LINH_KIEN` rồi sang `HOAN_TAT` kèm ghi chú kỹ thuật.
   - Tại **M3**: Đặt lịch hẹn giao máy vào khung giờ mong muốn và xác nhận.
2. **Chặng 2 (30s) — Xử lý dữ liệu sai & suy giảm có kiểm soát:**
   - Nhập lý do chuyển gán ngắn (ví dụ: `"KTV bận"`): Hệ thống báo lỗi rõ ràng `"Lý do chuyển gán phiếu phải có tối thiểu 10 ký tự (vi phạm QT-08)"`, không sập ứng dụng.
   - Bấm nút "Thử mã 401": Hệ thống tự động thu hồi phiên và mở modal đăng nhập.
3. **Chặng 3 (30s) — Minh chứng kiểm thử:**
   - Mở terminal chạy `npm test`: Hiển thị rõ **36/36 tests PASS** bằng 1 lệnh.
   - Chạy `npm run test:e2e`: Toàn bộ kịch bản 9 bước tích hợp chạy thành công 100%.
4. **Chặng 4 (60s) — Kể 1 lỗi đã gỡ theo 4 bước (Bug Log):**
   - Mở tệp `docs/bug-log.md`, thuyết minh lỗi **BUG-004** (Khách hàng thiếu tên) hoặc **BUG-005** (KTV xem phiếu của tôi) theo đủ 4 bước: Tái lập $\to$ Khoanh vùng $\to$ Sửa nguyên nhân $\to$ Xác nhận bằng Unit Test.

---

## 📌 MỤC 7. BỘ BA CÂU HỎI CHUẨN CỦA GIẢNG VIÊN (CHUẨN BỊ TRƯỚC)
1. **Câu hỏi 1: Vì sao em chọn cách này mà không phải cách kia?**
   - *Trả lời:* "Để đảm bảo tính Idempotent (C5) khi khởi tạo CSDL, em chọn giải pháp kiểm tra `CREATE TABLE IF NOT EXISTS` và câu lệnh `INSERT OR IGNORE` trong tệp seed, thay vì xóa bảng và tạo lại từ đầu (`DROP TABLE`). Cách này giúp hệ thống khởi động lại nhiều lần mà không bị lỗi trùng khóa chính và không làm mất dữ liệu giao dịch vừa thao tác. Ngoài ra, việc dùng SQLite nhúng giúp người chấm clone về chạy được ngay mà không phụ thuộc vào việc phải cài đặt và cấu hình dịch vụ cơ sở dữ liệu bên ngoài."
2. **Câu hỏi 2: Nếu dữ liệu tăng gấp 10 thì chỗ nào hỏng trước?**
   - *Trả lời:* "Màn hình danh sách phiếu bảo hành (M1) hiện đang lấy toàn bộ dữ liệu phiếu của trung tâm mà chưa phân trang. Khi số phiếu tăng lên hàng chục ngàn bản ghi, câu truy vấn `findAll()` sẽ chiếm nhiều bộ nhớ và giao diện sẽ bị đơ do render quá nhiều phần tử DOM. Cách em giải quyết là bổ sung phân trang kiểu con trỏ (Keyset Pagination) với `LIMIT` và `OFFSET`, đồng thời thêm composite index trên `(center_id, status, due_date)` trong CSDL để tối ưu hóa tốc độ lọc."
3. **Câu hỏi 3: Chỉ cho thầy dòng mã chịu trách nhiệm cho việc này?**
   - *Ràng buộc hạn SLA (QT-04):* `src/services/ticketService.js` (dòng 13–30).
   - *Ràng buộc tay nghề KTV (QT-06, QT-07):* `src/services/ticketService.js` (dòng 39–53) & SQL gợi ý trong `src/repositories/ticketRepository.js` (dòng 64–77).
   - *Ràng buộc lý do chuyển gán (QT-08):* `src/services/ticketService.js` (dòng 60–69).
   - *Ràng buộc tải lịch hẹn 30 phút (QT-09):* `src/services/ticketService.js` (dòng 76–84) & đếm slot trong `src/repositories/ticketRepository.js` (dòng 152–166).
   - *Hợp đồng dữ liệu ranh giới & Che giấu SĐT (QT-15 — Buổi 09):* `src/services/ticket.contract.js` (dòng 1–68) & `toTicketView` trong `src/services/ticketService.js`.
   - *Xử lý lỗi tập trung & Data Redaction (Buổi 11):* `src/middleware/errorHandler.js` và `src/utils/logger.js` (dòng 35–56).

---

## 📌 MỤC 8. BẢNG CHECKLIST NỘP BÀI TẬP 2 (ĐỐI CHIẾU 10 TIÊU CHÍ SLIDE 10)
| STT | Tiêu chí kỹ thuật & hình thức | Trạng thái | Ghi chú minh chứng |
| :---: | :--- | :---: | :--- |
| 1 | Một file PDF duy nhất `BT2_2374802013447_NguyenMinhPhu.pdf` | **HOÀN THÀNH** | Đã biên soạn đủ 7 mục nội dung chuẩn + Phụ lục AI. |
| 2 | Trang bìa có link GitHub repo, tên tag `v0.2`, Track SE, Luồng L4 | **HOÀN THÀNH** | Ghi rõ trên trang bìa PDF và README. |
| 3 | PDF đủ 7 mục: Tóm tắt, Kiến trúc, Module cốt lõi, Test, Kết quả, Dựng lại, Thay đổi | **HOÀN THÀNH** | Đầy đủ cấu trúc 6–9 trang theo quy định. |
| 4 | Ảnh chụp kết quả chạy thật trong PDF (Module chạy, Test PASS, 3 trạng thái) | **HOÀN THÀNH** | Chèn ảnh minh chứng chụp từ terminal và giao diện thực tế. |
| 5 | Phụ lục bảng khai báo sử dụng công cụ AI cụ thể kèm cam kết | **HOÀN THÀNH** | Đầy đủ họ tên, MSSV, ngày 26/10/2026 trong `docs/ai-disclosure.md`. |
| 6 | Tag `v0.2` đã đẩy và trang releases mở được trên GitHub | **HOÀN THÀNH** | Đã tạo và đẩy tag `v0.2`. |
| 7 | Repository để chế độ PUBLIC | **HOÀN THÀNH** | Kiểm tra mở được ở chế độ ẩn danh. |
| 8 | Có `docs/thay-doi-thiet-ke.md` (TD-01 $\to$ TD-10, TD-08b) và `docs/bug-log.md` | **HOÀN THÀNH** | Đầy đủ các quyết định thiết kế và 4 ca bug theo 4 bước. |
| 9 | Không có `.env` thật và secret trong repo; có `.env.example` đầy đủ | **HOÀN THÀNH** | Đã kiểm tra qua `.dockerignore` và `.gitignore`. |
| 10 | Đã nộp file PDF trên VLU E-learning | **SẴN SÀNG** | File PDF sẵn sàng tại `docs/BT2_2374802013447_NguyenMinhPhu.pdf`. |
