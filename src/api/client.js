/**
 * src/api/client.js
 * HTTP Client tập trung theo yêu cầu Buổi 10 (Sprint 2 - Track SE).
 * Đóng gói toàn bộ cấu hình mạng, thêm header Authorization và tự động xử lý mã lỗi 401.
 */

const BASE_URL = typeof window !== 'undefined' && window.location 
    ? `${window.location.origin}/api/v1` 
    : (process.env.API_BASE_URL || 'http://localhost:3000/api/v1');

async function request(endpoint, options = {}) {
    const url = endpoint.startsWith('http') ? endpoint : `${BASE_URL}${endpoint}`;
    
    const headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        ...(options.headers || {})
    };

    // Tự động gắn Token nếu có trong localStorage (trình duyệt)
    if (typeof localStorage !== 'undefined') {
        const token = localStorage.getItem('token');
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }
    }

    try {
        const response = await fetch(url, {
            ...options,
            headers
        });

        // Xử lý mã lỗi 401: Xóa token và tự động chuyển về trang Đăng nhập
        if (response.status === 401) {
            if (typeof localStorage !== 'undefined') {
                localStorage.removeItem('token');
                localStorage.removeItem('user');
            }
            if (typeof window !== 'undefined' && window.handleAuthError) {
                window.handleAuthError();
            }
            const errData = await response.json().catch(() => ({}));
            const error = new Error(errData.error?.message || 'Phiên làm việc hết hạn (401). Vui lòng đăng nhập lại.');
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
        const error = new Error('Không thể kết nối đến máy chủ Backend (Connection refused). Vui lòng kiểm tra lại dịch vụ.');
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

if (typeof module !== 'undefined' && module.exports) {
    module.exports = apiClient;
}
if (typeof window !== 'undefined') {
    window.apiClient = apiClient;
}
