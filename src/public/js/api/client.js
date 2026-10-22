/**
 * src/public/js/api/client.js
 * Frontend HTTP Client đóng gói fetch, tự động đính token và bắt lỗi 401.
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

    try {
        const response = await fetch(url, {
            ...options,
            headers
        });

        // Xử lý mã lỗi 401: Xóa token và tự động chuyển về trạng thái đăng nhập
        if (response.status === 401) {
            localStorage.removeItem('token');
            localStorage.removeItem('user');
            if (window.handleAuthError) {
                window.handleAuthError();
            }
            const errData = await response.json().catch(() => ({}));
            const error = new Error(errData.error?.message || 'Phiên làm việc hết hạn (401). Đã tự động đăng xuất.');
            error.statusCode = 401;
            throw error;
        }

        const data = await response.json().catch(() => ({}));

        if (!response.ok) {
            const error = new Error(data.error?.message || `Lỗi máy chủ (${response.status})`);
            error.statusCode = response.status;
            error.data = data;
            throw error;
        }

        return data;
    } catch (networkError) {
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
