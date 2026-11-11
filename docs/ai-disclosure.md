# PHỤ LỤC: BẢNG KHAI BÁO SỬ DỤNG CÔNG CỤ AI

**Tên học phần:** Chuyên đề tốt nghiệp 1 (HK261)  
**Tên bài tập:** BÀI TẬP 3 — Kiểm thử và Đóng gói prototype (20%)  
**Họ và tên sinh viên:** Nguyễn Minh Phú  
**MSSV:** 2374802013447 | **Track:** SE (Kỹ thuật phần mềm) | **Luồng:** L4 - Phân công kỹ thuật viên & Lịch hẹn  
**Repository:** [https://github.com/P-HUBcode/cdtn1-NGUYEN-MINH-PHU-l4](https://github.com/P-HUBcode/cdtn1-NGUYEN-MINH-PHU-l4) (Tag `v1.0`)  

---

## Bảng Khai Báo Sử Dụng Công Cụ AI Theo Từng Giai Đoạn

| STT | Công cụ AI | Phần áp dụng | Cách dùng (tóm tắt yêu cầu đã gửi) | Nội dung sinh viên đã chỉnh sửa, đối chiếu & kiểm chứng |
| :---: | :--- | :--- | :--- | :--- |
| **1** | Trợ lý AI (Google Antigravity) | Phân tích yêu cầu & User Stories (BT1 & BT2) | "Gợi ý rút gọn 7 User Story cho luồng L4 phân công KTV và lịch hẹn bảo hành kèm tiêu chí Given-When-Then" | Đã rà soát và chỉnh sửa lại theo chuẩn INVEST, gộp về đúng 7 User Story (5 MUST, 2 SHOULD), bổ sung các kịch bản ngoại lệ cụ thể (KTV quá tải, không tìm thấy KTV tay nghề $\ge 3$, quá hạn lịch hẹn). |
| **2** | Trợ lý AI (Google Antigravity) | Thiết kế Kiến trúc & Dữ liệu (BT1 & Sprint 1) | "Viết 3 câu lập luận lựa chọn kiến trúc 3 lớp và bổ sung thực thể customers vào ERD chuẩn 3NF" | Đã chuẩn hóa lại đúng khuôn mẫu: *'Vì NFR... đòi hỏi..., tôi chọn..., đánh đổi là...'*. Tự tay kiểm tra chuẩn 3NF, thêm ràng buộc `CHECK` SLA, proficiency 1-5, và composite indexes. |
| **3** | Trợ lý AI (Google Antigravity) | Giao diện Frontend & API Client Layer (Buổi 10) | "Hướng dẫn thiết kế kiến trúc Frontend tách lớp client.js, ticket.api.js và thành phần DataState xử lý 3 trạng thái" | Tự tay kiểm tra không còn bất kỳ lệnh `fetch(` nào trong mã giao diện người dùng; kiểm chứng cơ chế bắt lỗi 401 tự động điều hướng đăng nhập; bổ sung nút thao tác và modal hỗ trợ người dùng. |
| **4** | Trợ lý AI (Google Antigravity) | Hợp đồng Dữ liệu & Chuẩn hóa Ranh giới (Buổi 09) | "Tư vấn thiết kế Hợp đồng dữ liệu ranh giới toTicketView và hàm che giấu SĐT theo quy tắc QT-15" | Xây dựng `src/services/ticket.contract.js`, chuẩn hóa thời gian ISO 8601, thuật toán che SĐT QT-15 (`maskPhoneNumber`), và viết 6 Unit Tests kiểm chứng ranh giới. |
| **5** | Trợ lý AI (Google Antigravity) | Hệ thống Logging & Xử lý lỗi xuyên lớp (Buổi 11) | "Tư vấn cấu trúc Structured Logger JSON ra stdout và Middleware tập trung xử lý lỗi xuyên lớp phân biệt LoiNghiepVu và LoiTruyCapDuLieu" | Hiện thực `src/errors.js`, `src/utils/logger.js`, `src/middleware/errorHandler.js` và `src/middleware/requestId.js`. Tự kiểm tra regex Data Redaction để đảm bảo password, token, SĐT không bị lọt vào log. |
| **6** | Trợ lý AI (Google Antigravity) | Đóng gói Docker & Docker Compose (Buổi 11 & BT3) | "Gợi ý cấu hình Dockerfile nhiều lớp tối ưu cache và docker-compose.yml cho ứng dụng Node.js kèm CSDL SQLite persist" | Tự tay cấu hình `node:20-alpine`, kiểm tra thứ tự copy `package*.json` trước `npm ci --omit=dev`, cấu hình `.dockerignore` bảo mật và thêm Healthcheck tự động thăm dò `/api`. |
| **7** | Trợ lý AI (Google Antigravity) | Test Plan rút gọn & Chiến lược kiểm thử (Buổi 13) | "Tư vấn khung Test Plan 4 mục trả lời câu hỏi 'Làm sao em biết là đã kiểm thử ĐỦ?'" | Tự xác định tiêu chí đủ: 4 quy tắc nghiệp vụ cốt lõi đều có test luồng đúng và test biên, 2 test dữ liệu sai, 1 test bảo mật A01 và 1 test tái lập. Ghi rõ phần chủ ý không kiểm (màn hình cấu hình). |
| **8** | Trợ lý AI (Google Antigravity) | Bộ 12 ca kiểm thử thực tế & Bug Log (Buổi 14) | "Gợi ý thiết kế kịch bản kiểm thử 5 nhóm và mẫu Bug Log 7 dòng kèm commit hash riêng cho từng bug" | Hiện thực `tests/run_12_test_cases.js`, chạy thật trên máy, ghi nhận thực tế 12/12 PASS; ghi nhận 3 bug thật (BUG-01, BUG-02, BUG-03) với 3 commit riêng biệt, giải thích rõ nguyên nhân gốc rễ và bài học rút ra. |
| **9** | Trợ lý AI (Google Antigravity) | Checklist Bảo Mật & Tiêu chí Track SE (Buổi 15) | "Rà soát 7 mục bảo mật OWASP cơ bản và các tiêu chí S1-S4 cho chuyên ngành SE" | Triển khai mã băm mật khẩu SHA-256 + salt trong SQLite và bộ nhớ, thêm kiểm soát phân quyền KTV theo sở hữu (A01), kiểm tra ẩn dấu vết lỗi nội bộ, và chạy `npm audit fix` đạt `found 0 vulnerabilities`. |
| **10** | Trợ lý AI (Google Antigravity) | Deployment Guide & API Documentation tiếng Anh (Buổi 16) | "Tư vấn cấu trúc tài liệu kỹ thuật bàn giao bằng tiếng Anh: Deployment Guide 5 mục và API Docs 15 endpoints" | Tự tay soạn thảo `docs/deployment-guide.md` với quy trình 2 lệnh dựng hệ thống máy trắng, và `docs/api-docs.md` mô tả chi tiết 15 endpoints với đầy đủ 7 mục bắt buộc và JSON payload thực tế. |

---

**Cam kết liêm chính học thuật:**  
Tôi xác nhận đã đọc, hiểu và chịu trách nhiệm về toàn bộ nội dung nộp. Mọi dòng mã, cấu hình và báo cáo đều được tôi trực tiếp kiểm chứng, hiểu rõ logic hoạt động và sẵn sàng giải thích chi tiết trước Giảng viên tại buổi đánh giá.

- **Họ và tên sinh viên:** Nguyễn Minh Phú  
- **Mã số sinh viên (MSSV):** 2374802013447  
- **Ngày hoàn thành & nộp bài:** 11/11/2026  
