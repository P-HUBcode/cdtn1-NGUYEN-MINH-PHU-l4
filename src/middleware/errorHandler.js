/**
 * MIDDLEWARE XỬ LÝ LỖI TẬP TRUNG XUYÊN LỚP (CENTRALIZED ERROR HANDLER)
 * Học phần: Chuyên đề tốt nghiệp 1 - Smart CRM Mekong Mobile
 * Sinh viên: Nguyễn Minh Phú - MSSV: 2374802013447
 * Tuân thủ thiết kế Buổi 11 (Slide 24 - 26):
 *  - Là nơi DUY NHẤT trong hệ thống ánh xạ Domain Error sang HTTP Status Code
 *  - Ghi log đúng 1 LẦN duy nhất tại điểm cuối cùng
 *  - Phân loại: LoiNghiepVu -> Log INFO (nghiệp vụ từ chối hợp lệ); LoiTruyCapDuLieu/Crash -> Log ERROR
 *  - Tuyệt đối KHÔNG trả err.stack, câu SQL ra client (chỉ trả thông điệp + requestId tra cứu)
 */

const { LoiNghiepVu, LoiTruyCapDuLieu } = require('../errors');
const logger = require('../utils/logger').child('ErrorHandler');

function errorHandler(err, req, res, next) {
    const requestId = req.requestId || 'req-unknown';

    // 1. Trường hợp 1: Lỗi nghiệp vụ có chủ đích (Domain Business Rules)
    if (err instanceof LoiNghiepVu) {
        logger.info({
            requestId,
            path: req.path,
            method: req.method,
            errorCode: err.ma,
            user_id: req.body?.user_id
        }, `Vi phạm quy tắc nghiệp vụ: ${err.message}`);

        return res.status(err.httpStatus || 400).json({
            error: err.ma,
            message: err.message,
            requestId
        });
    }

    // 2. Trường hợp 2: Lỗi truy cập cơ sở dữ liệu (Database / Infrastructure Error)
    if (err instanceof LoiTruyCapDuLieu) {
        logger.error({
            requestId,
            path: req.path,
            method: req.method,
            err: err.cause || err
        }, 'Sự cố truy cập cơ sở dữ liệu hạ tầng');

        return res.status(503).json({
            error: 'LOI_TRUY_CAP_DU_LIEU',
            message: `Hệ thống cơ sở dữ liệu tạm thời gián đoạn. Vui lòng thử lại sau ít phút. Mã tra cứu: ${requestId}`,
            requestId
        });
    }

    // 3. Trường hợp 3: Lỗi hệ thống không lường trước (Unhandled 500)
    const statusCode = err.statusCode || 500;
    const errorCode = statusCode === 400 ? 'VALIDATION_FAILED' : 
                     (statusCode === 401 ? 'UNAUTHORIZED' : 
                     (statusCode === 404 ? 'NOT_FOUND' : 'LOI_HE_THONG'));

    if (statusCode >= 500) {
        logger.error({
            requestId,
            path: req.path,
            method: req.method,
            err
        }, `Lỗi máy chủ nội bộ: ${err.message}`);
    } else {
        logger.info({
            requestId,
            path: req.path,
            method: req.method,
            errorCode
        }, err.message);
    }

    return res.status(statusCode).json({
        error: errorCode,
        message: statusCode >= 500 
            ? `Hệ thống đang gặp sự cố. Vui lòng liên hệ bộ phận hỗ trợ kèm mã tra cứu: ${requestId}` 
            : err.message,
        requestId
    });
}

module.exports = errorHandler;
