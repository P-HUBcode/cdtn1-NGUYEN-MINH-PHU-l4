const ticketRepository = require('../repositories/ticketRepository');

class TicketService {
    // 1. Lấy danh sách phiếu bảo hành
    getAllTickets(filters) {
        return ticketRepository.findAll(filters);
    }

    // 2. Tìm phiếu theo ID
    getTicketById(id) {
        const ticket = ticketRepository.findById(id);
        if (!ticket) {
            const err = new Error('Không tìm thấy phiếu bảo hành');
            err.statusCode = 404;
            throw err;
        }
        return ticket;
    }

    // 3. Tạo phiếu bảo hành mới (Tính SLA ban đầu theo QT-04)
    createTicket(data) {
        if (!data.customer_id || !data.center_id || !data.issue_category || !data.issue_desc) {
            const err = new Error('Thiếu trường dữ liệu bắt buộc (customer_id, center_id, issue_category, issue_desc)');
            err.statusCode = 400;
            throw err;
        }

        if (data.issue_desc.length < 10) {
            const err = new Error('Mô tả sự cố phải có tối thiểu 10 ký tự');
            err.statusCode = 400;
            throw err;
        }

        // Tự sinh mã phiếu bảo hành duy nhất
        const randomNum = Math.floor(1000 + Math.random() * 9000);
        const ticketCode = `BH-${Date.now().toString().slice(-6)}-${randomNum}`;

        // Tính SLA ban đầu theo QT-04
        const priority = data.priority || 'TRUNG_BINH';
        let slaHours = 48; // Mặc định TRUNG_BÌNH
        if (priority === 'CAO') slaHours = 24;
        if (priority === 'THAP') slaHours = 72;

        const dueDate = new Date(Date.now() + slaHours * 60 * 60 * 1000).toISOString();

        const newTicket = ticketRepository.create({
            ticket_code: ticketCode,
            customer_id: data.customer_id,
            center_id: data.center_id,
            issue_category: data.issue_category,
            issue_desc: data.issue_desc,
            priority: priority,
            due_date: dueDate
        });

        // Ghi log khởi tạo
        ticketRepository.createStatusLog({
            ticket_id: newTicket.ticket_id,
            from_status: null,
            to_status: 'MOI',
            reason: 'Tiếp nhận tạo mới phiếu',
            changed_by: data.user_id || 1
        });

        return newTicket;
    }

    // 4. Lấy danh sách KTV gợi ý (US2, QT-07)
    getRecommendedTechnicians(ticketId) {
        const ticket = this.getTicketById(ticketId);
        return ticketRepository.findRecommendedTechnicians(ticket.center_id, ticket.issue_category);
    }

    // 5. Phân công KTV cho phiếu bảo hành (US2, QT-04, QT-06, QT-07)
    assignTechnician(ticketId, technicianId, userId, note) {
        const ticket = this.getTicketById(ticketId);

        // Kiểm tra KTV có thuộc danh sách hợp lệ không
        const recommended = ticketRepository.findRecommendedTechnicians(ticket.center_id, ticket.issue_category);
        const matchedTech = recommended.find(t => t.technician_id === parseInt(technicianId, 10));

        if (!matchedTech) {
            const err = new Error('Kỹ thuật viên không thuộc cùng trung tâm hoặc chưa đạt trình độ tay nghề (proficiency >= 3)');
            err.statusCode = 400;
            throw err;
        }

        // Cập nhật SLA due_date tại thời điểm phân công (QT-04)
        let slaHours = 48;
        if (ticket.priority === 'CAO') slaHours = 24;
        if (ticket.priority === 'THAP') slaHours = 72;
        const newDueDate = new Date(Date.now() + slaHours * 60 * 60 * 1000).toISOString();

        const updatedTicket = ticketRepository.assignTechnician(
            ticketId,
            technicianId,
            'DANG_XU_LY',
            newDueDate
        );

        // Ghi log chuyển trạng thái
        ticketRepository.createStatusLog({
            ticket_id: ticketId,
            from_status: ticket.status,
            to_status: 'DANG_XU_LY',
            from_technician_id: ticket.technician_id,
            to_technician_id: technicianId,
            reason: 'Phân công KTV theo chuẩn tay nghề và SLA',
            note: note || 'Phân công thành công',
            changed_by: userId || 1
        });

        return updatedTicket;
    }
}

module.exports = new TicketService();
