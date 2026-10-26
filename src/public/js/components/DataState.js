/**
 * src/public/js/components/DataState.js
 * Thành phần bao đóng 3 trạng thái dữ liệu (DataState):
 * 1. Đang tải (Loading)
 * 2. Dữ liệu rỗng (Empty)
 * 3. Lỗi kết nối (Error kèm nút "Thử lại")
 */

const DataState = {
    _retryCounts: {},

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
        this.resetRetryCount(containerId);
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

    // Xử lý lỗi theo chuẩn Buổi 11 (Slide 25): Giới hạn thử lại <= 3 lần, có giãn cách
    renderError(containerId, errorMessage, retryCallback) {
        const el = document.getElementById(containerId);
        if (!el) return;
        
        const count = (this._retryCounts[containerId] || 0) + 1;
        this._retryCounts[containerId] = count;
        const maxRetries = 3;
        const isExceeded = count > maxRetries;
        
        const retryBtnId = `btn-retry-${Math.random().toString(36).substring(2, 9)}`;
        
        el.innerHTML = `
            <div class="datastate-box datastate-error">
                <div class="icon-error">⚠️</div>
                <h4 class="datastate-title">Đã xảy ra lỗi kết nối</h4>
                <p class="datastate-text text-danger">${errorMessage || 'Không thể lấy dữ liệu từ máy chủ backend'}</p>
                ${!isExceeded 
                    ? `<button id="${retryBtnId}" class="btn btn-primary btn-retry">
                           🔄 Thử lại ngay (Lần ${count}/${maxRetries})
                       </button>`
                    : `<p style="font-size: 12px; color: #DC2626; font-style: italic; margin-bottom: 8px;">
                           Đã thử lại tối đa ${maxRetries} lần thất bại. Vui lòng kiểm tra lại dịch vụ Backend.
                       </p>
                       <button id="${retryBtnId}" class="btn btn-outline btn-sm">
                           ⚡ Đặt lại bộ đếm & Thử lại
                       </button>`
                }
            </div>
        `;

        if (typeof retryCallback === 'function') {
            document.getElementById(retryBtnId)?.addEventListener('click', () => {
                if (isExceeded) {
                    this._retryCounts[containerId] = 0;
                }
                DataState.renderLoading(containerId, 'Đang thử kết nối lại...');
                setTimeout(retryCallback, 500); // Giãn cách 500ms
            });
        }
    },

    resetRetryCount(containerId) {
        if (containerId) delete this._retryCounts[containerId];
        else this._retryCounts = {};
    }
};

window.DataState = DataState;
