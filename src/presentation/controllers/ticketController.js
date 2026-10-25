/**
 * TẦNG ĐIỀU KHIỂN (CONTROLLER LAYER)
 * Học phần: Chuyên đề tốt nghiệp 1 - Smart CRM Mekong Mobile
 * Sinh viên: Nguyễn Minh Phú - MSSV: 2374802013447
 * Tuân thủ thiết kế Buổi 11 (Slide 24 - 26):
 *  - Tiếp nhận HTTP Request, giải nén params/body, gọi Service
 *  - Phản hồi HTTP 200/201 khi thành công
 *  - Mọi ngoại lệ/lỗi được chuyển giao trực tiếp cho next(error) để Middleware xử lý lỗi tập trung
 *  - Tuyệt đối không log lỗi phân tán tại Controller
 */

const ticketService = require('../../services/ticketService');
const { LoiNghiepVu } = require('../../errors');

class TicketController {
    // GET /api/v1/tickets
    getAll(req, res, next) {
        try {
            const { status, center_id } = req.query;
            const tickets = ticketService.getAllTickets({ status, center_id });
            res.status(200).json({
                success: true,
                count: tickets.length,
                data: tickets
            });
        } catch (error) {
            next(error);
        }
    }

    // GET /api/v1/tickets/:id
    getById(req, res, next) {
        try {
            const ticket = ticketService.getTicketById(req.params.id);
            res.status(200).json({
                success: true,
                data: ticket
            });
        } catch (error) {
            next(error);
        }
    }

    // POST /api/v1/tickets
    create(req, res, next) {
        try {
            const newTicket = ticketService.createTicket(req.body);
            res.status(201).json({
                success: true,
                message: 'Tạo phiếu bảo hành thành công',
                data: newTicket
            });
        } catch (error) {
            next(error);
        }
    }

    // GET /api/v1/tickets/:id/recommend-technicians
    getRecommended(req, res, next) {
        try {
            const techs = ticketService.getRecommendedTechnicians(req.params.id);
            res.status(200).json({
                success: true,
                count: techs.length,
                data: techs
            });
        } catch (error) {
            next(error);
        }
    }

    // POST /api/v1/tickets/:id/assign
    assign(req, res, next) {
        try {
            const { technician_id, note, user_id } = req.body;
            if (!technician_id) {
                throw new LoiNghiepVu('THIEU_MA_KTV', 'Thiếu mã kỹ thuật viên (technician_id)', 400);
            }
            const updated = ticketService.assignTechnician(req.params.id, technician_id, user_id, note);
            res.status(200).json({
                success: true,
                message: 'Phân công kỹ thuật viên thành công',
                data: updated
            });
        } catch (error) {
            next(error);
        }
    }

    // POST /api/v1/tickets/:id/reassign (US6, QT-08)
    reassign(req, res, next) {
        try {
            const { technician_id, reason, note, user_id } = req.body;
            if (!technician_id) {
                throw new LoiNghiepVu('THIEU_MA_KTV', 'Thiếu mã kỹ thuật viên mới (technician_id)', 400);
            }
            const updated = ticketService.reassignTechnician(req.params.id, technician_id, user_id, reason, note);
            res.status(200).json({
                success: true,
                message: 'Chuyển gán kỹ thuật viên thành công',
                data: updated
            });
        } catch (error) {
            next(error);
        }
    }

    // GET /api/v1/technicians (Màn hình M1)
    getTechnicians(req, res, next) {
        try {
            const { center_id } = req.query;
            const list = ticketService.getTechniciansWorkload(center_id);
            res.status(200).json({
                success: true,
                count: list.length,
                data: list
            });
        } catch (error) {
            next(error);
        }
    }

    // GET /api/v1/tickets/:id/appointments (Màn hình M3)
    getAppointments(req, res, next) {
        try {
            const appointments = ticketService.getAppointments(req.params.id);
            res.status(200).json({
                success: true,
                count: appointments.length,
                data: appointments
            });
        } catch (error) {
            next(error);
        }
    }

    // POST /api/v1/tickets/:id/appointments (Màn hình M3, QT-09)
    createAppointment(req, res, next) {
        try {
            const appointment = ticketService.createAppointment(req.params.id, req.body);
            res.status(201).json({
                success: true,
                message: 'Đặt lịch hẹn giao nhận thành công',
                data: appointment
            });
        } catch (error) {
            next(error);
        }
    }

    // GET /api/v1/tickets/:id/logs (Audit Log)
    getLogs(req, res, next) {
        try {
            const logs = ticketService.getStatusLogs(req.params.id);
            res.status(200).json({
                success: true,
                count: logs.length,
                data: logs
            });
        } catch (error) {
            next(error);
        }
    }
}

module.exports = new TicketController();
