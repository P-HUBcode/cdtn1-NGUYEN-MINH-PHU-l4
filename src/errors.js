/**
 * HỆ THỐNG ĐỊNH NGHĨA LỖI XUYÊN LỚP (APPLICATION ERROR HIERARCHY)
 * Học phần: Chuyên đề tốt nghiệp 1 - Smart CRM Mekong Mobile
 * Sinh viên: Nguyễn Minh Phú - MSSV: 2374802013447
 * Tuân thủ thiết kế Buổi 11 (Slide 23 - 26)
 */

/**
 * Lỗi Nghiệp vụ (Domain/Business Error)
 * Phát sinh từ Service layer khi vi phạm các quy tắc nghiệp vụ QT-xx
 * Ví dụ: QT-04 (SLA), QT-06 (Trung tâm), QT-07 (Tay nghề), QT-08 (Lý do chuyển gán), QT-09 (Tải lịch hẹn)
 */
class LoiNghiepVu extends Error {
    /**
     * @param {string} ma - Mã máy đọc duy nhất (VD: 'KTV_KHONG_PHU_HOP', 'LICH_HEN_QUA_TAI')
     * @param {string} thongDiep - Thông điệp tiếng Việt thân thiện với người dùng
     * @param {number} [httpStatus=400] - Mã trạng thái HTTP tương ứng (400, 404, 409)
     */
    constructor(ma, thongDiep, httpStatus = 400) {
        super(thongDiep);
        this.name = 'LoiNghiepVu';
        this.ma = ma;
        this.httpStatus = httpStatus;
        Error.captureStackTrace(this, this.constructor);
    }
}

/**
 * Lỗi Truy cập Dữ liệu (Data Access / Infrastructure Error)
 * Phát sinh từ Repository layer khi gặp sự cố CSDL, truy vấn sai, mất kết nối
 * Bọc lỗi gốc (cause) để phục vụ điều tra trong log, không lộ cho người dùng
 */
class LoiTruyCapDuLieu extends Error {
    /**
     * @param {string} thongDiep - Mô tả ngữ cảnh xảy ra sự cố
     * @param {Error} [cause] - Lỗi gốc từ database driver
     */
    constructor(thongDiep = 'Lỗi truy cập dữ liệu', cause = null) {
        super(thongDiep);
        this.name = 'LoiTruyCapDuLieu';
        this.cause = cause;
        this.httpStatus = 503;
        Error.captureStackTrace(this, this.constructor);
    }
}

module.exports = {
    LoiNghiepVu,
    LoiTruyCapDuLieu
};
