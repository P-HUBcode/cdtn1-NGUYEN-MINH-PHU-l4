/**
 * src/public/js/app.js
 * Điều phối giao diện người dùng cho Luồng L4.
 * TUYỆT ĐỐI KHÔNG chứa lệnh "fetch(" trực tiếp, toàn bộ gọi qua window.ticketApi.
 */

document.addEventListener('DOMContentLoaded', () => {
    let currentTicketId = null;
    let selectedTechnicianId = null;
    let isReassignMode = false;
    let cachedTickets = [];

    // =========================================================================
    // 1. QUẢN LÝ XÁC THỰC VÀ SỰ KIỆN 401
    // =========================================================================
    function updateAuthUI() {
        const token = localStorage.getItem('token');
        const userJson = localStorage.getItem('user');
        const userDisplay = document.getElementById('user-display');
        const loginBtn = document.getElementById('btn-login-modal');

        if (token && userJson) {
            try {
                const user = JSON.parse(userJson);
                userDisplay.innerHTML = `👤 <strong>${user.fullName}</strong>`;
                loginBtn.textContent = 'Đăng xuất';
                loginBtn.classList.remove('btn-outline');
                loginBtn.classList.add('btn-danger');
            } catch (e) {
                clearAuth();
            }
        } else {
            userDisplay.textContent = '👤 Chưa đăng nhập';
            loginBtn.textContent = 'Đăng nhập';
            loginBtn.classList.add('btn-outline');
            loginBtn.classList.remove('btn-danger');
        }
    }

    function clearAuth() {
        localStorage.removeItem('token');
        localStorage.removeItem('user');
        updateAuthUI();
    }

    window.handleAuthError = function() {
        updateAuthUI();
        alert('Phiên làm việc của bạn đã hết hạn (Mã lỗi 401). Vui lòng đăng nhập lại.');
        document.getElementById('modal-login').classList.add('active');
    };

    document.getElementById('btn-login-modal')?.addEventListener('click', () => {
        if (localStorage.getItem('token')) {
            clearAuth();
            alert('Đã đăng xuất khỏi hệ thống.');
        } else {
            document.getElementById('modal-login').classList.add('active');
        }
    });

    document.getElementById('btn-close-login')?.addEventListener('click', () => {
        document.getElementById('modal-login').classList.remove('active');
    });

    document.querySelectorAll('.btn-quick-account').forEach(btn => {
        btn.addEventListener('click', (e) => {
            const u = e.currentTarget.getAttribute('data-user');
            document.getElementById('login-username').value = u;
            document.getElementById('login-password').value = '123456';
        });
    });

    document.getElementById('form-login')?.addEventListener('submit', async (e) => {
        e.preventDefault();
        const u = document.getElementById('login-username').value;
        const p = document.getElementById('login-password').value;
        const errMsg = document.getElementById('login-error-msg');
        errMsg.style.display = 'none';

        try {
            const res = await window.ticketApi.login(u, p);
            localStorage.setItem('token', res.token);
            localStorage.setItem('user', JSON.stringify(res.user));
            updateAuthUI();
            document.getElementById('modal-login').classList.remove('active');
            alert(`Đăng nhập thành công! Xin chào ${res.user.fullName}`);
            loadM1Tickets();
        } catch (err) {
            errMsg.textContent = err.message;
            errMsg.style.display = 'block';
        }
    });

    // Nút Thử mã 401 (Kiểm thử theo slide 4)
    document.getElementById('btn-test-401')?.addEventListener('click', async () => {
        try {
            await window.ticketApi.triggerTest401();
        } catch (err) {
            console.log('Test 401 caught:', err.message);
        }
    });

    // =========================================================================
    // 2. CHUYỂN TAB GIAO DIỆN (M1, M2, M3)
    // =========================================================================
    document.querySelectorAll('.nav-tab').forEach(tab => {
        tab.addEventListener('click', () => {
            document.querySelectorAll('.nav-tab').forEach(t => t.classList.remove('active'));
            document.querySelectorAll('.screen-section').forEach(s => s.classList.remove('active'));

            tab.classList.add('active');
            const targetId = tab.getAttribute('data-tab');
            document.getElementById(targetId)?.classList.add('active');

            if (targetId === 'screen-m1') {
                loadM1Tickets();
                loadM1TechniciansWorkload();
            } else if (targetId === 'screen-m3') {
                populateM3TicketSelect();
            }
        });
    });

    // =========================================================================
    // 3. MÀN HÌNH M1: D/S PHIẾU CHỜ & TẢI KTV
    // =========================================================================
    async function loadM1Tickets() {
        const containerId = 'm1-tickets-container';
        window.DataState.renderLoading(containerId, 'Đang tải danh sách phiếu bảo hành...');

        const centerId = document.getElementById('m1-center-filter')?.value || '';
        const status = document.getElementById('m1-status-filter')?.value || '';
        const params = {};
        if (centerId) params.center_id = centerId;
        if (status) params.status = status;

        try {
            const res = await window.ticketApi.getTickets(params);
            cachedTickets = res.data || [];
            updateM2QuickTicketSelect(cachedTickets);

            if (!cachedTickets || cachedTickets.length === 0) {
                window.DataState.renderEmpty(containerId, 'Không có phiếu bảo hành nào thỏa mãn điều kiện lọc. Bạn có thể bấm "➕ Tiếp nhận phiếu mới" hoặc "⚡ Khôi phục mẫu MOI".');
                return;
            }

            let html = `
                <table class="data-table">
                    <thead>
                        <tr>
                            <th>MÃ PHIẾU</th>
                            <th>KHÁCH HÀNG / SĐT</th>
                            <th>SỰ CỐ & MỨC ƯU TIÊN</th>
                            <th>TRUNG TÂM</th>
                            <th>TRẠNG THÁI</th>
                            <th>HẠN SLA (QT-04)</th>
                            <th>THAO TÁC</th>
                        </tr>
                    </thead>
                    <tbody>
            `;

            cachedTickets.forEach(t => {
                const badgeClass = t.priority === 'CAO' ? 'badge-cao' : (t.priority === 'THAP' ? 'badge-thap' : 'badge-tb');
                const statusClass = t.status === 'MOI' ? 'badge-moi' : (t.status === 'DANG_XU_LY' ? 'badge-dangxuly' : 'badge-hoantat');
                const dueText = new Date(t.due_date).toLocaleString('vi-VN');
                html += `
                    <tr>
                        <td><strong>#${t.ticket_code}</strong></td>
                        <td>${t.customer_name}<br><small style="color: #666;">📞 ${t.customer_phone}</small></td>
                        <td>
                            <span class="badge ${badgeClass}">${t.priority}</span> — <strong>${t.issue_category}</strong>
                            <div style="font-size: 11.5px; color: #555;">${t.issue_desc}</div>
                        </td>
                        <td>${t.center_name}</td>
                        <td><span class="badge ${statusClass}">${t.status}</span></td>
                        <td><span style="color: var(--primary); font-weight: 600;">${dueText}</span></td>
                        <td>
                            <button class="btn btn-primary btn-sm btn-select-ticket" data-id="${t.ticket_id}">
                                ⚡ Gợi ý KTV (M2)
                            </button>
                        </td>
                    </tr>
                `;
            });

            html += `</tbody></table>`;
            document.getElementById(containerId).innerHTML = html;

            // Gắn sự kiện chọn phiếu chuyển sang M2
            document.querySelectorAll('.btn-select-ticket').forEach(btn => {
                btn.addEventListener('click', (e) => {
                    const id = e.currentTarget.getAttribute('data-id');
                    selectTicketForM2(id);
                });
            });

        } catch (err) {
            window.DataState.renderError(containerId, err.message, loadM1Tickets);
        }
    }

    async function loadM1TechniciansWorkload() {
        const containerId = 'm1-workload-container';
        window.DataState.renderLoading(containerId, 'Đang tải thông tin tải công việc kỹ thuật viên...');

        const centerId = document.getElementById('m1-center-filter').value;
        try {
            const res = await window.ticketApi.getTechniciansWorkload(centerId);
            const techs = res.data || [];

            if (techs.length === 0) {
                window.DataState.renderEmpty(containerId, 'Chưa có kỹ thuật viên nào trong trung tâm này.');
                return;
            }

            let html = `
                <table class="data-table">
                    <thead>
                        <tr>
                            <th>KỸ THUẬT VIÊN</th>
                            <th>TRUNG TÂM</th>
                            <th>TRẠNG THÁI</th>
                            <th>SỐ PHIẾU ĐANG GIỮ</th>
                            <th>KỸ NĂNG CHUYÊN MÔN</th>
                        </tr>
                    </thead>
                    <tbody>
            `;

            techs.forEach(tech => {
                const isBusy = tech.active_tickets >= 3;
                html += `
                    <tr>
                        <td><strong>${tech.full_name}</strong> (${tech.technician_code})</td>
                        <td>${tech.center_name}</td>
                        <td>
                            <span class="badge ${tech.status === 'HOAT_DONG' ? 'badge-hoantat' : 'badge-cao'}">
                                ${tech.status}
                            </span>
                        </td>
                        <td>
                            <strong style="color: ${isBusy ? 'var(--danger)' : 'var(--accent)'};">
                                ${tech.active_tickets} phiếu
                            </strong>
                        </td>
                        <td><small>${tech.skills || 'Chưa cập nhật'}</small></td>
                    </tr>
                `;
            });

            html += `</tbody></table>`;
            document.getElementById(containerId).innerHTML = html;
        } catch (err) {
            window.DataState.renderError(containerId, err.message, loadM1TechniciansWorkload);
        }
    }

    document.getElementById('m1-btn-refresh')?.addEventListener('click', () => {
        loadM1Tickets();
        loadM1TechniciansWorkload();
    });

    document.getElementById('m1-center-filter')?.addEventListener('change', () => {
        loadM1Tickets();
        loadM1TechniciansWorkload();
    });

    // =========================================================================
    // 4. MÀN HÌNH M2: CHI TIẾT & GỢI Ý KTV & RE-ASSIGN
    // =========================================================================
    async function selectTicketForM2(ticketId) {
        currentTicketId = ticketId;
        selectedTechnicianId = null;

        // Chuyển sang Tab M2
        document.querySelectorAll('.nav-tab').forEach(t => t.classList.remove('active'));
        document.querySelectorAll('.screen-section').forEach(s => s.classList.remove('active'));
        document.querySelector('[data-tab="screen-m2"]')?.classList.add('active');
        document.getElementById('screen-m2')?.classList.add('active');

        await loadM2TicketDetail(ticketId);
        await loadM2RecommendedTechnicians(ticketId);
        await loadM2StatusLogs(ticketId);
    }

    async function loadM2TicketDetail(ticketId) {
        const container = document.getElementById('m2-ticket-detail-container');
        container.innerHTML = `<div class="datastate-box datastate-loading"><div class="spinner"></div><p>Đang tải chi tiết phiếu...</p></div>`;

        try {
            const res = await window.ticketApi.getTicketById(ticketId);
            const t = res.data;

            const badgeClass = t.priority === 'CAO' ? 'badge-cao' : (t.priority === 'THAP' ? 'badge-thap' : 'badge-tb');
            container.innerHTML = `
                <div style="font-size: 13.5px; line-height: 1.8;">
                    <p><strong>Mã phiếu:</strong> <span style="color: var(--primary); font-weight: 700;">#${t.ticket_code}</span></p>
                    <p><strong>Khách hàng:</strong> ${t.customer_name} — 📞 <strong>${t.customer_phone}</strong> (Từ bảng customers - TD-05)</p>
                    <p><strong>Trung tâm:</strong> ${t.center_name}</p>
                    <p><strong>Sự cố:</strong> <span class="badge ${badgeClass}">${t.priority}</span> ${t.issue_category}</p>
                    <p><strong>Mô tả lỗi:</strong> ${t.issue_desc}</p>
                    <p><strong>KTV hiện phụ trách:</strong> ${t.technician_name ? `<strong>${t.technician_name}</strong>` : '<span style="color: #999;">Chưa gán</span>'}</p>
                    <p><strong>Hạn cam kết SLA (QT-04):</strong> <span style="color: var(--danger); font-weight: 700;">${new Date(t.due_date).toLocaleString('vi-VN')}</span></p>
                    <p><strong>Trạng thái:</strong> <span class="badge badge-moi">${t.status}</span></p>
                </div>
            `;
        } catch (err) {
            container.innerHTML = `<div class="alert alert-danger">${err.message}</div>`;
        }
    }

    async function loadM2RecommendedTechnicians(ticketId) {
        const containerId = 'm2-recommend-container';
        window.DataState.renderLoading(containerId, 'Đang phân tích kỹ năng và tải công việc KTV...');

        try {
            const res = await window.ticketApi.getRecommendedTechnicians(ticketId);
            const techs = res.data || [];

            if (techs.length === 0) {
                window.DataState.renderEmpty(containerId, 'Không tìm thấy KTV nào trong cùng trung tâm có trình độ tay nghề >= 3 cho loại sự cố này.');
                document.getElementById('m2-assign-actions').style.display = 'none';
                return;
            }

            let html = `
                <table class="data-table">
                    <thead>
                        <tr>
                            <th width="40">CHỌN</th>
                            <th>KỸ THUẬT VIÊN</th>
                            <th>TAY NGHỀ (QT-07)</th>
                            <th>TẢI HIỆN TẠI</th>
                        </tr>
                    </thead>
                    <tbody>
            `;

            techs.forEach((tech, idx) => {
                const checked = idx === 0 ? 'checked' : '';
                if (idx === 0) selectedTechnicianId = tech.technician_id;

                html += `
                    <tr>
                        <td>
                            <input type="radio" name="tech-radio" value="${tech.technician_id}" ${checked}>
                        </td>
                        <td><strong>${tech.full_name}</strong> (${tech.technician_code})</td>
                        <td><span class="badge badge-hoantat">⭐ ${tech.proficiency} / 5</span></td>
                        <td>${tech.active_tickets} phiếu đang xử lý</td>
                    </tr>
                `;
            });

            html += `</tbody></table>`;
            document.getElementById(containerId).innerHTML = html;
            document.getElementById('m2-assign-actions').style.display = 'block';

            // Sự kiện chọn radio KTV
            document.querySelectorAll('input[name="tech-radio"]').forEach(radio => {
                radio.addEventListener('change', (e) => {
                    selectedTechnicianId = e.target.value;
                });
            });

        } catch (err) {
            window.DataState.renderError(containerId, err.message, () => loadM2RecommendedTechnicians(ticketId));
        }
    }

    async function loadM2StatusLogs(ticketId) {
        const container = document.getElementById('m2-logs-container');
        try {
            const res = await window.ticketApi.getStatusLogs(ticketId);
            const logs = res.data || [];

            if (logs.length === 0) {
                container.innerHTML = `<p style="color: #888; font-style: italic;">Chưa có nhật ký thay đổi trạng thái nào.</p>`;
                return;
            }

            let html = `<ul style="padding-left: 20px; line-height: 1.8;">`;
            logs.forEach(l => {
                const time = new Date(l.changed_at).toLocaleString('vi-VN');
                html += `
                    <li>
                        <strong>[${time}]</strong> Chuyển từ <code>${l.from_status || 'GỐC'}</code> &rarr; <code>${l.to_status}</code>:
                        <em>${l.reason || 'N/A'}</em> ${l.note ? `(Ghi chú: ${l.note})` : ''}
                    </li>
                `;
            });
            html += `</ul>`;
            container.innerHTML = html;
        } catch (e) {
            container.innerHTML = `<p class="text-danger">Không tải được nhật ký log.</p>`;
        }
    }

    // Toggle Re-assign Mode
    document.getElementById('btn-toggle-reassign')?.addEventListener('click', () => {
        isReassignMode = !isReassignMode;
        const reasonBox = document.getElementById('reassign-reason-box');
        const submitBtn = document.getElementById('btn-submit-assign');
        const toggleBtn = document.getElementById('btn-toggle-reassign');

        if (isReassignMode) {
            reasonBox.style.display = 'block';
            submitBtn.textContent = '🔄 Xác nhận chuyển gán (Re-assign)';
            submitBtn.classList.remove('btn-success');
            submitBtn.classList.add('btn-primary');
            toggleBtn.textContent = 'Quay về Phân công thường';
        } else {
            reasonBox.style.display = 'none';
            submitBtn.textContent = '✅ Xác nhận phân công';
            submitBtn.classList.add('btn-success');
            submitBtn.classList.remove('btn-primary');
            toggleBtn.textContent = '🔄 Đổi sang Chuyển gán (Re-assign)';
        }
    });

    // Thực hiện Phân công hoặc Re-assign
    document.getElementById('btn-submit-assign')?.addEventListener('click', async () => {
        if (!currentTicketId || !selectedTechnicianId) {
            alert('Vui lòng chọn kỹ thuật viên để phân công.');
            return;
        }

        const note = document.getElementById('assign-note-input').value;
        const reason = document.getElementById('reassign-reason-input').value;

        try {
            if (isReassignMode) {
                // Kiểm tra nghiệp vụ QT-08: Tối thiểu 10 ký tự
                if (!reason || reason.trim().length < 10) {
                    alert('Quy tắc QT-08: Lý do chuyển gán phiếu bắt buộc phải có tối thiểu 10 ký tự!');
                    return;
                }
                await window.ticketApi.reassignTechnician(currentTicketId, {
                    technician_id: selectedTechnicianId,
                    reason: reason.trim(),
                    note: note
                });
                alert('Chuyển gán KTV thành công!');
            } else {
                await window.ticketApi.assignTechnician(currentTicketId, {
                    technician_id: selectedTechnicianId,
                    note: note
                });
                alert('Phân công KTV thành công!');
            }

            // Làm mới lại dữ liệu M2 và M1
            loadM2TicketDetail(currentTicketId);
            loadM2RecommendedTechnicians(currentTicketId);
            loadM2StatusLogs(currentTicketId);
        } catch (err) {
            alert(`Lỗi: ${err.message}`);
        }
    });

    // =========================================================================
    // 5. MÀN HÌNH M3: TIẾP NHẬN ĐẶT & DỜI LỊCH HẸN (US3, QT-09)
    // =========================================================================
    async function populateM3TicketSelect() {
        const select = document.getElementById('m3-ticket-select');
        select.innerHTML = '<option value="">-- Đang tải danh sách phiếu... --</option>';

        try {
            const res = await window.ticketApi.getTickets();
            const tickets = res.data || [];

            select.innerHTML = '<option value="">-- Chọn phiếu bảo hành --</option>';
            tickets.forEach(t => {
                const opt = document.createElement('option');
                opt.value = t.ticket_id;
                opt.textContent = `#${t.ticket_code} — ${t.customer_name} (${t.issue_category})`;
                if (currentTicketId && String(t.ticket_id) === String(currentTicketId)) {
                    opt.selected = true;
                }
                select.appendChild(opt);
            });

            if (select.value) {
                loadM3Appointments(select.value);
            }
        } catch (err) {
            select.innerHTML = '<option value="">Lỗi tải danh sách phiếu</option>';
        }
    }

    async function loadM3Appointments(ticketId) {
        const container = document.getElementById('m3-appointments-container');
        container.innerHTML = `<div class="datastate-box datastate-loading"><div class="spinner"></div><p>Đang tải lịch hẹn...</p></div>`;

        try {
            const res = await window.ticketApi.getAppointments(ticketId);
            const appts = res.data || [];

            if (appts.length === 0) {
                container.innerHTML = `<div class="alert alert-warning">Phiếu này hiện chưa có lịch hẹn nào.</div>`;
                return;
            }

            let html = `
                <table class="data-table">
                    <thead>
                        <tr>
                            <th>LOẠI LỊCH</th>
                            <th>THỜI GIAN HẸN</th>
                            <th>TRẠNG THÁI</th>
                            <th>GHI CHÚ</th>
                        </tr>
                    </thead>
                    <tbody>
            `;

            appts.forEach(a => {
                const typeText = a.appointment_type === 'NHAN_MAY' ? '📥 Tiếp nhận máy' : '📤 Trả giao máy';
                html += `
                    <tr>
                        <td><strong>${typeText}</strong></td>
                        <td>${new Date(a.appointment_date).toLocaleString('vi-VN')}</td>
                        <td><span class="badge badge-hoantat">${a.status}</span></td>
                        <td>${a.notes || '—'}</td>
                    </tr>
                `;
            });

            html += `</tbody></table>`;
            container.innerHTML = html;
        } catch (err) {
            container.innerHTML = `<div class="alert alert-danger">${err.message}</div>`;
        }
    }

    document.getElementById('m3-ticket-select')?.addEventListener('change', (e) => {
        if (e.target.value) {
            loadM3Appointments(e.target.value);
        }
    });

    document.getElementById('form-appointment')?.addEventListener('submit', async (e) => {
        e.preventDefault();
        const ticketId = document.getElementById('m3-ticket-select').value;
        const apptType = document.querySelector('input[name="m3-type"]:checked').value;
        const apptDate = document.getElementById('m3-datetime-input').value;
        const notes = document.getElementById('m3-notes-input').value;
        const alertBox = document.getElementById('m3-feedback-alert');

        if (!ticketId) {
            alert('Vui lòng chọn một phiếu bảo hành.');
            return;
        }

        try {
            alertBox.style.display = 'none';
            await window.ticketApi.createAppointment(ticketId, {
                appointment_type: apptType,
                appointment_date: new Date(apptDate).toISOString(),
                notes: notes
            });

            alertBox.className = 'alert alert-success';
            alertBox.textContent = '✅ Đặt lịch hẹn thành công (thỏa mãn quy tắc QT-09)!';
            alertBox.style.display = 'block';

            loadM3Appointments(ticketId);
        } catch (err) {
            alertBox.className = 'alert alert-danger';
            alertBox.textContent = `❌ ${err.message}`;
            alertBox.style.display = 'block';
        }
    });

    // =========================================================================
    // 6. CÁC TIỆN ÍCH TẠO PHIẾU & KHÔI PHỤC MẪU
    // =========================================================================
    function updateM2QuickTicketSelect(tickets) {
        const select = document.getElementById('m2-quick-ticket-select');
        if (!select) return;
        select.innerHTML = '<option value="">-- Đổi phiếu xem nhanh --</option>';
        tickets.forEach(t => {
            const opt = document.createElement('option');
            opt.value = t.ticket_id;
            opt.textContent = `#${t.ticket_code} — ${t.customer_name} (${t.status})`;
            if (currentTicketId && String(t.ticket_id) === String(currentTicketId)) {
                opt.selected = true;
            }
            select.appendChild(opt);
        });
    }

    document.getElementById('m2-quick-ticket-select')?.addEventListener('change', (e) => {
        if (e.target.value) {
            selectTicketForM2(e.target.value);
        }
    });

    document.getElementById('m1-status-filter')?.addEventListener('change', () => {
        loadM1Tickets();
    });

    // Nút Khôi phục dữ liệu mẫu MOI
    document.getElementById('btn-reset-demo')?.addEventListener('click', async () => {
        try {
            await window.ticketApi.resetDemoTickets();
            alert('Đã khôi phục thành công các phiếu mẫu về trạng thái MOI!');
            loadM1Tickets();
            loadM1TechniciansWorkload();
        } catch (err) {
            alert(`Lỗi: ${err.message}`);
        }
    });

    // Mở / Đóng Modal Tạo phiếu mới
    document.getElementById('btn-open-create-ticket')?.addEventListener('click', () => {
        document.getElementById('modal-create-ticket')?.classList.add('active');
    });

    document.getElementById('btn-header-create-ticket')?.addEventListener('click', () => {
        document.getElementById('modal-create-ticket')?.classList.add('active');
    });

    document.getElementById('btn-close-create-ticket')?.addEventListener('click', () => {
        document.getElementById('modal-create-ticket')?.classList.remove('active');
    });

    // Chuyển đổi giữa Tự nhập khách hàng mới & Chọn khách có sẵn
    document.querySelectorAll('input[name="customer-mode"]').forEach(radio => {
        radio.addEventListener('change', (e) => {
            const isNew = e.target.value === 'new';
            const boxNew = document.getElementById('box-new-customer');
            const boxExist = document.getElementById('box-existing-customer');
            if (boxNew) boxNew.style.display = isNew ? 'block' : 'none';
            if (boxExist) boxExist.style.display = isNew ? 'none' : 'block';
        });
    });

    // Submit Tạo phiếu mới (Hỗ trợ cả tự gõ khách mới và chọn khách cũ)
    document.getElementById('form-create-ticket')?.addEventListener('submit', async (e) => {
        e.preventDefault();
        const mode = document.querySelector('input[name="customer-mode"]:checked')?.value || 'new';
        const center_id = parseInt(document.getElementById('create-center-id').value, 10);
        const priority = document.getElementById('create-priority').value;
        const issue_category = document.getElementById('create-issue-category').value;
        const issue_desc = document.getElementById('create-issue-desc').value.trim();

        if (issue_desc.length < 10) {
            alert('Mô tả sự cố phải có tối thiểu 10 ký tự!');
            return;
        }

        const payload = {
            center_id,
            priority,
            issue_category,
            issue_desc
        };

        if (mode === 'new') {
            const customer_name = document.getElementById('create-customer-name')?.value.trim() || '';
            const customer_phone = document.getElementById('create-customer-phone')?.value.trim() || '';
            const customer_address = document.getElementById('create-customer-address')?.value.trim() || '';

            if (!customer_name) {
                alert('Vui lòng nhập họ và tên khách hàng!');
                return;
            }
            if (!customer_phone || customer_phone.length < 8) {
                alert('Vui lòng nhập số điện thoại hợp lệ (tối thiểu 8 số)!');
                return;
            }
            payload.customer_name = customer_name;
            payload.customer_phone = customer_phone;
            payload.customer_address = customer_address;
        } else {
            payload.customer_id = parseInt(document.getElementById('create-customer-id').value, 10);
        }

        try {
            const res = await window.ticketApi.createTicket(payload);
            document.getElementById('modal-create-ticket')?.classList.remove('active');
            alert(`🎉 Tạo phiếu bảo hành thành công!\n• Mã phiếu: #${res.data.ticket_code}\n• Khách hàng: ${res.data.customer_name}\n• Hạn SLA (QT-04): ${res.data.due_date}\n• Trạng thái: MOI`);
            document.getElementById('form-create-ticket').reset();
            const boxNew = document.getElementById('box-new-customer');
            const boxExist = document.getElementById('box-existing-customer');
            if (boxNew) boxNew.style.display = 'block';
            if (boxExist) boxExist.style.display = 'none';
            loadM1Tickets();
        } catch (err) {
            alert(`Lỗi khi tạo phiếu: ${err.message}`);
        }
    });

    // =========================================================================
    // KHỞI CHẠY LẦN ĐẦU
    // =========================================================================
    updateAuthUI();
    loadM1Tickets();
    loadM1TechniciansWorkload();
});
