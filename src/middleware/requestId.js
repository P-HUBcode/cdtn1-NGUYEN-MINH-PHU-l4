/**
 * MIDDLEWARE GÁN MÃ YÊU CẦU (REQUEST ID)
 * Sinh mã định danh duy nhất cho từng HTTP request để theo dõi xuyên lớp (Tracing)
 * Sinh viên: Nguyễn Minh Phú - MSSV: 2374802013447
 */

const crypto = require('node:crypto');

function requestIdMiddleware(req, res, next) {
    // Ưu tiên dùng requestId từ client gửi lên (nếu có), hoặc sinh mới UUID v4
    const reqId = req.headers['x-request-id'] || `req-${crypto.randomUUID().slice(0, 8)}`;
    req.requestId = reqId;
    res.setHeader('X-Request-Id', reqId);
    next();
}

module.exports = requestIdMiddleware;
