# BẢN ĐẶC TẢ YÊU CẦU PHẦN MỀM (SRS RÚT GỌN) & CÁC SẢN PHẨM BUỔI 04

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
- Không tự động mua sắm hoặc đặt hàng linh kiện tự động từ nhà cung cấp bên ngoài.
- Không tích hợp thanh toán trực tuyến chi phí ngoài bảo hành trong phiên bản này.
- Không tự động điều phối KTV di chuyển sửa chữa tại nhà khách hàng (chỉ quản lý tại trung tâm).

### 1.4 Bảng thuật ngữ nghiệp vụ
| Thuật ngữ | Khái niệm / Giải thích |
| :--- | :--- |
| **Phiếu bảo hành (Ticket)** | Yêu cầu bảo hành/sửa chữa thiết bị do khách hàng gửi, có mã định danh duy nhất. |
| **Kỹ thuật viên (KTV)** | Nhân viên kỹ thuật thực hiện chẩn đoán và sửa chữa thiết bị tại trung tâm. |
| **Hạn cam kết (SLA / Due Date)** | Thời hạn tối đa hệ thống/trung tâm cam kết hoàn thành sửa chữa cho khách hàng. |
| **Tay nghề (Proficiency)** | Mức độ thành thạo của KTV với nhóm kỹ năng/thiết bị cụ thể (thang điểm 1–5). |
| **Lịch hẹn (Appointment)** | Khung thời gian hẹn trước giữa khách hàng và trung tâm để giao máy hoặc nhận lại máy. |
| **Nhật ký trạng thái (Status Log)** | Bản ghi lịch sử ghi nhận mỗi lần phiếu bảo hành thay đổi trạng thái, KTV hoặc lịch hẹn. |

---

## MỤC 2. CÁC BÊN LIÊN QUAN VÀ VAI TRÒ NGƯỜI DÙNG

| Vai trò (Actor) | Mô tả vai trò | Quyền hạn & Trách nhiệm chính |
| :--- | :--- | :--- |
| **Quản lý trung tâm bảo hành** | Người điều hành công việc tại 1 trung tâm bảo hành cụ thể. | - Xem danh sách phiếu chờ phân công & tải công việc KTV.<br>- Phân công và chuyển gán phiếu cho KTV.<br>- Đặt và quản lý lịch hẹn giao – nhận máy.<br>- Theo dõi báo cáo tiến độ & SLA. |
| **Kỹ thuật viên (KTV)** | Nhân viên trực tiếp thao tác sửa chữa thiết bị. | - Xem danh sách phiếu được gán ưu tiên theo SLA.<br>- Cập nhật tiến độ trạng thái xử lý phiếu.<br>- Tra cứu lịch sử sửa chữa thiết bị theo IMEI/Serial. |
| **Hệ thống cảnh báo SLA (Timer)** | Actor hệ thống tự động chạy theo lịch. | - Tự động tính hạn SLA khi phân công.<br>- Phát cảnh báo phiếu sắp quá hạn hoặc đã quá hạn. |

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

### 3.2 Danh sách 8 User Story đạt chuẩn INVEST & Phân mức MoSCoW

#### US1. Xem danh sách chờ phân công & tải công việc KTV (MUST)
- **Phát biểu**: Là Quản lý trung tâm bảo hành, tôi muốn xem danh sách phiếu chờ phân công kèm khối lượng công việc (số phiếu đang giữ) của các KTV trong trung tâm để nắm tổng quan tình hình và đưa ra quyết định phân công hợp lý.
- **Mức MoSCoW**: **MUST**
- **Tiêu chí chấp nhận (Given-When-Then)**:
  - **AC1 (Happy path)**: `GIVEN` Quản lý đã đăng nhập hệ thống và truy cập màn hình phân công, `WHEN` chọn trung tâm quản lý, `THEN` hệ thống hiển thị danh sách phiếu chờ phân công và danh sách KTV thuộc trung tâm cùng số phiếu `Đang xử lý` hiện tại của từng người.
  - **AC2 (Exception - Không có phiếu)**: `GIVEN` Trung tâm không có phiếu nào đang ở trạng thái `MỚI` hoặc `TỰ ĐỘNG_TẠO`, `WHEN` Quản lý mở danh sách chờ, `THEN` hệ thống hiển thị thông báo "Không có phiếu bảo hành nào đang chờ phân công".

#### US2. Gợi ý & Phân công KTV phù hợp (MUST)
- **Phát biểu**: Là Quản lý trung tâm bảo hành, tôi muốn hệ thống tự động gợi ý KTV phù hợp dựa trên tay nghề (proficiency $\ge$ 3), cùng trung tâm và có ít phiếu nhất để phân công đúng người đúng việc và tránh KTV bị quá tải (giải quyết V3).
- **Mức MoSCoW**: **MUST**
- **Tiêu chí chấp nhận (Given-When-Then)**:
  - **AC1 (Happy path)**: `GIVEN` Phiếu bảo hành thuộc nhóm sự cố "MAN_HINH", `WHEN` Quản lý nhấn "Gợi ý KTV", `THEN` hệ thống trả về danh sách KTV cùng trung tâm có điểm kỹ năng "MAN_HINH" $\ge$ 3, xếp thứ tự ưu tiên từ số phiếu đang xử lý ít nhất đến nhiều nhất.
  - **AC2 (Happy path - Xác nhận gán)**: `GIVEN` Danh sách KTV gợi ý, `WHEN` Quản lý chọn KTV và bấm "Xác nhận phân công", `THEN` hệ thống cập nhật `technician_id`, chuyển trạng thái phiếu sang `ĐANG_XỬ_LÝ`, tính `due_date` theo SLA và lưu log.
  - **AC3 (Exception - Không tìm thấy KTV đủ điều kiện)**: `GIVEN` Không có KTV nào thuộc trung tâm có proficiency $\ge$ 3 cho nhóm sự cố của phiếu, `WHEN` bấm "Gợi ý KTV", `THEN` hệ thống hiển thị cảnh báo "Không có KTV phù hợp đạt chuẩn tay nghề, đề nghị chọn KTV hỗ trợ hoặc chuyển trung tâm".

#### US3. Đặt lịch hẹn giao – nhận máy (MUST)
- **Phát biểu**: Là Quản lý trung tâm bảo hành, tôi muốn đặt và quản lý lịch hẹn giao – nhận máy với khách hàng để sắp xếp khung giờ làm việc tối ưu và nâng cao trải nghiệm khách hàng.
- **Mức MoSCoW**: **MUST**
- **Tiêu chí chấp nhận (Given-When-Then)**:
  - **AC1 (Happy path)**: `GIVEN` Phiếu bảo hành hợp lệ, `WHEN` Quản lý chọn ngày hẹn, khung giờ hẹn (ví dụ: 09:00 - 09:30) và loại hẹn (`NHẬN_MÁY` / `GIAO_MÁY`), `THEN` hệ thống lưu bản ghi lịch hẹn mới vào `appointments` và liên kết với phiếu.
  - **AC2 (Exception - Trùng khung giờ hoặc quá hạn)**: `GIVEN` Khung giờ được chọn đã đủ tối đa 5 lịch hẹn của trung tâm hoặc chọn ngày trong quá khứ, `WHEN` nhấn "Lưu lịch hẹn", `THEN` hệ thống từ chối và thông báo lỗi "Khung giờ hẹn đã kín hoặc thời gian không hợp lệ".

#### US4. Xem danh sách công việc gán cho KTV sắp xếp theo SLA (MUST)
- **Phát biểu**: Là Kỹ thuật viên, tôi muốn xem danh sách các phiếu bảo hành được gán cho tôi sắp xếp ưu tiên theo Hạn cam kết (due_date / SLA) để biết chính xác công việc cần làm và ưu tiên xử lý các phiếu sắp quá hạn trước (giải quyết V2).
- **Mức MoSCoW**: **MUST**
- **Tiêu chí chấp nhận (Given-When-Then)**:
  - **AC1 (Happy path)**: `GIVEN` KTV đã đăng nhập vào hệ thống, `WHEN` mở trang "Phiếu của tôi", `THEN` hệ thống hiển thị tất cả phiếu bảo hành đang gán cho KTV đó, sắp xếp mặc định theo `due_date` tăng dần (phiếu sắp hết hạn/quá hạn nằm ở trên cùng với nhãn cảnh báo đỏ/vàng).
  - **AC2 (Exception - KTV chưa được gán phiếu nào)**: `GIVEN` KTV không giữ phiếu nào ở trạng thái `ĐANG_XỬ_LÝ` hoặc `CHỜ_LINH_KIỆN`, `WHEN` xem danh sách, `THEN` hệ thống hiển thị "Hiện tại bạn không có phiếu bảo hành nào cần xử lý".

#### US5. Cập nhật trạng thái xử lý phiếu & Lưu lịch sử log (MUST)
- **Phát biểu**: Là Kỹ thuật viên, tôi muốn cập nhật chuyển trạng thái xử lý phiếu (Đang xử lý $\rightarrow$ Chờ linh kiện $\rightarrow$ Hoàn tất) kèm ghi chú lý do để minh bạch tiến độ sửa chữa và tự động lưu nhật ký lịch sử (`ticket_status_log`).
- **Mức MoSCoW**: **MUST**
- **Tiêu chí chấp nhận (Given-When-Then)**:
  - **AC1 (Happy path)**: `GIVEN` Phiếu đang ở trạng thái `ĐANG_XỬ_LÝ`, `WHEN` KTV đổi trạng thái sang `CHỜ_LINH_KIỆN` và nhập ghi chú "Chờ màn hình thay thế từ kho tổng", `THEN` hệ thống lưu trạng thái mới, tạo 1 bản ghi vào `ticket_status_log` kèm mốc thời gian và `actor_id`.
  - **AC2 (Exception - Chuyển trạng thái không hợp lệ)**: `GIVEN` Phiếu đang ở trạng thái `MỚI` (chưa phân công), `WHEN` KTV cố gắng bấm chuyên sang `HOÀN_TẤT`, `THEN` hệ thống chặn thao tác và thông báo "Phiếu chưa được phân công KTV, không thể hoàn tất".

#### US6. Chuyển gán phiếu bảo hành sang KTV khác (SHOULD)
- **Phát biểu**: Là Quản lý trung tâm bảo hành, tôi muốn thực hiện chuyển phiếu bảo hành sang kỹ thuật viên khác kèm bắt buộc nhập lý do để đảm bảo phiếu vẫn được xử lý đúng hạn SLA khi KTV cũ vắng mặt hoặc gặp sự cố.
- **Mức MoSCoW**: **SHOULD**
- **Tiêu chí chấp nhận (Given-When-Then)**:
  - **AC1 (Happy path)**: `GIVEN` Phiếu đang gán cho KTV A bị ốm, `WHEN` Quản lý chọn phiếu, chọn KTV B và nhập lý do "KTV A nghỉ phép đột xuất", `THEN` hệ thống đổi `technician_id` sang KTV B và lưu ghi chú chuyển gán vào `ticket_status_log`.
  - **AC2 (Exception - Thiếu lý do chuyển)**: `GIVEN` Quản lý chọn KTV B nhưng để trống ô lý do chuyển, `WHEN` nhấn "Chuyển KTV", `THEN` hệ thống báo lỗi "Bắt buộc nhập lý do chuyển kỹ thuật viên (tối thiểu 10 ký tự)".

#### US7. Tra cứu lịch sử sửa chữa thiết bị theo IMEI / Serial (SHOULD)
- **Phát biểu**: Là Kỹ thuật viên / Quản lý, tôi muốn tra cứu lịch sử các lần sửa chữa trước đó của thiết bị (theo IMEI / Serial) để phát hiện lỗi hệ thống/lô hàng lặp lại và có phương án xử lý phù hợp mà không phải hỏi lại thông tin từ khách.
- **Mức MoSCoW**: **SHOULD**
- **Tiêu chí chấp nhận (Given-When-Then)**:
  - **AC1 (Happy path)**: `GIVEN` IMEI / Serial hợp lệ của thiết bị, `WHEN` người dùng nhập vào thanh tìm kiếm, `THEN` hệ thống hiển thị toàn bộ danh sách phiếu bảo hành quá khứ, các linh kiện đã thay và lịch sử sửa chữa của thiết bị đó.

#### US8. Cập nhật và dời lịch hẹn giao – nhận máy (SHOULD)
- **Phát biểu**: Là Quản lý trung tâm bảo hành, tôi muốn cập nhật hoặc hủy/dời lịch hẹn giao - nhận máy khi có yêu cầu từ khách hàng hoặc linh kiện bị trễ để chủ động tiến độ phục vụ.
- **Mức MoSCoW**: **SHOULD**
- **Tiêu chí chấp nhận (Given-When-Then)**:
  - **AC1 (Happy path)**: `GIVEN` Lịch hẹn đã tồn tại ở trạng thái `ĐÃ_XÁC_NHẬN`, `WHEN` Quản lý đổi mốc thời gian mới và cập nhật ghi chú, `THEN` hệ thống lưu thông tin lịch hẹn cập nhật và đổi trạng thái lịch hẹn thành `ĐÃ_DỜI_LỊCH`.

---

## MỤC 4. YÊU CẦU PHI CHỨC NĂNG (NFR) CÓ NGƯỠNG ĐO ĐƯỢC

- **NFR1 (Performance - Hiệu năng)**: Màn hình danh sách phiếu chờ phân công và khối lượng KTV phải load và hiển thị hoàn tất trong thời gian **được dưới 1.5 giây** với cơ sở dữ liệu thử nghiệm chứa **10.000 phiếu bảo hành** và **50 KTV** trên máy chủ RAM 8 GB.
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
| :--- | :--- | :---: | :---: | :---: | :--- |
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
- **Điều kiện trước (Pre-conditions)**:
  - Quản lý đã đăng nhập vào hệ thống với quyền `SERVICE_CENTER_MANAGER`.
  - Phiếu bảo hành đang ở trạng thái `MỚI` hoặc `TỰ ĐỘNG_TẠO` và thuộc trung tâm quản lý.
- **Điều kiện sau (Post-conditions)**:
  - Phiếu bảo hành được cập nhật `technician_id` và đổi trạng thái sang `ĐANG_XỬ_LÝ`.
  - Hạn cam kết SLA (`due_date`) được ghi nhận.
  - Bản ghi nhật ký mới được tạo trong `ticket_status_log`.
- **Liên quan**: US1, US2 | **Mức MoSCoW**: MUST

#### LUỒNG CHÍNH (Happy Path):
1. Quản lý mở danh sách phiếu bảo hành chờ phân công và chọn 1 phiếu cụ thể.
2. Quản lý nhấn nút "Gợi ý KTV phù hợp".
3. Hệ thống xác định nhóm sự cố (`category_id` / `issue_category`) và `center_id` của phiếu.
4. Hệ thống truy vấn danh sách KTV thuộc cùng `center_id` có điểm tay nghề `proficiency >= 3` cho nhóm sự cố đó.
5. Hệ thống tính số phiếu `ĐANG_XỬ_LÝ` của từng KTV hợp lệ và sắp xếp danh sách gợi ý tăng dần theo số phiếu đang giữ.
6. Hệ thống hiển thị danh sách KTV gợi ý kèm điểm tay nghề và số phiếu đang giữ.
7. Quản lý chọn 1 KTV từ danh sách gợi ý và nhấn "Xác nhận phân công".
8. Hệ thống tính mốc SLA `due_date` theo quy tắc QT-04 dựa trên priority của phiếu.
9. Hệ thống cập nhật phiếu (`technician_id`, `status='ĐANG_XỬ_LÝ'`, `due_date`), ghilog `ticket_status_log` và hiển thị thông báo "Phân công thành công".

#### LUỒNG NGOẠI LỆ:
- **4a. Không có KTV nào đạt chuẩn tay nghề (proficiency >= 3)**:
  - 4a1. Hệ thống hiển thị cảnh báo: "Không tìm thấy KTV đạt trình độ tay nghề >= 3 trong trung tâm".
  - 4a2. Hệ thống gợi ý danh sách toàn bộ KTV thuộc trung tâm (kèm điểm tay nghề thực tế) để Quản lý cân nhắc phân công thủ công hoặc chuyển phiếu sang trung tâm khác.
- **7a. KTV được chọn bị quá tải vượt ngưỡng quy định (> 10 phiếu)**:
  - 7a1. Hệ thống hiển thị hộp thoại cảnh báo: "KTV này đang giữ 11 phiếu bảo hành. Bạn có chắc chắn muốn phân công thêm?".
  - 7a2. Quản lý chọn "Tiếp tục" $\rightarrow$ Quay lại bước 8.
  - 7a3. Quản lý chọn "Hủy" $\rightarrow$ Quay lại bước 6 để chọn KTV khác.
- **9a. Lỗi kết nối CSDL trong quá trình lưu phân công**:
  - 9a1. Hệ thống Rollback giao dịch, giữ nguyên trạng thái phiếu là `MỚI`.
  - 9a2. Hệ thống hiển thị thông báo lỗi: "Không thể lưu thông tin phân công. Vui lòng thử lại".

---

## MỤC 8. ĐẶC TẢ HỢP ĐỒNG API (TRACK SE - API CONTRACT)

### 8.1 Quy ước chung
- **Định dạng trao đổi**: JSON, UTF-8. Header bắt buộc: `Content-Type: application/json`, `Authorization: Bearer <token>`.
- **Đặt tên trường**: Dùng kiểu `snake_case` khớp với schema CSDL (`ticket_id`, `technician_id`, `due_date`...).
- **Định dạng thời gian**: ISO 8601 kèm timezone, ví dụ: `2026-10-01T14:30:00+07:00`.
- **Cấu trúc Response lỗi chuẩn**:
```json
{
  "error": {
    "code": "VALIDATION_FAILED | NOT_FOUND | CONFLICT | FORBIDDEN",
    "message": "Thông báo lỗi chi tiết dành cho người dùng",
    "fields": {
      "field_name": "Mô tả lỗi cụ thể của trường"
    }
  }
}
```

### 8.2 Danh sách API Endpoints

| Phương thức | Đường dẫn (Path) | Mục đích | User Story |
| :--- | :--- | :--- | :---: |
| `GET` | `/api/v1/tickets/unassigned` | Lấy danh sách phiếu chờ phân công kèm tải công việc KTV | US1 |
| `GET` | `/api/v1/tickets/{id}/recommend-technicians` | Lấy danh sách KTV gợi ý phù hợp dựa trên tay nghề & tải | US2 |
| `POST` | `/api/v1/tickets/{id}/assign` | Phân công phiếu bảo hành cho KTV | US2 |
| `POST` | `/api/v1/tickets/{id}/reassign` | Chuyển phiếu bảo hành sang KTV khác (bắt buộc lý do) | US6 |
| `POST` | `/api/v1/appointments` | Đặt lịch hẹn giao – nhận máy cho phiếu bảo hành | US3 |
| `GET` | `/api/v1/technicians/me/tickets` | KTV xem danh sách phiếu được gán sắp xếp theo SLA | US4 |
| `PATCH` | `/api/v1/tickets/{id}/status` | KTV cập nhật trạng thái phiếu kèm lý do/ghi chú | US5 |
| `GET` | `/api/v1/devices/{identifier}/history` | Tra cứu lịch sử sửa chữa thiết bị theo IMEI/Serial | US7 |

---

### 8.3 Chi tiết các API Endpoints MUST

#### 1. API: `POST /api/v1/tickets/{id}/assign` (Phân công phiếu cho KTV - US2)
- **Description**: Phân công phiếu bảo hành cho KTV thuộc trung tâm, tính SLA due_date và đổi trạng thái phiếu.

##### Request Body mẫu:
```json
{
  "technician_id": 14,
  "note": "Phân công theo gợi ý hệ thống cho KTV có tay nghề cao"
}
```

##### Response 200 OK (Thành công):
```json
{
  "success": true,
  "data": {
    "ticket_id": 7821,
    "ticket_code": "BH-20261001-7821",
    "status": "DANG_XU_LY",
    "center_id": 2,
    "technician_id": 14,
    "technician_name": "Trần Văn Bình",
    "assigned_at": "2026-10-01T16:30:00+07:00",
    "due_date": "2026-10-03T16:30:00+07:00",
    "sla_hours": 48
  }
}
```

##### Response 400 Bad Request (Lỗi validation dữ liệu):
```json
{
  "error": {
    "code": "VALIDATION_FAILED",
    "message": "Dữ liệu phân công không hợp lệ",
    "fields": {
      "technician_id": "Mã kỹ thuật viên là trường bắt buộc và phải là số nguyên dương"
    }
  }
}
```

##### Response 409 Conflict (KTV khác trung tâm / Trạng thái không hợp lệ):
```json
{
  "error": {
    "code": "CENTER_MISMATCH",
    "message": "Kỹ thuật viên được chọn thuộc Trung tâm bảo hành 3, không cùng Trung tâm 2 của phiếu bảo hành",
    "fields": {}
  }
}
```

---

#### 2. API: `POST /api/v1/appointments` (Tạo lịch hẹn giao - nhận máy - US3)
- **Description**: Đặt lịch hẹn giao hoặc nhận máy với khách hàng.

##### Request Body mẫu:
```json
{
  "ticket_id": 7821,
  "appointment_type": "GIAO_MAY",
  "appointment_date": "2026-10-04T09:30:00+07:00",
  "notes": "Hẹn khách hàng mang máy đến trung tâm kiểm tra trực tiếp"
}
```

##### Response 201 Created (Tạo thành công):
```json
{
  "success": true,
  "data": {
    "appointment_id": 1205,
    "ticket_id": 7821,
    "appointment_type": "GIAO_MAY",
    "appointment_date": "2026-10-04T09:30:00+07:00",
    "status": "DA_XAC_NHAN",
    "created_at": "2026-10-01T16:35:00+07:00"
  }
}
```

##### Response 400 Bad Request (Khung giờ trong quá khứ hoặc quá tải):
```json
{
  "error": {
    "code": "INVALID_APPOINTMENT_TIME",
    "message": "Thời gian lịch hẹn không được chọn trong quá khứ hoặc khung giờ đã vượt quá 5 lịch hẹn",
    "fields": {
      "appointment_date": "Khung giờ 09:30:00 ngày 2026-10-04 đã đầy"
    }
  }
}
```

---

#### 3. API: `PATCH /api/v1/tickets/{id}/status` (Cập nhật trạng thái phiếu - US5)
- **Description**: KTV cập nhật tiến độ chuyển trạng thái xử lý phiếu và ghi log.

##### Request Body mẫu:
```json
{
  "status": "CHO_LINH_KIEN",
  "reason_code": "SPARE_PART_WAITING",
  "note": "Cần thay thế cụm màn hình OLED chính hãng, đã tạo phiếu yêu cầu linh kiện #LK-992"
}
```

##### Response 200 OK (Thành công):
```json
{
  "success": true,
  "data": {
    "ticket_id": 7821,
    "previous_status": "DANG_XU_LY",
    "current_status": "CHO_LINH_KIEN",
    "updated_at": "2026-10-01T16:40:00+07:00",
    "updated_by": 14,
    "log_id": 38115
  }
}
```

##### Response 400 Bad Request (Chuyển trạng thái sai quy trình):
```json
{
  "error": {
    "code": "INVALID_STATUS_TRANSITION",
    "message": "Không thể chuyển trực tiếp từ MOI sang HOAN_TAT",
    "fields": {
      "status": "Trạng thái tiếp theo phải là DANG_XU_LY"
    }
  }
}
```

---

### 8.4 Bảng quy tắc Validation dữ liệu cho các API Track SE

| Đường dẫn Endpoint | Tên trường (Field) | Bắt buộc | Kiểu dữ liệu / Ràng buộc | Thông báo lỗi khi vi phạm |
| :--- | :--- | :---: | :--- | :--- |
| `POST /tickets/{id}/assign` | `technician_id` | **Có** | Integer > 0, tồn tại trong `technicians` | "Kỹ thuật viên không tồn tại trong hệ thống" |
| `POST /tickets/{id}/assign` | `note` | Không | String, tối đa 500 ký tự | "Ghi chú không được vượt quá 500 ký tự" |
| `POST /tickets/{id}/reassign` | `new_technician_id` | **Có** | Integer > 0, khác `current_technician_id` | "Kỹ thuật viên mới phải khác kỹ thuật viên hiện tại" |
| `POST /tickets/{id}/reassign` | `reason` | **Có** | String, độ dài từ 10 - 500 ký tự | "Bắt buộc nhập lý do chuyển phiếu (tối thiểu 10 ký tự)" |
| `POST /appointments` | `ticket_id` | **Có** | Integer > 0, tồn tại trong `tickets_history` | "Mã phiếu bảo hành không tồn tại" |
| `POST /appointments` | `appointment_type` | **Có** | Enum: `NHAN_MAY`, `GIAO_MAY` | "Loại lịch hẹn chỉ nhận giá trị NHAN_MAY hoặc GIAO_MAY" |
| `POST /appointments` | `appointment_date` | **Có** | ISO 8601 String, $\ge$ `current_timestamp` | "Thời gian hẹn phải là thời điểm trong tương lai" |
| `PATCH /tickets/{id}/status` | `status` | **Có** | Enum: `DANG_XU_LY`, `CHO_LINH_KIEN`, `HOAN_TAT`, `DA_GIAO` | "Trạng thái phiếu không hợp lệ" |
| `PATCH /tickets/{id}/status` | `note` | **Có** | String, độ dài từ 5 - 1000 ký tự | "Vui lòng nhập ghi chú nội dung xử lý (tối thiểu 5 ký tự)" |

---

