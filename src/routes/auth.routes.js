const express = require('express');
const router = express.Router();
const { DEMO_ACCOUNTS, DEMO_TOKEN, verifyPassword } = require('../middleware/auth');
const logger = require('../utils/logger').child('AuthRoutes');
const { LoiNghiepVu } = require('../errors');

// POST /api/v1/auth/login
router.post('/login', (req, res, next) => {
    try {
        const { username, password } = req.body;
        const account = DEMO_ACCOUNTS[username];

        if (account && verifyPassword(password, account.passwordHash, account.salt)) {
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
                    technicianId: account.technicianId || null,
                    technicianName: account.technicianName || null,
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

// GET /api/v1/auth/accounts
router.get('/accounts', (req, res) => {
    const list = Object.entries(DEMO_ACCOUNTS).map(([username, info]) => ({
        username,
        fullName: info.fullName,
        role: info.role,
        description: info.description
    }));
    res.json({ success: true, count: list.length, data: list });
});

module.exports = router;
