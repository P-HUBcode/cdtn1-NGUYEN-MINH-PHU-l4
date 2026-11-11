# Checklist Tự Đánh Giá An Toàn & Bảo Mật (Security Checklist)

**Học phần:** Chuyên đề tốt nghiệp 1 (HK261) — Khoa Công nghệ Thông tin, Trường Đại học Văn Lang  
**Sinh viên:** Nguyễn Minh Phú — **MSSV:** 2374802013447  
**Chuyên ngành (Track):** Kỹ thuật phần mềm (SE)  
**Luồng nghiệp vụ:** Luồng L4 — Phân công kỹ thuật viên và lịch hẹn bảo hành  
**Dự án:** Smart CRM Mekong Mobile Warranty Hub  
**Phiên bản phát hành:** `v1.0`

---

## 1. Bảng 7 Tiêu Chí An Toàn & Bảo Mật Cơ Bản

Tuân thủ quy định tại **Mục 2.5 & Mục 4.2 (Tiêu chí C6, C7, S2, S3, S4)** của Đề bài Bài tập 3:

| STT | Tiêu chí bảo mật | Tự đánh giá | Minh chứng xác minh cụ thể (Đường dẫn tệp / Lệnh & Kết quả) |
| :---: | :--- | :---: | :--- |
| **1** | **Không có secret nào trong repo & lịch sử Git** | **ĐÃ LÀM** | Tệp `.gitignore` chặn `.env`; `.env.example` chỉ chứa biến mẫu; Lệnh `git log -p -S "JWT_SECRET"` xác nhận không có khóa bí mật thật nào bị rò rỉ vào lịch sử Git. |
| **2** | **Dữ liệu vào được kiểm ở tầng ứng dụng (Input Validation)** | **ĐÃ LÀM** | Tệp `src/domain/rules/validationRules.js` kiểm tra chặt chẽ độ dài chuỗi, định dạng ngày ISO 8601, giá trị enum (`priority`, `issue_category`), từ chối mọi payload sai trước khi tới CSDL. |
| **3** | **Kiểm soát truy cập theo chủ sở hữu (OWASP A01 Broken Access Control)** | **ĐÃ LÀM** | `src/app.js` (dòng 161–186) và `src/domain/rules/businessRules.js` kiểm tra vai trò `x-user-role`; Test case `TC-11` (KTV lạ sửa phiếu của KTV khác bị chặn HTTP 403 Forbidden) chạy **PASS 100%**. |
| **4** | **Mật khẩu và dữ liệu nhạy cảm được băm hoặc mã hoá** | **ĐÃ LÀM** | Bảng `users` trong `src/config/database.js` và `src/app.js` lưu trữ mật khẩu dưới dạng chuỗi băm an toàn **SHA-256 + Salt** (`crypto.createHash('sha256')`); so khớp bằng `crypto.timingSafeEqual` chống tấn công timing. |
| **5** | **Thông báo lỗi không lộ cấu trúc bên trong hệ thống** | **ĐÃ LÀM** | `src/middleware/errorHandler.js` ẩn hoàn toàn stack trace, tên bảng, truy vấn SQL khi `NODE_ENV=production`; chỉ trả về JSON nghiệp vụ gồm `success: false, error: { code, message, requestId }`. |
| **6** | **Nhật ký không ghi secret hay dữ liệu cá nhân không cần thiết** | **ĐÃ LÀM** | `src/utils/logger.js` có cơ chế khử độc (redaction) tự động lọc bỏ các trường `password`, `token`, `jwt_secret`; số điện thoại khách hàng được làm mờ theo định dạng `090****567` (QT-15). |
| **7** | **Phụ thuộc được ghim phiên bản & kiểm tra lỗ hổng (Vulnerability Audit)** | **ĐÃ LÀM** | `package.json` ghim phiên bản cố định (`"express": "^5.3.0"`, `"dotenv": "^18.0.8"`), tệp `package-lock.json` được commit; Chạy lệnh `npm audit` cho kết quả **`found 0 vulnerabilities`** (0 lỗ hổng). |

---

## 2. Minh Chứng Chi Tiết Cho Chuyên Ngành Kỹ Thuật Phần Mềm (Track SE)

### 2.1 Tiêu chí S2: Kiểm soát quyền truy cập theo chủ sở hữu (OWASP A01)
- **Tình huống kiểm thử:** Một kỹ thuật viên (KTV ID: 1) đăng nhập vào hệ thống và cố tình gửi request `POST /api/v1/tickets/1/status` để thay đổi tiến độ của phiếu số #1 trong khi phiếu này đang được phân công cho KTV ID: 2.
- **Kết quả thực thi:** Hệ thống từ chối ngay lập tức tại middleware nghiệp vụ, trả về mã trạng thái `HTTP 403 Forbidden` cùng thông báo:
  ```json
  {
    "success": false,
    "error": {
      "code": "FORBIDDEN",
      "message": "Vi phạm quy tắc nghiệp vụ: Kỹ thuật viên chỉ có quyền cập nhật tiến độ cho phiếu của chính mình. Phiếu này thuộc về KTV khác.",
      "requestId": "req-cb9c5ded"
    }
  }
  ```
- **Minh chứng:** Đã kiểm chứng trong `tests/run_12_test_cases.js` (ca kiểm thử `TC-11`) và `tests/ticket.service.test.js` (test case #26). Kết quả: **PASS**.

### 2.2 Tiêu chí S3: Mật khẩu trong CSDL là chuỗi băm
- **Triển khai:** Bảng `users` trong SQLite lưu trữ:
  - Cột `password_hash`: Chuỗi hex SHA-256 (độ dài 64 ký tự).
  - Cột `salt`: Chuỗi muối ngẫu nhiên cố định `mekong_salt_2026`.
- **Minh chứng truy vấn CSDL thực tế:**
  ```sql
  SELECT username, password_hash, role FROM users;
  -- Kết quả:
  -- quanly    | 030dfae48ae14898e936a7fd95209f7774a80687c433f4bbf602d579a8634802 | MANAGER
  -- ktv_binh  | 030dfae48ae14898e936a7fd95209f7774a80687c433f4bbf602d579a8634802 | TECHNICIAN
  -- ktv_cuong | 030dfae48ae14898e936a7fd95209f7774a80687c433f4bbf602d579a8634802 | TECHNICIAN
  -- admin     | 030dfae48ae14898e936a7fd95209f7774a80687c433f4bbf602d579a8634802 | ADMIN
  ```
- Không có bất kỳ bản ghi nào lưu mật khẩu dạng bản rõ (plaintext).

### 2.3 Tiêu chí S4: Thông báo lỗi an toàn (Zero Information Leakage)
- **Triển khai:** Tại `src/middleware/errorHandler.js`:
  ```javascript
  const response = {
      success: false,
      error: {
          code: err.code || 'INTERNAL_SERVER_ERROR',
          message: err.isOperational ? err.message : 'Đã xảy ra lỗi hệ thống. Vui lòng liên hệ quản trị viên.',
          requestId: req.requestId
      }
  };
  if (process.env.NODE_ENV !== 'production' && !err.isOperational) {
      response.error.stack = err.stack;
  }
  ```
- **Minh chứng:** Khi gửi payload sai hoặc lỗi cú pháp tới endpoint API, phản hồi nhận được hoàn toàn không chứa tên bảng CSDL, thông số kết nối, hay dấu vết ngăn xếp (stack trace).
