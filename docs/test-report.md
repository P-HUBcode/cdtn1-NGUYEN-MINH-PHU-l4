# BÁO CÁO KẾT QUẢ KIỂM THỬ THỰC TẾ (TEST REPORT)
## LUỒNG L4: PHÂN CÔNG KỸ THUẬT VIÊN VÀ LỊCH HẸN BẢO HÀNH
**Môn học:** Chuyên đề tốt nghiệp 1 (232_71ITBS40103_01 — HK261)  
**Trường Đại học Văn Lang — Khoa Công nghệ Thông tin**  
**Sinh viên thực hiện:** Nguyễn Minh Phú — MSSV: 2374802013447  
**Track:** SE (Software Engineering) | **Giai đoạn 3 (Buổi 13–18) — Bài tập 3**  
**Repository:** [https://github.com/P-HUBcode/cdtn1-NGUYEN-MINH-PHU-l4](https://github.com/P-HUBcode/cdtn1-NGUYEN-MINH-PHU-l4)  
**Thư mục ảnh minh chứng:** [docs/screenshots/](./screenshots/)  

---

### 1. TỔNG HỢP KẾT QUẢ KIỂM THỬ

* **Tổng số test cases đã chạy thật:** **12 / 12 test cases**
* **Số ca kiểm thử đạt (PASS):** **12 / 12 (100%)**
* **Số ca kiểm thử không đạt (FAIL):** **0 (0%)**
* **Bao phủ đầy đủ 5 nhóm kiểm thử bắt buộc theo tiêu chí C2 của Bài tập 3:**
  1. **Luồng đúng (Happy Path):** 5 tests (`TC-01`, `TC-02`, `TC-03`, `TC-04`, `TC-05`) — Bao phủ 100% quy tắc nghiệp vụ (`QT-04`, `QT-06`, `QT-07`, `QT-08`, `QT-09`, `FR6/US5`).
  2. **Giá trị biên (Boundary):** 3 tests (`TC-06`, `TC-07`, `TC-08`) — Kiểm thử 2 phía ranh giới (tay nghề = 3 vs 2; lý do = 10 vs 9 ký tự; slot lịch hẹn = 4 $\to$ 5 vs 5 $\to$ 6).
  3. **Dữ liệu sai & Ngoại lệ (Exceptions):** 2 tests (`TC-09`, `TC-10`) — Kiểm mã trạng thái HTTP 400, thông báo lỗi tiếng Việt, không làm sập server, rollback CSDL an toàn.
  4. **Bảo mật & Phân quyền [SE] (Security / Access Control - OWASP A01):** 1 test (`TC-11`) — Kiểm soát truy cập theo quyền sở hữu (KTV khác bị từ chối với HTTP 403 Forbidden).
  5. **Tính tái lập (Reproducibility):** 1 test (`TC-12`) — Chạy nạp migration & seed lần 2 cho kết quả đồng nhất, không trùng khóa, không nhân đôi số bản ghi (C5).

---

### 2. BẢNG CHI TIẾT 12 CA KIỂM THỬ ĐÃ CHẠY THẬT (CHUẨN 8 CỘT)

| Mã test & Loại | Tiền điều kiện | Các bước thực hiện | Dữ liệu thử | Kết quả mong đợi | Mức ưu tiên | Kết quả thực tế (Đo lường chi tiết & Tác dụng phụ) | PASS / FAIL |
| :---: | :--- | :--- | :--- | :--- | :---: | :--- | :---: |
| **TC-01**<br>*(Luồng đúng)* | Đã có thời điểm tiếp nhận phiếu bảo hành hợp lệ. | 1. Gọi hàm tính SLA: `calculateSlaDueDate(receivedDate, priority)`<br>2. Kiểm tra chuỗi trả về | `receivedDate = "2026-10-15T08:00:00.000Z"`<br>`priority = "CAO"` | `due_date` được cộng chính xác **+24 giờ** $\to$ `"2026-10-16T08:00:00.000Z"` theo quy tắc QT-04. | **Cao** | Giá trị trả về: `"2026-10-16T08:00:00.000Z"`. Hàm thuần túy, 0 tác dụng phụ, không ghi CSDL.<br>*(Minh chứng: [TC-01.png](./screenshots/TC-01.png))* | **PASS** |
| **TC-02**<br>*(Luồng đúng)* | Phiếu bảo hành #1 ở trạng thái `MOI`, trung tâm tiếp nhận `center_id = 1` (Cần Thơ). | 1. Quản lý gọi `POST /api/v1/tickets/1/assign`<br>2. Gửi mã KTV #1 (Trần Văn Bình, tay nghề 5/5). | Body: `{"technicianId": 1}`<br>Role: `MANAGER` | HTTP 200 OK. Phiếu đổi sang `DANG_XU_LY`, gán `technician_id = 1`, ghi log `ticket_status_log`. | **Cao** | HTTP 200 OK. Response: `{"success": true, "status": "DANG_XU_LY"}`. Đếm `tickets` trước/sau: 9 $\to$ 9; thêm 1 dòng log kiểm toán.<br>*(Minh chứng: [TC-02.png](./screenshots/TC-02.png))* | **PASS** |
| **TC-03**<br>*(Luồng đúng)* | Phiếu #1 đang do KTV #1 phụ trách. Quản lý cần đổi sang KTV #2 (Lê Văn Cường). | 1. Quản lý gọi `POST /api/v1/tickets/1/reassign`<br>2. Gửi mã KTV mới và lý do nghiệp vụ $\ge 10$ ký tự. | Body: `{"newTechnicianId": 2, "reason": "KTV cu di cong tac dot xuat tai tinh"}` | HTTP 200 OK. `technician_id` đổi sang 2, lưu lý do chuyển gán vào `ticket_status_log` theo QT-08. | **Trung bình** | HTTP 200 OK. `reason` có 38 ký tự (> 10). Bảng `tickets.technician_id` đổi thành 2, thêm 1 bản ghi log.<br>*(Minh chứng: [TC-03.png](./screenshots/TC-03.png))* | **PASS** |
| **TC-04**<br>*(Luồng đúng)* | Phiếu bảo hành đã tiếp nhận. Khung giờ 09:00 - 09:30 ngày 15/11/2026 hiện có 2 lịch hẹn (2/5). | 1. Gọi `POST /api/v1/tickets/1/appointments`<br>2. Chọn loại hẹn và khung giờ. | Body: `{"appointmentType": "GIAO_MAY", "appointmentTime": "2026-11-15T09:00:00Z"}` | HTTP 201 Created. Tạo lịch hẹn thành công, trạng thái `DA_XAC_NHAN` theo quy tắc QT-09. | **Trung bình** | HTTP 201 Created. Cấp `appointmentId = 82`. Số lịch trong slot tăng 2 $\to$ 3 (vẫn $\le 5$).<br>*(Minh chứng: [TC-04.png](./screenshots/TC-04.png))* | **PASS** |
| **TC-05**<br>*(Luồng đúng)* | Phiếu #1 đang ở trạng thái `DANG_XU_LY` do KTV #2 phụ trách. | 1. KTV #2 gọi `POST /api/v1/tickets/1/status`<br>2. Cập nhật sang `CHO_LINH_KIEN` kèm ghi chú. | Header: `X-Technician-Id: 2`<br>Body: `{"status": "CHO_LINH_KIEN", "note": "Cho man hinh tu kho ve"}` | HTTP 200 OK. Phiếu đổi trạng thái, ghi chú lưu vào `ticket_status_log` (tiêu chí FR6/US5). | **Cao** | HTTP 200 OK. `status` đổi thành `CHO_LINH_KIEN`. Bảng `ticket_status_log` ghi nhận sự kiện kèm ghi chú.<br>*(Minh chứng: [TC-05.png](./screenshots/TC-05.png))* | **PASS** |
| **TC-06**<br>*(Giá trị biên)* | Ranh giới tay nghề KTV theo QT-07: ngưỡng tối thiểu là `proficiency >= 3`. | 1. Thử nghiệm với KTV có tay nghề đúng bằng 3 (`proficiency = 3`).<br>2. Thử nghiệm với KTV tay nghề 2 (`proficiency = 2`). | Subtest 1: `proficiency = 3`<br>Subtest 2: `proficiency = 2` | Subtest 1: PASS (Hợp lệ).<br>Subtest 2: Bị từ chối với mã lỗi `TAY_NGHE_KHONG_DAT` (HTTP 400). | **Cao** | Điểm biên 3: PASS, hợp lệ.<br>Điểm biên 2: Ném `LoiNghiepVu('TAY_NGHE_KHONG_DAT')`. Đo chính xác 2 phía ranh giới.<br>*(Minh chứng: [TC-06.png](./screenshots/TC-06.png))* | **PASS** |
| **TC-07**<br>*(Giá trị biên)* | Ranh giới độ dài lý do chuyển gán theo QT-08: ngưỡng tối thiểu là 10 ký tự. | 1. Thử nghiệm với chuỗi lý do đúng 10 ký tự.<br>2. Thử nghiệm với chuỗi lý do 9 ký tự. | Subtest 1: `"1234567890"` (10 ký tự)<br>Subtest 2: `"123456789"` (9 ký tự) | Subtest 1: PASS.<br>Subtest 2: Bị từ chối với mã lỗi `LY_DO_QUA_NGAN` (HTTP 400). | **Trung bình** | 10 ký tự: Hợp lệ, cho phép chuyển gán.<br>9 ký tự: Ném `LoiNghiepVu('LY_DO_QUA_NGAN')`. Đo chính xác 2 phía ranh giới.<br>*(Minh chứng: [TC-07.png](./screenshots/TC-07.png))* | **PASS** |
| **TC-08**<br>*(Giá trị biên)* | Ranh giới tải khung giờ lịch hẹn theo QT-09: tối đa 5 lịch trong 30 phút. | 1. Khung giờ đã có 4 lịch, đặt thêm lịch thứ 5.<br>2. Khung giờ đã có 5 lịch, cố tình đặt thêm lịch thứ 6. | Subtest 1: Slot hiện tại 4/5 $\to$ nạp 1 lịch.<br>Subtest 2: Slot hiện tại 5/5 $\to$ nạp 1 lịch. | Subtest 1: PASS (5/5).<br>Subtest 2: Bị từ chối với mã lỗi `LICH_HEN_QUA_TAI` (HTTP 409). | **Cao** | Lịch thứ 5: Cấp lịch thành công (5/5).<br>Lịch thứ 6: Bị chặn với lỗi `LICH_HEN_QUA_TAI`. Số lịch trong slot giữ nguyên 5.<br>*(Minh chứng: [TC-08.png](./screenshots/TC-08.png))* | **PASS** |
| **TC-09**<br>*(Dữ liệu sai)* | Phiếu bảo hành #1 thuộc trung tâm Cần Thơ (`center_id = 1`). | 1. Quản lý cố tình phân công KTV #99 thuộc trung tâm Mỹ Tho (`center_id = 2`). | Body: `{"technicianId": 99}`<br>Role: `MANAGER` | HTTP 400 Bad Request.<br>Mã lỗi: `KTV_KHAC_TRUNG_TAM`. Hệ thống từ chối, không sập. | **Cao** | HTTP 400 Bad Request. Body: `{"error": "KTV_KHAC_TRUNG_TAM", "message": "...", "requestId": "req-8a4bf291"}`. Bảng `tickets` giữ nguyên.<br>*(Minh chứng: [TC-09.png](./screenshots/TC-09.png))* | **PASS** |
| **TC-10**<br>*(Dữ liệu sai)* | Phiếu bảo hành #3 đã hoàn tất sửa chữa (`status = 'HOAN_TAT'`). | 1. Gọi `POST /api/v1/tickets/3/status` cố tình chuyển ngược về `DANG_XU_LY`. | Body: `{"status": "DANG_XU_LY", "note": "Thu sua lai phieu da xong"}` | HTTP 400 Bad Request.<br>Mã lỗi: `PHIEU_DA_HOAN_TAT` (BUG-006). Khóa vĩnh viễn trạng thái. | **Cao** | HTTP 400 Bad Request. Body: `{"error": "PHIEU_DA_HOAN_TAT", "message": "..."}`. Trạng thái phiếu #3 vẫn giữ nguyên là `HOAN_TAT`.<br>*(Minh chứng: [TC-10.png](./screenshots/TC-10.png))* | **PASS** |
| **TC-11**<br>*(Bảo mật / Phân quyền)* | Phiếu #1 đang được phân công cho KTV #2 (Lê Văn Cường). | 1. KTV #3 (Nguyễn Thị Dung) gửi request cập nhật tiến độ cho phiếu #1. | Header: `X-User-Role: TECHNICIAN`<br>`X-Technician-Id: 3` | HTTP 403 Forbidden.<br>Mã lỗi: `FORBIDDEN`. Kiểm soát truy cập theo quyền sở hữu (A01 OWASP). | **Cao** | HTTP 403 Forbidden. Body: `{"error": "FORBIDDEN", "message": "Ban khong co quyen cap nhat phieu..."}`. 0 bản ghi CSDL bị sửa.<br>*(Minh chứng: [TC-11.png](./screenshots/TC-11.png))* | **PASS** |
| **TC-12**<br>*(Tính tái lập)* | Hệ thống đã khởi động và nạp dữ liệu mẫu 9 phiếu bảo hành. | 1. Dừng server và chạy lại `node src/app.js` lần thứ hai.<br>2. Kiểm tra tính toàn vẹn CSDL. | Script khởi động lại server trên cùng file `warranty.sqlite`. | Không phát sinh lỗi trùng khóa chính (`SQLITE_CONSTRAINT`), không nhân đôi bản ghi (C5). | **Cao** | Chạy thành công. `COUNT(tickets)` lần 1: 9; lần 2: 9. Số lượng KTV: 3 $\to$ 3. Idempotent CSDL 100% đạt chuẩn.<br>*(Minh chứng: [TC-12.png](./screenshots/TC-12.png))* | **PASS** |

---

### 3. ĐỐI CHIẾU TIÊU CHÍ MINH BẠCH & LIÊM CHÍNH (SLIDE 6 & 7)

* **Cột kết quả thực tế:** Được ghi nhận bằng các số đo định lượng có thể kiểm chứng (mã HTTP status, mã lỗi máy đọc, đếm số bản ghi trước/sau, kiểm tra tác dụng phụ không gây rác dữ liệu).
* **Minh chứng độc lập:** 100% các ca kiểm thử đều có ảnh chụp màn hình terminal tương ứng được lưu trữ tại `docs/screenshots/TC-xx.png`.
* **Sẵn sàng vấn đáp tại lớp:** Sinh viên nắm vững cách tái lập và thực thi độc lập từng ca kiểm thử khi Giảng viên chỉ định ngẫu nhiên trong buổi Workshop.
