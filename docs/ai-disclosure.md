# PHỤ LỤC: BẢNG KHAI BÁO SỬ DỤNG CÔNG CỤ AI

**Tên học phần:** Chuyên đề tốt nghiệp 1 (HK261)  
**Tên bài tập:** Bài tập 1 & Bài tập 2 (Sprint 1) - Phân tích, Thiết kế & Hiện thực Core Module  
**Họ và tên sinh viên:** Nguyễn Minh Phú  
**MSSV:** 2374802013447 | **Track:** SE | **Luồng:** L4 - Phân công kỹ thuật viên & Lịch hẹn  

---

| STT | Công cụ AI | Phần áp dụng | Cách dùng (tóm tắt yêu cầu đã gửi) | Nội dung sinh viên đã chỉnh sửa, đối chiếu & kiểm chứng |
| :---: | :--- | :--- | :--- | :--- |
| 1 | Trợ lý AI (Google Antigravity) | Mục 1 - User Stories & Acceptance Criteria | "Gợi ý rút gọn 7 User Story cho luồng L4 phân công KTV và lịch hẹn bảo hành kèm tiêu chí Given-When-Then" | Đã rà soát và chỉnh sửa lại theo chuẩn INVEST, gộp về đúng 7 User Story (5 MUST, 2 SHOULD), bổ sung 3 kịch bản ngoại lệ cụ thể (KTV quá tải, không tìm thấy KTV tay nghề >= 3, quá hạn lịch hẹn). |
| 2 | Trợ lý AI (Google Antigravity) | Mục 3.2 - Ba câu lập luận kiến trúc | "Viết 3 câu lập luận lựa chọn kiến trúc 4 lớp phân tầng và Repository Pattern gắn với NFR1, NFR2, NFR3" | Đã chuẩn hóa lại đúng khuôn mẫu: *'Vì NFR... đòi hỏi..., tôi chọn..., đánh đổi là...'* và kiểm tra tính khả thi trên quy mô prototype. |
| 3 | Trợ lý AI (Google Antigravity) | Mục 4 & db/schema.sql - Mô hình ERD & SQL DDL | "Bổ sung bảng customers và khóa ngoại tickets.customer_id theo phản hồi của GV" | Tự tay kiểm tra chuẩn 3NF, thêm ràng buộc `CHECK` cho mốc SLA `due_date >= received_at`, `CHECK` proficiency điểm 1-5, và bổ sung các composite index trên `(technician_id, due_date)`. |
| 4 | Trợ lý AI (Google Antigravity) | Mục 5 - Wireframe 3 Màn hình | "Gợi ý bố cục layout text wireframe 3 màn hình (M1, M2, M3) cho Luồng L4" | Tự vẽ lại sơ đồ cấu trúc trên Draw.io, lập bảng đối chiếu 1-1 giữa từng trường hiển thị với cột trong CSDL và mã FR/US. |

---

**Cam kết liêm chính học thuật:**  
Tôi xác nhận đã đọc, hiểu và chịu trách nhiệm về toàn bộ nội dung nộp.

- **Họ và tên sinh viên:** Nguyễn Minh Phú  
- **Mã số sinh viên (MSSV):** 2374802013447  
- **Ngày nộp:** 15/10/2026  
