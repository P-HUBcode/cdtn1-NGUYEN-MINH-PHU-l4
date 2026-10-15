const { DatabaseSync } = require('node:sqlite');
const path = require('node:path');
const fs = require('node:fs');

const dbPath = path.resolve(__dirname, '../../db/warranty.sqlite');
const dbDir = path.dirname(dbPath);

if (!fs.existsSync(dbDir)) {
    fs.mkdirSync(dbDir, { recursive: true });
}

const db = new DatabaseSync(dbPath);

// Enable foreign keys
db.exec('PRAGMA foreign_keys = ON;');

function initDatabase() {
    // 1. Tạo bảng theo DDL chuẩn 3NF
    db.exec(`
        CREATE TABLE IF NOT EXISTS customers (
            customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_code TEXT NOT NULL UNIQUE,
            full_name TEXT NOT NULL,
            phone TEXT NOT NULL UNIQUE,
            address TEXT,
            created_at TEXT NOT NULL DEFAULT (datetime('now'))
        );

        CREATE TABLE IF NOT EXISTS service_centers (
            center_id INTEGER PRIMARY KEY AUTOINCREMENT,
            center_code TEXT NOT NULL UNIQUE,
            center_name TEXT NOT NULL,
            address TEXT NOT NULL,
            phone TEXT NOT NULL,
            created_at TEXT NOT NULL DEFAULT (datetime('now'))
        );

        CREATE TABLE IF NOT EXISTS technicians (
            technician_id INTEGER PRIMARY KEY AUTOINCREMENT,
            technician_code TEXT NOT NULL UNIQUE,
            full_name TEXT NOT NULL,
            phone TEXT NOT NULL UNIQUE,
            center_id INTEGER NOT NULL REFERENCES service_centers(center_id) ON DELETE RESTRICT,
            status TEXT NOT NULL DEFAULT 'HOAT_DONG' CHECK (status IN ('HOAT_DONG', 'NGHI_PHEP', 'TAM_NGUNG')),
            created_at TEXT NOT NULL DEFAULT (datetime('now'))
        );

        CREATE TABLE IF NOT EXISTS technician_skills (
            technician_id INTEGER NOT NULL REFERENCES technicians(technician_id) ON DELETE CASCADE,
            issue_category TEXT NOT NULL CHECK (issue_category IN ('MAN_HINH', 'PIN', 'SAC', 'PHAN_MEM', 'NUOC_VAO', 'KHAC')),
            proficiency INTEGER NOT NULL DEFAULT 3 CHECK (proficiency BETWEEN 1 AND 5),
            PRIMARY KEY (technician_id, issue_category)
        );

        CREATE TABLE IF NOT EXISTS tickets (
            ticket_id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticket_code TEXT NOT NULL UNIQUE,
            customer_id INTEGER NOT NULL REFERENCES customers(customer_id) ON DELETE RESTRICT,
            center_id INTEGER NOT NULL REFERENCES service_centers(center_id) ON DELETE RESTRICT,
            technician_id INTEGER REFERENCES technicians(technician_id) ON DELETE SET NULL,
            issue_category TEXT NOT NULL CHECK (issue_category IN ('MAN_HINH', 'PIN', 'SAC', 'PHAN_MEM', 'NUOC_VAO', 'KHAC')),
            issue_desc TEXT NOT NULL,
            priority TEXT NOT NULL DEFAULT 'TRUNG_BINH' CHECK (priority IN ('CAO', 'TRUNG_BINH', 'THAP')),
            status TEXT NOT NULL DEFAULT 'MOI' CHECK (status IN ('MOI', 'DANG_XU_LY', 'CHO_LINH_KIEN', 'HOAN_TAT', 'DA_GIAO', 'HUY')),
            received_at TEXT NOT NULL DEFAULT (datetime('now')),
            due_date TEXT NOT NULL,
            closed_at TEXT
        );

        CREATE TABLE IF NOT EXISTS ticket_status_log (
            log_id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticket_id INTEGER NOT NULL REFERENCES tickets(ticket_id) ON DELETE CASCADE,
            from_status TEXT,
            to_status TEXT NOT NULL,
            from_technician_id INTEGER REFERENCES technicians(technician_id),
            to_technician_id INTEGER REFERENCES technicians(technician_id),
            reason TEXT,
            note TEXT,
            changed_by INTEGER NOT NULL,
            changed_at TEXT NOT NULL DEFAULT (datetime('now'))
        );

        CREATE TABLE IF NOT EXISTS appointments (
            appointment_id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticket_id INTEGER NOT NULL REFERENCES tickets(ticket_id) ON DELETE CASCADE,
            appointment_type TEXT NOT NULL CHECK (appointment_type IN ('NHAN_MAY', 'GIAO_MAY')),
            appointment_date TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'DA_XAC_NHAN' CHECK (status IN ('CHO_XAC_NHAN', 'DA_XAC_NHAN', 'DA_HOAN_THANH', 'DA_DOI_LICH', 'DA_HUY')),
            notes TEXT,
            created_at TEXT NOT NULL DEFAULT (datetime('now'))
        );

        -- Indexes NFR1
        CREATE INDEX IF NOT EXISTS idx_tickets_technician_due ON tickets (technician_id, due_date ASC);
        CREATE INDEX IF NOT EXISTS idx_tickets_center_status ON tickets (center_id, status);
        CREATE INDEX IF NOT EXISTS idx_tickets_customer ON tickets (customer_id);
    `);

    // 2. Nạp dữ liệu Seed ban đầu nếu bảng rỗng
    const countCenters = db.prepare('SELECT COUNT(*) as count FROM service_centers').get();
    if (countCenters.count === 0) {
        db.exec(`
            INSERT INTO service_centers (center_id, center_code, center_name, address, phone) VALUES
            (1, 'TT-CT01', 'Trung tâm Bảo hành Cần Thơ', '123 Đường 30/4, Ninh Kiều, Cần Thơ', '02923888999'),
            (2, 'TT-AG01', 'Trung tâm Bảo hành An Giang', '45 Trần Hưng Đạo, Long Xuyên, An Giang', '02963777888');

            INSERT INTO customers (customer_id, customer_code, full_name, phone, address) VALUES
            (1, 'KH-001', 'Nguyễn Văn An', '0901234567', 'Ninh Kiều, Cần Thơ'),
            (2, 'KH-002', 'Trần Thị Bình', '0912345678', 'Cái Răng, Cần Thơ'),
            (3, 'KH-003', 'Lê Hoàng Cúc', '0987654321', 'Long Xuyên, An Giang');

            INSERT INTO technicians (technician_id, technician_code, full_name, phone, center_id, status) VALUES
            (1, 'KTV-001', 'Trần Văn Bình', '0909001001', 1, 'HOAT_DONG'),
            (2, 'KTV-002', 'Lê Văn Cường', '0909001002', 1, 'HOAT_DONG'),
            (3, 'KTV-003', 'Nguyễn Thị Dung', '0909001003', 1, 'NGHI_PHEP');

            INSERT INTO technician_skills (technician_id, issue_category, proficiency) VALUES
            (1, 'MAN_HINH', 5),
            (1, 'PIN', 4),
            (2, 'MAN_HINH', 3),
            (2, 'PHAN_MEM', 5);

            INSERT INTO tickets (ticket_id, ticket_code, customer_id, center_id, technician_id, issue_category, issue_desc, priority, status, received_at, due_date) VALUES
            (1, 'BH-202610-001', 1, 1, NULL, 'MAN_HINH', 'Màn hình sọc xanh, nhấp nháy liên tục khi sử dụng', 'CAO', 'MOI', datetime('now'), datetime('now', '+1 day')),
            (2, 'BH-202610-002', 2, 1, NULL, 'PIN', 'Pin chai tụt nhanh còn 20% sau 1 giờ', 'TRUNG_BINH', 'MOI', datetime('now'), datetime('now', '+2 day')),
            (3, 'BH-202610-003', 3, 1, 1, 'MAN_HINH', 'Vỡ kính góc dưới bên phải', 'THAP', 'DANG_XU_LY', datetime('now'), datetime('now', '+3 day'));
        `);
    }
}

module.exports = { db, initDatabase };
