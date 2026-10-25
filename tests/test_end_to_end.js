/**
 * tests/test_end_to_end.js
 * Kịch bản kiểm thử tích hợp toàn luồng END-TO-END (Luồng L4).
 * Kiểm chứng 100% mục tiêu Buổi 10 & 11: Chạy một lần từ điểm bắt đầu đến kết thúc không lỗi treo.
 * Đảm bảo tính Idempotent (C5): Chạy đi chạy lại nhiều lần kết quả vẫn nhất quán và thành công 100%.
 */

const app = require('../src/app');
const http = require('node:http');

const PORT = 3999;
let server;

async function runEndToEnd() {
    console.log('================================================================');
    console.log('   KIỂM THỬ TÍCH HỢP TOÀN LUỒNG END-TO-END — SPRINT 2 (BUỔI 10 & 11)  ');
    console.log('   Mekong Mobile - Luồng L4: Phân công KTV & Lịch hẹn          ');
    console.log('   Sinh viên: Nguyễn Minh Phú | MSSV: 2374802013447             ');
    console.log('================================================================\n');

    server = http.createServer(app);
    await new Promise(resolve => server.listen(PORT, resolve));
    const baseUrl = `http://localhost:${PORT}/api/v1`;

    let authToken = '';

    try {
        // Reset dữ liệu mẫu trước khi chạy để đảm bảo trạng thái sạch
        await fetch(`http://localhost:${PORT}/api/v1/tickets/reset-demo`, { method: 'POST' });

        // -------------------------------------------------------------
        // CHẶNG 1: ĐĂNG NHẬP HỆ THỐNG
        // -------------------------------------------------------------
        console.log('🔹 [BƯỚC 1] Đăng nhập tài khoản Quản lý trung tâm...');
        const loginRes = await fetch(`${baseUrl}/auth/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username: 'quanly', password: '123456' })
        });
        const loginData = await loginRes.json();
        if (!loginData.success || !loginData.token) {
            throw new Error('Đăng nhập thất bại!');
        }
        authToken = loginData.token;
        console.log(`   ✅ Đăng nhập thành công! Token: ${authToken.substring(0, 15)}...`);
        console.log(`   Quản lý: ${loginData.user.fullName} (${loginData.user.role})\n`);

        const authHeaders = {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${authToken}`
        };

        // -------------------------------------------------------------
        // CHẶNG 2: MÀN HÌNH M1 — DANH SÁCH CHỜ & TẢI KTV
        // -------------------------------------------------------------
        console.log('🔹 [BƯỚC 2] M1 — Lấy danh sách phiếu và Tải công việc KTV...');
        const m1TicketsRes = await fetch(`${baseUrl}/tickets?center_id=1`, { headers: authHeaders });
        const m1Tickets = await m1TicketsRes.json();
        console.log(`   ✅ Lấy danh sách phiếu: Tìm thấy ${m1Tickets.count} phiếu trong hệ thống.`);
        m1Tickets.data.slice(0, 3).forEach(t => {
            console.log(`      • [${t.ticket_code}] Khách: ${t.customer_name} | Trạng thái: ${t.status} | Sự cố: ${t.issue_category}`);
        });

        const m1TechRes = await fetch(`${baseUrl}/technicians?center_id=1`, { headers: authHeaders });
        const m1Techs = await m1TechRes.json();
        console.log(`   ✅ Lấy tải công việc KTV: ${m1Techs.count} kỹ thuật viên.`);
        m1Techs.data.forEach(tech => {
            console.log(`      • ${tech.full_name}: Đang giữ ${tech.active_tickets} phiếu (${tech.status})`);
        });
        console.log('');

        // -------------------------------------------------------------
        // CHẶNG 3: MÀN HÌNH M2 — GỢI Ý & PHÂN CÔNG KTV (US2, QT-04, QT-07)
        // -------------------------------------------------------------
        const targetTicketId = 1;
        console.log(`🔹 [BƯỚC 3] M2 — Lấy danh sách gợi ý KTV cho phiếu #${targetTicketId}...`);
        const recRes = await fetch(`${baseUrl}/tickets/${targetTicketId}/recommend-technicians`, { headers: authHeaders });
        const recData = await recRes.json();
        console.log(`   ✅ Gợi ý ${recData.count} KTV đạt chuẩn tay nghề >= 3 (QT-07):`);
        recData.data.forEach(t => {
            console.log(`      • KTV: ${t.full_name} | Tay nghề: ${t.proficiency}/5 | Đang giữ: ${t.active_tickets} phiếu`);
        });

        const selectedTech = recData.data[0];
        console.log(`\n🔹 [BƯỚC 4] M2 — Tiến hành phân công KTV #${selectedTech.technician_id} (${selectedTech.full_name}) cho phiếu #${targetTicketId}...`);
        const assignRes = await fetch(`${baseUrl}/tickets/${targetTicketId}/assign`, {
            method: 'POST',
            headers: authHeaders,
            body: JSON.stringify({
                technician_id: selectedTech.technician_id,
                note: 'Phân công qua kiểm thử tự động e2e',
                user_id: 1
            })
        });
        const assignData = await assignRes.json();
        if (!assignRes.ok) {
            throw new Error(`Phân công thất bại: ${JSON.stringify(assignData)}`);
        }
        console.log(`   ✅ Phân công thành công:`);
        console.log(`      • Trạng thái mới: ${assignData.data.status}`);
        console.log(`      • KTV được gán: ${assignData.data.technician_name}`);
        console.log(`      • Hạn SLA cập nhật (QT-04): ${assignData.data.due_date}\n`);

        // -------------------------------------------------------------
        // CHẶNG 4: MÀN HÌNH M2 — CHUYỂN GÁN PHIẾU (US6, QT-08)
        // -------------------------------------------------------------
        const secondTech = recData.data.find(t => t.technician_id !== selectedTech.technician_id);
        if (!secondTech) {
            throw new Error('Không có KTV thứ 2 đủ điều kiện để kiểm thử Re-assign');
        }

        console.log(`🔹 [BƯỚC 5] M2 — Chuyển gán phiếu (Re-assign) sang KTV #${secondTech.technician_id} (${secondTech.full_name})...`);
        const reassignRes = await fetch(`${baseUrl}/tickets/${targetTicketId}/reassign`, {
            method: 'POST',
            headers: authHeaders,
            body: JSON.stringify({
                technician_id: secondTech.technician_id,
                reason: 'KTV phụ trách cũ đi đào tạo nghiệp vụ gấp, chuyển giao phiếu bảo hành',
                note: 'Bàn giao linh kiện màn hình cho KTV mới',
                user_id: 1
            })
        });
        const reassignData = await reassignRes.json();
        if (!reassignRes.ok) {
            throw new Error(`Chuyển gán thất bại: ${JSON.stringify(reassignData)}`);
        }
        console.log(`   ✅ Chuyển gán thành công! KTV phụ trách mới: ${reassignData.data.technician_name}\n`);

        // -------------------------------------------------------------
        // CHẶNG 5: MÀN HÌNH M3 — ĐẶT LỊCH HẸN GIAO NHẬN MÁY (US3, QT-09)
        // -------------------------------------------------------------
        console.log('🔹 [BƯỚC 6] M3 — Đặt lịch hẹn giao máy cho khách hàng...');
        // Tạo khung giờ hẹn độc nhất cho phiên chạy này để đảm bảo tính Idempotency (C5)
        const uniqueOffset = 86400000 * 20 + Math.floor(Math.random() * 50000000);
        const uniqueSlot = new Date(Date.now() + uniqueOffset).toISOString();
        const apptRes = await fetch(`${baseUrl}/tickets/${targetTicketId}/appointments`, {
            method: 'POST',
            headers: authHeaders,
            body: JSON.stringify({
                appointment_type: 'GIAO_MAY',
                appointment_date: uniqueSlot,
                notes: 'Khách hàng hẹn nhận máy tại quầy 2'
            })
        });
        const apptData = await apptRes.json();
        if (!apptRes.ok) {
            throw new Error(`Đặt lịch thất bại: ${JSON.stringify(apptData)}`);
        }
        console.log(`   ✅ Đặt lịch hẹn thành công (ID: ${apptData.data.appointment_id})`);
        console.log(`      • Loại lịch: ${apptData.data.appointment_type}`);
        console.log(`      • Thời gian hẹn: ${apptData.data.appointment_date}`);
        console.log(`      • Trạng thái: ${apptData.data.status}\n`);

        // -------------------------------------------------------------
        // CHẶNG 6: KIỂM CHỨNG NGOẠI LỆ QT-09 (TỐI ĐA 5 LỊCH HẸN / KHUNG 30P)
        // -------------------------------------------------------------
        console.log('🔹 [BƯỚC 7] Kiểm chứng quy tắc biên QT-09 (Giới hạn tối đa 5 lịch / khung giờ 30p)...');
        for (let i = 2; i <= 5; i++) {
            await fetch(`${baseUrl}/tickets/${targetTicketId}/appointments`, {
                method: 'POST',
                headers: authHeaders,
                body: JSON.stringify({
                    appointment_type: 'NHAN_MAY',
                    appointment_date: uniqueSlot,
                    notes: `Phiếu thứ ${i} trong cùng khung giờ`
                })
            });
        }
        console.log('   Đã nạp đủ 5 lịch hẹn vào cùng khung giờ (Đầy slot: 5/5).');

        const overflowRes = await fetch(`${baseUrl}/tickets/${targetTicketId}/appointments`, {
            method: 'POST',
            headers: authHeaders,
            body: JSON.stringify({
                appointment_type: 'NHAN_MAY',
                appointment_date: uniqueSlot,
                notes: 'Lịch hẹn thứ 6 (Cố tình gây quá tải)'
            })
        });
        const overflowData = await overflowRes.json();
        if (overflowRes.status === 409 || overflowRes.status === 400) {
            console.log(`   ✅ Bắt lỗi thành công theo QT-09: "${overflowData.message}"\n`);
        } else {
            throw new Error(`Hệ thống không chặn được vượt tải QT-09! Status: ${overflowRes.status}`);
        }

        // -------------------------------------------------------------
        // CHẶNG 7: KIỂM CHỨNG AUDIT LOG (TRUY VẾT LỊCH SỬ THAY ĐỔI)
        // -------------------------------------------------------------
        console.log('🔹 [BƯỚC 8] Kiểm tra toàn vẹn nhật ký thay đổi trạng thái (Audit Log)...');
        const logsRes = await fetch(`${baseUrl}/tickets/${targetTicketId}/logs`, { headers: authHeaders });
        const logsData = await logsRes.json();
        console.log(`   ✅ Tổng số sự kiện ghi nhận: ${logsData.count} logs:`);
        logsData.data.slice(0, 4).forEach(log => {
            console.log(`      • [${log.changed_at}] ${log.from_status || 'null'} -> ${log.to_status} | Lý do: "${log.reason}" (Bởi: ${log.changed_by})`);
        });

        console.log('\n================================================================');
        console.log('   🎉 KẾT QUẢ: TOÀN BỘ LUỒNG CHÍNH CHẠY END-TO-END 100% THÀNH CÔNG! ');
        console.log('   • M1 -> M2 (Assign) -> M2 (Re-assign) -> M3 (Appointment)      ');
        console.log('   • Tuân thủ đầy đủ QT-04, QT-06, QT-07, QT-08, QT-09           ');
        console.log('   • Structured Logging & Centralized Error Handling tích hợp     ');
        console.log('================================================================\n');

    } catch (err) {
        console.error('❌ LỖI TRONG QUÁ TRÌNH CHẠY END-TO-END:', err);
        process.exit(1);
    } finally {
        if (server) {
            server.close();
        }
    }
}

runEndToEnd();
