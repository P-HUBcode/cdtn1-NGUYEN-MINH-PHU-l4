/**
 * HỢP ĐỒNG DỮ LIỆU RANH GIỚI (DATA CONTRACT AT BOUNDARIES)
 * Học phần: Chuyên đề tốt nghiệp 1 - Smart CRM Mekong Mobile
 * Sinh viên: Nguyễn Minh Phú - MSSV: 2374802013447
 * Tuân thủ thiết kế Buổi 9 (Slide 7 - 13, Slide 28):
 *  - Định nghĩa rõ 3 yếu tố: Hình dạng (Shape), Ý nghĩa (Semantics), Hành vi khi sai (Failure Mode)
 *  - Xóa bỏ phụ thuộc ngầm (Implicit Dependency) giữa Lớp Trình bày và CSDL
 *  - Áp dụng QT-15: Khử độc & che số điện thoại khách hàng (Phone Masking) tại một nơi duy nhất
 */

/**
 * Hàm hỗ trợ che số điện thoại khách hàng tuân thủ quy tắc bảo mật QT-15
 * @param {string|null} phone - Số điện thoại gốc
 * @returns {string} Số điện thoại đã che (VD: 090****567)
 */
function maskPhoneNumber(phone) {
    if (!phone || typeof phone !== 'string') {
        return '(chưa có SĐT)';
    }
    const cleanPhone = phone.trim();
    if (cleanPhone.length < 7) {
        return cleanPhone;
    }
    // Giữ 3 chữ số đầu và 3 chữ số cuối, che toàn bộ phần giữa bằng dấu ****
    return cleanPhone.slice(0, 3) + '****' + cleanPhone.slice(-3);
}

/**
 * Hợp đồng dữ liệu một phiếu bảo hành chuyển giao cho Lớp Trình bày (Presentation Layer)
 * 
 * HỢP ĐỒNG QUY ĐỊNH:
 *  - ticket_id        : số nguyên, ID duy nhất trong CSDL, luôn có
 *  - ticket_code      : chuỗi mã phiếu định dạng BH-YYYYMM-XXX hoặc BH-XXXXXX-XXXX, luôn có
 *  - customer_name    : chuỗi họ tên khách hàng, luôn có (fallback '(không rõ họ tên)' khi null)
 *  - customer_phone   : chuỗi SĐT đã được che giấu theo QT-15 (không để lộ dãy số liên tục >= 7 chữ số)
 *  - issue_category   : chuỗi phân loại sự cố ('MAN_HINH' | 'PIN' | 'NGUON' | 'PHAN_MEM' | 'CAMERA')
 *  - issue_desc       : chuỗi mô tả lỗi tối thiểu 10 ký tự
 *  - priority         : chuỗi mức ưu tiên ('CAO' | 'TRUNG_BINH' | 'THAP')
 *  - status           : chuỗi trạng thái ('MOI' | 'DANG_XU_LY' | 'CHO_LINH_KIEN' | 'HOAN_TAT' | 'HUY')
 *  - received_at      : chuỗi thời điểm tiếp nhận định dạng ISO 8601
 *  - due_date         : chuỗi hạn cam kết SLA định dạng ISO 8601
 *  - technician_id    : số nguyên ID của KTV phụ trách HOẶC null nếu chưa phân công
 *  - technician_name  : chuỗi họ tên KTV HOẶC 'Chưa phân công'
 *  - center_name      : chuỗi tên chi nhánh tiếp nhận bảo hành
 * 
 * @param {Object} rawTicket - Dòng bản ghi thô từ Database
 * @returns {Object} Đối tượng view tuân thủ hợp đồng dữ liệu ranh giới
 */
function toTicketView(rawTicket) {
    if (!rawTicket) {
        return null;
    }

    // Chuẩn hóa ngày due_date sang chuỗi ISO 8601
    let formattedDueDate = rawTicket.due_date;
    if (rawTicket.due_date) {
        const d = new Date(rawTicket.due_date);
        if (!isNaN(d.getTime())) {
            formattedDueDate = d.toISOString();
        }
    }

    return {
        ticket_id: rawTicket.ticket_id,
        ticket_code: rawTicket.ticket_code,
        customer_id: rawTicket.customer_id,
        customer_name: (rawTicket.customer_name ?? '').trim() || '(không rõ họ tên)',
        customer_phone: maskPhoneNumber(rawTicket.customer_phone),
        issue_category: rawTicket.issue_category,
        issue_desc: rawTicket.issue_desc,
        priority: rawTicket.priority || 'TRUNG_BINH',
        status: rawTicket.status,
        received_at: rawTicket.received_at,
        due_date: formattedDueDate,
        center_id: rawTicket.center_id,
        center_name: rawTicket.center_name || 'Trung tâm mặc định',
        technician_id: rawTicket.technician_id || null,
        technician_name: rawTicket.technician_name || 'Chưa phân công'
    };
}

module.exports = {
    toTicketView,
    maskPhoneNumber
};
