require('dotenv').config();
const express = require('express');
const { initDatabase } = require('./config/database');
const ticketController = require('./presentation/controllers/ticketController');

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware parsing JSON
app.use(express.json());

// Khởi tạo Database và Seed data
initDatabase();

// Routes cho Entity Tickets
app.get('/api/v1/tickets', (req, res, next) => ticketController.getAll(req, res, next));
app.get('/api/v1/tickets/:id', (req, res, next) => ticketController.getById(req, res, next));
app.post('/api/v1/tickets', (req, res, next) => ticketController.create(req, res, next));
app.get('/api/v1/tickets/:id/recommend-technicians', (req, res, next) => ticketController.getRecommended(req, res, next));
app.post('/api/v1/tickets/:id/assign', (req, res, next) => ticketController.assign(req, res, next));

// Root route
app.get('/', (req, res) => {
    res.json({
        name: 'Smart CRM Warranty Hub API - Luồng L4',
        version: '1.0.0',
        author: 'Nguyễn Minh Phú - 2374802013447',
        status: 'UP'
    });
});

// Centralized Error Handling Middleware
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
