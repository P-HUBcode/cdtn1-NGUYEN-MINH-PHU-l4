# HỢP ĐỒNG API (API CONTRACT - TRACK SE)

**Họ tên:** Nguyễn Minh Phú | **MSSV:** 2374802013447 | **Track:** SE | **Luồng:** L4 - Phân công KTV & Lịch hẹn

---

## 1. QUY ƯỚC CHUNG
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

## 2. DANH SÁCH ENDPOINTS
- `GET /api/v1/tickets/unassigned`: Lấy danh sách phiếu chờ phân công kèm tải KTV (US1)
- `GET /api/v1/tickets/{id}/recommend-technicians`: Lấy danh sách KTV gợi ý phù hợp (US2)
- `POST /api/v1/tickets/{id}/assign`: Phân công phiếu bảo hành cho KTV (US2)
- `POST /api/v1/tickets/{id}/reassign`: Chuyển phiếu bảo hành sang KTV khác (US6)
- `POST /api/v1/appointments`: Đặt lịch hẹn giao – nhận máy (US3)
- `GET /api/v1/technicians/me/tickets`: KTV xem phiếu được gán xếp theo SLA (US4)
- `PATCH /api/v1/tickets/{id}/status`: KTV cập nhật trạng thái phiếu và ghi log (US5)
- `GET /api/v1/devices/{identifier}/history`: Tra cứu lịch sử sửa chữa thiết bị (US7)
