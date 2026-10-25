# BÁO CÁO HỌC TẬP VÀ THỰC THI BUỔI 09
## GIAO TIẾP GIỮA CÁC THÀNH PHẦN VÀ TRÌNH BÀY KẾT QUẢ CHO NGƯỜI DÙNG

**Học phần:** Chuyên đề tốt nghiệp 1 (HK261) — Khoa Công nghệ Thông tin, Trường Đại học Văn Lang  
**Sinh viên thực hiện:** Nguyễn Minh Phú  
**Mã số sinh viên (MSSV):** 2374802013447 | **Lớp học phần:** `232_71ITBS40103_01`  
**Chuyên ngành (Track):** SE (Kỹ thuật phần mềm)  
**Luồng nghiệp vụ:** Luồng L4 — Phân công kỹ thuật viên và lịch hẹn bảo hành (Smart CRM Mekong Mobile)  
**GitHub Repository:** [https://github.com/P-HUBcode/cdtn1-NGUYEN-MINH-PHU-l4](https://github.com/P-HUBcode/cdtn1-NGUYEN-MINH-PHU-l4) (Tag `v0.2`)  
**Ngày hoàn thành:** 26/10/2026  

---

## PHẦN 1. TỔNG QUAN LÝ THUYẾT VÀ NGUYÊN TẮC KỸ THUẬT (BUỔI 09)

Mục tiêu cốt lõi của Buổi 09 là thiết lập **HỢP ĐỒNG DỮ LIỆU TƯỜNG MINH (Explicit Data Contract)** giữa các thành phần phần mềm và chuẩn hóa trải nghiệm **TRÌNH BÀY KẾT QUẢ (User Presentation)** cho người dùng cuối.

### 1.1. Khái niệm Cốt lõi: Hợp đồng dữ liệu ranh giới (Data Contract)
- Hai thành phần chỉ có thể ghép nối an toàn khi cả hai cùng thống nhất về hình dạng dữ liệu đi qua ranh giới giữa chúng.
- **Phụ thuộc ngầm (Implicit Dependency):** Xảy ra khi Lớp Trình bày (Frontend/Controller) tự ý đoán tên cột của CSDL (`customer.name`, `due_date`). Khi CSDL đổi tên cột hoặc cấu trúc bảng, hệ thống sẽ bị vỡ lúc chạy (Runtime Crash) mà không có cảnh báo trước.
- **Hợp đồng tường minh:** Được hiện thực qua hàm chuyển đổi dữ liệu ranh giới `toTicketView(rawTicket)` đặt tại [`src/services/ticket.contract.js`](file:///d:/CDTN%201/src/services/ticket.contract.js). Lớp Trình bày chỉ biết đến Hợp đồng, không bao giờ chạm trực tiếp vào cấu trúc bảng CSDL.

### 1.2. Ba yếu tố bắt buộc trên mọi hợp đồng dữ liệu
1. **Hình dạng (Shape):** Gồm những trường nào, kiểu dữ liệu gì (`string`, `number`, `ISO 8601`), trường nào bắt buộc, trường nào tùy chọn.
2. **Ý nghĩa (Semantics):** Giá trị mang đơn vị gì, `null` có nghĩa là gì (`null` đối với KTV = *"Chưa phân công"*, `null` đối với ngày mua = *"Chưa xác minh"*).
3. **Hành vi khi sai (Failure Mode):** Khi không có dữ liệu thì trả về mảng rỗng `[]`, không tìm thấy thì trả về mã 404, vi phạm nghiệp vụ thì trả về 400/409 kèm mã máy đọc.

### 1.3. Áp dụng quy tắc bảo mật dữ liệu cá nhân QT-15 (Phone Masking)
- Quy tắc **QT-15** quy định: Số điện thoại khách hàng phải được che giấu trên giao diện và trong log để bảo vệ thông tin cá nhân.
- Nơi duy nhất thi hành QT-15 là tại hàm `toTicketView()` ở ranh giới Service $\to$ Presentation:
  ```javascript
  function maskPhoneNumber(phone) {
      if (!phone || typeof phone !== 'string') return '(chưa có SĐT)';
      const clean = phone.trim();
      if (clean.length < 7) return clean;
      return clean.slice(0, 3) + '****' + clean.slice(-3); // VD: 090****567
  }
  ```

### 1.4. Bốn nguyên tắc trình bày kết quả cho người dùng cuối
1. **Trả lời câu hỏi người dùng, không phô dữ liệu:** Quản lý cần biết *"Phiếu nào cần phân công ngay"*, hệ thống đưa đúng danh sách phiếu chờ xếp theo hạn cam kết SLA, không đổ ra bảng 500 dòng không lọc.
2. **Con số phải có ngữ cảnh so sánh:** Điểm tay nghề kèm thang chuẩn `5/5`, tải công việc kèm trạng thái hoạt động `1 phiếu (HOAT_DONG)`.
3. **Nêu rõ giới hạn và độ tin cậy:** Gợi ý KTV kèm điểm tay nghề rõ ràng theo danh mục sự cố.
4. **Dẫn tới hành động tiếp theo (Actionable):** Có sẵn nút bấm thao tác trực tiếp: *"⚡ Gợi ý KTV"*, *"✅ Xác nhận phân công"*, *"🔄 Chuyển gán (Re-assign)"*, *"📅 Đặt lịch hẹn"*.

### 1.5. Ba trạng thái bắt buộc của giao diện người dùng
Thành phần [`src/public/js/components/DataState.js`](file:///d:/CDTN%201/src/public/js/components/DataState.js) quản lý trọn vẹn:
- **ĐANG TẢI (Loading):** Spinner động giữ bố cục, báo hiệu hệ thống đang xử lý.
- **RỖNG (Empty):** Biểu tượng hộp thư rỗng kèm thông điệp giải thích vì sao không có dữ liệu và gợi ý đổi bộ lọc.
- **LỖI (Error):** Banner thông báo màu đỏ có 3 phần: Chuyện gì xảy ra $\to$ Vì sao $\to$ Làm gì tiếp theo (kèm mã tra cứu `requestId` và nút *"🔄 Thử lại ngay - Retry"*).

---

## PHẦN 2. GIẢI QUYẾT BÀI TẬP MINI-CASE TẠI LỚP (SLIDE 32 BUỔI 09)

### Đề bài Mini-Case:
Phân tích màn hình *"Phiếu quá hạn"* do một nhóm phát triển bàn giao:
```text
PHIEU QUA HAN
id  | customer.name   | due_date            | tech
----+-----------------+---------------------+------
98  | Nguyen Van A    | 2026-07-02 00:00:00 | null
101 | Tran Thi B      | 2026-07-03 00:00:00 | 17
Tổng: 2      CSAT: 3.8612
(Khi tắt máy chủ: màn hình trắng)
(Khi không có phiếu quá hạn: bảng chỉ có dòng tiêu đề)
(Frontend đọc t.customer.name trực tiếp từ bảng customers; số điện thoại hiện đầy đủ khi rê chuột vào tên)
```

### Kết quả giải quyết 6 vấn đề của sinh viên Nguyễn Minh Phú:

| STT | Vấn đề phát hiện | Khái niệm vi phạm | Hậu quả thực tế | Giải pháp khắc phục đã triển khai trong mã nguồn Luồng L4 |
| :---: | :--- | :--- | :--- | :--- |
| **1** | Frontend đọc trực tiếp `t.customer.name` và `due_date` từ CSDL | **Phụ thuộc ngầm (Implicit Dependency)** | Đổi tên cột trong CSDL làm vỡ giao diện lúc chạy; thiếu fallback khi `customer.name` bị null dẫn đến `TypeError`. | Xây dựng tệp [`src/services/ticket.contract.js`](file:///d:/CDTN%201/src/services/ticket.contract.js) và hàm `toTicketView(t)`. Frontend chỉ nhận dữ liệu chuẩn hóa, tự động fallback `'(không rõ họ tên)'`. |
| **2** | Rê chuột vào tên khách hàng hiện đầy đủ số điện thoại | **Vi phạm bảo vệ dữ liệu cá nhân (QT-15)** | Lộ thông tin cá nhân khách hàng, vi phạm quy định bảo mật chuỗi chi nhánh Mekong Mobile. | Áp dụng hàm `maskPhoneNumber()` tại ranh giới hợp đồng, số điện thoại luôn được che thành `090****567`. |
| **3** | Khi tắt máy chủ màn hình bị trắng tinh | **Thiếu xử lý trạng thái LỖI (Error State)** | Người dùng tưởng trình duyệt bị đơ, không biết hệ thống mất kết nối mạng. | Xây dựng `DataState.renderError()` hiển thị thông báo lỗi thân thiện, kèm nút *"🔄 Thử lại ngay"* và mã tra cứu `requestId`. |
| **4** | Khi không có phiếu quá hạn: bảng chỉ có dòng tiêu đề trống | **Thiếu xử lý trạng thái RỖNG (Empty State)** | Người dùng hoang mang không phân biệt được *"không có dữ liệu"* hay *"lỗi tải dữ liệu"*. | Xây dựng `DataState.renderEmpty()` hiển thị thông điệp *"Không có phiếu nào phù hợp bộ lọc hiện tại"*. |
| **5** | Con số `CSAT: 3.8612` để 4 số lẻ và không có ngữ cảnh | **Vi phạm nguyên tắc trình bày con số có ngữ cảnh** | Người quản lý không biết 3.8612 là cao hay thấp, so với mục tiêu thế nào. | Làm tròn 1 chữ số (`3.9/5.0`), bổ sung mốc tham chiếu: *"CSAT 3.9 — Đạt mục tiêu SLA (>= 3.8)"*. |
| **6** | Cột `tech` hiển thị `null` hoặc mã số thô `17`, không có nút hành động | **Không dẫn tới hành động (Not Actionable)** | Quản lý thấy phiếu quá hạn nhưng không thể xử lý ngay tại chỗ; hiện mã ID thay vì tên người đọc được. | Chuyển đổi `tech: 17` $\to$ `technician_name: 'Trần Văn Bình'`, `null` $\to$ `'Chưa phân công'`; bổ sung nút *"⚡ Phân công lại ngay"* trên từng dòng. |

---

## PHẦN 3. BỘ KIỂM THỬ HỢP ĐỒNG RANH GIỚI (DATA CONTRACT TESTS)

Đã xây dựng tệp kiểm thử chuyên biệt [`tests/ticket.contract.test.js`](file:///d:/CDTN%201/tests/ticket.contract.test.js) theo đúng chuẩn Slide 28 của Buổi 09:

```bash
$ npm run test:contract
TAP version 13
# Subtest: DATA CONTRACT TESTS — KIỂM CHỨNG HỢP ĐỒNG DỮ LIỆU RANH GIỚI (BUỔI 9)
    ok 1 - 1. toTicketView phải trả về đúng và đầy đủ các trường của hợp đồng dữ liệu
    ok 2 - 2. due_date phải được chuẩn hóa thành chuỗi thời gian ISO 8601 kèm múi giờ (Z)
    ok 3 - 3. QT-15: Số điện thoại khách hàng luôn được che giấu tại ranh giới (không lộ đầy đủ)
    ok 4 - 4. maskPhoneNumber xử lý đúng các trường hợp đặc biệt (null, chuỗi ngắn, chuỗi chuẩn)
    ok 5 - 5. technician_name trả về "Chưa phân công" và technician_id là null khi phiếu mới
    ok 6 - 6. customer_name trả về "(không rõ họ tên)" khi dữ liệu trong CSDL bị null hoặc rỗng
1..6
# tests 6 | # pass 6 | # fail 0
```

Kết hợp với bộ Unit Tests nghiệp vụ, tổng cộng toàn hệ thống sở hữu **28 Tests PASS 100%**:
```bash
$ npm test
# tests 28 | # suites 7 | # pass 28 | # fail 0 | duration_ms 135ms
```

---

## PHẦN 4. TRẢ LỜI NĂM CÂU HỎI TỰ KIỂM TRA NHANH (SLIDE 33 BUỔI 09)

1. **Ba thứ mọi hợp đồng dữ liệu phải nêu rõ là gì?**  
   - *Trả lời:* (1) **Hình dạng (Shape):** Danh sách trường, kiểu dữ liệu, tính bắt buộc; (2) **Ý nghĩa (Semantics):** Đơn vị đo lường, ý nghĩa của các giá trị đặc biệt hoặc `null`; (3) **Hành vi khi sai (Failure Mode):** Trả về mã lỗi gì, định dạng phản hồi thế nào khi dữ liệu không hợp lệ.

2. **Đổi đơn vị của trường `thoiGianXuLy` từ giờ sang phút là thay đổi tương thích hay phá vỡ? Vì sao?**  
   - *Trả lời:* Đây là **thay đổi phá vỡ (Breaking Change)**. Mặc dù tên trường và kiểu dữ liệu (số nguyên) không đổi, nhưng **ý nghĩa dữ liệu (Semantics)** đã thay đổi hoàn toàn. Bên nhận dữ liệu vẫn hiểu là giờ và sẽ tính toán sai gấp 60 lần mà không hề phát sinh lỗi cú pháp (lỗi âm thầm nguy hiểm). Cách sửa đúng là thêm trường mới `thoiGianXuLyPhut` song song, chuyển đổi dần rồi mới thu hẹp trường cũ.

3. **Một API trả về mã 500 khi người dùng nhập mô tả lỗi quá ngắn. Sai ở đâu và nên trả về gì?**  
   - *Trả lời:* Sai ở việc **nhầm lẫn giữa lỗi người dùng (Client Error) và lỗi hệ thống (Server Error)**. Việc nhập mô tả ngắn là hành vi người dùng vi phạm quy tắc kiểm tra hợp lệ đầu vào (Validation), không phải sự cố sập server. API phải trả về mã **`400 Bad Request`** (hoặc `422 Unprocessable Entity`) kèm cấu trúc JSON chuẩn:
     ```json
     {
       "error": "MO_TA_SU_CO_QUA_NGAN",
       "message": "Mô tả sự cố phải có tối thiểu 10 ký tự",
       "fields": { "issue_desc": "Tối thiểu 10 ký tự" }
     }
     ```

4. **Kể tên ba trạng thái mọi màn hình và mọi báo cáo phải xử lý; trạng thái nào hay bị quên nhất?**  
   - *Trả lời:* Ba trạng thái là: **ĐANG TẢI (Loading)**, **RỖNG (Empty)**, và **LỖI (Error)**. Trạng thái hay bị bỏ quên nhất là **RỖNG (Empty State)** — sinh viên thường chỉ kiểm thử với dữ liệu có sẵn, khi bộ lọc không khớp dòng nào thì màn hình hiện bảng trắng trơn khiến người dùng tưởng hệ thống bị lỗi.

5. **Vì sao nên ghép các module tăng dần thay vì ghép một lần rồi mới chạy (Big-Bang Integration)?**  
   - *Trả lời:* Vì khi ghép toàn bộ cùng một lúc, nếu xảy ra lỗi, lập trình viên sẽ đối mặt với không gian lỗi khổng lồ ở mọi mối nối ranh giới và không thể biết nguyên nhân đến từ đâu. Tích hợp tăng dần (mỗi lần thêm đúng 1 mối nối, phần chưa có thì dùng stub) giúp: nếu có lỗi thì thủ phạm **chắc chắn nằm ở mối nối vừa ghép**, từ đó khoanh vùng và sửa lỗi ngay lập tức.

---

## PHẦN 5. KẾT LUẬN VÀ LIÊN KẾT GIAI ĐOẠN 2

Toàn bộ các tiêu chuẩn kỹ thuật của **Buổi 09** đã được sinh viên tích hợp hoàn chỉnh vào mã nguồn dự án:
- Hợp đồng dữ liệu ranh giới: [`src/services/ticket.contract.js`](file:///d:/CDTN%201/src/services/ticket.contract.js)
- Bảo mật khử độc số điện thoại QT-15: `maskPhoneNumber()`
- Xử lý 3 trạng thái giao diện: [`src/public/js/components/DataState.js`](file:///d:/CDTN%201/src/public/js/components/DataState.js)
- Bộ kiểm thử hợp đồng tự động: [`tests/ticket.contract.test.js`](file:///d:/CDTN%201/tests/ticket.contract.test.js) (6 tests PASS)
- Báo cáo kết thúc Giai đoạn 2 Bài tập 2: [`docs/BT2_2374802013447_NguyenMinhPhu.pdf`](file:///d:/CDTN%201/docs/BT2_2374802013447_NguyenMinhPhu.pdf)

**Cam kết xác nhận:**  
Sinh viên: **Nguyễn Minh Phú** — MSSV: **2374802013447** — Ngày hoàn thành: **26/10/2026**.
