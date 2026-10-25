require('dotenv').config();
const express = require('express');
const path = require('node:path');
const { initDatabase } = require('./config/database');
const ticketController = require('./presentation/controllers/ticketController');
const requestIdMiddleware = require('./middleware/requestId');
const errorHandler = require('./middleware/errorHandler');
const logger = require('./utils/logger').child('Server');
const { LoiNghiepVu } = require('./errors');

const app = express();
const PORT = process.env.PORT || 3000;

// 1. Gán RequestId cho mỗi request (Buổi 11 - Slide 21, 25)
app.use(requestIdMiddleware);

// 2. Middleware CORS thủ công (đảm bảo không bị chặn khi frontend gọi API)
app.use((req, res, next) => {
    res.header('Access-Control-Allow-Origin', '*');
    res.header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');
    res.header('Access-Control-Allow-Headers', 'Origin, X-Requested-With, Content-Type, Accept, Authorization, X-Request-Id');
    if (req.method === 'OPTIONS') {
        return res.sendStatus(200);
    }
    next();
});

// 3. Middleware parsing JSON
app.use(express.json());

// 4. Request Logging Middleware (Structured Logging - Slide 20-23)
app.use((req, res, next) => {
    // Chỉ log các request vào API, bỏ qua static files để tránh rác log
    if (req.path.startsWith('/api')) {
        logger.info({
            requestId: req.requestId,
            method: req.method,
            path: req.path,
            ip: req.ip
        }, `Incoming API Request: ${req.method} ${req.path}`);
    }
    next();
});

// 5. Tắt cache để trình duyệt luôn cập nhật giao diện và script mới nhất ngay lập tức
app.use((req, res, next) => {
    res.setHeader('Cache-Control', 'no-store, no-cache, must-revalidate, proxy-revalidate');
    res.setHeader('Pragma', 'no-cache');
    res.setHeader('Expires', '0');
    next();
});

// 6. Phục vụ giao diện tĩnh Frontend (HTML/CSS/JS)
app.use(express.static(path.join(__dirname, 'public'), {
    etag: false,
    maxAge: 0
}));

// 7. Khởi tạo Database và Seed data (Idempotent - Chạy nhiều lần không trùng dữ liệu C5)
initDatabase();

// 8. Auth Middleware & Danh sách Tài khoản Đăng nhập (Luồng L4)
const DEMO_TOKEN = 'demo-jwt-token-smart-crm-2026';

const DEMO_ACCOUNTS = {
    'quanly': {
        password: '123456',
        fullName: 'Nguyễn Minh Phú (Quản lý)',
        role: 'MANAGER',
        description: 'Quản lý Trung tâm Cần Thơ — Toàn quyền điều phối, phân công & lịch hẹn'
    },
    'ktv_binh': {
        password: '123456',
        fullName: 'Trần Văn Bình (KTV-001)',
        role: 'TECHNICIAN',
        description: 'Kỹ thuật viên chuyên Màn hình (Proficiency: 5/5, Pin: 4/5)'
    },
    'ktv_cuong': {
        password: '123456',
        fullName: 'Lê Văn Cường (KTV-002)',
        role: 'TECHNICIAN',
        description: 'Kỹ thuật viên chuyên Phần mềm (Proficiency: 5/5, Màn hình: 3/5)'
    },
    'admin': {
        password: '123456',
        fullName: 'Quản trị viên Hệ thống',
        role: 'ADMIN',
        description: 'Quản trị viên cấp cao Mekong Mobile'
    }
};

app.post('/api/v1/auth/login', (req, res, next) => {
    try {
        const { username, password } = req.body;
        const account = DEMO_ACCOUNTS[username];

        if (account && account.password === password) {
            logger.info({
                requestId: req.requestId,
                username,
                role: account.role
            }, 'Người dùng đăng nhập thành công');

            return res.json({
                success: true,
                token: DEMO_TOKEN,
                user: {
                    username,
                    fullName: account.fullName,
                    role: account.role,
                    description: account.description
                }
            });
        }

        throw new LoiNghiepVu(
            'UNAUTHORIZED',
            'Sai tên đăng nhập hoặc mật khẩu! Thử các tài khoản: quanly, ktv_binh, ktv_cuong, admin (mật khẩu chung: 123456)',
            401
        );
    } catch (err) {
        next(err);
    }
});

// Endpoint trả về danh sách tài khoản demo để người dùng/giảng viên tiện chọn trên giao diện
app.get('/api/v1/auth/accounts', (req, res) => {
    const list = Object.entries(DEMO_ACCOUNTS).map(([username, info]) => ({
        username,
        fullName: info.fullName,
        role: info.role,
        description: info.description
    }));
    res.json({ success: true, count: list.length, data: list });
});

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

// Routes cho Entity Tickets & Luồng L4
app.get('/api/v1/tickets', authenticateToken, (req, res, next) => ticketController.getAll(req, res, next));
app.get('/api/v1/tickets/:id', authenticateToken, (req, res, next) => ticketController.getById(req, res, next));
app.post('/api/v1/tickets', authenticateToken, (req, res, next) => ticketController.create(req, res, next));
app.get('/api/v1/tickets/:id/recommend-technicians', authenticateToken, (req, res, next) => ticketController.getRecommended(req, res, next));
app.post('/api/v1/tickets/:id/assign', authenticateToken, (req, res, next) => ticketController.assign(req, res, next));
app.post('/api/v1/tickets/:id/reassign', authenticateToken, (req, res, next) => ticketController.reassign(req, res, next));

// Endpoint khôi phục dữ liệu phiếu mẫu về trạng thái MOI (tiện cho demo & kiểm thử)
app.post('/api/v1/tickets/reset-demo', (req, res) => {
    const { db } = require('./config/database');
    db.prepare(`UPDATE tickets SET status = 'MOI', technician_id = NULL WHERE ticket_id IN (1, 2)`).run();
    logger.info({ requestId: req.requestId }, 'Đã khôi phục các phiếu mẫu #1, #2 về trạng thái MOI');
    res.json({ success: true, message: 'Đã khôi phục các phiếu mẫu về trạng thái MOI!' });
});

// Routes phụ trợ Luồng L4
app.get('/api/v1/technicians', authenticateToken, (req, res, next) => ticketController.getTechnicians(req, res, next));
app.get('/api/v1/tickets/:id/appointments', authenticateToken, (req, res, next) => ticketController.getAppointments(req, res, next));
app.post('/api/v1/tickets/:id/appointments', authenticateToken, (req, res, next) => ticketController.createAppointment(req, res, next));
app.get('/api/v1/tickets/:id/logs', authenticateToken, (req, res, next) => ticketController.getLogs(req, res, next));

// API Test endpoint cố tình trả 401 để kiểm thử giao diện
app.get('/api/v1/test-401', (req, res, next) => {
    next(new LoiNghiepVu('UNAUTHORIZED', 'Mô phỏng phiên làm việc hết hạn (401)', 401));
});

// Root route JSON (Service Health & Info)
app.get('/api', (req, res) => {
    res.json({
        name: 'Smart CRM Warranty Hub API - Luồng L4',
        version: '1.0.0',
        author: 'Nguyễn Minh Phú - 2374802013447',
        status: 'UP',
        timestamp: new Date().toISOString()
    });
});

// 9. Centralized Error Handling Middleware (Đăng ký CUỐI CÙNG trong pipeline)
app.use(errorHandler);

if (require.main === module) {
    app.listen(PORT, () => {
        logger.info({ port: PORT }, `Server Smart CRM Warranty Hub is running at http://localhost:${PORT}`);
    });
}

module.exports = app;
