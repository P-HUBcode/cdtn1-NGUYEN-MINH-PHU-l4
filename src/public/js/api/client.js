/**
 * src/public/js/api/client.js
 * Frontend HTTP Client đóng gói fetch, tự động đính token và bắt lỗi 401.
 * Cập nhật Buổi 11: Nhận diện cấu trúc phản hồi lỗi chuẩn { error, message, requestId }
 */

const BASE_URL = `${window.location.origin}/api/v1`;

async function request(endpoint, options = {}) {
    const url = endpoint.startsWith('http') ? endpoint : `${BASE_URL}${endpoint}`;
    
    const headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        ...(options.headers || {})
    };

    const token = localStorage.getItem('token');
    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }

    const userStr = localStorage.getItem('user');
    if (userStr) {
        try {
            const u = JSON.parse(userStr);
            if (u.role) headers['X-User-Role'] = u.role;
            if (u.technicianId) headers['X-Technician-Id'] = u.technicianId;
        } catch (e) {
            console.warn('Dữ liệu user trong localStorage không hợp lệ, đang làm sạch:', e.message);
            localStorage.removeItem('user');
        }
    }

    // Cơ chế Timeout (Slide 25 Buổi 11: Ngăn chặn treo dịch vụ vô hạn)
    const timeoutMs = options.timeout || 10000;
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), timeoutMs);

    try {
        const response = await fetch(url, {
            ...options,
            headers,
            signal: options.signal || controller.signal
        });
        clearTimeout(timeoutId);

        // Xử lý mã lỗi 401: Xóa token và tự động chuyển về trạng thái đăng nhập
        if (response.status === 401) {
            localStorage.removeItem('token');
            localStorage.removeItem('user');
            if (window.handleAuthError) {
                window.handleAuthError();
            }
            const errData = await response.json().catch(() => ({}));
            const msg = errData.message || errData.error?.message || 'Phiên làm việc hết hạn (401). Đã tự động đăng xuất.';
            const error = new Error(msg);
            error.statusCode = 401;
            throw error;
        }

        const data = await response.json().catch(() => ({}));

        if (!response.ok) {
            const msg = data.message || (typeof data.error === 'object' ? data.error?.message : data.error) || `Lỗi máy chủ (${response.status})`;
            const error = new Error(msg);
            error.statusCode = response.status;
            error.data = data;
            error.requestId = data.requestId;
            throw error;
        }

        return data;
    } catch (networkError) {
        clearTimeout(timeoutId);
        if (networkError.name === 'AbortError') {
            const error = new Error(`Quá thời gian chờ phản hồi từ máy chủ (Timeout sau ${timeoutMs / 1000}s). Vui lòng thử lại.`);
            error.isTimeout = true;
            throw error;
        }
        if (networkError.statusCode) throw networkError;
        const error = new Error('Không thể kết nối đến máy chủ Backend (Connection refused). Vui lòng khởi động lại server hoặc kiểm tra mạng.');
        error.isNetworkError = true;
        throw error;
    }
}

const apiClient = {
    get: (endpoint, options = {}) => request(endpoint, { ...options, method: 'GET' }),
    post: (endpoint, body, options = {}) => request(endpoint, { ...options, method: 'POST', body: JSON.stringify(body) }),
    put: (endpoint, body, options = {}) => request(endpoint, { ...options, method: 'PUT', body: JSON.stringify(body) }),
    delete: (endpoint, options = {}) => request(endpoint, { ...options, method: 'DELETE' }),
    request
};

window.apiClient = apiClient;
