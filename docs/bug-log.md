# NHẬT KÝ GỠ LỖI CÓ PHƯƠNG PHÁP (SYSTEMATIC BUG LOG)
**Học phần:** Chuyên đề tốt nghiệp 1 (HK261) — Khoa CNTT, Đại học Văn Lang  
**Sinh viên:** Nguyễn Minh Phú — MSSV: 2374802013447 — Lớp: 232_71ITBS40103_01  
**Track:** SE (Kỹ thuật phần mềm) — Luồng L4: Phân công kỹ thuật viên & Lịch hẹn  
**Repository:** [https://github.com/P-HUBcode/cdtn1-NGUYEN-MINH-PHU-l4](https://github.com/P-HUBcode/cdtn1-NGUYEN-MINH-PHU-l4) (Tag `v0.2`)  
**Quy trình áp dụng:** 4 bước chuẩn Buổi 11: *Tái lập (Reproduce) → Khoanh vùng (Isolate) → Sửa nguyên nhân (Fix Root Cause) → Xác nhận bằng Test hồi quy (Verify)*.

---

## 1. BUG-001 · Major — Re-assign KTV không validate độ dài lý do dẫn đến vi phạm QT-08
1. **Mã và mức độ:** `BUG-001` · Mức độ: **Major** — Thiếu kiểm soát điều kiện chuyển gán phiếu bảo hành.
2. **Phát hiện bởi:** Kiểm thử tự động Sprint 1 (`tests/test_api.js`) & Test case TC-08.
3. **Triệu chứng:** Endpoint `POST /api/v1/tickets/1/reassign` chấp nhận các chuỗi lý do ngắn ngủn như `"bận"`, `"đổi"` và lưu vào CSDL với HTTP 200 thay vì từ chối.
4. **Cách tái lập:** Gửi request chuyển gán với lý do dưới 10 ký tự:
   ```bash
   curl -X POST http://localhost:3000/api/v1/tickets/1/reassign \
     -H "Content-Type: application/json" \
     -d '{"technician_id": 2, "reason": "KTV bận", "user_id": 1}'
   ```
5. **Nguyên nhân:** Lớp controller và service ban đầu chỉ kiểm tra `if (!reason)` mà không kiểm tra độ dài tối thiểu 10 ký tự theo yêu cầu quy định QT-08 trong SRS.
6. **Cách sửa:** Xây dựng hàm nghiệp vụ thuần túy `validateReassignReason(reason)` trong `src/services/ticketService.js`, chuẩn hóa cắt khoảng trắng và kiểm tra `cleanReason.length >= 10`. Nếu vi phạm, ném `LoiNghiepVu('LY_DO_KHONG_HOP_LE', ...)` với HTTP 400.
7. **Commit và xác nhận:** Commit [`08819d9`](https://github.com/P-HUBcode/cdtn1-NGUYEN-MINH-PHU-l4/commit/08819d9) · Unit test `"Dữ liệu sai / Ngoại lệ: Từ chối khi lý do dưới 10 ký tự (vi phạm QT-08)"` trong `tests/ticket.service.test.js` **PASS 100%**.

---

## 2. BUG-002 · Major — Đặt lịch hẹn vượt quá tải trọng 5 lịch / khung giờ 30 phút (QT-09)
1. **Mã và mức độ:** `BUG-002` · Mức độ: **Major** — Vi phạm tải trọng công suất trung tâm bảo hành.
2. **Phát hiện bởi:** Kịch bản kiểm thử tải đồng thời trong kịch bản E2E (`tests/test_end_to_end.js`).
3. **Triệu chứng:** Quản lý có thể tạo liên tiếp 7–10 lịch hẹn vào cùng một khung giờ 09:00 mà hệ thống không đưa ra bất kỳ cảnh báo nào.
4. **Cách tái lập:** Gọi liên tục 6 request đặt lịch hẹn giao/nhận cho cùng một mốc thời gian:
   ```bash
   curl -X POST http://localhost:3000/api/v1/tickets/1/appointments \
     -H "Content-Type: application/json" \
     -d '{"appointment_type": "NHAN_MAY", "appointment_date": "2026-11-15T09:00:00Z"}'
   ```
5. **Nguyên nhân:** Trong `ticketRepository.js`, câu truy vấn kiểm tra lịch hẹn ban đầu chỉ so sánh chuỗi chính xác `=` mà không tính dải dung sai thời gian (Slot window $\pm 15$ phút), dẫn đến các lịch cách nhau vài phút cùng nằm trong 1 slot 30 phút bị tính là slot khác nhau.
6. **Cách sửa:** Cập nhật hàm `countAppointmentsInSlot(appointmentDate)` trong `ticketRepository.js` dùng toán tử `BETWEEN [target - 15m] AND [target + 15m]`, kết hợp hàm kiểm soát `checkAppointmentSlotCapacity(currentCount)` ném `LoiNghiepVu('LICH_HEN_QUA_TAI', ..., 409)`.
7. **Commit và xác nhận:** Commit [`837e28b`](https://github.com/P-HUBcode/cdtn1-NGUYEN-MINH-PHU-l4/commit/837e28b) · Unit test `"Dữ liệu sai / Ngoại lệ: Từ chối khi khung giờ đã đầy 5/5 lịch hẹn (vi phạm QT-09)"` **PASS 100%**.

---

## 3. BUG-003 · Critical — Gợi ý KTV không lọc cùng trung tâm dẫn đến điều phối chéo địa bàn (QT-06)
1. **Mã và mức độ:** `BUG-003` · Mức độ: **Critical** — Lỗi điều phối vật lý vi phạm quy định cơ bản của chuỗi chi nhánh.
2. **Phát hiện bởi:** Thử nghiệm giao diện tiếp nhận phiếu tại Trung tâm Cần Thơ (Center ID = 1).
3. **Triệu chứng:** Phiếu bảo hành tiếp nhận tại Cần Thơ lại được gợi ý kỹ thuật viên thuộc Trung tâm Ninh Kiều hoặc Ô Môn để tiếp nhận.
4. **Cách tái lập:** Gọi endpoint gợi ý KTV cho phiếu thuộc trung tâm 1:
   ```bash
   curl http://localhost:3000/api/v1/tickets/2/recommend-technicians
   ```
5. **Nguyên nhân:** Câu SQL trong `findRecommendedTechnicians` chỉ lọc theo `ts.issue_category = ?` và `ts.proficiency >= 3` mà quên mệnh đề `WHERE tech.center_id = ?`.
6. **Cách sửa:** Bổ sung điều kiện `tech.center_id = ?` và `tech.status = 'HOAT_DONG'` vào câu SQL trong `src/repositories/ticketRepository.js`; đồng thời đặt hàng rào phòng thủ chiều sâu (Defense-in-Depth) tại hàm `checkTechnicianEligibility()` của `src/services/ticketService.js` kiểm tra chéo `technician.center_id !== requiredCenterId`.
7. **Commit và xác nhận:** Commit [`8186105`](https://github.com/P-HUBcode/cdtn1-NGUYEN-MINH-PHU-l4/commit/8186105) · Unit test `"Dữ liệu sai / Ngoại lệ: Từ chối khi KTV khác trung tâm tiếp nhận (vi phạm QT-06)"` **PASS 100%**.

---

## 4. BUG-004 · Major — Sập hiển thị phiếu bảo hành khi thông tin khách hàng bị thiếu/null (Chuẩn Slide 15-16)
1. **Mã và mức độ:** `BUG-004` · Mức độ: **Major** — Giao diện sập hoặc API trả 500 do vi phạm hợp đồng dữ liệu hiển thị.
2. **Phát hiện bởi:** Tích hợp kiểm thử khi dữ liệu cũ được import từ hệ thống kế thừa (Legacy CRM data migration).
3. **Triệu chứng:** Khi truy vấn danh sách phiếu hoặc chi tiết phiếu có khách hàng cũ chưa nhập đầy đủ họ tên, API ném ngoại lệ `TypeError: Cannot read properties of null (reading 'trim')` và trả mã HTTP 500.
4. **Cách tái lập:** Nạp bản ghi khách hàng có `full_name = NULL` rồi gọi `GET /api/v1/tickets/1`.
5. **Nguyên nhân:** Tầng Service và Frontend giả định bất thành văn rằng trường `customer_name` luôn luôn là chuỗi ký tự tồn tại, gọi trực tiếp `.trim()` hoặc định dạng chuỗi mà không có cơ chế fallback.
6. **Cách sửa:** Hiện thực hàm chuyển đổi đối tượng hiển thị an toàn `toTicketView(ticket)` tại tầng Service theo đúng chuẩn Buổi 11 (Slide 15–16), sử dụng toán tử nullish coalescing: `customer_name: (ticket.customer_name ?? '').trim() || '(không rõ họ tên)'`.
7. **Commit và xác nhận:** Commit [`9d3e6db`](https://github.com/P-HUBcode/cdtn1-NGUYEN-MINH-PHU-l4/commit/9d3e6db) · Unit test hồi quy `"toTicketView: Bảo toàn hợp đồng hiển thị khi họ tên khách hàng bị null (bug BUG-004)"` trong `tests/ticket.service.test.js` **PASS 100%**.

---

## 5. BUG-005 · Major — Kỹ thuật viên nhấn xem phiếu của tôi không thấy phiếu nào do kẹt dropdown trạng thái và hàm tìm kiếm bỏ sót tên KTV
1. **Mã và mức độ:** `BUG-005` · Mức độ: **Major** — Kỹ thuật viên không thể theo dõi danh sách các phiếu bảo hành được phân công cho mình (vi phạm US4, FR5).
2. **Phát hiện bởi:** Test case `TC-M05` "Kiểm thử thủ công luồng xem danh sách phiếu của Kỹ thuật viên sau phân công" (Kiểm thử thủ công trên giao diện Web M1).
3. **Triệu chứng:** Phiếu đã được phân công thành công vào CSDL với trạng thái `DANG_XU_LY` và gán cho `ktv_binh`, nhưng khi KTV vào màn hình M1 bấm nút lọc thì bảng hiển thị 0 phiếu.
4. **Cách tái lập:** Đăng nhập `quanly`, thực hiện phân công phiếu #1 cho KTV `ktv_binh`. Đăng xuất và đăng nhập `ktv_binh`, bấm *"🔍 Chỉ xem phiếu của tôi"* $\to$ Bảng M1 hiện `0 phiếu`.
5. **Nguyên nhân:**
   - Dropdown lọc trạng thái `#m1-status-filter` ban đầu ghim mặc định là `MOI` (Chờ phân công), khiến API Backend chỉ trả về các phiếu chưa phân công.
   - Hàm `renderM1TicketTable()` trên Frontend chỉ tìm kiếm từ khóa theo `customer_name`, `customer_phone`, `ticket_code`, `issue_desc`, `issue_category` mà quên so sánh trường `t.technician_name`. Khi nút gán từ khóa là tên KTV (VD: *"Trần Văn Bình"*), hệ thống tìm khách hàng mang tên KTV nên kết quả bị rỗng.
6. **Cách sửa:**
   - Chuyển giá trị mặc định của `#m1-status-filter` sang `-- Tất cả trạng thái --` và bổ sung đầy đủ các trạng thái (`MOI`, `DANG_XU_LY`, `CHO_LINH_KIEN`, `HOAN_TAT`).
   - Nâng cấp nút *"🔍 Chỉ xem phiếu của tôi"* lọc trực tiếp theo `t.technician_id === currentUser.technicianId` (hoặc tên KTV), hỗ trợ bật/tắt (Toggle) linh hoạt; tự động mở bộ lọc trạng thái nếu đang ở `MOI`.
   - Bổ sung `techNorm.includes(qNorm)` vào thanh tìm kiếm và hiển thị tên KTV phụ trách trực tiếp trên cột TRẠNG THÁI & KTV tại bảng M1.
7. **Commit và xác nhận:** Commit [`661bd96`](https://github.com/P-HUBcode/cdtn1-NGUYEN-MINH-PHU-l4/commit/661bd96) · Bộ Unit Tests #23 $\to$ #30 trong `tests/ticket.service.test.js` và kịch bản E2E kiểm chứng **PASS 100%**.

---

## 6. BUG-006 · Medium — Phiếu đã hoàn tất (HOAN_TAT) vẫn cho phép KTV/Quản lý chỉnh sửa trạng thái và gây nhầm lẫn trên hàng đợi M1
1. **Mã và mức độ:** `BUG-006` · Mức độ: **Medium / Business Flow** — Phiếu bảo hành sau khi đã sửa chữa xong (HOAN_TAT) vẫn có thể bị chỉnh sửa ngược lại trạng thái khác hoặc phân công lại; đồng thời danh sách M1 vẫn hiển thị phiếu đã xong chung với các việc đang chờ xử lý khiến KTV thắc mắc.
2. **Phát hiện bởi:** Test case `TC-M06` "Kiểm thử thủ công luồng hoàn tất sửa chữa và dọn sạch hàng đợi công việc của Kỹ thuật viên" (Kiểm thử thủ công trên giao diện Web M1 & M2).
3. **Triệu chứng:**
   - KTV hoặc Quản lý sau khi đánh dấu phiếu `HOAN_TAT` vẫn có thể bấm nút submit đổi lại thành `DANG_XU_LY` hoặc `CHO_LINH_KIEN`.
   - Quản lý vẫn có thể phân công lại phiếu đã hoàn thành cho KTV khác.
   - Trên bảng M1, các phiếu đã hoàn tất vẫn xuất hiện trong hàng đợi công việc của KTV khiến giao diện bị rối.
4. **Cách tái lập:**
   - Đăng nhập KTV, đổi trạng thái phiếu sang `HOAN_TAT` kèm ghi chú.
   - Tiếp tục chọn `CHO_LINH_KIEN` và bấm "Lưu cập nhật tiến độ" $\to$ Backend vẫn chấp nhận cập nhật.
   - Quay lại màn hình M1 $\to$ Phiếu `HOAN_TAT` vẫn nằm trong danh sách việc của KTV.
5. **Nguyên nhân:**
   - `validateStatusTransition` chưa có điều kiện kiểm tra nếu `ticket.status === 'HOAN_TAT'`.
   - `assignTechnician` và `reassignTechnician` chưa kiểm tra xem phiếu đã hoàn tất hay chưa trước khi cập nhật.
   - Màn hình M1 hiển thị toàn bộ phiếu mà chưa có cơ chế tự động tách biệt giữa "Hàng đợi đang xử lý" và "Lịch sử đã hoàn tất".
6. **Cách sửa:**
   - **Backend (Service):**
     - Trong `validateStatusTransition`: Bổ sung kiểm tra `if (ticket.status === 'HOAN_TAT')` từ chối ngay với mã lỗi `PHIEU_DA_HOAN_TAT` (HTTP 400): *"Phiếu bảo hành đã hoàn tất sửa chữa (HOAN_TAT). Không được phép chỉnh sửa hoặc thay đổi trạng thái của phiếu này nữa."*.
     - Trong `assignTechnician` và `reassignTechnician`: Thêm điều kiện chặn phân công lại phiếu đã `HOAN_TAT`.
   - **Frontend (M1 & M2):**
     - Trên M2: Khi `ticket.status === 'HOAN_TAT'`, ẩn toàn bộ `#form-update-progress` và `#m2-assign-actions`, hiển thị banner xanh lá khóa tiến độ vĩnh viễn (`#m2-progress-completed-notice` và `#m2-assign-completed-notice`).
     - Trên M1: Bổ sung checkbox *"Ẩn phiếu đã hoàn tất"* (mặc định được tích chọn) và khi KTV xem danh sách việc cần làm, hệ thống tự động ẩn các phiếu đã xong để tập trung vào các phiếu chưa xử lý. Nếu người dùng muốn xem lại lịch sử chỉ cần bỏ tích checkbox hoặc chọn trạng thái `HOAN_TAT`.
     - Chuyển nút bấm ở cột thao tác thành *"👁️ Chi tiết (Đã xong)"* đối với các phiếu đã hoàn tất.
7. **Commit và xác nhận:** Commit [`20946fe`](https://github.com/P-HUBcode/cdtn1-NGUYEN-MINH-PHU-l4/commit/20946fe) · Unit tests #31, #32 trong `tests/ticket.service.test.js` và kịch bản E2E kiểm chứng **PASS 100%**.
