const express = require('express');
const router = express.Router();
const logger = require('../utils/logger').child('TestRoutes');
const { LoiNghiepVu } = require('../errors');

// GET /api/v1/tests/run-all (Thực thi 12 ca kiểm thử phục vụ Live Test Dashboard)
router.get('/run-all', async (req, res, next) => {
    try {
        const { run12Tests } = require('../services/testRunnerService');
        const report = await run12Tests();
        logger.info({ requestId: req.requestId, passed: report.passed, total: report.total }, 'Thực thi bộ 12 ca kiểm thử thành công');
        res.json({ success: true, data: report });
    } catch (err) {
        next(err);
    }
});

// GET /api/v1/test-401 (Mô phỏng phiên hết hạn 401 để kiểm thử giao diện DataState)
router.get('/test-401', (req, res, next) => {
    next(new LoiNghiepVu('UNAUTHORIZED', 'Mô phỏng phiên làm việc hết hạn (401)', 401));
});

module.exports = router;
