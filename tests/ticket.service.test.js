const { describe, it } = require('node:test');
const assert = require('node:assert/strict');
const {
    calculateSlaDueDate,
    checkTechnicianEligibility,
    validateReassignReason,
    checkAppointmentSlotCapacity,
    toTicketView
} = require('../src/services/ticketService');
const { LoiNghiepVu } = require('../src/errors');

describe('UNIT TESTS — KIỂM CHỨNG LỚP NGHIỆP VỤ SPRINT 2 (BUỔI 10 & 11)', () => {

    // =========================================================================
    // NHÓM 1: QUY TẮC QT-04 (TÍNH TOÁN HẠN SLA CAM KẾT)
    // =========================================================================
    describe('QT-04: Tính hạn cam kết hoàn thành (calculateSlaDueDate)', () => {
        const baseTime = '2026-10-22T08:00:00.000Z';

        it('1. Luồng đúng: Priority CAO phải cộng chính xác +24 giờ vào thời điểm tiếp nhận', () => {
            const dueDate = calculateSlaDueDate(baseTime, 'CAO');
            const expectedTime = new Date('2026-10-23T08:00:00.000Z');
            assert.equal(dueDate.toISOString(), expectedTime.toISOString());
            assert.equal((dueDate.getTime() - new Date(baseTime).getTime()) / (1000 * 60 * 60), 24);
        });

        it('2. Luồng đúng: Priority TRUNG_BINH phải cộng chính xác +48 giờ', () => {
            const dueDate = calculateSlaDueDate(baseTime, 'TRUNG_BINH');
            const expectedTime = new Date('2026-10-24T08:00:00.000Z');
            assert.equal(dueDate.toISOString(), expectedTime.toISOString());
            assert.equal((dueDate.getTime() - new Date(baseTime).getTime()) / (1000 * 60 * 60), 48);
        });

        it('3. Luồng đúng: Priority THAP phải cộng chính xác +72 giờ', () => {
            const dueDate = calculateSlaDueDate(baseTime, 'THAP');
            const expectedTime = new Date('2026-10-25T08:00:00.000Z');
            assert.equal(dueDate.toISOString(), expectedTime.toISOString());
            assert.equal((dueDate.getTime() - new Date(baseTime).getTime()) / (1000 * 60 * 60), 72);
        });

        it('4. Trường hợp biên / Ngoại lệ: Ném lỗi khi mức ưu tiên không hợp lệ', () => {
            assert.throws(() => {
                calculateSlaDueDate(baseTime, 'KHAN_CAP_VOI');
            }, /Mức độ ưu tiên không hợp lệ/);
        });

        it('5. Dữ liệu sai: Ném lỗi khi thời điểm tiếp nhận bị null hoặc rỗng', () => {
            assert.throws(() => {
                calculateSlaDueDate(null, 'CAO');
            }, /Thời điểm tiếp nhận/);
        });
    });

    // =========================================================================
    // NHÓM 2: QUY TẮC QT-06 & QT-07 (ĐIỀU KIỆN PHÂN CÔNG KỸ THUẬT VIÊN)
    // =========================================================================
    describe('QT-06 & QT-07: Điều kiện phân công KTV (checkTechnicianEligibility)', () => {
        const mockTech = {
            technician_id: 1,
            full_name: 'Trần Văn Bình',
            center_id: 1,
            status: 'HOAT_DONG'
        };

        it('6. Luồng đúng: KTV cùng trung tâm, đang hoạt động và tay nghề 5/5 thì hợp lệ', () => {
            const result = checkTechnicianEligibility(mockTech, 1, 5);
            assert.equal(result.valid, true);
        });

        it('7. Trường hợp BIÊN quan trọng: KTV có tay nghề đúng bằng 3 (ngưỡng tối thiểu của QT-07)', () => {
            const result = checkTechnicianEligibility(mockTech, 1, 3);
            assert.equal(result.valid, true);
        });

        it('8. Dữ liệu sai / Ngoại lệ: Từ chối khi tay nghề < 3 (ví dụ: proficiency = 2, vi phạm QT-07)', () => {
            const result = checkTechnicianEligibility(mockTech, 1, 2);
            assert.equal(result.valid, false);
            assert.match(result.reason, /proficiency >= 3/);
        });

        it('9. Dữ liệu sai / Ngoại lệ: Từ chối khi KTV khác trung tâm tiếp nhận (vi phạm QT-06)', () => {
            const result = checkTechnicianEligibility(mockTech, 2, 5); // Khác center_id
            assert.equal(result.valid, false);
            assert.match(result.reason, /cùng trung tâm/);
        });

        it('10. Dữ liệu sai: Từ chối khi KTV đang ở trạng thái NGHI_PHEP', () => {
            const inactiveTech = { ...mockTech, status: 'NGHI_PHEP' };
            const result = checkTechnicianEligibility(inactiveTech, 1, 4);
            assert.equal(result.valid, false);
            assert.match(result.reason, /HOAT_DONG/);
        });
    });

    // =========================================================================
    // NHÓM 3: QUY TẮC QT-08 (LÝ DO CHUYỂN GÁN PHIẾU RE-ASSIGN)
    // =========================================================================
    describe('QT-08: Ràng buộc Lý do chuyển gán phiếu (validateReassignReason)', () => {
        it('11. Luồng đúng: Lý do hợp lệ đầy đủ nội dung', () => {
            const result = validateReassignReason('Kỹ thuật viên cũ bị ốm đột xuất, bàn giao gấp');
            assert.equal(result.valid, true);
        });

        it('12. Trường hợp BIÊN: Lý do có đúng 10 ký tự (ngưỡng tối thiểu cho phép)', () => {
            const result = validateReassignReason('1234567890'); // Đúng 10 ký tự
            assert.equal(result.valid, true);
        });

        it('13. Dữ liệu sai / Ngoại lệ: Từ chối khi lý do dưới 10 ký tự (vi phạm QT-08)', () => {
            const result = validateReassignReason('KTV bận'); // 7 ký tự
            assert.equal(result.valid, false);
            assert.match(result.message, /tối thiểu 10 ký tự/);
        });

        it('14. Dữ liệu sai: Từ chối khi lý do để trống hoặc toàn dấu cách', () => {
            const result = validateReassignReason('         ');
            assert.equal(result.valid, false);
        });
    });

    // =========================================================================
    // NHÓM 4: QUY TẮC QT-09 (TẢI KHUNG GIỜ ĐẶT LỊCH HẸN 30 PHÚT)
    // =========================================================================
    describe('QT-09: Tải khung giờ đặt lịch hẹn 30 phút (checkAppointmentSlotCapacity)', () => {
        it('15. Luồng đúng: Khung giờ còn trống slot (2/5 lịch) thì cho phép đặt', () => {
            const result = checkAppointmentSlotCapacity(2);
            assert.equal(result.allowed, true);
            assert.equal(result.availableSlots, 3);
        });

        it('16. Trường hợp BIÊN: Khung giờ đã có đúng 4 lịch (còn đúng 1 slot cuối cùng)', () => {
            const result = checkAppointmentSlotCapacity(4);
            assert.equal(result.allowed, true);
            assert.equal(result.availableSlots, 1);
        });

        it('17. Dữ liệu sai / Ngoại lệ: Từ chối khi khung giờ đã đầy 5/5 lịch hẹn (vi phạm QT-09)', () => {
            const result = checkAppointmentSlotCapacity(5);
            assert.equal(result.allowed, false);
            assert.match(result.message, /Khung giờ đã đầy/);
        });
    });

    // =========================================================================
    // NHÓM 5: TEST HỒI QUY (REGRESSION TESTS) CHO BUG-LOG (BUỔI 11 - SLIDE 16-18)
    // =========================================================================
    describe('REGRESSION TESTS: Kiểm chứng các lỗi trong docs/bug-log.md', () => {
        it('18. Test hồi quy BUG-001: validateReassignReason từ chối lý do vi phạm QT-08 với mã lỗi LY_DO_QUA_NGAN', () => {
            const result = validateReassignReason('Đổi KTV');
            assert.equal(result.valid, false);
            assert.equal(result.code, 'LY_DO_QUA_NGAN');
            assert.match(result.message, /tối thiểu 10 ký tự/);
        });

        it('19. Test hồi quy BUG-002: checkAppointmentSlotCapacity chặn vượt tải 5 lịch với mã lỗi LICH_HEN_QUA_TAI', () => {
            const result = checkAppointmentSlotCapacity(5);
            assert.equal(result.allowed, false);
            assert.equal(result.code, 'LICH_HEN_QUA_TAI');
            assert.match(result.message, /Khung giờ đã đầy/);
        });

        it('20. Test hồi quy BUG-003: checkTechnicianEligibility từ chối KTV khác trung tâm với mã lỗi KTV_KHAC_TRUNG_TAM', () => {
            const tech = { technician_id: 10, center_id: 2, status: 'HOAT_DONG' };
            const result = checkTechnicianEligibility(tech, 1, 4); // Trung tâm 1 vs 2
            assert.equal(result.valid, false);
            assert.equal(result.code, 'KTV_KHAC_TRUNG_TAM');
            assert.match(result.reason, /cùng trung tâm/);
        });

        it('21. Test hồi quy BUG-004: toTicketView bảo toàn hợp đồng hiển thị khi khách thiếu họ tên hoặc null (chuẩn Slide 15-16)', () => {
            const rawDbRow = {
                ticket_id: 1024,
                ticket_code: 'BH-202610-099',
                customer_name: null,       // Khách thiếu họ tên từ dữ liệu kế thừa
                customer_phone: null,
                technician_name: 'Trần Văn Bình',
                center_name: 'TT Cần Thơ'
            };
            const view = toTicketView(rawDbRow);
            assert.equal(view.customer_name, '(không rõ họ tên)');
            assert.equal(view.customer_phone, '(chưa có SĐT)');
            assert.equal(view.ticket_code, 'BH-202610-099');
        });

        it('22. Test hồi quy BUG-004: toTicketView tự động điền giá trị mặc định cho KTV chưa phân công', () => {
            const rawDbRow = {
                ticket_id: 1025,
                ticket_code: 'BH-202610-100',
                customer_name: 'Nguyễn Văn An',
                customer_phone: '0901234567',
                technician_name: null,     // Phiếu mới chưa phân công
                center_name: null
            };
            const view = toTicketView(rawDbRow);
            assert.equal(view.technician_name, 'Chưa phân công');
            assert.equal(view.center_name, 'Trung tâm mặc định');
        });
    });

});
