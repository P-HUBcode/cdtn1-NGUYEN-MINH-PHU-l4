require('dotenv').config();
const express = require('express');
const path = require('node:path');
const { initDatabase } = require('./config/database');
const ticketController = require('./presentation/controllers/ticketController');

const app = express();
const PORT = process.env.PORT || 3000;

// 1. Middleware CORS thủ công (đảm bảo không bị chặn khi frontend gọi API)
app.use((req, res, next) => {
    res.header('Access-Control-Allow-Origin', '*');
    res.header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');
    res.header('Access-Control-Allow-Headers', 'Origin, X-Requested-With, Content-Type, Accept, Authorization');
    if (req.method === 'OPTIONS') {
        return res.sendStatus(200);
    }
    next();
});

// 2. Middleware parsing JSON
app.use(express.json());

// 3. Phục vụ giao diện tĩnh Frontend (HTML/CSS/JS)
app.use(express.static(path.join(__dirname, 'public')));

// 4. Khởi tạo Database và Seed data
initDatabase();

// 5. Auth Middleware & Route (Buổi 10: Xử lý Đăng nhập & 401)
const DEMO_TOKEN = 'demo-jwt-token-smart-crm-2026';

app.post('/api/v1/auth/login', (req, res) => {
    const { username, password } = req.body;
    if (username === 'quanly' && password === '123456') {
        return res.json({
            success: true,
            token: DEMO_TOKEN,
            user: { username: 'quanly', fullName: 'Nguyễn Minh Phú (Quản lý)', role: 'MANAGER' }
        });
    }
    return res.status(401).json({
        error: {
            code: 'UNAUTHORIZED',
            message: 'Sai tên đăng nhập hoặc mật khẩu (Thử tài khoản: quanly / 123456)'
        }
    });
});

// Middleware kiểm tra xác thực nếu có header Authorization
function authenticateToken(req, res, next) {
    const authHeader = req.headers['authorization'];
    if (authHeader && authHeader.startsWith('Bearer ')) {
        const token = authHeader.split(' ')[1];
        if (token !== DEMO_TOKEN) {
            return res.status(401).json({
                error: {
                    code: 'UNAUTHORIZED',
                    message: 'Phiên làm việc hết hạn hoặc token không hợp lệ (401)'
                }
            });
        }
    }
    next();
}

// 6. Routes cho Entity Tickets & Luồng L4
app.get('/api/v1/tickets', authenticateToken, (req, res, next) => ticketController.getAll(req, res, next));
app.get('/api/v1/tickets/:id', authenticateToken, (req, res, next) => ticketController.getById(req, res, next));
app.post('/api/v1/tickets', authenticateToken, (req, res, next) => ticketController.create(req, res, next));
app.get('/api/v1/tickets/:id/recommend-technicians', authenticateToken, (req, res, next) => ticketController.getRecommended(req, res, next));
app.post('/api/v1/tickets/:id/assign', authenticateToken, (req, res, next) => ticketController.assign(req, res, next));
app.post('/api/v1/tickets/:id/reassign', authenticateToken, (req, res, next) => ticketController.reassign(req, res, next));

// Routes phụ trợ Luồng L4
app.get('/api/v1/technicians', authenticateToken, (req, res, next) => ticketController.getTechnicians(req, res, next));
app.get('/api/v1/tickets/:id/appointments', authenticateToken, (req, res, next) => ticketController.getAppointments(req, res, next));
app.post('/api/v1/tickets/:id/appointments', authenticateToken, (req, res, next) => ticketController.createAppointment(req, res, next));
app.get('/api/v1/tickets/:id/logs', authenticateToken, (req, res, next) => ticketController.getLogs(req, res, next));

// API Test endpoint cố tình trả 401 để kiểm thử giao diện
app.get('/api/v1/test-401', (req, res) => {
    res.status(401).json({
        error: { code: 'UNAUTHORIZED', message: 'Mô phỏng phiên làm việc hết hạn (401)' }
    });
});

// Root route JSON
app.get('/api', (req, res) => {
    res.json({
        name: 'Smart CRM Warranty Hub API - Luồng L4',
        version: '1.0.0',
        author: 'Nguyễn Minh Phú - 2374802013447',
        status: 'UP'
    });
});

// 7. Centralized Error Handling Middleware
app.use((err, req, res, next) => {
    const statusCode = err.statusCode || 500;
    res.status(statusCode).json({
        error: {
            code: statusCode === 400 ? 'VALIDATION_FAILED' : (statusCode === 404 ? 'NOT_FOUND' : 'SERVER_ERROR'),
            message: err.message || 'Đã có lỗi xảy ra trên máy chủ'
        }
    });
});

if (require.main === module) {
    app.listen(PORT, () => {
        console.log(`Server is running at http://localhost:${PORT}`);
    });
}

module.exports = app;
