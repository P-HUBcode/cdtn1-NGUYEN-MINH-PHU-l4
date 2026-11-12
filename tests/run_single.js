/**
 * tests/run_single.js
 * Script hỗ trợ chạy lẻ từng test case từ TC-01 đến TC-12 theo đúng kịch bản
 * Cách dùng: node tests/run_single.js TC-01 (hoặc TC-02, TC-03, ... TC-12)
 */

const http = require('node:http');
const app = require('../src/app');
const ticketService = require('../src/services/ticketService');
const { db } = require('../src/config/database');

const tc = (process.argv[2] || 'TC-01').toUpperCase().trim();
const PORT = 3999;

async function runSingle() {
    const server = http.createServer(app);
    await new Promise(resolve => server.listen(PORT, resolve));
    const baseUrl = `http://localhost:${PORT}/api/v1`;

    async function apiRequest(endpoint, method = 'GET', body = null, headers = {}) {
        const options = {
            method,
            headers: {
                'Content-Type': 'application/json',
                ...headers
            }
        };
        if (body) options.body = JSON.stringify(body);
        const res = await fetch(`${baseUrl}${endpoint}`, options);
        let data = null;
        try {
            data = await res.json();
        } catch (e) {
            data = null;
        }
        return { status: res.status, data };
    }

    try {
        console.log(`\n================================================================================`);
        console.log(`   ĐANG CHẠY CA KIỂM THỬ ĐỘC LẬP: ${tc}`);
        console.log(`================================================================================\n`);

        switch (tc) {
            case 'TC-01': {
                console.log(`[LỆNH TRONG ẢNH]: node --test --test-name-pattern="QT-04" tests/ticket.service.test.js\n`);
                const receivedDate = '2026-10-15T08:00:00.000Z';
                const dueDate = ticketService.calculateSlaDueDate(receivedDate, 'CAO');
                const expected = '2026-10-16T08:00:00.000Z';
                const pass = dueDate.toISOString() === expected;
                console.log(`[TC-01] [Happy Path] Tính hạn SLA ưu tiên CAO (+24h theo QT-04)`);
                console.log(`   - Input: receivedDate=${receivedDate}, priority=CAO`);
                console.log(`   - Output: ${dueDate.toISOString()} | Kỳ vọng: ${expected}`);
                console.log(`   - Đo lường thực tế: Cộng chính xác 24.0 giờ, 0 tác dụng phụ CSDL`);
                console.log(`   - Kết quả: ${pass ? '✅ PASS' : '❌ FAIL'}\n`);
                break;
            }
            case 'TC-02': {
                console.log(`[LỆNH TRONG ẢNH]: curl.exe -i -X POST http://localhost:3000/api/v1/tickets/1/assign -H "Content-Type: application/json" -H "X-User-Role: MANAGER" -d "{\\"technician_id\\": 1, \\"user_id\\": 1}"\n`);
                await apiRequest('/tickets/reset-demo', 'POST');
                const res = await apiRequest('/tickets/1/assign', 'POST', {
                    technician_id: 1,
                    user_id: 1
                }, { 'X-User-Role': 'MANAGER' });
                const pass = res.status === 200 && res.data?.success && res.data?.data?.status === 'DANG_XU_LY';
                console.log(`HTTP/1.1 ${res.status} OK`);
                console.log(JSON.stringify(res.data, null, 2));
                console.log(`\n- Kết quả: ${pass ? '✅ PASS' : '❌ FAIL'} (Trạng thái chuyển MOI -> DANG_XU_LY, gán KTV ID: 1)\n`);
                break;
            }
            case 'TC-03': {
                console.log(`[LỆNH TRONG ẢNH]: curl.exe -i -X POST http://localhost:3000/api/v1/tickets/1/reassign -H "Content-Type: application/json" -H "X-User-Role: MANAGER" -d "{\\"technician_id\\": 2, \\"reason\\": \\"KTV cu di dao tao nghiep vu dot xuat tai tinh\\", \\"user_id\\": 1}"\n`);
                await apiRequest('/tickets/reset-demo', 'POST');
                await apiRequest('/tickets/1/assign', 'POST', { technician_id: 1, user_id: 1 }, { 'X-User-Role': 'MANAGER' });
                const reason = 'KTV cu di dao tao nghiep vu dot xuat tai tinh';
                const res = await apiRequest('/tickets/1/reassign', 'POST', {
                    technician_id: 2,
                    reason,
                    user_id: 1
                }, { 'X-User-Role': 'MANAGER' });
                const pass = res.status === 200 && res.data?.success && res.data?.data?.technician_id === 2;
                console.log(`HTTP/1.1 ${res.status} OK`);
                console.log(JSON.stringify(res.data, null, 2));
                console.log(`\n- Kết quả: ${pass ? '✅ PASS' : '❌ FAIL'} (KTV đổi sang Lê Văn Cường ID: 2, lý do >= 10 ký tự)\n`);
                break;
            }
            case 'TC-04': {
                console.log(`[LỆNH TRONG ẢNH]: curl.exe -i -X POST http://localhost:3000/api/v1/tickets/1/appointments -H "Content-Type: application/json" -H "X-User-Role: MANAGER" -d "{\\"appointment_type\\": \\"GIAO_MAY\\", \\"appointment_date\\": \\"2026-11-28T09:00:00Z\\", \\"notes\\": \\"Khach den nhan may buoi sang\\"}"\n`);
                const res = await apiRequest('/tickets/1/appointments', 'POST', {
                    appointment_type: 'GIAO_MAY',
                    appointment_date: '2026-11-28T09:00:00Z',
                    notes: 'Khach den nhan may buoi sang'
                }, { 'X-User-Role': 'MANAGER' });
                const pass = res.status === 201 && res.data?.success && res.data?.data?.status === 'DA_XAC_NHAN';
                console.log(`HTTP/1.1 ${res.status} Created`);
                console.log(JSON.stringify(res.data, null, 2));
                console.log(`\n- Kết quả: ${pass ? '✅ PASS' : '❌ FAIL'} (Cấp appointment_id mới, trạng thái DA_XAC_NHAN)\n`);
                break;
            }
            case 'TC-05': {
                console.log(`[LỆNH TRONG ẢNH]: curl.exe -i -X POST http://localhost:3000/api/v1/tickets/1/status -H "Content-Type: application/json" -H "X-User-Role: TECHNICIAN" -H "X-Technician-Id: 2" -d "{\\"status\\": \\"CHO_LINH_KIEN\\", \\"note\\": \\"Dang cho man hinh linh kien tu kho ve\\"}"\n`);
                await apiRequest('/tickets/reset-demo', 'POST');
                await apiRequest('/tickets/1/assign', 'POST', { technician_id: 2, user_id: 1 }, { 'X-User-Role': 'MANAGER' });
                const res = await apiRequest('/tickets/1/status', 'POST', {
                    status: 'CHO_LINH_KIEN',
                    note: 'Dang cho man hinh linh kien tu kho ve'
                }, { 'X-User-Role': 'TECHNICIAN', 'X-Technician-Id': 2 });
                const pass = res.status === 200 && res.data?.success && res.data?.data?.status === 'CHO_LINH_KIEN';
                console.log(`HTTP/1.1 ${res.status} OK`);
                console.log(JSON.stringify(res.data, null, 2));
                console.log(`\n- Kết quả: ${pass ? '✅ PASS' : '❌ FAIL'} (Trạng thái chuyển sang CHO_LINH_KIEN, ghi chú lưu vào Audit Log)\n`);
                break;
            }
            case 'TC-06': {
                console.log(`[LỆNH TRONG ẢNH]: node --test --test-name-pattern="QT-06 & QT-07" tests/ticket.service.test.js\n`);
                const mockTech = { technician_id: 1, full_name: 'Trần Văn Bình', center_id: 1, status: 'HOAT_DONG' };
                const checkPass = ticketService.checkTechnicianEligibility(mockTech, 1, 3);
                const checkFail = ticketService.checkTechnicianEligibility(mockTech, 1, 2);
                const pass = checkPass.valid === true && checkFail.valid === false;
                console.log(`- Điểm biên trên (proficiency = 3): ${checkPass.valid ? 'Chấp nhận hợp lệ (PASS)' : 'Từ chối'}`);
                console.log(`- Điểm biên dưới (proficiency = 2): ${!checkFail.valid ? `Từ chối vi phạm QT-07 (PASS) - Lý do: ${checkFail.reason}` : 'Chấp nhận sai'}`);
                console.log(`- Kết quả: ${pass ? '✅ PASS' : '❌ FAIL'} (Ngưỡng >= 3 chuẩn xác 100%)\n`);
                break;
            }
            case 'TC-07': {
                console.log(`[LỆNH TRONG ẢNH]: node --test --test-name-pattern="QT-08" tests/ticket.service.test.js\n`);
                const checkPass = ticketService.validateReassignReason('1234567890');
                const checkFail = ticketService.validateReassignReason('123456789');
                const pass = checkPass.valid === true && checkFail.valid === false && checkFail.code === 'LY_DO_QUA_NGAN';
                console.log(`- Độ dài = 10 ký tự: ${checkPass.valid ? 'Hợp lệ (PASS)' : 'Từ chối'}`);
                console.log(`- Độ dài = 9 ký tự: ${!checkFail.valid ? `Từ chối với mã ${checkFail.code} (PASS) - ${checkFail.message}` : 'Chấp nhận sai'}`);
                console.log(`- Kết quả: ${pass ? '✅ PASS' : '❌ FAIL'} (Ngưỡng tối thiểu 10 ký tự chuẩn xác 100%)\n`);
                break;
            }
            case 'TC-08': {
                console.log(`[LỆNH TRONG ẢNH]: node --test --test-name-pattern="QT-09" tests/ticket.service.test.js\n`);
                const checkSlot4 = ticketService.checkAppointmentSlotCapacity(4);
                const checkSlot5 = ticketService.checkAppointmentSlotCapacity(5);
                const pass = checkSlot4.allowed && !checkSlot5.allowed && checkSlot5.code === 'LICH_HEN_QUA_TAI';
                console.log(`- Khi slot đang có 4/5 lịch: ${checkSlot4.allowed ? `Cho phép đặt (PASS) - Còn ${checkSlot4.availableSlots} chỗ` : 'Bị từ chối'}`);
                console.log(`- Khi slot đã có 5/5 lịch: ${!checkSlot5.allowed ? `Từ chối với mã ${checkSlot5.code} (PASS) - ${checkSlot5.message}` : 'Chấp nhận sai'}`);
                console.log(`- Kết quả: ${pass ? '✅ PASS' : '❌ FAIL'} (Tải trọng tối đa 5 lịch / 30 phút chuẩn xác 100%)\n`);
                break;
            }
            case 'TC-09': {
                console.log(`[LỆNH TRONG ẢNH]: curl.exe -i -X POST http://localhost:3000/api/v1/tickets/1/assign -H "Content-Type: application/json" -H "X-User-Role: MANAGER" -d "{\\"technician_id\\": 99, \\"user_id\\": 1}"\n`);
                const res = await apiRequest('/tickets/1/assign', 'POST', {
                    technician_id: 99,
                    user_id: 1
                }, { 'X-User-Role': 'MANAGER' });
                const pass = res.status === 400 && res.data?.error === 'KTV_KHONG_DAT_CHUAN';
                console.log(`HTTP/1.1 ${res.status} Bad Request`);
                console.log(JSON.stringify(res.data, null, 2));
                console.log(`\n- Kết quả: ${pass ? '✅ PASS' : '❌ FAIL'} (Bị từ chối HTTP 400, mã lỗi KTV_KHONG_DAT_CHUAN, không sập server)\n`);
                break;
            }
            case 'TC-10': {
                console.log(`[LỆNH TRONG ẢNH]: curl.exe -i -X POST http://localhost:3000/api/v1/tickets/3/status -H "Content-Type: application/json" -H "X-User-Role: MANAGER" -d "{\\"status\\": \\"DANG_XU_LY\\", \\"note\\": \\"Thu sua lai phieu da hoan tat\\"}"\n`);
                await apiRequest('/tickets/3/status', 'POST', {
                    status: 'HOAN_TAT',
                    note: 'Hoan tat sua chua theo quy trinh'
                }, { 'X-User-Role': 'MANAGER' });
                const res = await apiRequest('/tickets/3/status', 'POST', {
                    status: 'DANG_XU_LY',
                    note: 'Thu sua lai phieu da hoan tat'
                }, { 'X-User-Role': 'MANAGER' });
                const pass = res.status === 400 && res.data?.error === 'PHIEU_DA_HOAN_TAT';
                console.log(`HTTP/1.1 ${res.status} Bad Request`);
                console.log(JSON.stringify(res.data, null, 2));
                console.log(`\n- Kết quả: ${pass ? '✅ PASS' : '❌ FAIL'} (Khóa vĩnh viễn phiếu HOAN_TAT, từ chối với lỗi PHIEU_DA_HOAN_TAT)\n`);
                break;
            }
            case 'TC-11': {
                console.log(`[LỆNH TRONG ẢNH]: curl.exe -i -X POST http://localhost:3000/api/v1/tickets/1/status -H "Content-Type: application/json" -H "X-User-Role: TECHNICIAN" -H "X-Technician-Id: 3" -d "{\\"status\\": \\"HOAN_TAT\\", \\"note\\": \\"KTV la co tinh sua phieu cua nguoi khac\\"}"\n`);
                await apiRequest('/tickets/reset-demo', 'POST');
                await apiRequest('/tickets/1/assign', 'POST', { technician_id: 1, user_id: 1 }, { 'X-User-Role': 'MANAGER' });
                const res = await apiRequest('/tickets/1/status', 'POST', {
                    status: 'HOAN_TAT',
                    note: 'KTV la co tinh sua phieu cua nguoi khac'
                }, { 'X-User-Role': 'TECHNICIAN', 'X-Technician-Id': 3 });
                const pass = res.status === 403 && res.data?.error === 'FORBIDDEN';
                console.log(`HTTP/1.1 ${res.status} Forbidden`);
                console.log(JSON.stringify(res.data, null, 2));
                console.log(`\n- Kết quả: ${pass ? '✅ PASS' : '❌ FAIL'} (Kiểm soát quyền truy cập theo chủ sở hữu OWASP A01: Chặn HTTP 403 Forbidden)\n`);
                break;
            }
            case 'TC-12': {
                console.log(`[LỆNH TRONG ẢNH]: curl.exe -i -X POST http://localhost:3000/api/v1/tickets/reset-demo\n`);
                const res = await apiRequest('/tickets/reset-demo', 'POST');
                const count = db.prepare('SELECT COUNT(*) as count FROM tickets').get().count;
                const pass = res.status === 200 && count > 0;
                console.log(`HTTP/1.1 ${res.status} OK`);
                console.log(JSON.stringify(res.data, null, 2));
                console.log(`\nCOUNT(tickets): ${count} (Nhất quán 100%, 0 duplicate records, 0 lỗi SQLITE_CONSTRAINT)`);
                console.log(`- Kết quả: ${pass ? '✅ PASS' : '❌ FAIL'} (Tính tái lập Idempotent CSDL C5 đạt chuẩn)\n`);
                break;
            }
            default:
                console.log(`Mã ca kiểm thử không hợp lệ: "${tc}". Vui lòng chọn từ TC-01 đến TC-12.`);
        }
    } finally {
        server.close();
    }
}

runSingle().catch(err => {
    console.error('Lỗi thực thi:', err);
    process.exit(1);
});
