const ticketRepository = require('../repositories/ticketRepository');

// ============================================================================
// CÁC QUY TẮC NGHIỆP VỤ THUẦN TÚY (PURE BUSINESS RULES - DỄ DÀNG UNIT TEST)
// ============================================================================

/**
 * QT-04: Tính hạn cam kết hoàn thành (SLA due_date)
 * @param {string|Date} receivedAt - Thời điểm tiếp nhận
 * @param {string} priority - Mức độ ưu tiên ('CAO' | 'TRUNG_BINH' | 'THAP')
 * @returns {Date} Thời hạn SLA cam kết
 */
function calculateSlaDueDate(receivedAt, priority) {
    if (!receivedAt) {
        throw new Error('Thời điểm tiếp nhận (receivedAt) không được để trống');
    }
    const baseTime = new Date(receivedAt);
    if (isNaN(baseTime.getTime())) {
        throw new Error('Định dạng thời điểm tiếp nhận không hợp lệ');
    }

    let slaHours = 48; // Mặc định TRUNG_BINH
    if (priority === 'CAO') slaHours = 24;
    else if (priority === 'THAP') slaHours = 72;
    else if (priority !== 'TRUNG_BINH' && priority !== undefined) {
        throw new Error(`Mức độ ưu tiên không hợp lệ: ${priority}`);
    }

    return new Date(baseTime.getTime() + slaHours * 60 * 60 * 1000);
}

/**
 * QT-06 & QT-07: Kiểm tra tính hợp lệ của KTV khi phân công
 * @param {Object} technician - Thông tin KTV (center_id, status, proficiency)
 * @param {number} requiredCenterId - Trung tâm của phiếu bảo hành
 * @param {number} proficiency - Điểm tay nghề cho nhóm lỗi
 * @returns {{ valid: boolean, reason?: string }}
 */
function checkTechnicianEligibility(technician, requiredCenterId, proficiency) {
    if (!technician) {
        return { valid: false, reason: 'Kỹ thuật viên không tồn tại' };
    }
    if (technician.status !== 'HOAT_DONG') {
        return { valid: false, reason: 'Kỹ thuật viên hiện không ở trạng thái HOAT_DONG (nghỉ phép hoặc tạm ngưng)' };
    }
    if (technician.center_id !== requiredCenterId) {
        return { valid: false, reason: 'Kỹ thuật viên không thuộc cùng trung tâm tiếp nhận phiếu (vi phạm QT-06)' };
    }
    if (proficiency === undefined || proficiency === null || proficiency < 3) {
        return { valid: false, reason: 'Kỹ thuật viên chưa đạt yêu cầu tay nghề tối thiểu (proficiency >= 3 theo QT-07)' };
    }
    return { valid: true };
}

/**
 * QT-08: Kiểm tra tính hợp lệ của Lý do chuyển gán phiếu (Re-assign)
 * @param {string} reason - Chuỗi lý do người quản lý nhập
 * @returns {{ valid: boolean, reason?: string }}
 */
function validateReassignReason(reason) {
    if (!reason || typeof reason !== 'string') {
        return { valid: false, message: 'Lý do chuyển gán phiếu là bắt buộc' };
    }
    const cleanReason = reason.trim();
    if (cleanReason.length < 10) {
        return { valid: false, message: 'Lý do chuyển gán phiếu phải có tối thiểu 10 ký tự (vi phạm QT-08)' };
    }
    return { valid: true, cleanReason };
}

/**
 * QT-09: Kiểm tra tải khung giờ đặt lịch hẹn giao - nhận máy
 * @param {number} currentCountInSlot - Số lịch hẹn hiện có trong khung giờ 30 phút
 * @returns {{ allowed: boolean, message?: string }}
 */
function checkAppointmentSlotCapacity(currentCountInSlot) {
    if (currentCountInSlot >= 5) {
        return {
            allowed: false,
            message: `Khung giờ đã đầy (${currentCountInSlot}/5 lịch hẹn). Vui lòng chọn khung giờ khác theo QT-09`
        };
    }
    return { allowed: true, availableSlots: 5 - currentCountInSlot };
}

// ============================================================================
// SERVICE CLASS - TẦNG DỊCH VỤ ĐÓNG GÓI LOGIC VÀ KẾT NỐI REPOSITORY
// ============================================================================

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

    // 3. Tạo phiếu bảo hành mới (Áp dụng QT-04)
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

        const randomNum = Math.floor(1000 + Math.random() * 9000);
        const ticketCode = `BH-${Date.now().toString().slice(-6)}-${randomNum}`;

        const priority = data.priority || 'TRUNG_BINH';
        const dueDate = calculateSlaDueDate(new Date(), priority).toISOString();

        const newTicket = ticketRepository.create({
            ticket_code: ticketCode,
            customer_id: data.customer_id,
            center_id: data.center_id,
            issue_category: data.issue_category,
            issue_desc: data.issue_desc,
            priority: priority,
            due_date: dueDate
        });

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

    // 5. Phân công KTV cho phiếu (US2, QT-04, QT-06, QT-07)
    assignTechnician(ticketId, technicianId, userId, note) {
        const ticket = this.getTicketById(ticketId);
        const recommended = ticketRepository.findRecommendedTechnicians(ticket.center_id, ticket.issue_category);
        const matchedTech = recommended.find(t => t.technician_id === parseInt(technicianId, 10));

        if (!matchedTech) {
            const err = new Error('Kỹ thuật viên không thuộc cùng trung tâm hoặc chưa đạt trình độ tay nghề (proficiency >= 3 theo QT-07)');
            err.statusCode = 400;
            throw err;
        }

        const eligibility = checkTechnicianEligibility(matchedTech, ticket.center_id, matchedTech.proficiency);
        if (!eligibility.valid) {
            const err = new Error(eligibility.reason);
            err.statusCode = 400;
            throw err;
        }

        const newDueDate = calculateSlaDueDate(new Date(), ticket.priority).toISOString();

        const updatedTicket = ticketRepository.assignTechnician(
            ticketId,
            technicianId,
            'DANG_XU_LY',
            newDueDate
        );

        ticketRepository.createStatusLog({
            ticket_id: ticketId,
            from_status: ticket.status,
            to_status: 'DANG_XU_LY',
            from_technician_id: ticket.technician_id,
            to_technician_id: technicianId,
            reason: 'Phân công KTV theo gợi ý tay nghề & SLA',
            note: note || 'Phân công thành công',
            changed_by: userId || 1
        });

        return updatedTicket;
    }

    // 6. Chuyển gán phiếu (Re-assign) cho KTV khác (US6, QT-08)
    reassignTechnician(ticketId, newTechnicianId, userId, reason, note) {
        const validation = validateReassignReason(reason);
        if (!validation.valid) {
            const err = new Error(validation.message);
            err.statusCode = 400;
            throw err;
        }

        const ticket = this.getTicketById(ticketId);
        if (ticket.technician_id === parseInt(newTechnicianId, 10)) {
            const err = new Error('Kỹ thuật viên mới trùng với kỹ thuật viên hiện đang được gán');
            err.statusCode = 400;
            throw err;
        }

        const recommended = ticketRepository.findRecommendedTechnicians(ticket.center_id, ticket.issue_category);
        const matchedTech = recommended.find(t => t.technician_id === parseInt(newTechnicianId, 10));

        if (!matchedTech) {
            const err = new Error('Kỹ thuật viên mới không đủ điều kiện (phải cùng trung tâm và tay nghề >= 3)');
            err.statusCode = 400;
            throw err;
        }

        const newDueDate = calculateSlaDueDate(new Date(), ticket.priority).toISOString();

        const updatedTicket = ticketRepository.assignTechnician(
            ticketId,
            newTechnicianId,
            'DANG_XU_LY',
            newDueDate
        );

        ticketRepository.createStatusLog({
            ticket_id: ticketId,
            from_status: ticket.status,
            to_status: 'DANG_XU_LY',
            from_technician_id: ticket.technician_id,
            to_technician_id: newTechnicianId,
            reason: validation.cleanReason,
            note: note || 'Chuyển gán phiếu sang KTV khác',
            changed_by: userId || 1
        });

        return updatedTicket;
    }

    // 7. Lấy danh sách KTV và tải công việc (Màn hình M1)
    getTechniciansWorkload(centerId) {
        return ticketRepository.getTechniciansWorkload(centerId);
    }

    // 8. Lấy danh sách lịch hẹn của phiếu (Màn hình M3)
    getAppointments(ticketId) {
        this.getTicketById(ticketId); // Đảm bảo phiếu tồn tại
        return ticketRepository.getAppointmentsByTicket(ticketId);
    }

    // 9. Đặt lịch hẹn giao - nhận máy (US3, QT-09)
    createAppointment(ticketId, data) {
        this.getTicketById(ticketId);

        if (!data.appointment_type || !data.appointment_date) {
            const err = new Error('Thiếu thông tin loại lịch hẹn hoặc ngày giờ hẹn');
            err.statusCode = 400;
            throw err;
        }

        if (!['NHAN_MAY', 'GIAO_MAY'].includes(data.appointment_type)) {
            const err = new Error('Loại lịch hẹn chỉ được là NHAN_MAY hoặc GIAO_MAY');
            err.statusCode = 400;
            throw err;
        }

        const apptDate = new Date(data.appointment_date);
        if (isNaN(apptDate.getTime())) {
            const err = new Error('Định dạng thời gian hẹn không hợp lệ');
            err.statusCode = 400;
            throw err;
        }

        // Kiểm tra quy tắc QT-09: Khung giờ 30p tối đa 5 lịch hẹn
        const countInSlot = ticketRepository.countAppointmentsInSlot(apptDate.toISOString());
        const capacity = checkAppointmentSlotCapacity(countInSlot);
        if (!capacity.allowed) {
            const err = new Error(capacity.message);
            err.statusCode = 400;
            throw err;
        }

        const appt = ticketRepository.createAppointment({
            ticket_id: ticketId,
            appointment_type: data.appointment_type,
            appointment_date: apptDate.toISOString(),
            notes: data.notes
        });

        return appt;
    }

    // 10. Lấy lịch sử trạng thái của phiếu
    getStatusLogs(ticketId) {
        this.getTicketById(ticketId);
        return ticketRepository.getStatusLogs(ticketId);
    }
}

const serviceInstance = new TicketService();

module.exports = serviceInstance;
module.exports.calculateSlaDueDate = calculateSlaDueDate;
module.exports.checkTechnicianEligibility = checkTechnicianEligibility;
module.exports.validateReassignReason = validateReassignReason;
module.exports.checkAppointmentSlotCapacity = checkAppointmentSlotCapacity;
