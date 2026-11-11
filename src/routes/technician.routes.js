const express = require('express');
const router = express.Router();
const ticketController = require('../presentation/controllers/ticketController');
const { authenticateToken } = require('../middleware/auth');

router.use(authenticateToken);

// GET /api/v1/technicians (Màn hình M1: Danh sách KTV và tải công việc)
router.get('/', (req, res, next) => ticketController.getTechnicians(req, res, next));

module.exports = router;
