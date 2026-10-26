/**
 * TẦNG TRUY CẬP DỮ LIỆU (REPOSITORY LAYER)
 * Học phần: Chuyên đề tốt nghiệp 1 - Smart CRM Mekong Mobile
 * Sinh viên: Nguyễn Minh Phú - MSSV: 2374802013447
 * Tuân thủ thiết kế Buổi 11 (Slide 24):
 *  - Phụ trách toàn bộ truy vấn SQL (SQLite3)
 *  - DỊCH lỗi kỹ thuật CSDL thành LoiTruyCapDuLieu
 *  - Tuyệt đối KHÔNG chứa mã trạng thái HTTP, KHÔNG ghi log tại đây
 */

const { db } = require('../config/database');
const { LoiTruyCapDuLieu } = require('../errors');

class TicketRepository {
    // 1. Lấy danh sách phiếu bảo hành kèm thông tin Khách hàng & KTV
    findAll(filters = {}) {
        try {
            let query = `
                SELECT t.ticket_id, t.ticket_code, t.issue_category, t.issue_desc, t.priority, t.status, 
                       t.received_at, t.due_date,
                       c.full_name AS customer_name, c.phone AS customer_phone,
                       sc.center_id, sc.center_name,
                       tech.technician_id, tech.full_name AS technician_name
                FROM tickets t
                JOIN customers c ON t.customer_id = c.customer_id
                JOIN service_centers sc ON t.center_id = sc.center_id
                LEFT JOIN technicians tech ON t.technician_id = tech.technician_id
                WHERE 1=1
            `;
            const params = [];
            if (filters.status) {
                query += ` AND t.status = ?`;
                params.push(filters.status);
            }
            if (filters.center_id) {
                query += ` AND t.center_id = ?`;
                params.push(filters.center_id);
            }
            query += ` ORDER BY t.due_date ASC`;

            return db.prepare(query).all(...params);
        } catch (err) {
            throw new LoiTruyCapDuLieu('Lỗi khi truy vấn danh sách phiếu bảo hành', err);
        }
    }

    // 2. Tìm phiếu theo ID
    findById(id) {
        try {
            return db.prepare(`
                SELECT t.*, c.full_name AS customer_name, c.phone AS customer_phone,
                       sc.center_name, tech.full_name AS technician_name
                FROM tickets t
                JOIN customers c ON t.customer_id = c.customer_id
                JOIN service_centers sc ON t.center_id = sc.center_id
                LEFT JOIN technicians tech ON t.technician_id = tech.technician_id
                WHERE t.ticket_id = ?
            `).get(id);
        } catch (err) {
            throw new LoiTruyCapDuLieu(`Lỗi khi tìm phiếu bảo hành ID=${id}`, err);
        }
    }

    // 2b. Tìm hoặc tạo khách hàng mới
    findOrCreateCustomer(customerData) {
        try {
            const cleanPhone = (customerData.phone || '').trim();
            let customer = db.prepare(`SELECT * FROM customers WHERE phone = ?`).get(cleanPhone);
            if (!customer) {
                const code = `KH-${Date.now().toString().slice(-4)}-${Math.floor(100 + Math.random() * 900)}`;
                const result = db.prepare(`
                    INSERT INTO customers (customer_code, full_name, phone, address)
                    VALUES (?, ?, ?, ?)
                `).run(
                    code,
                    (customerData.full_name || 'Khách hàng mới').trim(),
                    cleanPhone,
                    (customerData.address || 'Tại quầy tiếp nhận').trim()
                );
                customer = db.prepare(`SELECT * FROM customers WHERE customer_id = ?`).get(result.lastInsertRowid);
            }
            return customer;
        } catch (err) {
            throw new LoiTruyCapDuLieu('Lỗi khi lưu thông tin khách hàng vào CSDL', err);
        }
    }

    // 3. Tạo phiếu bảo hành mới
    create(ticketData) {
        try {
            const stmt = db.prepare(`
                INSERT INTO tickets (ticket_code, customer_id, center_id, issue_category, issue_desc, priority, status, due_date)
                VALUES (?, ?, ?, ?, ?, ?, 'MOI', ?)
            `);
            const result = stmt.run(
                ticketData.ticket_code,
                ticketData.customer_id,
                ticketData.center_id,
                ticketData.issue_category,
                ticketData.issue_desc,
                ticketData.priority || 'TRUNG_BINH',
                ticketData.due_date
            );
            return this.findById(result.lastInsertRowid);
        } catch (err) {
            throw new LoiTruyCapDuLieu('Lỗi khi ghi phiếu bảo hành mới vào CSDL', err);
        }
    }

    // 4. Lấy danh sách KTV gợi ý theo tay nghề và tải công việc (US2, QT-07)
    findRecommendedTechnicians(centerId, issueCategory) {
        try {
            return db.prepare(`
                SELECT tech.technician_id, tech.technician_code, tech.full_name, tech.phone, tech.center_id, tech.status,
                       ts.proficiency,
                       (SELECT COUNT(*) FROM tickets WHERE technician_id = tech.technician_id AND status = 'DANG_XU_LY') AS active_tickets
                FROM technicians tech
                JOIN technician_skills ts ON tech.technician_id = ts.technician_id
                WHERE tech.center_id = ? 
                  AND tech.status = 'HOAT_DONG'
                  AND ts.issue_category = ?
                  AND ts.proficiency >= 3
                ORDER BY active_tickets ASC, ts.proficiency DESC
            `).all(centerId, issueCategory);
        } catch (err) {
            throw new LoiTruyCapDuLieu('Lỗi khi truy vấn danh sách kỹ thuật viên gợi ý', err);
        }
    }

    // 5. Cập nhật phân công KTV cho phiếu bảo hành
    assignTechnician(ticketId, technicianId, status, dueDate) {
        try {
            const updateStmt = db.prepare(`
                UPDATE tickets 
                SET technician_id = ?, status = ?, due_date = ?
                WHERE ticket_id = ?
            `);
            updateStmt.run(technicianId, status, dueDate, ticketId);
            return this.findById(ticketId);
        } catch (err) {
            throw new LoiTruyCapDuLieu(`Lỗi khi cập nhật phân công KTV cho phiếu ID=${ticketId}`, err);
        }
    }

    // 6. Ghi nhật ký trạng thái (ticket_status_log)
    createStatusLog(logData) {
        try {
            const stmt = db.prepare(`
                INSERT INTO ticket_status_log (ticket_id, from_status, to_status, from_technician_id, to_technician_id, reason, note, changed_by)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            `);
            stmt.run(
                logData.ticket_id,
                logData.from_status,
                logData.to_status,
                logData.from_technician_id || null,
                logData.to_technician_id || null,
                logData.reason || null,
                logData.note || null,
                logData.changed_by
            );
        } catch (err) {
            throw new LoiTruyCapDuLieu('Lỗi khi ghi nhật ký trạng thái phiếu (Audit Log)', err);
        }
    }

    // 7. Lấy lịch sử chuyển trạng thái
    getStatusLogs(ticketId) {
        try {
            return db.prepare(`
                SELECT log.*,
                       t1.full_name AS from_technician_name,
                       t2.full_name AS to_technician_name
                FROM ticket_status_log log
                LEFT JOIN technicians t1 ON log.from_technician_id = t1.technician_id
                LEFT JOIN technicians t2 ON log.to_technician_id = t2.technician_id
                WHERE log.ticket_id = ?
                ORDER BY log.changed_at DESC
            `).all(ticketId);
        } catch (err) {
            throw new LoiTruyCapDuLieu(`Lỗi khi lấy nhật ký trạng thái phiếu ID=${ticketId}`, err);
        }
    }

    // 8. Lấy danh sách KTV và tải công việc theo Trung tâm (Màn hình M1)
    getTechniciansWorkload(centerId) {
        try {
            let query = `
                SELECT tech.technician_id, tech.technician_code, tech.full_name, tech.phone, tech.status,
                       sc.center_name,
                       (SELECT COUNT(*) FROM tickets WHERE technician_id = tech.technician_id AND status = 'DANG_XU_LY') AS active_tickets,
                       GROUP_CONCAT(ts.issue_category || ': ' || ts.proficiency || '/5', ', ') AS skills
                FROM technicians tech
                JOIN service_centers sc ON tech.center_id = sc.center_id
                LEFT JOIN technician_skills ts ON tech.technician_id = ts.technician_id
            `;
            const params = [];
            if (centerId) {
                query += ` WHERE tech.center_id = ?`;
                params.push(centerId);
            }
            query += ` GROUP BY tech.technician_id ORDER BY active_tickets ASC, tech.full_name ASC`;
            return db.prepare(query).all(...params);
        } catch (err) {
            throw new LoiTruyCapDuLieu('Lỗi khi truy vấn tải công việc của kỹ thuật viên', err);
        }
    }

    // 9. Lấy danh sách lịch hẹn của phiếu (Màn hình M3)
    getAppointmentsByTicket(ticketId) {
        try {
            return db.prepare(`
                SELECT * FROM appointments
                WHERE ticket_id = ?
                ORDER BY appointment_date ASC
            `).all(ticketId);
        } catch (err) {
            throw new LoiTruyCapDuLieu(`Lỗi khi lấy danh sách lịch hẹn của phiếu ID=${ticketId}`, err);
        }
    }

    // 10. Đếm số lịch hẹn trong cùng khung giờ 30 phút (QT-09)
    countAppointmentsInSlot(appointmentDate) {
        try {
            const target = new Date(appointmentDate).getTime();
            const start = new Date(target - 15 * 60 * 1000).toISOString();
            const end = new Date(target + 15 * 60 * 1000).toISOString();

            const row = db.prepare(`
                SELECT COUNT(*) AS count
                FROM appointments
                WHERE appointment_date BETWEEN ? AND ?
                  AND status != 'DA_HUY'
            `).get(start, end);

            return row ? row.count : 0;
        } catch (err) {
            throw new LoiTruyCapDuLieu('Lỗi khi kiểm tra tải khung giờ lịch hẹn', err);
        }
    }

    // 11. Tạo lịch hẹn mới
    createAppointment(apptData) {
        try {
            const stmt = db.prepare(`
                INSERT INTO appointments (ticket_id, appointment_type, appointment_date, status, notes)
                VALUES (?, ?, ?, 'DA_XAC_NHAN', ?)
            `);
            const result = stmt.run(
                apptData.ticket_id,
                apptData.appointment_type,
                apptData.appointment_date,
                apptData.notes || null
            );
            return db.prepare(`SELECT * FROM appointments WHERE appointment_id = ?`).get(result.lastInsertRowid);
        } catch (err) {
            throw new LoiTruyCapDuLieu('Lỗi khi lưu lịch hẹn vào CSDL', err);
        }
    }
}

module.exports = new TicketRepository();
