# PHỤ LỤC: BẢNG KHAI BÁO SỬ DỤNG CÔNG CỤ AI

**Tên học phần:** Chuyên đề tốt nghiệp 1 (HK261)  
**Tên bài tập:** BÀI TẬP 2 — Hiện thực Prototype, Tích hợp hệ thống & Kiểm thử (Sprint 1 & Sprint 2)  
**Họ và tên sinh viên:** Nguyễn Minh Phú  
**MSSV:** 2374802013447 | **Track:** SE (Kỹ thuật phần mềm) | **Luồng:** L4 - Phân công kỹ thuật viên & Lịch hẹn  
**Repository:** [https://github.com/P-HUBcode/cdtn1-NGUYEN-MINH-PHU-l4](https://github.com/P-HUBcode/cdtn1-NGUYEN-MINH-PHU-l4) (Tag `v0.2`)  

---

| STT | Công cụ AI | Phần áp dụng | Cách dùng (tóm tắt yêu cầu đã gửi) | Nội dung sinh viên đã chỉnh sửa, đối chiếu & kiểm chứng |
| :---: | :--- | :--- | :--- | :--- |
| 1 | Trợ lý AI (Google Antigravity) | Phân tích yêu cầu & User Stories (BT1 & BT2) | "Gợi ý rút gọn 7 User Story cho luồng L4 phân công KTV và lịch hẹn bảo hành kèm tiêu chí Given-When-Then" | Đã rà soát và chỉnh sửa lại theo chuẩn INVEST, gộp về đúng 7 User Story (5 MUST, 2 SHOULD), bổ sung các kịch bản ngoại lệ cụ thể (KTV quá tải, không tìm thấy KTV tay nghề $\ge 3$, quá hạn lịch hẹn). |
| 2 | Trợ lý AI (Google Antigravity) | Thiết kế Kiến trúc & Dữ liệu (BT1 & Sprint 1) | "Viết 3 câu lập luận lựa chọn kiến trúc 3 lớp và bổ sung thực thể customers vào ERD chuẩn 3NF" | Đã chuẩn hóa lại đúng khuôn mẫu: *'Vì NFR... đòi hỏi..., tôi chọn..., đánh đổi là...'*. Tự tay kiểm tra chuẩn 3NF, thêm ràng buộc `CHECK` SLA, proficiency 1-5, và composite indexes. |
| 3 | Trợ lý AI (Google Antigravity) | Giao diện Frontend & API Client Layer (Buổi 10) | "Hướng dẫn thiết kế kiến trúc Frontend tách lớp client.js, ticket.api.js và thành phần DataState xử lý 3 trạng thái" | Tự tay kiểm tra không còn bất kỳ lệnh `fetch(` nào trong mã giao diện người dùng; kiểm chứng cơ chế bắt lỗi 401 tự động điều hướng đăng nhập; bổ sung nút thao tác và modal hỗ trợ người dùng. |
| 4 | Trợ lý AI (Google Antigravity) | Hợp đồng Dữ liệu & Chuẩn hóa Ranh giới (Buổi 09) | "Tư vấn thiết kế Hợp đồng dữ liệu ranh giới toTicketView và hàm che giấu SĐT theo quy tắc QT-15" | Xây dựng `src/services/ticket.contract.js`, chuẩn hóa thời gian ISO 8601, thuật toán che SĐT QT-15 (`maskPhoneNumber`), và viết 6 Unit Tests kiểm chứng ranh giới. |
| 5 | Trợ lý AI (Google Antigravity) | Hệ thống Logging & Xử lý lỗi xuyên lớp (Buổi 11) | "Tư vấn cấu trúc Structured Logger JSON ra stdout và Middleware tập trung xử lý lỗi xuyên lớp phân biệt LoiNghiepVu và LoiTruyCapDuLieu" | Hiện thực `src/errors.js`, `src/utils/logger.js`, `src/middleware/errorHandler.js` và `src/middleware/requestId.js`. Tự kiểm tra regex Data Redaction để đảm bảo password, token, SĐT không bị lọt vào log. |
| 6 | Trợ lý AI (Google Antigravity) | Đóng gói Docker & Docker Compose (Buổi 11) | "Gợi ý cấu hình Dockerfile nhiều lớp tối ưu cache và docker-compose.yml cho ứng dụng Node.js kèm CSDL SQLite persist" | Tự tay cấu hình `node:20-alpine`, kiểm tra thứ tự copy `package*.json` trước `npm ci --omit=dev`, cấu hình `.dockerignore` bảo mật và thêm Healthcheck tự động thăm dò `/api`. |
| 7 | Trợ lý AI (Google Antigravity) | Bộ kiểm thử tự động & Gỡ lỗi Bug Log (Buổi 09, 10, 11) | "Gợi ý các ca kiểm thử biên (boundary) và mẫu ghi chép nhật ký gỡ lỗi Bug Log 7 dòng theo 4 bước chuẩn Buổi 11" | Tự viết và chạy thành công 28 Unit Tests (Happy path, Biên, Ngoại lệ, Hợp đồng ranh giới, Regression tests) và kịch bản E2E toàn luồng đạt tỷ lệ PASS 100%. |

---

**Cam kết liêm chính học thuật:**  
Tôi xác nhận đã đọc, hiểu và chịu trách nhiệm về toàn bộ nội dung nộp. Mọi dòng mã, cấu hình và báo cáo đều được tôi trực tiếp kiểm chứng, hiểu rõ logic hoạt động và sẵn sàng giải thích chi tiết trước Giảng viên tại buổi đánh giá.

- **Họ và tên sinh viên:** Nguyễn Minh Phú  
- **Mã số sinh viên (MSSV):** 2374802013447  
- **Ngày hoàn thành & nộp bài:** 26/10/2026  
