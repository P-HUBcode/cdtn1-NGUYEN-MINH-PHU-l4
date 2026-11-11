const express = require('express');
const router = express.Router();
const ticketController = require('../presentation/controllers/ticketController');
const { authenticateToken } = require('../middleware/auth');
const { LoiNghiepVu } = require('../errors');

router.use(authenticateToken);

// CRUD Appointments (Khắc phục S1 BT2 - CRUD đầy đủ cho thực thể thứ 2)
// 1. Lấy danh sách toàn bộ lịch hẹn (Read all)
router.get('/', (req, res, next) => ticketController.getAllAppointments(req, res, next));

// 2. Lấy chi tiết lịch hẹn theo ID (Read one)
router.get('/:id', (req, res, next) => ticketController.getAppointmentById(req, res, next));

// 3. Cập nhật lịch hẹn (Update) - Chỉ Quản lý / Lễ tân thực hiện
router.put('/:id', (req, res, next) => {
    const role = req.headers['x-user-role'];
    if (role === 'TECHNICIAN') {
        return next(new LoiNghiepVu('FORBIDDEN', 'Kỹ thuật viên không có quyền điều chỉnh lịch hẹn giao nhận.', 403));
    }
    ticketController.updateAppointment(req, res, next);
});

// 4. Xóa / Hủy lịch hẹn (Delete) - Chỉ Quản lý / Lễ tân thực hiện
router.delete('/:id', (req, res, next) => {
    const role = req.headers['x-user-role'];
    if (role === 'TECHNICIAN') {
        return next(new LoiNghiepVu('FORBIDDEN', 'Kỹ thuật viên không có quyền xóa lịch hẹn.', 403));
    }
    ticketController.deleteAppointment(req, res, next);
});

module.exports = router;
