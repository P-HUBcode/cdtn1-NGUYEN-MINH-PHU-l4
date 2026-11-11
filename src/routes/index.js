const express = require('express');
const router = express.Router();

const authRoutes = require('./auth.routes');
const ticketRoutes = require('./ticket.routes');
const appointmentRoutes = require('./appointment.routes');
const technicianRoutes = require('./technician.routes');
const testRoutes = require('./test.routes');

// Đăng ký các module routes con vào /api/v1
router.use('/auth', authRoutes);
router.use('/tickets', ticketRoutes);
router.use('/appointments', appointmentRoutes);
router.use('/technicians', technicianRoutes);
router.use('/tests', testRoutes);

// Endpoint mô phỏng 401 hỗ trợ cả đường dẫn trực tiếp /api/v1/test-401
router.get('/test-401', (req, res, next) => {
    const { LoiNghiepVu } = require('../errors');
    next(new LoiNghiepVu('UNAUTHORIZED', 'Mô phỏng phiên làm việc hết hạn (401)', 401));
});

module.exports = router;
