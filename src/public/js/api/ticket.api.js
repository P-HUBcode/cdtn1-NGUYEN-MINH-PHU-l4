/**
 * src/public/js/api/ticket.api.js
 * API Adapter cho Frontend.
 * Đảm bảo mọi màn hình gọi qua đối tượng này, KHÔNG dùng fetch trực tiếp.
 */

const ticketApi = {
    // 1. Đăng nhập hệ thống
    login(username, password) {
        return window.apiClient.post('/auth/login', { username, password });
    },

    // 2. M1: Lấy danh sách phiếu bảo hành
    getTickets(params = {}) {
        const query = new URLSearchParams(params).toString();
        return window.apiClient.get(`/tickets${query ? `?${query}` : ''}`);
    },

    // 3. M1: Lấy danh sách KTV và tải công việc
    getTechniciansWorkload(centerId = '') {
        const query = centerId ? `?center_id=${centerId}` : '';
        return window.apiClient.get(`/technicians${query}`);
    },

    // 4. M2: Xem chi tiết phiếu bảo hành
    getTicketById(ticketId) {
        return window.apiClient.get(`/tickets/${ticketId}`);
    },

    // 5. M2: Lấy danh sách KTV gợi ý (tay nghề >= 3, cùng trung tâm)
    getRecommendedTechnicians(ticketId) {
        return window.apiClient.get(`/tickets/${ticketId}/recommend-technicians`);
    },

    // 6. M2: Phân công kỹ thuật viên (US2, QT-04, QT-07)
    assignTechnician(ticketId, payload) {
        return window.apiClient.post(`/tickets/${ticketId}/assign`, payload);
    },

    // 7. M2: Chuyển gán phiếu (Re-assign) cho KTV khác (US6, QT-08: lý do >= 10 ký tự)
    reassignTechnician(ticketId, payload) {
        return window.apiClient.post(`/tickets/${ticketId}/reassign`, payload);
    },

    // 8. M3: Lấy danh sách lịch hẹn của phiếu
    getAppointments(ticketId) {
        return window.apiClient.get(`/tickets/${ticketId}/appointments`);
    },

    // 9. M3: Đặt lịch hẹn giao - nhận máy (US3, QT-09: kiểm tra slot 30p tối đa 5 lịch)
    createAppointment(ticketId, payload) {
        return window.apiClient.post(`/tickets/${ticketId}/appointments`, payload);
    },

    // 10. Lấy lịch sử chuyển trạng thái
    getStatusLogs(ticketId) {
        return window.apiClient.get(`/tickets/${ticketId}/logs`);
    },

    // 11. Tạo phiếu bảo hành mới (tiếp nhận tạo phiếu)
    createTicket(payload) {
        return window.apiClient.post('/tickets', payload);
    },

    // 12. Khôi phục phiếu mẫu về trạng thái MOI
    resetDemoTickets() {
        return window.apiClient.post('/tickets/reset-demo', {});
    },

    // 13. Endpoint thử nghiệm lỗi 401
    triggerTest401() {
        return window.apiClient.get('/test-401');
    },

    // 14. Kỹ thuật viên & Quản lý cập nhật tiến độ xử lý phiếu bảo hành (FR6, US5)
    updateTicketStatus(ticketId, payload) {
        return window.apiClient.post(`/tickets/${ticketId}/status`, payload);
    }
};

window.ticketApi = ticketApi;
