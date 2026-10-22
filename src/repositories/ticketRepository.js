const { db } = require('../config/database');

class TicketRepository {
    // 1. Lấy danh sách phiếu bảo hành kèm thông tin Khách hàng & KTV
    findAll(filters = {}) {
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
    }

    // 2. Tìm phiếu theo ID
    findById(id) {
        return db.prepare(`
            SELECT t.*, c.full_name AS customer_name, c.phone AS customer_phone,
                   sc.center_name, tech.full_name AS technician_name
            FROM tickets t
            JOIN customers c ON t.customer_id = c.customer_id
            JOIN service_centers sc ON t.center_id = sc.center_id
            LEFT JOIN technicians tech ON t.technician_id = tech.technician_id
            WHERE t.ticket_id = ?
        `).get(id);
    }

    // 3. Tạo phiếu bảo hành mới
    create(ticketData) {
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
    }

    // 4. Lấy danh sách KTV gợi ý theo tay nghề và tải công việc (US2, QT-07)
    findRecommendedTechnicians(centerId, issueCategory) {
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
    }

    // 5. Cập nhật phân công KTV cho phiếu bảo hành
    assignTechnician(ticketId, technicianId, status, dueDate) {
        const updateStmt = db.prepare(`
            UPDATE tickets 
            SET technician_id = ?, status = ?, due_date = ?
            WHERE ticket_id = ?
        `);
        updateStmt.run(technicianId, status, dueDate, ticketId);
        return this.findById(ticketId);
    }

    // 6. Ghi nhật ký trạng thái (ticket_status_log)
    createStatusLog(logData) {
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
    }

    // 7. Lấy lịch sử chuyển trạng thái
    getStatusLogs(ticketId) {
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
    }

    // 8. Lấy danh sách KTV và tải công việc theo Trung tâm (Màn hình M1)
    getTechniciansWorkload(centerId) {
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
    }

    // 9. Lấy danh sách lịch hẹn của phiếu (Màn hình M3)
    getAppointmentsByTicket(ticketId) {
        return db.prepare(`
            SELECT * FROM appointments
            WHERE ticket_id = ?
            ORDER BY appointment_date ASC
        `).all(ticketId);
    }

    // 10. Đếm số lịch hẹn trong cùng khung giờ 30 phút (QT-09)
    countAppointmentsInSlot(appointmentDate) {
        // Cho phép dung sai 15 phút quanh thời điểm hẹn để kiểm tra khung giờ 30 phút
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
    }

    // 11. Tạo lịch hẹn mới
    createAppointment(apptData) {
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
    }
}

module.exports = new TicketRepository();
