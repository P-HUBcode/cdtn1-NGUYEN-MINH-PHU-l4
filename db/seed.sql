-- =============================================================================
-- DỮ LIỆU MẪU BAN ĐẦU (SEED DATA SPRINT 1) - LUỒNG L4
-- =============================================================================

-- 1. Trung tâm bảo hành (Service Centers)
INSERT INTO service_centers (center_id, center_code, center_name, address, phone) VALUES
(1, 'TT-CT01', 'Trung tâm Bảo hành Cần Thơ', '123 Đường 30/4, Ninh Kiều, Cần Thơ', '02923888999'),
(2, 'TT-AG01', 'Trung tâm Bảo hành An Giang', '45 Trần Hưng Đạo, Long Xuyên, An Giang', '02963777888'),
(3, 'TT-TG01', 'Trung tâm Bảo hành Tiền Giang', '78 Ấp Bắc, Mỹ Tho, Tiền Giang', '02733666555')
ON CONFLICT (center_id) DO NOTHING;

-- 2. Khách hàng (Customers)
INSERT INTO customers (customer_id, customer_code, full_name, phone, address) VALUES
(1, 'KH-001', 'Nguyễn Văn An', '0901234567', 'Ninh Kiều, Cần Thơ'),
(2, 'KH-002', 'Trần Thị Bình', '0912345678', 'Cái Răng, Cần Thơ'),
(3, 'KH-003', 'Lê Hoàng Cúc', '0987654321', 'Long Xuyên, An Giang'),
(4, 'KH-004', 'Phạm Minh Đức', '0933445566', 'Châu Đốc, An Giang'),
(5, 'KH-005', 'Võ Thị Hoa', '0944556677', 'Mỹ Tho, Tiền Giang')
ON CONFLICT (customer_id) DO NOTHING;

-- 3. Kỹ thuật viên (Technicians)
INSERT INTO technicians (technician_id, technician_code, full_name, phone, center_id, status) VALUES
(1, 'KTV-001', 'Trần Văn Bình', '0909001001', 1, 'HOAT_DONG'),
(2, 'KTV-002', 'Lê Văn Cường', '0909001002', 1, 'HOAT_DONG'),
(3, 'KTV-003', 'Nguyễn Thị Dung', '0909001003', 1, 'NGHI_PHEP'),
(4, 'KTV-004', 'Hoàng Minh Em', '0909002001', 2, 'HOAT_DONG'),
(5, 'KTV-005', 'Đặng Quốc Hùng', '0909002002', 2, 'HOAT_DONG')
ON CONFLICT (technician_id) DO NOTHING;

-- 4. Kỹ năng KTV (Technician Skills)
INSERT INTO technician_skills (technician_id, issue_category, proficiency) VALUES
(1, 'MAN_HINH', 5),
(1, 'PIN', 4),
(1, 'SAC', 4),
(2, 'MAN_HINH', 3),
(2, 'PHAN_MEM', 5),
(2, 'PIN', 3),
(3, 'MAN_HINH', 4),
(4, 'MAN_HINH', 4),
(4, 'NUOC_VAO', 4),
(5, 'PIN', 5),
(5, 'SAC', 4)
ON CONFLICT (technician_id, issue_category) DO NOTHING;

-- 5. Phiếu bảo hành (Tickets)
INSERT INTO tickets (ticket_id, ticket_code, customer_id, center_id, technician_id, issue_category, issue_desc, priority, status, received_at, due_date) VALUES
(1, 'BH-202610-001', 1, 1, NULL, 'MAN_HINH', 'Màn hình sọc xanh, nhấp nháy liên tục khi sử dụng', 'CAO', 'MOI', '2026-10-15 08:30:00+07', '2026-10-16 08:30:00+07'),
(2, 'BH-202610-002', 2, 1, NULL, 'PIN', 'Pin chai tụt nhanh còn 20% sau 1 giờ', 'TRUNG_BINH', 'MOI', '2026-10-15 09:15:00+07', '2026-10-17 09:15:00+07'),
(3, 'BH-202610-003', 3, 2, 4, 'NUOC_VAO', 'Rơi vào nước, không lên nguồn', 'CAO', 'DANG_XU_LY', '2026-10-14 14:00:00+07', '2026-10-15 14:00:00+07')
ON CONFLICT (ticket_id) DO NOTHING;

-- 6. Lịch sử trạng thái (Status Log)
INSERT INTO ticket_status_log (ticket_id, from_status, to_status, from_technician_id, to_technician_id, reason, note, changed_by, changed_at) VALUES
(3, 'MOI', 'DANG_XU_LY', NULL, 4, 'Phân công theo gợi ý tay nghề', 'Phân công cho KTV Hoàng Minh Em', 1, '2026-10-14 14:30:00+07');

-- 7. Lịch hẹn (Appointments)
INSERT INTO appointments (appointment_id, ticket_id, appointment_type, appointment_date, status, notes) VALUES
(1, 1, 'NHAN_MAY', '2026-10-16 09:30:00+07', 'DA_XAC_NHAN', 'Khách hẹn mang máy đến trung tâm kiểm tra trực tiếp');
