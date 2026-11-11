require('dotenv').config();
const express = require('express');
const path = require('node:path');
const { initDatabase } = require('./config/database');
const requestIdMiddleware = require('./middleware/requestId');
const errorHandler = require('./middleware/errorHandler');
const logger = require('./utils/logger').child('Server');
const apiRoutes = require('./routes');

const app = express();
const PORT = process.env.PORT || 3000;

// 1. Gán RequestId cho mỗi request (Buổi 11 - Slide 21, 25)
app.use(requestIdMiddleware);

// 2. Middleware CORS thủ công (đảm bảo không bị chặn khi frontend gọi API)
app.use((req, res, next) => {
    res.header('Access-Control-Allow-Origin', '*');
    res.header('Access-Control-Allow-Methods', 'GET, POST, PUT, PATCH, DELETE, OPTIONS');
    res.header('Access-Control-Allow-Headers', 'Origin, X-Requested-With, Content-Type, Accept, Authorization, X-Request-Id, X-User-Role, X-Technician-Id');
    if (req.method === 'OPTIONS') {
        return res.sendStatus(200);
    }
    next();
});

// 3. Middleware parsing JSON
app.use(express.json());

// 4. Request Logging Middleware (Structured Logging - Slide 20-23)
app.use((req, res, next) => {
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

// 8. Đăng ký toàn bộ Router nghiệp vụ được tách lớp độc lập trong src/routes/
// (Khắc phục góp ý của Giảng viên ở BT2: Tách routes ra khỏi app.js)
app.use('/api/v1', apiRoutes);

// Root route JSON (Service Health & System Info cho Docker Compose & Health Check)
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
