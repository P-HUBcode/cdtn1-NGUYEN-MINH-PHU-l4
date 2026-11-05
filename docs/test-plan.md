# TEST PLAN RÚT GỌN — HỆ THỐNG SMART CRM MEKONG MOBILE
## LUỒNG L4: PHÂN CÔNG KỸ THUẬT VIÊN VÀ LỊCH HẸN BẢO HÀNH
**Môn học:** Chuyên đề tốt nghiệp 1 (232_71ITBS40103_01 — HK261)  
**Trường Đại học Văn Lang — Khoa Công nghệ Thông tin**  
**Sinh viên thực hiện:** Nguyễn Minh Phú — MSSV: 2374802013447  
**Track:** SE (Software Engineering) | **Giai đoạn 3 (Buổi 13–18) — Bài tập 3**  
**Repository:** [https://github.com/P-HUBcode/cdtn1-NGUYEN-MINH-PHU-l4](https://github.com/P-HUBcode/cdtn1-NGUYEN-MINH-PHU-l4)  

---

### 1. PHẠM VI KIỂM THỬ VÀ PHẦN CHỦ Ý KHÔNG KIỂM

* **Các chức năng và quy tắc nghiệp vụ BẮT BUỘC kiểm thử:**
  1. **Quy tắc SLA `due_date` (QT-04):** Tính hạn cam kết theo mức độ ưu tiên (CAO: +24h, TRUNG_BÌNH: +48h, THẤP: +72h).
  2. **Quy tắc phân công KTV duy nhất & cùng trung tâm (QT-06, QT-07):** KTV phải hoạt động (`HOAT_DONG`), cùng chi nhánh tiếp nhận (`center_id`), và có điểm tay nghề sự cố tương ứng $\ge 3$ (`proficiency >= 3`).
  3. **Quy tắc chuyển gán phiếu Re-assign (QT-08):** Bắt buộc nhập lý do thay đổi KTV có độ dài $\ge 10$ ký tự, tự động ghi nhật ký `ticket_status_log`.
  4. **Quy tắc giới hạn tải lịch hẹn (QT-09):** Khống chế tối đa 5 lịch hẹn trong một khung giờ 30 phút tại cùng trung tâm tiếp nhận.
  5. **Quy tắc chuyển đổi trạng thái & tiến độ sửa chữa (FR6 / US5):** KTV chuyển tuần tự `DANG_XU_LY` $\to$ `CHO_LINH_KIEN` $\to$ `HOAN_TAT`. Chặn phiếu chưa phân công (`MOI`), chặn cập nhật trùng trạng thái, chặn thiếu ghi chú tiến độ.
  6. **Quy tắc khóa vĩnh viễn phiếu đã xong (`BUG-006`):** Khóa trạng thái khi phiếu đạt `HOAN_TAT`, chặn KTV và Quản lý chuyển ngược trạng thái hoặc gán lại.
  7. **Hợp đồng dữ liệu ranh giới & Che giấu PII (QT-15):** Định dạng ISO 8601 (múi giờ UTC Z), che giấu số điện thoại khách hàng ranh giới (`090****567`).
  8. **Kiểm soát truy cập theo quyền sở hữu (Security A01 OWASP):** KTV chỉ được cập nhật phiếu được gán cho mình, chặn KTV khác can thiệp (HTTP 403 Forbidden).

* **Phần CHỦ Ý KHÔNG KIỂM THỬ (kèm lý do kỹ thuật):**
  - *Màn hình cấu hình hệ thống & Quản lý danh mục trung tâm:* Vì đây là các danh mục tĩnh (Lookup Tables: `service_centers`), chỉ phục vụ đọc (Read-only) trong phạm vi prototype luồng L4, không chứa quy tắc nghiệp vụ động.
  - *Module thanh toán chi phí linh kiện ngoài bảo hành & Mua sắm chuỗi cung ứng:* Thuộc phạm vi chủ ý không làm (WON'T Have: `WON'T-01`, `WON'T-02`) đã được thống nhất tại bản đặc tả SRS từ Bài tập 1.
  - *Tấn công từ chối dịch vụ (DDoS) và thâm nhập hạ tầng chuyên sâu:* Thuộc phạm vi kiểm thử an ninh nâng cao của Chuyên đề tốt nghiệp 2.

---

### 2. LOẠI TEST VÀ SỐ LƯỢNG MỖI TẦNG (TEST PYRAMID)

Hệ thống áp dụng mô hình Kim tự tháp kiểm thử (Testing Pyramid) gồm 3 tầng:

| Tầng kiểm thử | Công cụ / Thư viện | Số lượng ca kiểm thử | Mục đích kiểm chứng |
| :--- | :--- | :---: | :--- |
| **1. Unit & Contract Tests** | `node:test`, `node:assert/strict` | **38 tests** | Kiểm tra logic nghiệp vụ thuần túy (`ticketService.js`) và hợp đồng dữ liệu ranh giới (`ticket.contract.js`), không phụ thuộc mạng. |
| **2. Integration Tests** | `node:test`, SQLite thật | **4 tests** | Kiểm tra tương tác với cơ sở dữ liệu SQLite thật: ràng buộc toàn vẹn khóa ngoại, lưu vết Audit Log, tính idempotent CSDL. |
| **3. End-to-End API Tests** | Script `tests/test_end_to_end.js` | **9 bước toàn luồng** | Kiểm thử tích hợp xuyên suốt từ đăng nhập $\to$ duyệt danh sách M1 $\to$ gợi ý phân công M2 $\to$ KTV cập nhật tiến độ $\to$ khóa HOAN_TAT $\to$ đặt lịch hẹn M3. |
| **TỔNG HỢP TEST REPORT (BT3)** | Bộ 12 Test Cases trọng tâm | **12 test cases** | Trích xuất và đối soát theo chuẩn 8 cột của đề bài BT3 (bao phủ đủ 5 nhóm kiểm thử bắt buộc). |

---

### 3. TIÊU CHÍ THÀNH CÔNG ĐO ĐƯỢC (MEASURABLE EXIT CRITERIA)

Một lượt kiểm thử được xác nhận là ĐẠT khi thỏa mãn đồng thời toàn bộ các tiêu chí định lượng sau:
1. **100% Test Cases PASS:** Toàn bộ 38 Unit Tests và 12 Test Cases trong Test Report đạt kết quả `PASS` (0 FAIL, 0 Skipped).
2. **Bao phủ 100% quy tắc nghiệp vụ:** Mỗi quy tắc (`QT-04`, `QT-06`, `QT-07`, `QT-08`, `QT-09`, `FR6/US5`, `BUG-006`) đều có ít nhất 01 test luồng đúng và 01 test biên.
3. **0 Bug nghiêm trọng còn mở:** Không còn bất kỳ bug nào ở mức `CRITICAL` hoặc `MAJOR` chưa được khắc phục trong `docs/bug-log.md`.
4. **Hiệu năng thực thi:** Toàn bộ bộ test chạy hoàn tất trong thời gian $\le 1.0$ giây trên máy sạch.
5. **Độ an toàn dữ liệu:** 100% các cuộc gọi thất bại do dữ liệu sai hoặc vi phạm phân quyền không gây tác dụng phụ làm thay đổi bản ghi trong CSDL (Rollback an toàn).

---

### 4. MÔI TRƯỜNG VÀ DỮ LIỆU THỬ

* **Môi trường thực thi:**
  - *Môi trường Node.js cục bộ:* Node.js v20.x LTS trở lên, npm v10.x trên hệ điều hành Windows / Linux / macOS.
  - *Môi trường Container:* Docker Desktop / Docker Compose v2 với image nền `node:20-alpine`.
* **Cơ chế nạp và cách ly dữ liệu thử:**
  - Dữ liệu thử mẫu ban đầu gồm 9 phiếu bảo hành (`tickets`), 3 kỹ thuật viên (`technicians`), 3 chi nhánh trung tâm (`service_centers`) được nạp tự động qua file `src/config/database.js` với tính chất **Idempotent** (`INSERT OR IGNORE`).
  - Trước mỗi lượt kiểm thử luồng chính hoặc test E2E, hệ thống cung cấp endpoint hỗ trợ cách ly: `POST /api/v1/tickets/reset-demo` để khôi phục trạng thái các phiếu kiểm thử (#1, #2) về trạng thái sạch ban đầu mà không làm ảnh hưởng đến các dữ liệu khác.

---

### 💡 TRẢ LỜI CÂU HỎI MẤU CHỐT: "LÀM SAO BIẾT LÀ ĐÃ KIỂM THỬ ĐỦ?"

> **Câu trả lời đạt chuẩn kỹ thuật:**  
> Hệ thống được xem là kiểm thử ĐỦ dựa trên 4 căn cứ định lượng rõ ràng:
> 1. **Tiêu chí bao phủ quy tắc nghiệp vụ:** 100% quy tắc nghiệp vụ đã phân tích trong SRS (từ QT-04 đến QT-09, FR6/US5 và khóa trạng thái BUG-006) đều có ít nhất một bài kiểm thử luồng đúng (Happy Path) và một bài kiểm thử giá trị biên (Boundary Value).
> 2. **Tiêu chí bao phủ ranh giới lỗi:** Có đầy đủ các test case cho dữ liệu sai (nhập thiếu trường, sai định dạng, KTV khác chi nhánh) nhằm đảm bảo hệ thống phản hồi lỗi lịch sự (HTTP 400/409) và tuyệt đối không bao giờ bị sập (Crash).
> 3. **Tiêu chí an ninh theo chuẩn OWASP A01:** Đã thiết lập test case kiểm soát quyền truy cập theo chủ sở hữu (chặn KTV can thiệp phiếu của người khác với HTTP 403).
> 4. **Minh bạch phạm vi:** Đã xác định rõ phần chủ ý không kiểm thử (màn hình cấu hình tĩnh) ngay tại Mục 1 kèm lý do kỹ thuật.
