const crypto = require('node:crypto');
const { LoiNghiepVu } = require('../errors');
const logger = require('../utils/logger').child('AuthMiddleware');

// Auth Configuration & Danh sách Tài khoản Đăng nhập (Luồng L4)
// Tuân thủ tiêu chí bảo mật SE (S3): Mật khẩu được băm an toàn bằng SHA-256 + Salt
const DEMO_TOKEN = 'demo-jwt-token-smart-crm-2026';
const PASSWORD_SALT = 'mekong_salt_2026';
// Hash SHA-256 của chuỗi '123456' + 'mekong_salt_2026'
const HASHED_DEFAULT_PW = '030dfae48ae14898e936a7fd95209f7774a80687c433f4bbf602d579a8634802';

function verifyPassword(inputPassword, storedHash, salt) {
    if (!inputPassword || !storedHash || !salt) return false;
    const computedHash = crypto.createHash('sha256').update(inputPassword + salt).digest('hex');
    return crypto.timingSafeEqual(Buffer.from(computedHash), Buffer.from(storedHash));
}

const DEMO_ACCOUNTS = {
    'quanly': {
        passwordHash: HASHED_DEFAULT_PW,
        salt: PASSWORD_SALT,
        fullName: 'Nguyễn Minh Phú (Quản lý)',
        role: 'MANAGER',
        technicianId: null,
        description: 'Quản lý Trung tâm Cần Thơ — Toàn quyền điều phối, phân công & lịch hẹn'
    },
    'ktv_binh': {
        passwordHash: HASHED_DEFAULT_PW,
        salt: PASSWORD_SALT,
        fullName: 'Trần Văn Bình (KTV-001)',
        role: 'TECHNICIAN',
        technicianId: 1,
        technicianName: 'Trần Văn Bình',
        description: 'Kỹ thuật viên chuyên Màn hình (Proficiency: 5/5, Pin: 4/5)'
    },
    'ktv_cuong': {
        passwordHash: HASHED_DEFAULT_PW,
        salt: PASSWORD_SALT,
        fullName: 'Lê Văn Cường (KTV-002)',
        role: 'TECHNICIAN',
        technicianId: 2,
        technicianName: 'Lê Văn Cường',
        description: 'Kỹ thuật viên chuyên Phần mềm (Proficiency: 5/5, Màn hình: 3/5)'
    },
    'admin': {
        passwordHash: HASHED_DEFAULT_PW,
        salt: PASSWORD_SALT,
        fullName: 'Quản trị viên Hệ thống',
        role: 'ADMIN',
        technicianId: null,
        description: 'Quản trị viên cấp cao Mekong Mobile'
    }
};

// Middleware kiểm tra xác thực nếu có header Authorization
function authenticateToken(req, res, next) {
    const authHeader = req.headers['authorization'];
    if (authHeader && authHeader.startsWith('Bearer ')) {
        const token = authHeader.split(' ')[1];
        if (token !== DEMO_TOKEN) {
            return next(new LoiNghiepVu('UNAUTHORIZED', 'Phiên làm việc hết hạn hoặc token không hợp lệ (401)', 401));
        }
    }
    next();
}

module.exports = {
    DEMO_TOKEN,
    PASSWORD_SALT,
    HASHED_DEFAULT_PW,
    DEMO_ACCOUNTS,
    verifyPassword,
    authenticateToken
};
