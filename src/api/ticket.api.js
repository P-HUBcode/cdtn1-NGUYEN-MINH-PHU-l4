/**
 * src/api/ticket.api.js
 * API Adapter cho toàn bộ nghiệp vụ Phiếu Bảo Hành (Luồng L4).
 * TUYỆT ĐỐI không gọi fetch() trực tiếp từ UI/View mà gọi qua tệp này.
 */

const client = (typeof window !== 'undefined' && window.apiClient) 
    ? window.apiClient 
    : require('./client');

const ticketApi = {
    // 1. Đăng nhập hệ thống
    login(username, password) {
        return client.post('/auth/login', { username, password });
    },

    // 2. M1: Lấy danh sách phiếu bảo hành
    getTickets(params = {}) {
        const query = new URLSearchParams(params).toString();
        return client.get(`/tickets${query ? `?${query}` : ''}`);
    },

    // 3. M1: Lấy danh sách KTV và tải công việc
    getTechniciansWorkload(centerId = '') {
        const query = centerId ? `?center_id=${centerId}` : '';
        return client.get(`/technicians${query}`);
    },

    // 4. M2: Xem chi tiết phiếu bảo hành
    getTicketById(ticketId) {
        return client.get(`/tickets/${ticketId}`);
    },

    // 5. M2: Lấy danh sách KTV gợi ý (tay nghề >= 3, cùng trung tâm)
    getRecommendedTechnicians(ticketId) {
        return client.get(`/tickets/${ticketId}/recommend-technicians`);
    },

    // 6. M2: Phân công kỹ thuật viên (US2, QT-04, QT-07)
    assignTechnician(ticketId, payload) {
        return client.post(`/tickets/${ticketId}/assign`, payload);
    },

    // 7. M2: Chuyển gán phiếu (Re-assign) cho KTV khác (US6, QT-08: lý do >= 10 ký tự)
    reassignTechnician(ticketId, payload) {
        return client.post(`/tickets/${ticketId}/reassign`, payload);
    },

    // 8. M3: Lấy danh sách lịch hẹn của phiếu
    getAppointments(ticketId) {
        return client.get(`/tickets/${ticketId}/appointments`);
    },

    // 9. M3: Đặt lịch hẹn giao - nhận máy (US3, QT-09: kiểm tra slot 30p)
    createAppointment(ticketId, payload) {
        return client.post(`/tickets/${ticketId}/appointments`, payload);
    },

    // 10. Lấy lịch sử trạng thái của phiếu
    getStatusLogs(ticketId) {
        return client.get(`/tickets/${ticketId}/logs`);
    },

    // 11. Endpoint mô phỏng lỗi 401 để kiểm thử giao diện
    triggerTest401() {
        return client.get('/test-401');
    }
};

if (typeof module !== 'undefined' && module.exports) {
    module.exports = ticketApi;
}
if (typeof window !== 'undefined') {
    window.ticketApi = ticketApi;
}
