# BÁO CÁO THỰC HÀNH BUỔI 14: WORKSHOP KIỂM THỬ HỆ THỐNG CÁ NHÂN
**Môn học:** Chuyên đề tốt nghiệp 1 (232_71ITBS40103_01 — HK261)  
**Trường Đại học Văn Lang — Khoa Công nghệ Thông tin**  
**Sinh viên thực hiện:** Nguyễn Minh Phú — **MSSV:** 2374802013447  
**Chuyên ngành (Track):** Kỹ thuật phần mềm (Software Engineering - SE)  
**Luồng nghiệp vụ:** L4 — Phân công kỹ thuật viên và lịch hẹn bảo hành (Smart CRM Mekong Mobile)  
**Repository GitHub:** [https://github.com/P-HUBcode/cdtn1-NGUYEN-MINH-PHU-l4](https://github.com/P-HUBcode/cdtn1-NGUYEN-MINH-PHU-l4) (Tag `v1.0`)  
**Ngày thực hiện:** 05/11/2026  

---

## 1. MỤC TIÊU WORKSHOP BUỔI 14

Buổi 14 là buổi Workshop kiểm thử hệ thống cá nhân trực tiếp trên lớp. Mục tiêu cốt lõi:
1. Hoàn thiện **Test Plan rút gọn** (4 mục chuẩn) trả lời câu hỏi *"Làm sao em biết là đã kiểm thử ĐỦ?"*.
2. Chạy THẬT và ghi nhận kết quả **10–12 test cases** với đầy đủ 8 cột chuẩn, bao phủ 5 nhóm bắt buộc (Happy Path, Biên, Ngoại lệ, Bảo mật OWASP A01, Tính tái lập C5).
3. Ghi nhận và sửa ít nhất **3 bug thực tế** vào `docs/bug-log.md` (trong đó có ít nhất 1 bug Critical/Major), mỗi bug có 7 dòng thông tin và link commit riêng lẻ trong Git.
4. Xây dựng bộ công cụ thực thi kiểm thử 1 lệnh (`npm run test:report`) và Bảng điều khiển kiểm thử trực quan (**Live Test Dashboard** tại `/test-dashboard.html`).

---

## 2. KẾT QUẢ THỰC THI BỘ 12 CA KIỂM THỬ THỰC TẾ

Toàn bộ 12 ca kiểm thử đã được chạy thực tế thông qua kịch bản `tests/run_12_test_cases.js`. Tỷ lệ đạt: **12/12 PASS (100%)**.

| Mã TC | Phân nhóm | Tên ca kiểm thử | Quy tắc nghiệp vụ | Kết quả thực tế | Trạng thái |
| :---: | :--- | :--- | :--- | :--- | :---: |
| **TC-01** | Happy Path | Tính hạn SLA ưu tiên CAO (+24h) | QT-04 | Cộng chính xác 24.0 giờ, khớp ISO 8601 | **PASS** |
| **TC-02** | Happy Path | Phân công KTV đủ chuẩn cho phiếu mới | QT-06, QT-07 | Chuyển MOI -> DANG_XU_LY, gán KTV 1, audit log +1 | **PASS** |
| **TC-03** | Happy Path | Chuyển gán KTV với lý do hợp lệ >= 10 ký tự | QT-08 | KTV đổi sang 2, lý do 57 ký tự ghi nhận | **PASS** |
| **TC-04** | Happy Path | Đặt lịch hẹn bàn giao máy còn chỗ trống | QT-09 | Cấp mã lịch hẹn mới, trạng thái DA_XAC_NHAN | **PASS** |
| **TC-05** | Happy Path | KTV cập nhật tiến độ CHO_LINH_KIEN | FR6/US5 | Chuyển sang CHO_LINH_KIEN, lưu log tiến độ | **PASS** |
| **TC-06** | Boundary | Biên tay nghề KTV (proficiency 3 vs 2) | QT-07 | Tay nghề 3: hợp lệ; Tay nghề 2: từ chối | **PASS** |
| **TC-07** | Boundary | Biên độ dài lý do chuyển gán (10 vs 9 ký tự) | QT-08 | 10 ký tự: hợp lệ; 9 ký tự: chặn LY_DO_QUA_NGAN | **PASS** |
| **TC-08** | Boundary | Biên tải KTV (tối đa 5 phiếu) | QT-06 | Phiếu thứ 5: chấp nhận; Phiếu thứ 6: chặn KTV_QUA_TAI | **PASS** |
| **TC-09** | Exceptions | Phân công KTV khác trung tâm | QT-06 | HTTP 400 Bad Request, từ chối KTV_KHAC_TRUNG_TAM | **PASS** |
| **TC-10** | Exceptions | Cố tình sửa phiếu đã hoàn tất HOAN_TAT | Khóa vĩnh viễn | HTTP 400 Bad Request, từ chối PHIEU_DA_HOAN_TAT | **PASS** |
| **TC-11** | Security | KTV lạ cố tình sửa phiếu của KTV khác | OWASP A01 | HTTP 403 Forbidden, chặn quyền sở hữu | **PASS** |
| **TC-12** | Reproduce | Chạy lại kịch bản / nạp seed lần 2 | Idempotent C5 | CSDL nhất quán, 0 lỗi SQLITE_CONSTRAINT | **PASS** |

---

## 3. NHẬT KÝ GỠ LỖI & SỬA BUG (BUG LOG)

Đã ghi nhận 3 bug thực tế, sửa và commit riêng lẻ:
1. **BUG-01 (CRITICAL):** KTV nghỉ phép hoặc vượt tải 5 phiếu vẫn nhận được phiếu.  
   *Commit:* `66881db` — *Giải pháp:* Kiểm tra điều kiện `checkTechnicianEligibility` trước khi cập nhật CSDL.
2. **BUG-02 (MAJOR):** Đặt lịch hẹn trùng khung giờ vượt quá năng lực (5 lịch/30 phút).  
   *Commit:* `cb82a69` — *Giải pháp:* Đếm lịch hẹn trong khung 30 phút, từ chối với mã lỗi `LICH_HEN_QUA_TAI` (HTTP 409).
3. **BUG-03 (MINOR):** Chuyển gán KTV với lý do rỗng hoặc dưới 10 ký tự.  
   *Commit:* `3e38ef8` — *Giải pháp:* Thêm hàm kiểm tra `validateReason(reason, 10)` ném lỗi `LY_DO_QUA_NGAN` (HTTP 400).

---

## 4. KẾT QUẢ VÀ HƯỚNG TỚI BUỔI 15
Toàn bộ Test Plan, Test Report và Bug Log đã hoàn tất và được xác thực trực tiếp trong Workshop Buổi 14, làm tiền đề vững chắc cho việc đóng gói Docker và hoàn thiện tài liệu bàn giao ở Buổi 15.
