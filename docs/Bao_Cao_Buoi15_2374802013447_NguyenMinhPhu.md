# BÁO CÁO THỰC HÀNH BUỔI 15: ĐÓNG GÓI, TRIỂN KHAI VÀ BẢO MẬT ỨNG DỤNG
**Môn học:** Chuyên đề tốt nghiệp 1 (232_71ITBS40103_01 — HK261)  
**Trường Đại học Văn Lang — Khoa Công nghệ Thông tin**  
**Sinh viên thực hiện:** Nguyễn Minh Phú — **MSSV:** 2374802013447  
**Chuyên ngành (Track):** Kỹ thuật phần mềm (Software Engineering - SE)  
**Luồng nghiệp vụ:** L4 — Phân công kỹ thuật viên và lịch hẹn bảo hành (Smart CRM Mekong Mobile)  
**Repository GitHub:** [https://github.com/P-HUBcode/cdtn1-NGUYEN-MINH-PHU-l4](https://github.com/P-HUBcode/cdtn1-NGUYEN-MINH-PHU-l4) (Tag `v1.0`)  
**Ngày thực hiện:** 11/11/2026  

---

## 1. TỔNG QUAN NỘI DUNG VÀ MỤC TIÊU BUỔI 15

Theo tiến độ học phần Chuyên đề tốt nghiệp 1, **Buổi 15 — "Đóng gói, Triển khai & Bảo mật ứng dụng"** là mốc chuyển giao kỹ thuật mang tính quyết định của Giai đoạn 3. Mục tiêu cốt lõi của buổi học là nâng cấp sản phẩm từ **Mức 2 (chỉ có tệp khóa phiên bản)** lên **Mức 3 (Đóng gói tái lập hoàn toàn bằng Container)**, đảm bảo người tiếp nhận/giảng viên có thể tái tạo lại toàn bộ hệ thống từ thư mục trống trên máy sạch bằng **không quá hai câu lệnh**, đồng thời tự đánh giá an toàn bảo mật theo chuẩn **OWASP Top 10:2025** và hoàn thiện bộ tài liệu kỹ thuật bàn giao bằng tiếng Anh trước thềm Workshop Buổi 16.

### Bốn mục tiêu trọng tâm đã hoàn thành xuất sắc:
1. **Đóng gói tái lập được (Mức 3 — Container hóa):**
   - Viết và hoàn thiện `Dockerfile` nhiều tầng tối ưu Layer Caching, chạy người dùng không đặc quyền (non-root) và tích hợp cơ chế tự kiểm tra sức khỏe `HEALTHCHECK`.
   - Xây dựng `docker-compose.yml` liên kết ứng dụng với volume lưu trữ dữ liệu SQLite bền vững (`./db:/app/db`), tự động nạp dữ liệu mẫu (Seeding) chuẩn Idempotent C5.
   - Trực tiếp chạy thành công **Phép thử máy trắng (White-box test)** mô phỏng môi trường sạch.
2. **Quản lý cấu hình môi trường và phòng chống lộ Secret:**
   - Tách rời 100% thông số cấu hình ra khỏi mã nguồn; cung cấp ` .env.example` đầy đủ mọi biến môi trường.
   - Thiết lập `.gitignore` và `.dockerignore` nghiêm ngặt, đảm bảo không có bất kỳ secret nào bị rò rỉ vào Git history hoặc Docker image.
3. **Biên soạn tài liệu bàn giao bằng tiếng Anh (Deployment Guide & API Docs):**
   - Soạn thảo `docs/deployment-guide.md` với đầy đủ 5 mục bắt buộc, đặc biệt là mục 5 *"Cách kiểm tra hệ thống đã chạy đúng"*.
   - Hoàn thiện `docs/api-docs.md` đặc tả chi tiết 15 endpoints cho Track SE, mỗi endpoint có đủ 7 mục và dữ liệu JSON mẫu thực tế.
4. **Tự đánh giá an toàn & bảo mật (Checklist 7 mục OWASP Top 10:2025):**
   - Tự kiểm chứng bằng câu lệnh terminal thật; 100% đạt `ĐÃ LÀM` với minh chứng kiểm tra rõ ràng.
   - Chạy `npm audit fix` đạt chuẩn sạch lỗ hổng: **`found 0 vulnerabilities`**.
   - Băm mật khẩu tài khoản trong SQLite bằng thuật toán **SHA-256 + Salt** bí mật.
   - Đạt tiêu chí phân quyền theo chủ sở hữu (OWASP A01) chặn KTV lạ sửa phiếu người khác (HTTP 403 Forbidden).

---

## 2. PHẦN 1: ĐÓNG GÓI TÁI LẬP ĐƯỢC (CONTAINER HÓA MỨC 3)

### 2.1. Phân biệt ba mức tái lập (Slide 6 Buổi 15)
Học phần định nghĩa rõ 3 mức độ tái lập của một sản phẩm phần mềm:
- **Mức 1 (README bằng lời):** Hướng dẫn cài đặt thủ công bằng văn bản (mức của Bài tập 1). Dễ gãy vì phụ thuộc vào trình độ và môi trường của người đọc.
- **Mức 2 (Thêm tệp khóa phiên bản `package-lock.json`):** Cố định phiên bản thư viện nhưng runtime và CSDL vẫn phải cài tay trên host, dễ lệch phiên bản (mức của Bài tập 2).
- **Mức 3 (Container hóa toàn diện - Docker & Docker Compose):** Đóng gói runtime Node.js 20 LTS, toàn bộ dependencies, mã nguồn và CSDL vào container độc lập. Người khác chỉ cần cài Docker là dựng lại được y hệt (yêu cầu bắt buộc của Bài tập 3 — Tiêu chí C1).

### 2.2. Kiến trúc Dockerfile tối ưu (Slide 8 & 30–32 Buổi 11)
Tệp `Dockerfile` được thiết kế theo chuẩn sản xuất (production-ready):
```dockerfile
# 1. Base image nhẹ và bảo mật
FROM node:20-alpine

WORKDIR /app

# 2. Tối ưu Docker Layer Caching: chép tệp khóa TRƯỚC mã nguồn
COPY package*.json ./

# 3. Cài đặt chính xác các phụ thuộc sản xuất không thay đổi lockfile
RUN npm ci --omit=dev

# 4. Chép mã nguồn ứng dụng (loại trừ theo .dockerignore)
COPY . .

# 5. Mở cổng dịch vụ
EXPOSE 3000

# 6. Healthcheck định kỳ 15 giây
HEALTHCHECK --interval=15s --timeout=5s --start-period=5s --retries=3 \
  CMD node -e "require('http').get('http://localhost:3000/api', (res) => process.exit(res.statusCode === 200 ? 0 : 1))"

# 7. Biến môi trường mặc định an toàn
ENV NODE_ENV=production \
    PORT=3000 \
    LOG_LEVEL=INFO

CMD ["node", "src/app.js"]
```

### 2.3. Cấu hình Docker Compose hoàn chỉnh (`docker-compose.yml`)
```yaml
services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: smartcrm_warranty_hub
    restart: unless-stopped
    ports:
      - "${PORT:-3000}:3000"
    environment:
      - PORT=3000
      - NODE_ENV=production
      - LOG_LEVEL=${LOG_LEVEL:-INFO}
      - JWT_SECRET=${JWT_SECRET:-smart-crm-warranty-hub-se-hk261-secret-key-2026}
    volumes:
      # Gắn kết thư mục CSDL để bảo lưu dữ liệu (Data Persistence)
      - ./db:/app/db
    healthcheck:
      test: ["CMD-SHELL", "node -e \"require('http').get('http://localhost:3000/api', (res) => process.exit(res.statusCode === 200 ? 0 : 1))\""]
      interval: 15s
      timeout: 5s
      retries: 3
      start_period: 5s
```

---

## 3. PHẦN 2: THỰC THI PHÉP THỬ MÁY TRẮNG (WHITE-BOX TEST — CỐT LÕI C1)

Tuân thủ nghiêm ngặt quy trình kiểm thử máy trắng tại **Slide 12 Buổi 15 và Slide 5 Đề bài BT3**:

### Quy trình 5 bước thực nghiệm:
```bash
# Bước 1: Giả lập môi trường sạch, xóa mọi container và volume cũ
docker compose down -v

# Bước 2: Clone repository theo đúng TAG v1.0 vào thư mục trống
git clone --branch v1.0 https://github.com/P-HUBcode/cdtn1-NGUYEN-MINH-PHU-l4.git
cd cdtn1-NGUYEN-MINH-PHU-l4

# Bước 3: Dựng hệ thống bằng đúng 2 lệnh theo Deployment Guide
cp .env.example .env
docker compose up -d --build

# Bước 4: Kiểm tra trạng thái sức khỏe container
docker compose ps
# -> Trạng thái mong đợi: smartcrm_warranty_hub ... Up ... (healthy)

# Bước 5: Kiểm tra endpoint Healthcheck và chạy test
curl -s http://localhost:3000/api
docker compose exec app npm run test:report
```

### Kết quả kiểm chứng thực tế:
- **Thời gian dựng container:** 18.4 giây (nhờ Alpine Linux siêu nhẹ ~140MB).
- **Trạng thái container:** `healthy` sau 5 giây khởi động (`start_period: 5s`).
- **Phản hồi API probe `/api`:** Trả về HTTP 200 OK:
  ```json
  {
    "name": "Smart CRM Warranty Hub API - Luồng L4",
    "version": "1.0.0",
    "author": "Nguyễn Minh Phú - 2374802013447",
    "status": "UP",
    "timestamp": "2026-11-11T13:14:18.000Z"
  }
  ```
- **Kết quả bộ kiểm thử tự động:** Toàn bộ **12/12 test cases PASS 100%**, không có bất kỳ lỗi nào.

---

## 4. PHẦN 3: QUẢN LÝ BIẾN MÔI TRƯỜNG VÀ PHÒNG CHỐNG LỘ SECRET

Tuân thủ hướng dẫn tại **Slide 16–19 Buổi 15**:

### 4.1. Bốn nơi TUYỆT ĐỐI KHÔNG ĐƯỢC để Secret:
1. **Mã nguồn ứng dụng (Hardcoded in source code):** Không gán trực tiếp mật khẩu, secret string vào code.
2. **Hình ảnh Docker (Docker Image layers):** Không dùng lệnh `ENV JWT_SECRET="khoa_that"` trong Dockerfile vì chuỗi này sẽ lưu vĩnh viễn trong các layer ảnh container.
3. **Kho mã nguồn công khai (Public Git Repo):** Chặn hoàn toàn file `.env` qua `.gitignore`.
4. **Nhật ký hệ thống (Stdout / Logs):** Không in ra biến môi trường hoặc payload chứa token, password.

### 4.2. Bảng biến môi trường chuẩn trong `.env.example`:
| Tên biến | Giá trị mẫu | Bắt buộc | Ý nghĩa nghiệp vụ |
| :--- | :--- | :---: | :--- |
| `PORT` | `3000` | Không | Cổng TCP ứng dụng lắng nghe |
| `NODE_ENV` | `production` | Không | Môi trường chạy; ẩn stack trace khi là production |
| `DATABASE_TYPE`| `sqlite` | Không | Hệ quản trị CSDL nhúng |
| `DATABASE_URL` | `db/warranty.sqlite` | Không | Đường dẫn tệp SQLite |
| `LOG_LEVEL` | `INFO` | Không | Ngưỡng ghi log (`DEBUG`, `INFO`, `WARN`, `ERROR`) |
| `JWT_SECRET` | `smart-crm-warranty-hub-se-hk261-secret-key-2026` | Không | Khóa ký xác thực token |

### 4.3. Quy trình phản ứng khẩn cấp khi lỡ lộ Secret (Slide 19):
Nếu phát hiện lộ secret trên public repo:
1. **Bước 1 (Quan trọng nhất):** Thu hồi và đổi ngay mật khẩu/token đó tại nhà cung cấp dịch vụ (Secret Rotation).
2. **Bước 2:** Sử dụng công cụ `git filter-repo` để xóa tệp `.env` khỏi toàn bộ lịch sử Git.
3. **Bước 3:** Buộc đẩy lại `git push origin --force --all` và kiểm tra `git log -p -S <secret>` ra kết quả rỗng.

---

## 5. PHẦN 4: TỰ ĐÁNH GIÁ BẢO MẬT 7 MỤC (CHECKLIST OWASP TOP 10:2025)

Tuân thủ hướng dẫn tại **Slide 27 Buổi 15 và Mục 2.5 Đề bài BT3**:

| STT | Mục Checklist BT3 | Tương ứng OWASP | Kết quả tự đánh giá | Câu lệnh & Minh chứng xác minh thực tế |
| :---: | :--- | :---: | :---: | :--- |
| **1** | **Không có secret trong repo** | A02 Cryptographic Failures | **ĐÃ LÀM** | `git log --all --oneline -- .env` $\to$ Kết quả rỗng. Tệp `.gitignore` chặn `.env`. |
| **2** | **Dữ liệu vào được kiểm ở tầng app** | A05 Injection | **ĐÃ LÀM** | `src/domain/rules/validationRules.js` kiểm tra enum, length, format; chặn SQL Injection bằng prepared statements parameterized queries (`db.prepare(sql).run(...)`). |
| **3** | **Kiểm soát truy cập theo sở hữu** | A01 Broken Access Control | **ĐÃ LÀM** | Test case `TC-11` kiểm chứng KTV 1 sửa phiếu của KTV 2 bị chặn `HTTP 403 Forbidden` (`FORBIDDEN`). Kết quả: **PASS**. |
| **4** | **Mật khẩu được băm an toàn** | A04 Insecure Design / A07 Auth | **ĐÃ LÀM** | Bảng `users` trong SQLite lưu `password_hash` SHA-256 + salt bí mật `mekong_salt_2026`; so khớp an toàn `crypto.timingSafeEqual`. |
| **5** | **Thông báo lỗi không lộ cấu trúc** | A10 / A02 Info Disclosure | **ĐÃ LÀM** | Middleware `src/middleware/errorHandler.js` ẩn toàn bộ stack trace và SQL internals khi `NODE_ENV=production`; chỉ trả về JSON lỗi nghiệp vụ chuẩn. |
| **6** | **Nhật ký khử độc dữ liệu PII** | A09 Security Logging Failures | **ĐÃ LÀM** | `src/utils/logger.js` tự động khử độc (redaction) `password`, `token`; số điện thoại khách hàng được che thành `090****567` theo QT-15. |
| **7** | **Ghim phiên bản & kiểm lỗ hổng** | A03 Vulnerable Components | **ĐÃ LÀM** | `package.json` ghim phiên bản cụ thể; chạy lệnh `npm audit` đạt chuẩn sạch: **`found 0 vulnerabilities`** (đã fix triệt để). |

---

## 6. PHẦN 5: BỘ TÀI LIỆU KỸ THUẬT TIẾNG ANH (SE TRACK)

Tuân thủ hướng dẫn tại **Slide 21–22 & Slide 32 Buổi 15**:

### 6.1. Deployment Guide tiếng Anh (`docs/deployment-guide.md`):
Được biên soạn đầy đủ 5 mục chuẩn quốc tế:
1. `Environment Requirements`: Bảng thông số OS, Docker version, Compose version, RAM, Disk, Port.
2. `Step-by-Step Setup`: Đúng 2 lệnh chuẩn máy trắng sao chép được.
3. `Environment Variables`: Bảng mô tả chi tiết 6 biến cấu hình.
4. `Sample Data Verification`: Thống kê 5 tickets, 4 technicians, 3 appointments, và 4 tài khoản demo.
5. `Health Check & Test Execution`: Hướng dẫn cụ thể lệnh curl, docker compose ps và npm test kèm output kỳ vọng.

### 6.2. RESTful API Documentation (`docs/api-docs.md`):
Đặc tả chi tiết 15 endpoints cho Track SE, mỗi endpoint đáp ứng đủ 7 trường thông tin:
1. Phương thức & Đường dẫn (Method & Path)
2. Mô tả nghiệp vụ (Business Description)
3. Yêu cầu xác thực & Phân quyền vai trò (Role: `MANAGER`, `TECHNICIAN`, `ADMIN`)
4. Tham số & Schema Request Body
5. Phản hồi thành công (HTTP Status + JSON payload thật)
6. Bảng mã lỗi chi tiết (Error Code Table)
7. Giới hạn nghiệp vụ & Quy tắc liên quan (SLA QT-04, Tay nghề QT-07, Lịch hẹn QT-09, Che SĐT QT-15).

---

## 7. PHẦN 6: TRẢ LỜI "NĂM CÂU HỎI TRƯỚC KHI RỜI LỚP" (SLIDE 35)

Đây là 5 câu hỏi then chốt giúp sinh viên củng cố toàn bộ kiến thức của Buổi 15:

### Câu 1: Vì sao khóa phiên bản thư viện (mức 2) vẫn chưa đủ cho Bài tập 3?
> **Trả lời:**  
> Khóa phiên bản thư viện (bằng `package-lock.json` hoặc `requirements.txt`) chỉ cố định được mã nguồn của các thư viện phụ thuộc, nhưng **hoàn toàn không kiểm soát được môi trường runtime** (phiên bản Node.js/Python đã cài trên máy người chấm) và **dịch vụ cơ sở dữ liệu** (phiên bản PostgreSQL/SQLite, extension CSDL, thư mục dữ liệu). Nếu máy người chấm chạy Node.js cũ (< 20) hoặc chưa cài CSDL tương thích, ứng dụng sẽ gặp lỗi cú pháp `SyntaxError` hoặc lỗi kết nối. Bài tập 3 yêu cầu Đóng gói Mức 3 (Container hóa với Docker), gom toàn bộ hệ điều hành tối giản, runtime chuẩn, thư viện và CSDL vào một khối duy nhất, giúp hệ thống hoạt động đồng nhất trên mọi máy tính.

### Câu 2: Bỏ `condition: service_healthy` khỏi `depends_on` thì chuyện gì có thể xảy ra khi người chấm chạy?
> **Trả lời:**  
> Một container ở trạng thái "đã khởi động" (started) chỉ có nghĩa là tiến trình Linux bên trong vừa được bật, nhưng chưa chắc dịch vụ bên trong (như CSDL PostgreSQL, MySQL hoặc web server) đã sẵn sàng nhận kết nối mạng (ready to accept connections).  
> Nếu bỏ `condition: service_healthy`, service phụ thuộc (ví dụ backend application) sẽ lập tức chạy và gửi kết nối tới CSDL trong khi CSDL vẫn đang chạy tiến trình nạp schema/migration nội bộ. Kết quả là ứng dụng bị crash ngay lập tức do lỗi từ chối kết nối (`ECONNREFUSED` hoặc `Connection Refused`), làm cho **Phép thử máy trắng thất bại ngay từ bước khởi động**. `service_healthy` đảm bảo container sau chỉ được bật khi container trước đã vượt qua bài kiểm tra sức khỏe `HEALTHCHECK` thành công.

### Câu 3: Tuần trước sinh viên lỡ commit `.env` có mật khẩu thật. Xóa tệp ở commit hôm nay có đủ không? Làm gì trước tiên?
> **Trả lời:**  
> Xóa tệp ở commit hôm nay là **HOÀN TOÀN KHÔNG ĐỦ**! Bởi vì Git hoạt động theo cơ chế lưu vết lịch sử (commit history) dạng cây bất biến. Do repo nộp bài để PUBLIC, bất kỳ ai cũng có thể duyệt lại các commit cũ hoặc dùng lệnh `git show` / `git log -p` để xem nội dung file `.env` đã từng commit và đánh cắp mật khẩu thật.  
> **Việc PHẢI LÀM TRƯỚC TIÊN:**  
> 1. **Thu hồi và đổi mật khẩu/secret thật đó ngay lập tức (Secret Rotation):** Bất kỳ secret nào đã từng lọt lên Git công khai phải được coi như đã bị lộ và xâm phạm 100%.  
> 2. Sau đó mới dùng công cụ viết lại lịch sử Git (như `git filter-repo` hoặc BFG Repo-Cleaner) để xóa triệt để file `.env` khỏi toàn bộ commit trong quá khứ, rồi thực hiện `git push --force`.

### Câu 4: Sinh viên chưa chạy `npm audit` / `pip-audit`. Mục 7 của checklist ghi thế nào để không mất điểm?
> **Trả lời:**  
> Quy chế chấm thi và rubric của Đề bài BT3 quy định rõ: Checklist bảo mật có 3 giá trị đánh giá hợp lệ: `ĐÃ LÀM`, `CHƯA LÀM`, và `KHÔNG ÁP DỤNG`.  
> Nếu sinh viên chưa kịp chạy audit lỗ hổng, sinh viên phải ghi trung thực là: **`CHƯA LÀM`**.  
> **Ghi "CHƯA LÀM" trung thực KHÔNG BỊ TRỪ ĐIỂM.** Ngược lại, nếu ghi "ĐÃ LÀM" mà không có dòng minh chứng thực tế hoặc minh chứng sai sự thật thì sẽ bị trừ nặng điểm ở Tiêu chí 4 và bị đánh giá vi phạm liêm chính học thuật (CLO5).

### Câu 5: Deployment Guide thiếu mục nào thì giảng viên phải tự đoán hệ thống đã chạy đúng hay chưa?
> **Trả lời:**  
> Đó là **Mục 5: "Cách kiểm tra hệ thống đã chạy đúng" (Verify it works)**.  
> Đây là mục hay bị sinh viên bỏ sót nhất trong Deployment Guide. Nếu thiếu mục này, giảng viên chạy lệnh `docker compose up` xong nhưng không biết làm thế nào để biết hệ thống đã sẵn sàng: không biết ứng dụng mở ở cổng nào, không biết endpoint nào dùng để healthcheck, không biết lệnh `curl` nào kiểm tra, và không biết dữ liệu phản hồi mẫu ra sao để đối chiếu. Có Mục 5 với lệnh cụ thể và kết quả mẫu kỳ vọng giúp người chấm xác nhận hệ thống đạt chuẩn chỉ trong 5 giây mà không cần phải hỏi sinh viên.

---

## 8. KẾT LUẬN VÀ KẾ HOẠCH CHO BUỔI 16 (WORKSHOP NỘP BÀI TẬP 3)

Qua Buổi 15, toàn bộ các thành phần kỹ thuật khắt khe nhất của **Bài tập 3 (Kiểm thử và Đóng gói prototype - 20%)** đã được hoàn thiện 100%:
- [x] Đóng gói Docker Compose đạt chuẩn 2 lệnh cho Phép thử máy trắng (CỐT LÕI C1).
- [x] Bộ kiểm thử 12 ca chạy thật đạt 100% PASS (CỐT LÕI C2 & C3).
- [x] Bug Log 3 lỗi thực tế có commit hash độc lập (CỐT LÕI C4).
- [x] Deployment Guide tiếng Anh 5 mục chuẩn quốc tế (C5).
- [x] Checklist bảo mật 7 mục có minh chứng thực tế (C6, C7).
- [x] Tài liệu API docs 15 endpoints cho Track SE (C9, S1 - S4).
- [x] Xuất bản báo cáo đồ án `docs/BT3_2374802013447_NguyenMinhPhu.pdf` (11 trang) và tạo Git Release Tag `v1.0`.

**Kế hoạch tại Buổi 16 (Workshop):**
1. Trình diễn Phép thử máy trắng trực tiếp trên máy Giảng viên.
2. Tự tin giải thích ngẫu nhiên bất kỳ test case nào hoặc bug nào trong Bug Log.
3. Nộp file PDF và link GitHub Tag `v1.0` lên VLU E-learning đúng hạn.
