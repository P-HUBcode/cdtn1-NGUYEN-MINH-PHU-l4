-- =============================================================================
-- TRƯỜNG ĐẠI HỌC VĂN LANG - KHOA CÔNG NGHỆ THÔNG TIN
-- CHUYÊN ĐỀ TỐT NGHIỆP 1 (HK261)
-- BÀI TẬP 1: SQL DDL SKELETON (TRACK SE - CHUẨN 3NF)
-- LUỒNG L4: PHÂN CÔNG KỸ THUẬT VIÊN VÀ LỊCH HẸN
-- Sinh viên: Nguyễn Minh Phú - MSSV: 2374802013447
-- =============================================================================

-- 1. Bảng Trung tâm bảo hành (Service Centers)
CREATE TABLE service_centers (
    center_id SERIAL PRIMARY KEY,
    center_code VARCHAR(20) NOT NULL UNIQUE,
    center_name VARCHAR(100) NOT NULL,
    address TEXT NOT NULL,
    phone VARCHAR(15) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- 2. Bảng Kỹ thuật viên (Technicians)
CREATE TABLE technicians (
    technician_id SERIAL PRIMARY KEY,
    technician_code VARCHAR(20) NOT NULL UNIQUE,
    full_name VARCHAR(100) NOT NULL,
    phone VARCHAR(15) NOT NULL UNIQUE,
    center_id INT NOT NULL REFERENCES service_centers(center_id) ON DELETE RESTRICT,
    status VARCHAR(20) NOT NULL DEFAULT 'HOAT_DONG' CHECK (status IN ('HOAT_DONG', 'NGHI_PHEP', 'TAM_NGUNG')),
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- 3. Bảng Tay nghề / Kỹ năng KTV (Technician Skills)
CREATE TABLE technician_skills (
    technician_id INT NOT NULL REFERENCES technicians(technician_id) ON DELETE CASCADE,
    issue_category VARCHAR(50) NOT NULL CHECK (issue_category IN ('MAN_HINH', 'PIN', 'SAC', 'PHAN_MEM', 'NUOC_VAO', 'KHAC')),
    proficiency INT NOT NULL DEFAULT 3 CHECK (proficiency BETWEEN 1 AND 5),
    PRIMARY KEY (technician_id, issue_category)
);

-- 4. Bảng Phiếu bảo hành (Tickets)
CREATE TABLE tickets (
    ticket_id SERIAL PRIMARY KEY,
    ticket_code VARCHAR(30) NOT NULL UNIQUE,
    customer_id INT NOT NULL,
    center_id INT NOT NULL REFERENCES service_centers(center_id) ON DELETE RESTRICT,
    technician_id INT REFERENCES technicians(technician_id) ON DELETE SET NULL,
    issue_category VARCHAR(50) NOT NULL CHECK (issue_category IN ('MAN_HINH', 'PIN', 'SAC', 'PHAN_MEM', 'NUOC_VAO', 'KHAC')),
    issue_desc TEXT NOT NULL,
    priority VARCHAR(20) NOT NULL DEFAULT 'TRUNG_BINH' CHECK (priority IN ('CAO', 'TRUNG_BINH', 'THAP')),
    status VARCHAR(30) NOT NULL DEFAULT 'MOI' CHECK (status IN ('MOI', 'DANG_XU_LY', 'CHO_LINH_KIEN', 'HOAN_TAT', 'DA_GIAO', 'HUY')),
    received_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    due_date TIMESTAMPTZ NOT NULL,
    closed_at TIMESTAMPTZ,
    CONSTRAINT check_due_date CHECK (due_date >= received_at)
);

-- 5. Bảng Nhật ký đổi trạng thái & Phân công (Ticket Status Log)
CREATE TABLE ticket_status_log (
    log_id BIGSERIAL PRIMARY KEY,
    ticket_id INT NOT NULL REFERENCES tickets(ticket_id) ON DELETE CASCADE,
    from_status VARCHAR(30),
    to_status VARCHAR(30) NOT NULL,
    from_technician_id INT REFERENCES technicians(technician_id),
    to_technician_id INT REFERENCES technicians(technician_id),
    reason TEXT,
    note TEXT,
    changed_by INT NOT NULL,
    changed_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- 6. Bảng Lịch hẹn giao – nhận máy (Appointments)
CREATE TABLE appointments (
    appointment_id SERIAL PRIMARY KEY,
    ticket_id INT NOT NULL REFERENCES tickets(ticket_id) ON DELETE CASCADE,
    appointment_type VARCHAR(20) NOT NULL CHECK (appointment_type IN ('NHAN_MAY', 'GIAO_MAY')),
    appointment_date TIMESTAMPTZ NOT NULL,
    status VARCHAR(30) NOT NULL DEFAULT 'DA_XAC_NHAN' CHECK (status IN ('CHO_XAC_NHAN', 'DA_XAC_NHAN', 'DA_HOAN_THANH', 'DA_DOI_LICH', 'DA_HUY')),
    notes TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- =============================================================================
-- CREATING INDEXES FOR PERFORMANCE OPTIMIZATION (GẮN VỚI NFR1)
-- =============================================================================

-- Index tối ưu truy vấn danh sách phiếu theo KTV và sắp xếp hạn SLA due_date (US4, NFR1)
CREATE INDEX idx_tickets_technician_due ON tickets (technician_id, due_date ASC);

-- Index ghép cho bộ lọc danh sách phiếu theo trạng thái và trung tâm (US1, NFR1)
CREATE INDEX idx_tickets_center_status ON tickets (center_id, status);

-- Index tăng tốc gợi ý KTV theo chuyên môn và tay nghề (US2)
CREATE INDEX idx_tech_skills_cat_prof ON technician_skills (issue_category, proficiency DESC);

-- Index tra cứu lịch sử log theo phiếu bảo hành
CREATE INDEX idx_ticket_log_ticket_id ON ticket_status_log (ticket_id, changed_at DESC);

-- Index tra cứu lịch hẹn theo phiếu bảo hành và mốc thời gian
CREATE INDEX idx_appointments_ticket_date ON appointments (ticket_id, appointment_date);
