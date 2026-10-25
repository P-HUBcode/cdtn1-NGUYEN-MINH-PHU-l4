const { describe, it } = require('node:test');
const assert = require('node:assert/strict');
const { toTicketView, maskPhoneNumber } = require('../src/services/ticket.contract');

describe('DATA CONTRACT TESTS — KIỂM CHỨNG HỢP ĐỒNG DỮ LIỆU RANH GIỚI (BUỔI 9)', () => {

    // 1. Kiểm tra cấu trúc hình dạng (Shape) của hợp đồng
    it('1. toTicketView phải trả về đúng và đầy đủ các trường của hợp đồng dữ liệu', () => {
        const mockRawTicket = {
            ticket_id: 101,
            ticket_code: 'BH-202610-001',
            customer_id: 1,
            customer_name: 'Nguyễn Văn An',
            customer_phone: '0901234567',
            issue_category: 'MAN_HINH',
            issue_desc: 'Màn hình sọc xanh, nhấp nháy liên tục khi sử dụng',
            priority: 'CAO',
            status: 'DANG_XU_LY',
            received_at: '2026-10-15 09:58:09',
            due_date: '2026-10-16 09:58:09',
            center_id: 1,
            center_name: 'Trung tâm Bảo hành Cần Thơ',
            technician_id: 1,
            technician_name: 'Trần Văn Bình'
        };

        const view = toTicketView(mockRawTicket);

        // Kiểm tra đầy đủ các khóa của hợp đồng
        const expectedKeys = [
            'ticket_id', 'ticket_code', 'customer_id', 'customer_name', 'customer_phone',
            'issue_category', 'issue_desc', 'priority', 'status', 'received_at',
            'due_date', 'center_id', 'center_name', 'technician_id', 'technician_name'
        ].sort();

        assert.deepEqual(Object.keys(view).sort(), expectedKeys);
        assert.equal(view.ticket_code, 'BH-202610-001');
    });

    // 2. Kiểm tra định dạng thời gian ISO 8601 của trường due_date
    it('2. due_date phải được chuẩn hóa thành chuỗi thời gian ISO 8601 kèm múi giờ (Z)', () => {
        const mockRawTicket = {
            ticket_id: 102,
            ticket_code: 'BH-202610-002',
            due_date: '2026-10-24 08:00:00'
        };
        const view = toTicketView(mockRawTicket);
        assert.match(view.due_date, /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}/);
    });

    // 3. Quy tắc QT-15: Che số điện thoại khách hàng (Data Redaction / Phone Masking)
    it('3. QT-15: Số điện thoại khách hàng luôn được che giấu tại ranh giới (không lộ đầy đủ)', () => {
        const mockRawTicket = {
            ticket_id: 103,
            ticket_code: 'BH-202610-003',
            customer_phone: '0901234567' // SĐT 10 số
        };
        const view = toTicketView(mockRawTicket);
        // Không chứa chuỗi số liên tiếp 7 ký tự trở lên (QT-15)
        assert.doesNotMatch(view.customer_phone, /\d{7,}/);
        assert.equal(view.customer_phone, '090****567');
    });

    // 4. Kiểm tra hàm maskPhoneNumber độc lập
    it('4. maskPhoneNumber xử lý đúng các trường hợp đặc biệt (null, chuỗi ngắn, chuỗi chuẩn)', () => {
        assert.equal(maskPhoneNumber(null), '(chưa có SĐT)');
        assert.equal(maskPhoneNumber(''), '(chưa có SĐT)');
        assert.equal(maskPhoneNumber('12345'), '12345');
        assert.equal(maskPhoneNumber('0987654321'), '098****321');
    });

    // 5. Kiểm tra giá trị mặc định khi KTV chưa phân công
    it('5. technician_name trả về "Chưa phân công" và technician_id là null khi phiếu mới', () => {
        const mockRawTicket = {
            ticket_id: 104,
            ticket_code: 'BH-202610-004',
            technician_id: null,
            technician_name: null
        };
        const view = toTicketView(mockRawTicket);
        assert.equal(view.technician_name, 'Chưa phân công');
        assert.equal(view.technician_id, null);
    });

    // 6. Kiểm tra fallback an toàn khi khách hàng thiếu họ tên
    it('6. customer_name trả về "(không rõ họ tên)" khi dữ liệu trong CSDL bị null hoặc rỗng', () => {
        const mockRawTicket = {
            ticket_id: 105,
            ticket_code: 'BH-202610-005',
            customer_name: null
        };
        const view = toTicketView(mockRawTicket);
        assert.equal(view.customer_name, '(không rõ họ tên)');
    });

});
