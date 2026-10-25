/**
 * TẦNG NGHIỆP VỤ (SERVICE LAYER)
 * Học phần: Chuyên đề tốt nghiệp 1 - Smart CRM Mekong Mobile
 * Sinh viên: Nguyễn Minh Phú - MSSV: 2374802013447
 * Tuân thủ thiết kế Buổi 11 (Slide 24 - 26):
 *  - Độc lập hoàn toàn với giao thức HTTP (không chứa req, res, status codes)
 *  - Kiểm soát toàn bộ ràng buộc nghiệp vụ QT-04, QT-06, QT-07, QT-08, QT-09
 *  - Khi vi phạm nghiệp vụ: ném LoiNghiepVu kèm mã máy đọc (ma) và thông điệp
 *  - Áp dụng toTicketView() để bảo vệ hợp đồng dữ liệu (Data Contract - Slide 15-16)
 */

const ticketRepository = require('../repositories/ticketRepository');
const { LoiNghiepVu } = require('../errors');
const { toTicketView, maskPhoneNumber } = require('./ticket.contract');

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
        throw new LoiNghiepVu('THIEU_THOI_DIEM_TIEP_NHAN', 'Thời điểm tiếp nhận (receivedAt) không được để trống', 400);
    }
    const baseTime = new Date(receivedAt);
    if (isNaN(baseTime.getTime())) {
        throw new LoiNghiepVu('DINH_DANG_NGAY_SAI', 'Định dạng thời điểm tiếp nhận không hợp lệ', 400);
    }

    let slaHours = 48; // Mặc định TRUNG_BINH
    if (priority === 'CAO') slaHours = 24;
    else if (priority === 'THAP') slaHours = 72;
    else if (priority !== 'TRUNG_BINH' && priority !== undefined) {
        throw new LoiNghiepVu('MUC_UU_TIEN_KHONG_HOP_LE', `Mức độ ưu tiên không hợp lệ: ${priority}`, 400);
    }

    return new Date(baseTime.getTime() + slaHours * 60 * 60 * 1000);
}

/**
 * QT-06 & QT-07: Kiểm tra tính hợp lệ của KTV khi phân công
 * @param {Object} technician - Thông tin KTV (center_id, status, proficiency)
 * @param {number} requiredCenterId - Trung tâm của phiếu bảo hành
 * @param {number} proficiency - Điểm tay nghề cho nhóm lỗi
 * @returns {{ valid: boolean, reason?: string, code?: string }}
 */
function checkTechnicianEligibility(technician, requiredCenterId, proficiency) {
    if (!technician) {
        return { valid: false, reason: 'Kỹ thuật viên không tồn tại', code: 'KTV_KHONG_TON_TAI' };
    }
    if (technician.status !== 'HOAT_DONG') {
        return { valid: false, reason: 'Kỹ thuật viên hiện không ở trạng thái HOAT_DONG (nghỉ phép hoặc tạm ngưng)', code: 'KTV_KHONG_HOAT_DONG' };
    }
    if (technician.center_id !== requiredCenterId) {
        return { valid: false, reason: 'Kỹ thuật viên không thuộc cùng trung tâm tiếp nhận phiếu (vi phạm QT-06)', code: 'KTV_KHAC_TRUNG_TAM' };
    }
    if (proficiency === undefined || proficiency === null || proficiency < 3) {
        return { valid: false, reason: 'Kỹ thuật viên chưa đạt yêu cầu tay nghề tối thiểu (proficiency >= 3 theo QT-07)', code: 'KTV_TAY_NGHE_THAP' };
    }
    return { valid: true };
}

/**
 * QT-08: Kiểm tra tính hợp lệ của Lý do chuyển gán phiếu (Re-assign)
 * @param {string} reason - Chuỗi lý do người quản lý nhập
 * @returns {{ valid: boolean, message?: string, cleanReason?: string, code?: string }}
 */
function validateReassignReason(reason) {
    if (!reason || typeof reason !== 'string') {
        return { valid: false, message: 'Lý do chuyển gán phiếu là bắt buộc', code: 'THIEU_LY_DO_CHUYEN_GAN' };
    }
    const cleanReason = reason.trim();
    if (cleanReason.length < 10) {
        return { valid: false, message: 'Lý do chuyển gán phiếu phải có tối thiểu 10 ký tự (vi phạm QT-08)', code: 'LY_DO_QUA_NGAN' };
    }
    return { valid: true, cleanReason };
}

/**
 * QT-09: Kiểm tra tải khung giờ đặt lịch hẹn giao - nhận máy
 * @param {number} currentCountInSlot - Số lịch hẹn hiện có trong khung giờ 30 phút
 * @returns {{ allowed: boolean, message?: string, availableSlots?: number, code?: string }}
 */
function checkAppointmentSlotCapacity(currentCountInSlot) {
    if (currentCountInSlot >= 5) {
        return {
            allowed: false,
            message: `Khung giờ đã đầy (${currentCountInSlot}/5 lịch hẹn). Vui lòng chọn khung giờ khác theo QT-09`,
            code: 'LICH_HEN_QUA_TAI'
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
        const tickets = ticketRepository.findAll(filters);
        return tickets.map(toTicketView);
    }

    // 2. Tìm phiếu theo ID
    getTicketById(id) {
        const ticket = ticketRepository.findById(id);
        if (!ticket) {
            throw new LoiNghiepVu('PHIEU_KHONG_TON_TAI', `Không tìm thấy phiếu bảo hành ID=${id}`, 404);
        }
        return toTicketView(ticket);
    }

    // 3. Tạo phiếu bảo hành mới (Áp dụng QT-04)
    createTicket(data) {
        if (!data.customer_id || !data.center_id || !data.issue_category || !data.issue_desc) {
            throw new LoiNghiepVu('THIEU_TRUONG_BAT_BUOC', 'Thiếu trường dữ liệu bắt buộc (customer_id, center_id, issue_category, issue_desc)', 400);
        }

        if (typeof data.issue_desc !== 'string' || data.issue_desc.trim().length < 10) {
            throw new LoiNghiepVu('MO_TA_SU_CO_QUA_NGAN', 'Mô tả sự cố phải có tối thiểu 10 ký tự', 400);
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
            issue_desc: data.issue_desc.trim(),
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

        return toTicketView(newTicket);
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
            throw new LoiNghiepVu(
                'KTV_KHONG_DAT_CHUAN',
                'Kỹ thuật viên không thuộc cùng trung tâm hoặc chưa đạt trình độ tay nghề (proficiency >= 3 theo QT-07)',
                400
            );
        }

        const eligibility = checkTechnicianEligibility(matchedTech, ticket.center_id, matchedTech.proficiency);
        if (!eligibility.valid) {
            throw new LoiNghiepVu(eligibility.code || 'KTV_KHONG_DU_DIEU_KIEN', eligibility.reason, 400);
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

        return toTicketView(updatedTicket);
    }

    // 6. Chuyển gán phiếu (Re-assign) cho KTV khác (US6, QT-08)
    reassignTechnician(ticketId, newTechnicianId, userId, reason, note) {
        const validation = validateReassignReason(reason);
        if (!validation.valid) {
            throw new LoiNghiepVu(validation.code || 'LY_DO_KHONG_HOP_LE', validation.message, 400);
        }

        const ticket = this.getTicketById(ticketId);
        if (ticket.technician_id === parseInt(newTechnicianId, 10)) {
            throw new LoiNghiepVu('TRUNG_KTV_HIEN_TAI', 'Kỹ thuật viên mới trùng với kỹ thuật viên hiện đang được gán', 400);
        }

        const recommended = ticketRepository.findRecommendedTechnicians(ticket.center_id, ticket.issue_category);
        const matchedTech = recommended.find(t => t.technician_id === parseInt(newTechnicianId, 10));

        if (!matchedTech) {
            throw new LoiNghiepVu('KTV_MOI_KHONG_DU_DIEU_KIEN', 'Kỹ thuật viên mới không đủ điều kiện (phải cùng trung tâm và tay nghề >= 3)', 400);
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

        return toTicketView(updatedTicket);
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
            throw new LoiNghiepVu('THIEU_THONG_TIN_LICH_HEN', 'Thiếu thông tin loại lịch hẹn hoặc ngày giờ hẹn', 400);
        }

        if (!['NHAN_MAY', 'GIAO_MAY'].includes(data.appointment_type)) {
            throw new LoiNghiepVu('LOAI_LICH_HEN_KHONG_HOP_LE', 'Loại lịch hẹn chỉ được là NHAN_MAY hoặc GIAO_MAY', 400);
        }

        const apptDate = new Date(data.appointment_date);
        if (isNaN(apptDate.getTime())) {
            throw new LoiNghiepVu('NGAY_HEN_KHONG_HOP_LE', 'Định dạng thời gian hẹn không hợp lệ', 400);
        }

        // Kiểm tra quy tắc QT-09: Khung giờ 30p tối đa 5 lịch hẹn
        const countInSlot = ticketRepository.countAppointmentsInSlot(apptDate.toISOString());
        const capacity = checkAppointmentSlotCapacity(countInSlot);
        if (!capacity.allowed) {
            throw new LoiNghiepVu('LICH_HEN_QUA_TAI', capacity.message, 409);
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
module.exports.toTicketView = toTicketView;
module.exports.maskPhoneNumber = maskPhoneNumber;
