const express = require('express');
const router = express.Router();
const ticketController = require('../presentation/controllers/ticketController');
const { authenticateToken } = require('../middleware/auth');
const { LoiNghiepVu } = require('../errors');

// Tất cả các routes tickets đều đi qua authenticateToken (nếu có header Authorization)
router.use(authenticateToken);

// 1. Endpoint khôi phục dữ liệu mẫu về MOI (chuyển logic SQL về Repository theo góp ý GV)
// Lưu ý: Đặt TRƯỚC route /:id để tránh Express nhầm 'reset-demo' là tham số :id
router.post('/reset-demo', (req, res, next) => ticketController.resetDemo(req, res, next));

// 2. CRUD Tickets (Khắc phục S1 BT2 - CRUD đầy đủ)
// 2.1. Đọc danh sách phiếu (Read all)
router.get('/', (req, res, next) => ticketController.getAll(req, res, next));

// 2.2. Tạo phiếu mới (Create) - Chỉ Quản lý / Lễ tân thực hiện
router.post('/', (req, res, next) => {
    const role = req.headers['x-user-role'];
    if (role === 'TECHNICIAN') {
        return next(new LoiNghiepVu('FORBIDDEN', 'Kỹ thuật viên không có quyền tiếp nhận tạo phiếu mới tại quầy. Thao tác này thuộc thẩm quyền của Quản lý.', 403));
    }
    ticketController.create(req, res, next);
});

// 2.3. Xem chi tiết phiếu theo ID (Read one)
router.get('/:id', (req, res, next) => ticketController.getById(req, res, next));

// 2.4. Cập nhật thông tin phiếu (Update) - Khắc phục S1 BT2
router.put('/:id', (req, res, next) => {
    const role = req.headers['x-user-role'];
    if (role === 'TECHNICIAN') {
        return next(new LoiNghiepVu('FORBIDDEN', 'Kỹ thuật viên không có quyền chỉnh sửa thông tin chung của phiếu. Thao tác này thuộc thẩm quyền của Quản lý.', 403));
    }
    ticketController.update(req, res, next);
});

// 2.5. Xóa phiếu bảo hành (Delete) - Khắc phục S1 BT2
router.delete('/:id', (req, res, next) => {
    const role = req.headers['x-user-role'];
    if (role === 'TECHNICIAN') {
        return next(new LoiNghiepVu('FORBIDDEN', 'Kỹ thuật viên không có quyền xóa phiếu bảo hành. Thao tác này thuộc thẩm quyền của Quản lý.', 403));
    }
    ticketController.delete(req, res, next);
});

// 3. Nghiệp vụ điều phối Luồng L4
// 3.1. Gợi ý KTV thông minh (US2, QT-07)
router.get('/:id/recommend-technicians', (req, res, next) => ticketController.getRecommended(req, res, next));

// 3.2. Phân công KTV (US2, QT-06, QT-07)
router.post('/:id/assign', (req, res, next) => {
    const role = req.headers['x-user-role'];
    if (role === 'TECHNICIAN') {
        return next(new LoiNghiepVu('FORBIDDEN', 'Kỹ thuật viên không có quyền phân công phiếu cho KTV khác. Thao tác này thuộc thẩm quyền của Quản lý trung tâm.', 403));
    }
    ticketController.assign(req, res, next);
});

// 3.3. Chuyển gán phiếu sang KTV khác (US6, QT-08)
router.post('/:id/reassign', (req, res, next) => {
    const role = req.headers['x-user-role'];
    if (role === 'TECHNICIAN') {
        return next(new LoiNghiepVu('FORBIDDEN', 'Kỹ thuật viên không có quyền chuyển gán phiếu. Thao tác này thuộc thẩm quyền của Quản lý trung tâm.', 403));
    }
    ticketController.reassign(req, res, next);
});

// 3.4. Cập nhật tiến độ xử lý phiếu (FR6, US5)
router.post('/:id/status', (req, res, next) => ticketController.updateStatus(req, res, next));
router.patch('/:id/status', (req, res, next) => ticketController.updateStatus(req, res, next));

// 3.5. Lịch hẹn của phiếu
router.get('/:id/appointments', (req, res, next) => ticketController.getAppointments(req, res, next));
router.post('/:id/appointments', (req, res, next) => {
    const role = req.headers['x-user-role'];
    if (role === 'TECHNICIAN') {
        return next(new LoiNghiepVu('FORBIDDEN', 'Kỹ thuật viên không có quyền đặt lịch hẹn của trung tâm. Thao tác này thuộc thẩm quyền của Quản lý / Lễ tân.', 403));
    }
    ticketController.createAppointment(req, res, next);
});

// 3.6. Nhật ký kiểm toán (Audit Log)
router.get('/:id/logs', (req, res, next) => ticketController.getLogs(req, res, next));

module.exports = router;
