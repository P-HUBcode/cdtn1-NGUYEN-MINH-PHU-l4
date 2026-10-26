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

/**
 * QT-10 / US5: Kiểm tra tính hợp lệ của thao tác chuyển trạng thái xử lý phiếu (FR6)
 * @param {Object} ticket - Thông tin phiếu hiện tại
 * @param {string} newStatus - Trạng thái mới muốn chuyển
 * @param {string} note - Ghi chú tiến độ
 * @param {Object} user - Người dùng thực hiện ({ role, technicianId })
 * @returns {{ valid: boolean, message?: string, code?: string, cleanNote?: string }}
 */
function validateStatusTransition(ticket, newStatus, note, user = {}) {
    if (!ticket) {
        return { valid: false, message: 'Phiếu bảo hành không tồn tại', code: 'PHIEU_KHONG_TON_TAI' };
    }

    // Tiêu chí AC5.2: Phiếu trạng thái MOI chưa được phân công thì không thể hoàn tất hay cập nhật tiến độ
    if (ticket.status === 'MOI') {
        return {
            valid: false,
            message: 'Phiếu bảo hành đang ở trạng thái MỚI, chưa được phân công KTV (vi phạm AC5.2)',
            code: 'PHIEU_CHUA_PHAN_CONG'
        };
    }

    const validStatuses = ['DANG_XU_LY', 'CHO_LINH_KIEN', 'HOAN_TAT'];
    if (!validStatuses.includes(newStatus)) {
        return {
            valid: false,
            message: `Trạng thái mới không hợp lệ: ${newStatus}. Trạng thái cho phép: ${validStatuses.join(', ')}`,
            code: 'TRANG_THAI_KHONG_HOP_LE'
        };
    }

    if (ticket.status === newStatus) {
        return {
            valid: false,
            message: `Phiếu bảo hành hiện đã ở trạng thái ${newStatus}`,
            code: 'TRANG_THAI_TRUNG_LAP'
        };
    }

    // Phân quyền: Kỹ thuật viên chỉ được cập nhật phiếu được phân công cho chính mình
    if (user && user.role === 'TECHNICIAN') {
        if (!user.technicianId || ticket.technician_id !== user.technicianId) {
            return {
                valid: false,
                message: `Kỹ thuật viên chỉ có quyền cập nhật tiến độ cho phiếu của chính mình. Phiếu này thuộc về KTV khác.`,
                code: 'FORBIDDEN'
            };
        }
    }

    if (!note || typeof note !== 'string' || note.trim().length < 3) {
        return {
            valid: false,
            message: 'Ghi chú tiến độ kỹ thuật là bắt buộc (tối thiểu 3 ký tự)',
            code: 'THIEU_GHI_CHU_TIEN_DO'
        };
    }

    return { valid: true, cleanNote: note.trim() };
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
        let customerId = data.customer_id;

        // Nếu người dùng tự nhập khách hàng mới (customer_name + customer_phone)
        if (!customerId && (data.customer_name || data.customer_phone)) {
            if (!data.customer_name || data.customer_name.trim().length < 2) {
                throw new LoiNghiepVu('TEN_KH_QUA_NGAN', 'Họ tên khách hàng phải có tối thiểu 2 ký tự', 400);
            }
            const phoneDigits = (data.customer_phone || '').replace(/\D/g, '');
            if (phoneDigits.length < 8) {
                throw new LoiNghiepVu('SDT_KHONG_HOP_LE', 'Số điện thoại khách hàng phải có ít nhất 8 chữ số', 400);
            }
            const customer = ticketRepository.findOrCreateCustomer({
                full_name: data.customer_name,
                phone: data.customer_phone,
                address: data.customer_address
            });
            customerId = customer.customer_id;
        }

        if (!customerId || !data.center_id || !data.issue_category || !data.issue_desc) {
            throw new LoiNghiepVu('THIEU_TRUONG_BAT_BUOC', 'Thiếu thông tin bắt buộc (Khách hàng, Trung tâm, Nhóm sự cố, Mô tả sự cố)', 400);
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
            customer_id: customerId,
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

    // 11. Cập nhật tiến độ xử lý phiếu bảo hành (KTV / Quản lý - FR6, US5)
    updateTicketStatus(ticketId, newStatus, note, user = {}) {
        const ticket = this.getTicketById(ticketId);
        const check = validateStatusTransition(ticket, newStatus, note, user);
        if (!check.valid) {
            const statusCode = check.code === 'FORBIDDEN' ? 403 : (check.code === 'PHIEU_KHONG_TON_TAI' ? 404 : 400);
            throw new LoiNghiepVu(check.code, check.message, statusCode);
        }

        const closedAt = newStatus === 'HOAN_TAT' ? new Date().toISOString() : null;
        const updatedTicket = ticketRepository.updateStatus(ticketId, newStatus, closedAt);

        ticketRepository.createStatusLog({
            ticket_id: ticketId,
            from_status: ticket.status,
            to_status: newStatus,
            from_technician_id: ticket.technician_id,
            to_technician_id: ticket.technician_id,
            reason: 'KTV cập nhật tiến độ sửa chữa',
            note: check.cleanNote,
            changed_by: user.technicianId || user.userId || 1
        });

        return toTicketView(updatedTicket);
    }
}

const serviceInstance = new TicketService();

module.exports = serviceInstance;
module.exports.calculateSlaDueDate = calculateSlaDueDate;
module.exports.checkTechnicianEligibility = checkTechnicianEligibility;
module.exports.validateReassignReason = validateReassignReason;
module.exports.checkAppointmentSlotCapacity = checkAppointmentSlotCapacity;
module.exports.validateStatusTransition = validateStatusTransition;
module.exports.toTicketView = toTicketView;
module.exports.maskPhoneNumber = maskPhoneNumber;
