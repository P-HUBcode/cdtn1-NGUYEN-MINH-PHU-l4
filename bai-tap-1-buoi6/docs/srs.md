# BẢN ĐẶC TẢ YÊU CẦU PHẦN MỀM (SRS RÚT GỌN) & HỒ SƠ BÀI TẬP 1

**Thông tin sinh viên:**
- Họ và tên: Nguyễn Minh Phú
- MSSV: 2374802013447
- Chuyên ngành (Track): **SE (Software Engineering)**
- Luồng nghiệp vụ chọn: **L4 - Phân công kỹ thuật viên và lịch hẹn**

---

## MỤC 1. GIỚI THIỆU VÀ PHẠM VI

### 1.1 Bối cảnh doanh nghiệp
Hệ thống bảo hành dịch vụ kỹ thuật quản lý việc tiếp nhận, sửa chữa, phân công và bàn giao thiết bị bảo hành cho khách hàng qua chuỗi trung tâm. Việc phân công kỹ thuật viên (KTV) trước đây chủ yếu thực hiện thủ công, dễ dẫn đến tình trạng quá tải cục bộ (Vấn đề V3), phiếu bảo hành bị trễ hạn cam kết SLA (Vấn đề V2) và thiếu minh bạch trong lịch sử xử lý.

### 1.2 Luồng nghiệp vụ chọn & Phạm vi (Một câu)
> Hệ thống hỗ trợ Quản lý trung tâm bảo hành phân công phiếu bảo hành cho kỹ thuật viên phù hợp dựa trên tay nghề, trung tâm làm việc và khối lượng công việc hiện tại; cho phép đặt và quản lý lịch hẹn giao – nhận máy với khách hàng, đồng thời tự động theo dõi hạn cam kết (SLA) và lịch sử chuyển trạng thái.

### 1.3 Điều CHỦ Ý KHÔNG LÀM (Mức WON'T của MoSCoW)
| Mã | Nội dung chủ ý không làm | Ghi chú phạm vi |
| :---: | :--- | :--- |
| **WON'T-01** | Không tự động mua sắm hoặc đặt hàng linh kiện tự động từ nhà cung cấp bên ngoài. | Thuộc hệ thống quản lý chuỗi cung ứng độc lập |
| **WON'T-02** | Không tích hợp thanh toán trực tuyến chi phí ngoài bảo hành trong phiên bản này. | Xử lý thủ công tại quầy thu ngân trung tâm |
| **WON'T-03** | Không tự động điều phối KTV di chuyển sửa chữa tại nhà khách hàng. | Chỉ áp dụng với bảo hành tại trung tâm |

### 1.4 Bảng thuật ngữ nghiệp vụ
| STT | Thuật ngữ | Khái niệm / Giải thích nghiệp vụ |
| :---: | :--- | :--- |
| 1 | **Phiếu bảo hành (Ticket)** | Yêu cầu bảo hành/sửa chữa thiết bị do khách hàng gửi, có mã định danh duy nhất. |
| 2 | **Kỹ thuật viên (KTV)** | Nhân viên kỹ thuật thực hiện chẩn đoán và sửa chữa thiết bị tại trung tâm. |
| 3 | **Hạn cam kết (SLA / Due Date)** | Thời hạn tối đa hệ thống/trung tâm cam kết hoàn thành sửa chữa cho khách hàng. |
| 4 | **Tay nghề (Proficiency)** | Mức độ thành thạo của KTV với nhóm kỹ năng/thiết bị cụ thể (thang điểm 1–5). |
| 5 | **Lịch hẹn (Appointment)** | Khung thời gian hẹn trước giữa khách hàng và trung tâm để giao máy hoặc nhận lại máy. |
| 6 | **Nhật ký trạng thái (Status Log)** | Bản ghi lịch sử ghi nhận mỗi lần phiếu bảo hành thay đổi trạng thái, KTV hoặc lịch hẹn. |

---

## MỤC 2. CÁC BÊN LIÊN QUAN VÀ VAI TRÒ NGƯỜI DÙNG

| Vai trò / Tác nhân | Loại Actor | Mô tả vai trò | Quyền hạn & Trách nhiệm chính |
| :--- | :---: | :--- | :--- |
| **Quản lý trung tâm bảo hành** | Human | Người điều hành công việc tại 1 trung tâm bảo hành cụ thể. | • Xem danh sách phiếu chờ phân công & tải KTV<br>• Phân công & chuyển gán phiếu cho KTV<br>• Đặt & quản lý lịch hẹn giao – nhận máy |
| **Kỹ thuật viên (KTV)** | Human | Nhân viên trực tiếp thao tác sửa chữa thiết bị. | • Xem phiếu gán cho mình xếp theo SLA<br>• Cập nhật trạng thái tiến độ xử lý phiếu<br>• Tra cứu lịch sử thiết bị theo IMEI/Serial |
| **Hệ thống cảnh báo SLA** | Timer | Actor tự động chạy theo lịch định kỳ. | • Tự động tính hạn SLA khi phân công phiếu<br>• Phát cảnh báo khi phiếu sắp quá hạn hoặc quá hạn SLA |

---

## MỤC 3. YÊU CẦU CHỨC NĂNG VÀ DANH SÁCH USER STORY

### 3.1 Danh sách Yêu cầu Chức năng (Functional Requirements - FR)
- **FR1**: Hệ thống cho phép Quản lý trung tâm xem danh sách phiếu chờ phân công kèm số lượng phiếu đang xử lý của từng KTV trong cùng trung tâm.
- **FR2**: Hệ thống cung cấp tính năng tự động gợi ý danh sách KTV phù hợp dựa trên tay nghề (proficiency $\ge$ 3), trung tâm hoạt động và tải công việc thấp nhất.
- **FR3**: Hệ thống cho phép Quản lý trung tâm thực hiện gán phiếu bảo hành hoặc chuyển gán phiếu (re-assign) sang KTV khác kèm lý do bắt buộc.
- **FR4**: Hệ thống hỗ trợ khởi tạo và quản lý lịch hẹn giao – nhận máy với khách hàng (chọn khung giờ, loại hẹn).
- **FR5**: Hệ thống cho phép KTV xem danh sách công việc được gán, tự động sắp xếp theo hạn cam kết SLA (due_date) tăng dần.
- **FR6**: Hệ thống cho phép KTV cập nhật trạng thái xử lý phiếu bảo hành và ghi nhận tự động vào lịch sử log (`ticket_status_log`).
- **FR7**: Hệ thống hỗ trợ tra cứu lịch sử sửa chữa thiết bị theo IMEI / Serial.

### 3.2 Bảng Danh sách 8 User Story đạt chuẩn INVEST & MoSCoW (Rút gọn)

| Mã US | Vai trò (Role) | Mục tiêu & Giá trị (User Story) | MoSCoW | Tiêu chí chấp nhận Given-When-Then (Acceptance Criteria) |
| :---: | :---: | :--- | :---: | :--- |
| **US1** | Quản lý trung tâm | Tôi muốn xem danh sách phiếu chờ phân công kèm số phiếu đang giữ của các KTV trung tâm để nắm tổng quan và phân công hợp lý. | **MUST** | • **AC1.1 (Happy)**: GIVEN Quản lý chọn trung tâm, THEN hiển thị phiếu MỚI và tải công việc từng KTV.<br>• **AC1.2 (Exception)**: GIVEN Không có phiếu chờ, THEN hiển thị "Không có phiếu bảo hành nào đang chờ phân công". |
| **US2** | Quản lý trung tâm | Tôi muốn hệ thống tự động gợi ý KTV phù hợp theo tay nghề (proficiency $\ge$ 3), cùng trung tâm & tải ít nhất để phân công đúng người, tránh quá tải (V3). | **MUST** | • **AC2.1 (Happy)**: GIVEN Nhóm 'MAN_HINH', WHEN nhấn 'Gợi ý KTV', THEN trả về KTV proficiency $\ge$ 3 xếp theo số phiếu đang giữ tăng dần.<br>• **AC2.2 (Happy)**: GIVEN Chọn KTV & bấm Phân công, THEN đổi status='DANG_XU_LY', tính SLA due_date và ghi log.<br>• **AC2.3 (Exception)**: GIVEN Không có KTV proficiency $\ge$ 3, THEN cảnh báo "Không có KTV phù hợp đạt chuẩn tay nghề, đề nghị chọn thủ công". |
| **US3** | Quản lý trung tâm | Tôi muốn đặt và quản lý lịch hẹn giao – nhận máy với khách hàng theo khung giờ 30 phút để tối ưu lịch làm việc trung tâm. | **MUST** | • **AC3.1 (Happy)**: GIVEN Phiếu hợp lệ, WHEN chọn ngày, khung giờ (09:00-09:30) & loại hẹn, THEN lưu lịch hẹn mới vào `appointments`.<br>• **AC3.2 (Exception)**: GIVEN Chọn ngày quá khứ hoặc khung giờ hẹn đã đủ 5 lịch, THEN báo lỗi "Khung giờ hẹn đã kín hoặc thời gian không hợp lệ". |
| **US4** | Kỹ thuật viên | Tôi muốn xem danh sách phiếu bảo hành được gán sắp xếp ưu tiên theo hạn cam kết SLA (due_date) để ưu tiên phiếu sắp quá hạn trước (V2). | **MUST** | • **AC4.1 (Happy)**: GIVEN KTV đăng nhập, WHEN mở 'Phiếu của tôi', THEN hiển thị các phiếu gán sắp xếp theo due_date tăng dần.<br>• **AC4.2 (Exception)**: GIVEN KTV không giữ phiếu nào, THEN hiển thị "Hiện tại bạn không có phiếu bảo hành nào cần xử lý". |
| **US5** | Kỹ thuật viên | Tôi muốn cập nhật chuyển trạng thái xử lý phiếu kèm ghi chú lý do để minh bạch tiến độ sửa chữa và tự động lưu log (`ticket_status_log`). | **MUST** | • **AC5.1 (Happy)**: GIVEN Phiếu 'DANG_XU_LY', WHEN đổi sang 'CHO_LINH_KIEN' kèm ghi chú, THEN hệ thống lưu trạng thái mới và ghi log.<br>• **AC5.2 (Exception)**: GIVEN Phiếu trạng thái 'MOI', WHEN KTV cố bấm 'HOAN_TAT', THEN hệ thống chặn và thông báo "Phiếu chưa được phân công KTV". |
| **US6** | Quản lý trung tâm | Tôi muốn chuyển phiếu bảo hành sang KTV khác kèm bắt buộc nhập lý do chuyển để đảm bảo phiếu xử lý đúng SLA. | **SHOULD** | • **AC6.1 (Happy)**: GIVEN KTV A nghỉ phép, WHEN chọn KTV B & nhập lý do $\ge 10$ ký tự, THEN hệ thống đổi `technician_id` sang KTV B và ghi log. |
| **US7** | KTV / Quản lý | Tôi muốn tra cứu lịch sử sửa chữa trước đó của thiết bị theo IMEI / Serial để phát hiện lỗi lặp lại và có phương án kỹ thuật phù hợp. | **SHOULD** | • **AC7.1 (Happy)**: GIVEN Nhập IMEI/Serial hợp lệ, WHEN bấm Tra cứu, THEN hiển thị toàn bộ lịch sử các phiếu bảo hành quá khứ. |
| **US8** | Quản lý trung tâm | Tôi muốn cập nhật và dời lịch hẹn giao - nhận máy khi phát sinh sự cố để quản lý thời gian linh hoạt. | **SHOULD** | • **AC8.1 (Happy)**: GIVEN Lịch hẹn đã xác nhận, WHEN chọn mốc thời gian mới, THEN lưu cập nhật và đổi trạng thái lịch hẹn thành 'DA_DOI_LICH'. |

---

## MỤC 4. YÊU CẦU PHI CHỨC NĂNG (NFR) CÓ NGƯỠNG ĐO ĐƯỢC

- **NFR1 (Performance - Hiệu năng)**: Màn hình danh sách phiếu chờ phân công và khối lượng KTV phải load và hiển thị hoàn tất trong thời gian **dưới 1.5 giây** với cơ sở dữ liệu thử nghiệm chứa **10.000 phiếu bảo hành** và **50 KTV** trên máy chủ RAM 8 GB.
- **NFR2 (Security - Bảo mật & Phân quyền)**: **100%** các thao tác phân công KTV (`/assign`, `/reassign`) chỉ được thực hiện bởi tài khoản có role `SERVICE_CENTER_MANAGER`. KTV thông thường gọi API phân công phải bị từ chối với mã HTTP `403 Forbidden`.
- **NFR3 (Reliability & Data Integrity - Tin cậy & Vẹn toàn dữ liệu)**: **100%** thao tác chuyển trạng thái phiếu, phân công KTV và tạo lịch hẹn phải được thực hiện trong **Database Transaction**. Nếu ghi log thất bại, toàn bộ quá trình cập nhật phiếu phải Rollback để đảm bảo không mất mát lịch sử.
- **NFR4 (Usability - Khả dụng)**: Quản lý trung tâm bảo hành thao tác phân công 1 phiếu dựa trên gợi ý tự động của hệ thống hoàn tất trong **dưới 30 giây** (tối đa 3 lượt click chuột).

---

## MỤC 5. RÀNG BUỘC VÀ QUY TẮC NGHIỆP VỤ (BUSINESS RULES)

- **QT-04 (Quy tắc SLA)**: Hạn cam kết SLA (`due_date`) được tự động tính tại thời điểm phân công phiếu:
  - Mức ưu tiên `CAO`: `received_at` + 24 giờ.
  - Mức ưu tiên `TRUNG_BÌNH`: `received_at` + 48 giờ.
  - Mức ưu tiên `THẤP`: `received_at` + 72 giờ.
- **QT-06 (Quy tắc Gán KTV duy nhất & Cùng trung tâm)**: Tại một thời điểm, một phiếu bảo hành chỉ được gán cho duy nhất 1 KTV. KTV được gán BẮT BUỘC phải làm việc tại đúng Trung tâm bảo hành (`center_id`) tiếp nhận phiếu đó.
- **QT-07 (Quy tắc Tay nghề gợi ý)**: Hệ thống chỉ đưa KTV vào danh sách gợi ý phân công nếu điểm tay nghề của KTV đó đối với nhóm sự cố của phiếu (`issue_category`) đạt điểm `proficiency >= 3`.
- **QT-08 (Quy tắc Chuyển phiếu bắt buộc lý do)**: Thao tác re-assign phiếu từ KTV cũ sang KTV mới yêu cầu bắt buộc nhập `reason` (chuỗi ký tự $\ge 10$ ký tự) và ghi lại log trong `ticket_status_log`.
- **QT-09 (Quy tắc Lịch hẹn)**: Lịch hẹn giao/nhận máy không được chọn mốc thời gian trong quá khứ (`appointment_date >= current_timestamp`). Mỗi khung giờ 30 phút tại 1 trung tâm tối đa nhận 5 lịch hẹn.

---

## MỤC 6. BẢNG TRUY VẾT YÊU CẦU (REQUIREMENT TRACEABILITY MATRIX)

| Mã FR | Yêu cầu chức năng | User Story | Use Case | MoSCoW | Test Case (BT3) |
| :---: | :--- | :---: | :---: | :---: | :--- |
| **FR1** | Xem danh sách chờ phân công & khối lượng KTV | US1 | UC1 | **MUST** | TC_FR1_01, TC_FR1_02 |
| **FR2** | Gợi ý & phân công KTV dựa trên tay nghề & tải | US2 | UC2 | **MUST** | TC_FR2_01, TC_FR2_02, TC_FR2_03 |
| **FR3** | Phân công / Chuyển gán KTV kèm bắt buộc nhập lý do | US2, US6 | UC2, UC6 | **MUST / SHOULD** | TC_FR3_01, TC_FR3_02 |
| **FR4** | Đặt & quản lý lịch hẹn giao – nhận máy với khách | US3, US8 | UC3 | **MUST** | TC_FR4_01, TC_FR4_02 |
| **FR5** | Xem danh sách phiếu của KTV sắp xếp theo SLA | US4 | UC4 | **MUST** | TC_FR5_01, TC_FR5_02 |
| **FR6** | Cập nhật trạng thái phiếu & tự động lưu nhật ký log | US5 | UC5 | **MUST** | TC_FR6_01, TC_FR6_02 |
| **FR7** | Tra cứu lịch sử sửa chữa thiết bị theo IMEI / Serial | US7 | UC7 | **SHOULD** | TC_FR7_01 |

---

## MỤC 7. ĐẶC TẢ CHI TIẾT USE CASE QUAN TRỌNG NHẤT (UC2)

### UC2 – GỢI Ý VÀ PHÂN CÔNG KỸ THUẬT VIÊN CHO PHIẾU BẢO HÀNH

- **Actor chính**: Quản lý trung tâm bảo hành
- **Mục tiêu**: Phân công phiếu bảo hành cho KTV phù hợp nhất thuộc trung tâm để tiến hành sửa chữa đúng hạn SLA.
- **Điều kiện trước**: Quản lý đã đăng nhập với quyền `SERVICE_CENTER_MANAGER`. Phiếu bảo hành ở trạng thái `MỚI` và thuộc trung tâm quản lý.
- **Điều kiện sau**: Phiếu bảo hành được cập nhật `technician_id`, đổi `status='DANG_XU_LY'`, có SLA `due_date` và ghi log `ticket_status_log`.

#### LUỒNG CHÍNH (Happy Path):
1. Quản lý chọn 1 phiếu bảo hành chờ phân công.
2. Quản lý nhấn nút "Gợi ý KTV phù hợp".
3. Hệ thống xác định `category_id` và `center_id` của phiếu.
4. Hệ thống truy vấn KTV thuộc `center_id` có `proficiency >= 3`.
5. Hệ thống đếm số phiếu `DANG_XU_LY` và sắp xếp KTV tăng dần theo tải.
6. Hệ thống hiển thị danh sách KTV gợi ý kèm điểm tay nghề và số phiếu giữ.
7. Quản lý chọn 1 KTV từ danh sách gợi ý và nhấn "Xác nhận phân công".
8. Hệ thống tính SLA `due_date` theo quy tắc QT-04 dựa trên priority của phiếu.
9. Hệ thống cập nhật phiếu (`technician_id`, `status='DANG_XU_LY'`, `due_date`), ghi log `ticket_status_log` và hiển thị thông báo "Phân công thành công".

#### LUỒNG NGOẠI LỆ:
- **4a. Không có KTV nào đạt chuẩn tay nghề (proficiency >= 3)**:
  - 4a1. Hệ thống hiển thị cảnh báo: "Không tìm thấy KTV đạt trình độ tay nghề >= 3 trong trung tâm".
  - 4a2. Hệ thống gợi ý toàn bộ KTV trung tâm để Quản lý chọn thủ công hoặc chuyển trung tâm.
- **7a. KTV được chọn bị quá tải (> 10 phiếu)**:
  - 7a1. Hệ thống cảnh báo: "KTV này đang giữ 11 phiếu bảo hành. Bạn có chắc muốn phân công?".
  - 7a2. Quản lý chọn "Tiếp tục" $\rightarrow$ Quay lại bước 8.
- **9a. Lỗi kết nối CSDL khi lưu phân công**:
  - 9a1. Hệ thống Rollback giao dịch, giữ nguyên trạng thái phiếu là `MỚI`.

---

## MỤC 8. ĐẶC TẢ HỢP ĐỒNG API (TRACK SE - API CONTRACT)

### 8.1 Quy ước chung
- **Định dạng trao đổi**: JSON, UTF-8. Header bắt buộc: `Content-Type: application/json`, `Authorization: Bearer <token>`.
- **Đặt tên trường**: Dùng kiểu `snake_case` khớp với schema CSDL (`ticket_id`, `technician_id`, `due_date`...).
- **Định dạng thời gian**: ISO 8601 kèm timezone, ví dụ: `2026-10-01T14:30:00+07:00`.

### 8.2 Danh sách API Endpoints
- `GET /api/v1/tickets/unassigned`: Lấy danh sách phiếu chờ phân công kèm tải KTV (US1)
- `GET /api/v1/tickets/{id}/recommend-technicians`: Lấy danh sách KTV gợi ý phù hợp (US2)
- `POST /api/v1/tickets/{id}/assign`: Phân công phiếu bảo hành cho KTV (US2)
- `POST /api/v1/tickets/{id}/reassign`: Chuyển phiếu bảo hành sang KTV khác (US6)
- `POST /api/v1/appointments`: Đặt lịch hẹn giao – nhận máy (US3)
- `GET /api/v1/technicians/me/tickets`: KTV xem phiếu được gán xếp theo SLA (US4)
- `PATCH /api/v1/tickets/{id}/status`: KTV cập nhật trạng thái phiếu và ghi log (US5)
- `GET /api/v1/devices/{identifier}/history`: Tra cứu lịch sử sửa chữa thiết bị (US7)

---

## PHỤ LỤC. BẢNG KHAI BÁO SỬ DỤNG CÔNG CỤ AI

| STT | Công cụ AI | Phần áp dụng | Cách dùng (tóm tắt yêu cầu) | Nội dung em đã chỉnh sửa & kiểm chứng |
| :---: | :--- | :--- | :--- | :--- |
| 1 | Trợ lý AI (Google Antigravity) | Mục 1 - User Stories & AC | Gợi ý bộ 8 User Story cho luồng L4 phân công KTV và lịch hẹn | Rà soát và chỉnh sửa lại theo chuẩn INVEST, bổ sung 3 kịch bản ngoại lệ cụ thể và gán mức MoSCoW. |
| 2 | Trợ lý AI (Google Antigravity) | Mục 3.2 - Ba câu lập luận | Viết 3 câu lập luận lựa chọn kiến trúc 4 lớp và Repository Pattern gắn với NFR1, NFR2, NFR3 | Chuẩn hóa lại đúng khuôn mẫu: 'Vì NFR... đòi hỏi..., tôi chọn..., đánh đổi là...' và kiểm tra tính khả thi. |
| 3 | Trợ lý AI (Google Antigravity) | Mục 4 - ERD & SQL DDL | Gợi ý cấu trúc bảng SQL DDL chuẩn 3NF cho 6 bảng luồng L4 kèm FK, UNIQUE, INDEX | Kiểm tra chuẩn 3NF, thêm CHECK due_date >= received_at, proficiency 1-5, và tạo Composite Index (technician_id, due_date). |
| 4 | Trợ lý AI (Google Antigravity) | Mục 5 - Wireframe 3 Màn hình | Gợi ý bố cục layout text wireframe 3 màn hình cho Luồng L4 | Tự vẽ lại trên Draw.io, lập bảng đối chiếu 1-1 giữa từng trường hiển thị với cột trong CSDL và mã FR/US. |

> **Dòng cam kết bắt buộc:** Tôi xác nhận đã đọc, hiểu và chịu trách nhiệm về toàn bộ nội dung nộp.  
> **Họ tên - MSSV - Ngày:** Nguyễn Minh Phú | MSSV: 2374802013447 | Ngày nộp: 08/10/2026
