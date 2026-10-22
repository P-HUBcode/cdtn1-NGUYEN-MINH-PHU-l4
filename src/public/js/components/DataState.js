/**
 * src/public/js/components/DataState.js
 * Thành phần bao đóng 3 trạng thái dữ liệu (DataState):
 * 1. Đang tải (Loading)
 * 2. Dữ liệu rỗng (Empty)
 * 3. Lỗi kết nối (Error kèm nút "Thử lại")
 */

const DataState = {
    renderLoading(containerId, message = 'Đang tải dữ liệu từ máy chủ...') {
        const el = document.getElementById(containerId);
        if (!el) return;
        el.innerHTML = `
            <div class="datastate-box datastate-loading">
                <div class="spinner"></div>
                <p class="datastate-text">${message}</p>
            </div>
        `;
    },

    renderEmpty(containerId, message = 'Hiện không có phiếu bảo hành hoặc dữ liệu nào.') {
        const el = document.getElementById(containerId);
        if (!el) return;
        el.innerHTML = `
            <div class="datastate-box datastate-empty">
                <div class="icon-empty">📭</div>
                <h4 class="datastate-title">Danh sách rỗng</h4>
                <p class="datastate-text">${message}</p>
            </div>
        `;
    },

    renderError(containerId, errorMessage, retryCallback) {
        const el = document.getElementById(containerId);
        if (!el) return;
        
        // Tạo unique ID cho nút retry
        const retryBtnId = `btn-retry-${Math.random().toString(36).substring(2, 9)}`;
        
        el.innerHTML = `
            <div class="datastate-box datastate-error">
                <div class="icon-error">⚠️</div>
                <h4 class="datastate-title">Đã xảy ra lỗi kết nối</h4>
                <p class="datastate-text text-danger">${errorMessage || 'Không thể lấy dữ liệu từ máy chủ backend'}</p>
                <button id="${retryBtnId}" class="btn btn-primary btn-retry">
                    🔄 Thử lại ngay
                </button>
            </div>
        `;

        if (typeof retryCallback === 'function') {
            document.getElementById(retryBtnId)?.addEventListener('click', () => {
                DataState.renderLoading(containerId, 'Đang thử kết nối lại...');
                setTimeout(retryCallback, 300);
            });
        }
    }
};

window.DataState = DataState;
