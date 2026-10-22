const ticketService = require('../../services/ticketService');

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
                return res.status(400).json({
                    error: {
                        code: 'VALIDATION_FAILED',
                        message: 'Thiếu mã kỹ thuật viên (technician_id)'
                    }
                });
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
                return res.status(400).json({
                    error: {
                        code: 'VALIDATION_FAILED',
                        message: 'Thiếu mã kỹ thuật viên mới (technician_id)'
                    }
                });
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

    // GET /api/v1/technicians (M1: Tải công việc KTV)
    getTechnicians(req, res, next) {
        try {
            const { center_id } = req.query;
            const techs = ticketService.getTechniciansWorkload(center_id);
            res.status(200).json({
                success: true,
                count: techs.length,
                data: techs
            });
        } catch (error) {
            next(error);
        }
    }

    // GET /api/v1/tickets/:id/appointments (M3: Lịch hẹn)
    getAppointments(req, res, next) {
        try {
            const appts = ticketService.getAppointments(req.params.id);
            res.status(200).json({
                success: true,
                count: appts.length,
                data: appts
            });
        } catch (error) {
            next(error);
        }
    }

    // POST /api/v1/tickets/:id/appointments (M3: Đặt lịch hẹn, QT-09)
    createAppointment(req, res, next) {
        try {
            const appt = ticketService.createAppointment(req.params.id, req.body);
            res.status(201).json({
                success: true,
                message: 'Đặt lịch hẹn thành công',
                data: appt
            });
        } catch (error) {
            next(error);
        }
    }

    // GET /api/v1/tickets/:id/logs
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
