/**
 * HỆ THỐNG LOGGING CÓ CẤU TRÚC (STRUCTURED LOGGING)
 * Học phần: Chuyên đề tốt nghiệp 1 - Smart CRM Mekong Mobile
 * Sinh viên: Nguyễn Minh Phú - MSSV: 2374802013447
 * Tuân thủ thiết kế Buổi 11 (Slide 20 - 23):
 *  - 4 mức log: DEBUG, INFO, WARN, ERROR (lấy từ process.env.LOG_LEVEL)
 *  - 3 yếu tố bắt buộc: THỜI ĐIỂM (ISO 8601), NGỮ CẢNH (requestId, IDs), NỘI DUNG (message)
 *  - Tự động khử độc / che dấu (Redaction) các trường nhạy cảm: password, token, SĐT, PII
 *  - Xuất JSON chuẩn ra stdout để phục vụ Docker container và giám sát tập trung
 */

const LOG_LEVELS = {
    DEBUG: 10,
    INFO: 20,
    WARN: 30,
    ERROR: 40
};

// Đọc level cấu hình từ biến môi trường (mặc định là INFO)
const CURRENT_LEVEL_NAME = (process.env.LOG_LEVEL || 'INFO').toUpperCase();
const CURRENT_LEVEL = LOG_LEVELS[CURRENT_LEVEL_NAME] || LOG_LEVELS.INFO;

// Danh sách các trường nhạy cảm cần tự động che giấu (Data Redaction)
const SENSITIVE_KEYS = new Set([
    'password',
    'mat_khau',
    'token',
    'authorization',
    'jwt',
    'secret',
    'customer_phone',
    'phone',
    'so_dien_thoai',
    'sdt'
]);

/**
 * Đệ quy làm sạch object, che dấu thông tin nhạy cảm
 * @param {*} data 
 * @returns {*}
 */
function sanitizeData(data) {
    if (!data || typeof data !== 'object') {
        return data;
    }

    if (Array.isArray(data)) {
        return data.map(item => sanitizeData(item));
    }

    const clean = {};
    for (const [key, val] of Object.entries(data)) {
        const lowerKey = key.toLowerCase();
        if (SENSITIVE_KEYS.has(lowerKey)) {
            clean[key] = '***REDACTED***';
        } else if (typeof val === 'object' && val !== null) {
            clean[key] = sanitizeData(val);
        } else {
            clean[key] = val;
        }
    }
    return clean;
}

class Logger {
    constructor(moduleName = 'App') {
        this.moduleName = moduleName;
    }

    _write(levelName, context, message) {
        if (LOG_LEVELS[levelName] < CURRENT_LEVEL) {
            return;
        }

        let ctx = {};
        let msg = message;

        // Cho phép gọi logger.info('thông điệp') hoặc logger.info({ ctx }, 'thông điệp')
        if (typeof context === 'string' && message === undefined) {
            msg = context;
            ctx = {};
        } else if (typeof context === 'object' && context !== null) {
            ctx = sanitizeData(context);
        }

        // Bóc tách lỗi nếu có truyền vào context
        if (ctx.err instanceof Error) {
            ctx.error = {
                name: ctx.err.name,
                message: ctx.err.message,
                stack: ctx.err.stack
            };
            delete ctx.err;
        }

        const logEntry = {
            timestamp: new Date().toISOString(),
            level: levelName,
            module: this.moduleName,
            ...ctx,
            message: msg
        };

        // Ghi ra stdout dưới dạng JSON 1 dòng (chuẩn 12-factor app & Docker logging)
        process.stdout.write(JSON.stringify(logEntry) + '\n');
    }

    debug(context, message) {
        this._write('DEBUG', context, message);
    }

    info(context, message) {
        this._write('INFO', context, message);
    }

    warn(context, message) {
        this._write('WARN', context, message);
    }

    error(context, message) {
        this._write('ERROR', context, message);
    }

    child(moduleName) {
        return new Logger(`${this.moduleName}:${moduleName}`);
    }
}

const defaultLogger = new Logger('SmartCRM');

module.exports = defaultLogger;
module.exports.Logger = Logger;
module.exports.sanitizeData = sanitizeData;
