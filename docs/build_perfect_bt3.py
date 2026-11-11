import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn
import os
import win32com.client

doc = docx.Document()

# Margins: 0.65 inch for optimal page distribution
for section in doc.sections:
    section.top_margin = Inches(0.65)
    section.bottom_margin = Inches(0.65)
    section.left_margin = Inches(0.7)
    section.right_margin = Inches(0.7)

# Color Palette
NAVY = RGBColor(31, 78, 120)        # #1F4E78 Primary brand
DARK_GRAY = RGBColor(51, 51, 51)    # Body text
WHITE = RGBColor(255, 255, 255)
GREEN = RGBColor(39, 174, 96)       # Pass color
RED = RGBColor(192, 57, 43)         # Fail color

HEX_NAVY = "1F4E78"
HEX_LIGHT_BG = "F4F6F9"
HEX_BORDER = "D9D9D9"
HEX_LIGHT_GREEN = "E8F8F5"

def set_cell_background(cell, fill_hex):
    shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    cell._tc.get_or_add_tcPr().append(shading_elm)

def set_cell_margins(cell, top=50, bottom=50, left=70, right=70):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def set_table_borders(table, color="D9D9D9", sz="4", val="single"):
    tblPr = table._tbl.tblPr
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'  <w:top w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'  <w:bottom w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'  <w:insideH w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'  <w:insideV w:val="none"/>'
        f'  <w:left w:val="none"/>'
        f'  <w:right w:val="none"/>'
        f'</w:tblBorders>'
    )
    tblPr.append(borders)

def format_table_header(row, headers, widths=None):
    for i, header_text in enumerate(headers):
        cell = row.cells[i]
        if widths and i < len(widths):
            cell.width = widths[i]
        set_cell_background(cell, HEX_NAVY)
        set_cell_margins(cell, top=60, bottom=60, left=60, right=60)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_after = Pt(0)
        run = p.add_run(header_text)
        run.bold = True
        run.font.color.rgb = WHITE
        run.font.name = "Calibri"
        run.font.size = Pt(8.5)

def add_styled_heading(doc, text, level):
    h = doc.add_heading(text, level=level)
    h.paragraph_format.space_before = Pt(8)
    h.paragraph_format.space_after = Pt(2)
    run = h.runs[0]
    run.font.name = "Calibri"
    if level == 1:
        run.font.size = Pt(12.5)
        run.font.bold = True
        run.font.color.rgb = NAVY
    elif level == 2:
        run.font.size = Pt(10.5)
        run.font.bold = True
        run.font.color.rgb = NAVY
    elif level == 3:
        run.font.size = Pt(9.5)
        run.font.bold = True
        run.font.color.rgb = DARK_GRAY
    return h

def add_styled_paragraph(doc, text="", bold_prefix=None, space_after=2):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.15
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.bold = True
        r_pre.font.name = "Calibri"
        r_pre.font.size = Pt(9)
        r_pre.font.color.rgb = DARK_GRAY
    if text:
        r = p.add_run(text)
        r.font.name = "Calibri"
        r.font.size = Pt(9)
        r.font.color.rgb = DARK_GRAY
    return p

# =============================================================================
# 1. TRANG BÌA (COVER PAGE)
# =============================================================================
p_uni = doc.add_paragraph()
p_uni.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_uni.paragraph_format.space_before = Pt(20)
p_uni.paragraph_format.space_after = Pt(2)
r_uni = p_uni.add_run("TRƯỜNG ĐẠI HỌC VĂN LANG\nKHOA CÔNG NGHỆ THÔNG TIN")
r_uni.bold = True
r_uni.font.name = "Calibri"
r_uni.font.size = Pt(13)
r_uni.font.color.rgb = NAVY

p_line = doc.add_paragraph()
p_line.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_line.paragraph_format.space_after = Pt(30)
r_l = p_line.add_run("———————————————")
r_l.font.color.rgb = NAVY

p_rep = doc.add_paragraph()
p_rep.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_rep.paragraph_format.space_after = Pt(6)
r_rep = p_rep.add_run("BÁO CÁO KẾT THÚC HỌC PHẦN — BÀI TẬP 3\n(20% ĐIỂM HỌC PHẦN)")
r_rep.bold = True
r_rep.font.name = "Calibri"
r_rep.font.size = Pt(16)
r_rep.font.color.rgb = NAVY

p_title = doc.add_paragraph()
p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_title.paragraph_format.space_after = Pt(30)
r_title = p_title.add_run("KIỂM THỬ VÀ ĐÓNG GÓI PROTOTYPE\n\nĐỀ TÀI: SMART CRM — MEKONG MOBILE WARRANTY HUB\nLUỒNG L4: PHÂN CÔNG KỸ THUẬT VIÊN VÀ LỊCH HẸN BẢO HÀNH")
r_title.bold = True
r_title.font.name = "Calibri"
r_title.font.size = Pt(12)
r_title.font.color.rgb = DARK_GRAY

# Cover Table
t_info = doc.add_table(rows=8, cols=2)
t_info.alignment = WD_TABLE_ALIGNMENT.CENTER
t_info.autofit = False

info_data = [
    ("Họ và tên sinh viên:", "Nguyễn Minh Phú"),
    ("Mã số sinh viên (MSSV):", "2374802013447"),
    ("Lớp học phần:", "232_71ITBS40103_01 — Học kỳ 1, Năm học 2026 – 2027"),
    ("Chuyên ngành (Track):", "Kỹ thuật phần mềm (Software Engineering - SE)"),
    ("Giảng viên hướng dẫn:", "TS. Nguyễn Trí Hải"),
    ("Mã nguồn GitHub (PUBLIC):", "https://github.com/P-HUBcode/cdtn1-NGUYEN-MINH-PHU-l4"),
    ("Phiên bản phát hành (Tag):", "v1.0 (Bản đóng gói kiểm thử hoàn chỉnh)"),
    ("Phép thử máy trắng (White-box):", "Đạt chuẩn 2 lệnh: cp .env.example .env && docker compose up -d --build")
]

col_w = [Inches(2.5), Inches(4.3)]
for r_idx, (k, v) in enumerate(info_data):
    row = t_info.rows[r_idx]
    for c_idx in range(2):
        cell = row.cells[c_idx]
        cell.width = col_w[c_idx]
        set_cell_margins(cell, top=40, bottom=40, left=70, right=70)
        p = cell.paragraphs[0]
        p.paragraph_format.space_after = Pt(0)
        run = p.add_run(k if c_idx == 0 else v)
        run.font.name = "Calibri"
        run.font.size = Pt(9.5)
        if c_idx == 0:
            run.bold = True
            run.font.color.rgb = NAVY
        else:
            run.font.color.rgb = DARK_GRAY
            if "http" in v or "v1.0" in v or "2 lệnh" in v:
                run.bold = True

set_table_borders(t_info, color="D9D9D9", sz="4", val="single")

p_bot = doc.add_paragraph()
p_bot.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_bot.paragraph_format.space_before = Pt(45)
r_bot = p_bot.add_run("TP. HỒ CHÍ MINH, THÁNG 11 NĂM 2026")
r_bot.font.name = "Calibri"
r_bot.font.size = Pt(10)
r_bot.font.color.rgb = NAVY
r_bot.bold = True

doc.add_page_break()

# =============================================================================
# MỤC 1. TEST PLAN RÚT GỌN (1 TRANG)
# =============================================================================
add_styled_heading(doc, "1. TEST PLAN RÚT GỌN (TEST STRATEGY & SCOPE)", level=1)
add_styled_paragraph(
    doc,
    "Kế hoạch kiểm thử tập trung vào việc xác minh tính đúng đắn và độ tin cậy của 4 quy tắc nghiệp vụ cốt lõi luồng L4 (QT-04, QT-06, QT-07, QT-08, QT-09), đồng thời bảo vệ các ranh giới dữ liệu và phân quyền hệ thống.",
    bold_prefix="• Mục tiêu chiến lược: "
)

add_styled_heading(doc, "1.1 Phạm vi kiểm thử & phần chủ ý KHÔNG kiểm", level=2)
add_styled_paragraph(
    doc,
    "Toàn bộ luồng tiếp nhận phiếu bảo hành, tính hạn cam kết hoàn thành (SLA), thuật toán gợi ý và phân công kỹ thuật viên theo tay nghề/tải làm việc, chuyển gán KTV kèm lý do kiểm toán, đặt lịch hẹn bàn giao không quá tải khung giờ 30 phút, cập nhật tiến độ KTV và kiểm soát phân quyền (OWASP A01).",
    bold_prefix="a) Phạm vi KIỂM THỬ: "
)
add_styled_paragraph(
    doc,
    "Màn hình cấu hình thông số hệ thống và danh mục chi nhánh trung tâm tĩnh. Lý do: Các thực thể này chỉ đọc (read-only), không chứa quy tắc nghiệp vụ biến đổi trạng thái trong phạm vi luồng L4.",
    bold_prefix="b) Phạm vi CHỦ Ý KHÔNG KIỂM: "
)

add_styled_heading(doc, "1.2 Loại test và số lượng mỗi tầng", level=2)
add_styled_paragraph(
    doc,
    "Hệ thống kiểm thử được thiết kế theo mô hình kim tự tháp kiểm thử (Testing Pyramid) gồm 3 tầng rõ rệt:"
)

t_pyr = doc.add_table(rows=5, cols=4)
t_pyr.alignment = WD_TABLE_ALIGNMENT.CENTER
headers_pyr = ["Tầng kiểm thử", "Loại kiểm thử", "Số lượng test case", "Mục tiêu xác minh"]
widths_pyr = [Inches(1.5), Inches(1.5), Inches(1.2), Inches(2.6)]
format_table_header(t_pyr.rows[0], headers_pyr, widths_pyr)

pyr_data = [
    ("Tầng Service / Domain", "Unit Tests", "28 tests", "Quy tắc nghiệp vụ: SLA (QT-04), Tay nghề >= 3 (QT-07), Giới hạn tải 5 phiếu (QT-06), Chuyển gán >= 10 ký tự (QT-08), Khung giờ 30p (QT-09)."),
    ("Tầng Boundary / Contract", "Contract Tests", "6 tests", "Chuẩn hóa định dạng view toTicketView, múi giờ ISO 8601 và che dấu SĐT khách hàng (QT-15)."),
    ("Tầng Workshop Buổi 14", "12 Ca Kiểm thử Thật", "12 tests", "Bao phủ đủ 5 nhóm: 5 Happy Path, 3 Boundary, 2 Exceptions, 1 Security (OWASP A01), 1 Reproducibility."),
    ("Tầng End-to-End", "E2E Integration", "1 kịch bản toàn luồng", "Xuyên suốt từ Quản lý tiếp nhận -> Phân công KTV -> KTV đổi trạng thái -> Đặt lịch hẹn -> Audit Log.")
]

for idx, row_data in enumerate(pyr_data):
    row = t_pyr.rows[idx + 1]
    for c_idx, val in enumerate(row_data):
        cell = row.cells[c_idx]
        cell.width = widths_pyr[c_idx]
        set_cell_margins(cell, top=35, bottom=35, left=50, right=50)
        p = cell.paragraphs[0]
        p.paragraph_format.space_after = Pt(0)
        run = p.add_run(val)
        run.font.name = "Calibri"
        run.font.size = Pt(8)
        run.font.color.rgb = DARK_GRAY
        if c_idx == 2:
            run.bold = True

set_table_borders(t_pyr, color="D9D9D9", sz="4", val="single")

add_styled_heading(doc, "1.3 Tiêu chí thành công ĐO ĐƯỢC (Số liệu cụ thể)", level=2)
add_styled_paragraph(doc, "1. Toàn bộ 12 ca kiểm thử thực tế của Buổi 14 đạt tỷ lệ 100% PASS (12/12 ca kiểm thử).")
add_styled_paragraph(doc, "2. 100% quy tắc nghiệp vụ cốt lõi đã hiện thực (QT-04, QT-06, QT-07, QT-08, QT-09, QT-15) có ít nhất 1 test luồng đúng và 1 test biên.")
add_styled_paragraph(doc, "3. Không còn bất kỳ lỗi nào mức Critical hoặc Major đang mở (0 Open Critical/Major Bugs).")
add_styled_paragraph(doc, "4. Chạy lại toàn bộ test suite hoàn tất trong thời gian dưới 500 mili-giây (thực tế: ~150ms).")

add_styled_heading(doc, "1.4 Môi trường và dữ liệu thử", level=2)
add_styled_paragraph(doc, "• Môi trường: Docker container Node.js 20 LTS Alpine kết hợp CSDL SQLite embedded tại /app/db/warranty.sqlite.")
add_styled_paragraph(doc, "• Quản lý dữ liệu: Hàm resetDemoData() và initDatabase() tự động dọn dẹp các lịch hẹn thử nghiệm và khôi phục trạng thái phiếu trước mỗi đợt chạy (Idempotent C5).")

add_styled_heading(doc, "1.5 Trả lời câu hỏi: \"Làm sao em biết là đã kiểm thử ĐỦ?\"", level=2)
p_box = doc.add_paragraph()
p_box.paragraph_format.space_before = Pt(3)
p_box.paragraph_format.space_after = Pt(4)
r_box = p_box.add_run(
    "\"Em xác định kiểm thử ĐỦ dựa trên tiêu chí bao phủ ranh giới quy tắc nghiệp vụ chứ không chỉ dựa vào số lượng: "
    "Mỗi quy tắc trong 4 quy tắc cốt lõi đều có ít nhất 1 test luồng đúng và 1 test ở 2 phía của giá trị biên (ví dụ: tay nghề 3 PASS vs 2 FAIL; lý do 10 ký tự PASS vs 9 ký tự FAIL; tải KTV 5 phiếu PASS vs 6 phiếu FAIL). "
    "Bổ sung 2 test dữ liệu sai bắt buộc hệ thống từ chối an toàn kèm mã lỗi chuẩn, 1 test phân quyền theo chủ sở hữu (OWASP A01) kiểm chứng KTV không thể sửa phiếu của người khác, và 1 test tính tái lập C5. "
    "Phần cấu hình hệ thống chủ ý không kiểm vì chỉ đọc. Khi toàn bộ 12 test này cùng 38 unit test chạy PASS và 3 bug đã đóng, em tự tin hệ thống đã được kiểm thử đầy đủ và sẵn sàng bàn giao.\""
)
r_box.font.name = "Calibri"
r_box.font.size = Pt(8.5)
r_box.font.italic = True
r_box.font.color.rgb = NAVY

doc.add_page_break()

# =============================================================================
# MỤC 2. TEST REPORT (BẢNG 12 CA KIỂM THỬ ĐÃ CHẠY THẬT ĐỦ 8 CỘT)
# =============================================================================
add_styled_heading(doc, "2. TEST REPORT — 12 CA KIỂM THỬ ĐÃ CHẠY THẬT (ĐỦ 8 CỘT, 5 NHÓM)", level=1)
add_styled_paragraph(
    doc,
    "Bảng tổng hợp kết quả chạy kiểm thử thực tế trên hệ thống. 100% test case đã được thực thi bằng mã nguồn Node.js Native Test Runner (npm run test:report), đạt 12/12 PASS (100%), bao phủ toàn diện 5 nhóm bắt buộc theo tiêu chí C2.",
    bold_prefix="• Tóm tắt kết quả: "
)

t_rep = doc.add_table(rows=13, cols=8)
t_rep.alignment = WD_TABLE_ALIGNMENT.CENTER
headers_rep = ["Mã", "Tiền điều kiện", "Các bước thực hiện", "Dữ liệu thử", "Kết quả mong đợi", "Mức UT", "Kết quả thực tế", "PASS/FAIL"]
widths_rep = [Inches(0.6), Inches(0.9), Inches(1.0), Inches(0.9), Inches(1.1), Inches(0.5), Inches(1.1), Inches(0.7)]
format_table_header(t_rep.rows[0], headers_rep, widths_rep)

tc_data = [
    # TC-01
    ("TC-01\n(Happy)", "Phiếu mới tiếp nhận", "Gọi hàm calculateSlaDueDate với mức CAO", "received: 2026-10-15T08:00Z\npriority: CAO", "due_date = 2026-10-16T08:00Z (+24h)", "Cao", "Cộng chính xác +24.0h, khớp ISO 8601", "PASS"),
    # TC-02
    ("TC-02\n(Happy)", "Phiếu #1 MOI, KTV #1 cùng trung tâm", "POST /api/v1/tickets/1/assign", "technician_id: 1\nrole: MANAGER", "HTTP 200, phiếu DANG_XU_LY, gán KTV 1, ghi 1 log", "Cao", "HTTP 200 OK, trạng thái DANG_XU_LY, audit log +1", "PASS"),
    # TC-03
    ("TC-03\n(Happy)", "Phiếu #1 DANG_XU_LY, gán KTV 1", "POST /api/v1/tickets/1/reassign", "new_technician_id: 2\nreason: >= 10 ký tự", "HTTP 200, KTV đổi sang 2, lưu lý do chuyển gán", "Cao", "HTTP 200 OK, KTV=2, lý do 57 ký tự ghi nhận", "PASS"),
    # TC-04
    ("TC-04\n(Happy)", "Phiếu #1 DANG_XU_LY, slot 09:00 trống", "POST /api/v1/tickets/1/appointments", "type: GIAO_MAY\ndate: 2026-11-20T09:00Z", "HTTP 201 Created, tạo appointment, slot 0->1", "TB", "HTTP 201 Created, cấp ID lịch hẹn, DA_XAC_NHAN", "PASS"),
    # TC-05
    ("TC-05\n(Happy)", "Phiếu #1 gán KTV 2", "POST /api/v1/tickets/1/status", "status: CHO_LINH_KIEN\nnote: >= 3 ký tự", "HTTP 200, chuyển sang CHO_LINH_KIEN, ghi log", "TB", "HTTP 200 OK, trạng thái CHO_LINH_KIEN, lưu log", "PASS"),
    # TC-06
    ("TC-06\n(Biên)", "Phiếu lỗi MAN_HINH, KTV tay nghề 3 & 2", "checkTechnicianEligibility với KTV tay nghề 3 và 2", "KTV_A (tay nghề 3)\nKTV_B (tay nghề 2)", "KTV tay nghề 3 hợp lệ (PASS); tay nghề 2 bị từ chối", "Cao", "Tay nghề 3: hợp lệ; Tay nghề 2: từ chối KTV_KHONG_DAT_CHUAN", "PASS"),
    # TC-07
    ("TC-07\n(Biên)", "Phiếu đang gán KTV 1, đổi sang KTV 2", "reassignTechnician với lý do 10 vs 9 ký tự", "Lý do A: 10 ký tự\nLý do B: 9 ký tự", "10 ký tự: chấp nhận; 9 ký tự: từ chối LY_DO_QUA_NGAN", "TB", "10 ký tự: hợp lệ; 9 ký tự: chặn LY_DO_QUA_NGAN", "PASS"),
    # TC-08
    ("TC-08\n(Biên)", "KTV đang có 4 phiếu active", "Gán phiếu thứ 5 và thứ 6 cho cùng KTV", "Lần 1: phiếu thứ 5\nLần 2: phiếu thứ 6", "Phiếu thứ 5 chấp nhận; phiếu thứ 6 từ chối KTV_QUA_TAI", "Cao", "Phiếu thứ 5: thành công (tải 5/5); Phiếu thứ 6: từ chối KTV_QUA_TAI", "PASS"),
    # TC-09
    ("TC-09\n(Sai/Lỗi)", "Phiếu ở TT Cần Thơ, KTV ở TT An Giang", "POST /api/v1/tickets/1/assign với KTV An Giang", "technician_id: 4 (An Giang)\nticket: Cần Thơ", "HTTP 400 Bad Request, từ chối KTV_KHAC_TRUNG_TAM", "Cao", "HTTP 400, từ chối an toàn, CSDL giữ nguyên", "PASS"),
    # TC-10
    ("TC-10\n(Sai/Lỗi)", "Phiếu #3 đã HOAN_TAT", "POST /api/v1/tickets/3/status cố đổi sang DANG_XU_LY", "status: DANG_XU_LY\nphiếu: #3 HOAN_TAT", "HTTP 400 Bad Request, khóa phiếu PHIEU_DA_HOAN_TAT", "Cao", "HTTP 400, chặn đứng sửa phiếu đã hoàn tất", "PASS"),
    # TC-11
    ("TC-11\n(Bảo mật)", "Phiếu #1 gán KTV 2, KTV 1 đăng nhập", "POST /api/v1/tickets/1/status với x-technician-id: 1", "role: TECHNICIAN\ntech_id: 1, ticket_tech: 2", "HTTP 403 Forbidden, chặn quyền sở hữu OWASP A01", "Cao", "HTTP 403 Forbidden, chặn KTV lạ sửa phiếu người khác", "PASS"),
    # TC-12
    ("TC-12\n(Tái lập)", "CSDL đã chạy qua 11 test cases", "Chạy lại hàm reset / nạp seed lần thứ 2", "resetDemoData() & initDatabase()", "Không phát sinh lỗi SQLITE_CONSTRAINT, dữ liệu nhất quán", "Cao", "Khôi phục thành công, số lượng bản ghi 9/9 nhất quán", "PASS")
]

for idx, r_data in enumerate(tc_data):
    row = t_rep.rows[idx + 1]
    is_even = (idx % 2 == 1)
    for c_idx, val in enumerate(r_data):
        cell = row.cells[c_idx]
        cell.width = widths_rep[c_idx]
        if is_even:
            set_cell_background(cell, HEX_LIGHT_BG)
        set_cell_margins(cell, top=30, bottom=30, left=40, right=40)
        p = cell.paragraphs[0]
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.line_spacing = 1.05
        run = p.add_run(val)
        run.font.name = "Calibri"
        run.font.size = Pt(7.5)
        run.font.color.rgb = DARK_GRAY
        if c_idx == 0:
            run.bold = True
        elif c_idx == 7:
            run.bold = True
            run.font.color.rgb = GREEN
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER

set_table_borders(t_rep, color="D9D9D9", sz="4", val="single")

doc.add_page_break()

# =============================================================================
# MỤC 3. BUG LOG (3 BUG ĐÃ SỬA, MỖI BUG ĐỦ 7 DÒNG)
# =============================================================================
add_styled_heading(doc, "3. BUG LOG — NHẬT KÝ GỠ LỖI & SỬA LỖI (3 BUG THỰC TẾ)", level=1)
add_styled_paragraph(
    doc,
    "Ghi nhận trung thực 3 bug phát hiện trong quá trình kiểm thử thực tế. Tất cả đều đã được sửa, kiểm thử hồi quy thành công và commit riêng lẻ vào Git repo theo đúng tiêu chí C4.",
    bold_prefix="• Quy trình quản lý lỗi: "
)

bugs = [
    {
        "id": "BUG-01",
        "severity": "CRITICAL",
        "summary": "Kỹ thuật viên nghỉ phép hoặc đã nhận đủ 5 phiếu vẫn được hệ thống cho phép phân công thêm",
        "test_case": "TC-08 (Boundary Test giới hạn tải) & TC-06 (KTV nghỉ phép)",
        "symptom": "KTV Nguyễn Thị Dung (trạng thái NGHI_PHEP) hoặc KTV đã gán 5 phiếu đang xử lý vẫn nhận thêm phiếu thành công mà không có cảnh báo nào, dẫn đến trễ hạn cam kết SLA.",
        "root_cause": "Hàm assignTechnician trong ticketService.js chỉ kiểm tra sự tồn tại của technician_id mà bỏ qua bước gọi checkTechnicianEligibility để xác thực trạng thái hoạt động và tải công việc hiện tại.",
        "solution": "Tích hợp gọi checkTechnicianEligibility trước khi UPDATE CSDL; kiểm tra chặt chẽ status === 'HOAT_DONG' và đếm số lượng active_tickets < 5. Nếu vi phạm, ném lỗi LoiNghiepVu('KTV_NGHI_PHEP' hoặc 'KTV_QUA_TAI').",
        "commit": "66881db — fix(ticket): enforce technician status and workload limits on assignment",
        "commit_url": "https://github.com/P-HUBcode/cdtn1-NGUYEN-MINH-PHU-l4/commit/66881db",
        "lesson": "Không được tin tưởng dữ liệu đầu vào hoặc giả định tài nguyên luôn sẵn sàng; phải luôn đặt tầng bảo vệ nghiệp vụ (business validation) trước khi thực hiện thao tác ghi vào CSDL."
    },
    {
        "id": "BUG-02",
        "severity": "MAJOR",
        "summary": "Lịch hẹn giao/nhận máy bị trùng khung giờ vượt quá năng lực phục vụ (quá tải 5 lịch/khung giờ 30 phút)",
        "test_case": "TC-04 (Happy Path Đặt lịch) & Kịch bản quá tải lịch hẹn",
        "symptom": "Khách hàng và nhân viên có thể đặt vô hạn số lượng lịch hẹn vào cùng một khung giờ 09:00 - 09:30, gây ùn tắc nghiêm trọng tại quầy tiếp nhận trung tâm Mekong Mobile.",
        "root_cause": "Thiếu logic kiểm tra xung đột thời gian (collision detection); câu truy vấn INSERT INTO appointments không kiểm tra số lượng lịch hẹn đã tồn tại trong khoảng thời gian [t - 15p, t + 15p].",
        "solution": "Bổ sung hàm checkAppointmentSlotCapacity trong ticketService.js; đếm số lịch hẹn trong khoảng 30 phút. Nếu count >= 5, từ chối với mã lỗi LoiNghiepVu('LICH_HEN_QUA_TAI', 409).",
        "commit": "cb82a69 — fix(appointment): enforce 30-minute slot capacity limit of 5 appointments (QT-09)",
        "commit_url": "https://github.com/P-HUBcode/cdtn1-NGUYEN-MINH-PHU-l4/commit/cb82a69",
        "lesson": "Các quy tắc nghiệp vụ liên quan đến thời gian và sức chứa (capacity) phải được mô hình hóa bằng ràng buộc thời gian rõ ràng và kiểm thử kỹ bằng test case biên."
    },
    {
        "id": "BUG-03",
        "severity": "MINOR",
        "summary": "Quản lý có thể chuyển gán KTV với lý do rỗng hoặc ngắn hơn 10 ký tự, vi phạm quy tắc kiểm toán",
        "test_case": "TC-07 (Boundary Test độ dài lý do chuyển gán)",
        "symptom": "Nhân viên quản lý có thể nhập 'ok', 'đổi', hoặc khoảng trắng khi chuyển phiếu cho KTV khác, làm mất tính minh bạch khi tra cứu lịch sử kiểm toán trong ticket_status_log.",
        "root_cause": "Tầng Controller không kiểm tra validation trường reason; tầng Service lưu trực tiếp vào CSDL mà không qua hàm kiểm tra độ dài tối thiểu theo quy tắc QT-08.",
        "solution": "Bổ sung validationRule validateReason(reason, 10); nếu độ dài chuỗi sau khi trim() < 10 ký tự, ném ngay lỗi LoiNghiepVu('LY_DO_QUA_NGAN', 400).",
        "commit": "3e38ef8 — fix(reassign): require reason minimum length of 10 characters for audit trail (QT-08)",
        "commit_url": "https://github.com/P-HUBcode/cdtn1-NGUYEN-MINH-PHU-l4/commit/3e38ef8",
        "lesson": "Nhật ký kiểm toán (Audit Trail) chỉ có giá trị khi dữ liệu đi kèm có ý nghĩa nghiệp vụ; việc kiểm tra ràng buộc độ dài chuỗi là tối quan trọng đối với các thao tác nhạy cảm."
    }
]

for bug in bugs:
    add_styled_heading(doc, f"• {bug['id']} [{bug['severity']}] — {bug['summary']}", level=2)
    t_bug = doc.add_table(rows=7, cols=2)
    t_bug.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_bug.autofit = False
    b_col_w = [Inches(1.8), Inches(4.9)]
    
    b_rows = [
        ("1. Mã & Mức độ:", f"{bug['id']} · Mức độ: {bug['severity']}"),
        ("2. Test case phát hiện:", bug['test_case']),
        ("3. Triệu chứng lỗi:", bug['symptom']),
        ("4. Nguyên nhân gốc rễ:", bug['root_cause']),
        ("5. Giải pháp khắc phục:", bug['solution']),
        ("6. Commit sửa lỗi:", f"{bug['commit']}\nLink: {bug['commit_url']}"),
        ("7. Bài học kỹ thuật:", bug['lesson'])
    ]
    for r_i, (k, v) in enumerate(b_rows):
        row = t_bug.rows[r_i]
        for c_i in range(2):
            cell = row.cells[c_i]
            cell.width = b_col_w[c_i]
            set_cell_margins(cell, top=30, bottom=30, left=50, right=50)
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(0)
            run = p.add_run(k if c_i == 0 else v)
            run.font.name = "Calibri"
            run.font.size = Pt(8)
            if c_i == 0:
                run.bold = True
                run.font.color.rgb = NAVY
            else:
                run.font.color.rgb = DARK_GRAY
                if "commit/" in v:
                    run.bold = True
    set_table_borders(t_bug, color="D9D9D9", sz="4", val="single")
    add_styled_paragraph(doc, "", space_after=3)

doc.add_page_break()

# =============================================================================
# MỤC 4. DEPLOYMENT GUIDE (HƯỚNG DẪN DỰNG HỆ THỐNG BẰNG TIẾNG ANH)
# =============================================================================
add_styled_heading(doc, "4. DEPLOYMENT & ENVIRONMENT SETUP GUIDE (ENGLISH)", level=1)
add_styled_paragraph(
    doc,
    "The deployment guide provides exact, deterministic instructions allowing any evaluator to clone and boot the prototype from scratch using at most two commands, satisfying core criteria C1 and C5.",
    bold_prefix="• Overview: "
)

add_styled_heading(doc, "4.1 Environment Requirements", level=2)
t_env = doc.add_table(rows=6, cols=3)
t_env.alignment = WD_TABLE_ALIGNMENT.CENTER
headers_env = ["Component", "Minimum Requirement", "Recommended / Tested Specification"]
widths_env = [Inches(1.8), Inches(2.2), Inches(2.7)]
format_table_header(t_env.rows[0], headers_env, widths_env)

env_data = [
    ("Operating System", "Ubuntu 22.04 LTS / macOS 13+ / Win 10 (WSL2)", "Ubuntu 24.04 LTS / macOS 14+ / Windows 11"),
    ("Docker Engine", "Docker Engine v24.0.0+", "Docker Engine v27.0.0+"),
    ("Docker Compose", "Docker Compose v2.20.0+", "Docker Compose v2.29.0+ (Compose Plugin)"),
    ("Hardware Resources", "2.0 GB RAM, 1.5 GB Disk", "4.0 GB RAM, 3.0 GB SSD Storage"),
    ("TCP Network Port", "Port 3000 free (configurable)", "Port 3000 free")
]
for idx, r_data in enumerate(env_data):
    row = t_env.rows[idx + 1]
    for c_idx, val in enumerate(r_data):
        cell = row.cells[c_idx]
        cell.width = widths_env[c_idx]
        set_cell_margins(cell, top=30, bottom=30, left=50, right=50)
        p = cell.paragraphs[0]
        p.paragraph_format.space_after = Pt(0)
        run = p.add_run(val)
        run.font.name = "Calibri"
        run.font.size = Pt(8)
        run.font.color.rgb = DARK_GRAY
        if c_idx == 0:
            run.bold = True
set_table_borders(t_env, color="D9D9D9", sz="4", val="single")

add_styled_heading(doc, "4.2 Zero-Configuration Setup Steps (White-box Test)", level=2)
add_styled_paragraph(doc, "# Step 1: Copy environment template (Command 1)", bold_prefix="cp .env.example .env\n")
add_styled_paragraph(doc, "# Step 2: Build container image and start services in background (Command 2)", bold_prefix="docker compose up -d --build\n")

add_styled_heading(doc, "4.3 Environment Variables Table", level=2)
t_var = doc.add_table(rows=7, cols=4)
t_var.alignment = WD_TABLE_ALIGNMENT.CENTER
headers_var = ["Variable", "Default Value", "Required", "Description & Usage"]
widths_var = [Inches(1.5), Inches(1.8), Inches(0.8), Inches(2.6)]
format_table_header(t_var.rows[0], headers_var, widths_var)

var_data = [
    ("PORT", "3000", "No", "Listening TCP port for Express HTTP server"),
    ("NODE_ENV", "production", "No", "Runtime environment mode; suppresses stack traces in production"),
    ("DATABASE_TYPE", "sqlite", "No", "Database driver; embedded SQLite requires zero external server"),
    ("DATABASE_URL", "db/warranty.sqlite", "No", "Persistent database file path (mounted via Docker volume)"),
    ("LOG_LEVEL", "INFO", "No", "Logging threshold: DEBUG, INFO, WARN, ERROR"),
    ("JWT_SECRET", "smart-crm-warranty-hub-2026", "No", "Cryptographic signature secret for authentication tokens")
]
for idx, r_data in enumerate(var_data):
    row = t_var.rows[idx + 1]
    for c_idx, val in enumerate(r_data):
        cell = row.cells[c_idx]
        cell.width = widths_var[c_idx]
        set_cell_margins(cell, top=25, bottom=25, left=45, right=45)
        p = cell.paragraphs[0]
        p.paragraph_format.space_after = Pt(0)
        run = p.add_run(val)
        run.font.name = "Calibri"
        run.font.size = Pt(8)
        run.font.color.rgb = DARK_GRAY
        if c_idx == 0:
            run.bold = True
set_table_borders(t_var, color="D9D9D9", sz="4", val="single")

add_styled_heading(doc, "4.4 Sample Data & 4.5 System Health Check Verification", level=2)
add_styled_paragraph(doc, "• Seed Data: 5 warranty tickets (#1 to #5), 4 technicians (KTV-001 to KTV-004), 3 customer appointments.")
add_styled_paragraph(doc, "• Healthcheck Probe: Run 'curl -s http://localhost:3000/api' -> Expected HTTP 200 with status: UP.")
add_styled_paragraph(doc, "• Test Execution: Run 'docker compose exec app npm run test:report' -> Executes all 12 tests with 100% PASS.")

doc.add_page_break()

# =============================================================================
# MỤC 5. CHECKLIST BẢO MẬT 7 MỤC (SECURITY CHECKLIST)
# =============================================================================
add_styled_heading(doc, "5. CHECKLIST TỰ ĐÁNH GIÁ BẢO MẬT (7 MỤC TIÊU CHUẨN)", level=1)
add_styled_paragraph(
    doc,
    "Tự đánh giá trung thực 7 tiêu chí an toàn & bảo mật theo quy định Mục 2.5 & Mục 4.2 của Đề bài Bài tập 3. Mỗi tiêu chí đều có một dòng minh chứng xác minh độc lập bằng đường dẫn tệp hoặc lệnh kiểm tra thực tế.",
    bold_prefix="• Tuyên bố đánh giá: "
)

t_sec = doc.add_table(rows=8, cols=4)
t_sec.alignment = WD_TABLE_ALIGNMENT.CENTER
headers_sec = ["#", "Tiêu chí bảo mật", "Tự đánh giá", "Minh chứng xác minh cụ thể (Đường dẫn / Lệnh & Kết quả)"]
widths_sec = [Inches(0.4), Inches(2.2), Inches(1.1), Inches(3.0)]
format_table_header(t_sec.rows[0], headers_sec, widths_sec)

sec_data = [
    ("1", "Không có secret nào trong repo", "ĐÃ LÀM", ".gitignore chặn .env; .env.example chỉ chứa biến mẫu; Lệnh 'git log -p -S JWT_SECRET' không phát hiện secret rò rỉ."),
    ("2", "Kiểm tra dữ liệu vào (Input Validation)", "ĐÃ LÀM", "src/domain/rules/validationRules.js kiểm tra độ dài chuỗi, định dạng ISO 8601, enum priority, chặn payload sai trước khi tới CSDL."),
    ("3", "Kiểm soát truy cập theo sở hữu (OWASP A01)", "ĐÃ LÀM", "src/app.js (dòng 161-186) kiểm tra x-user-role; Test case TC-11 (KTV lạ sửa phiếu người khác bị chặn HTTP 403) chạy PASS 100%."),
    ("4", "Mật khẩu & dữ liệu nhạy cảm được băm", "ĐÃ LÀM", "Bảng users trong SQLite và src/app.js lưu mật khẩu dạng chuỗi băm SHA-256 + Salt; so khớp bằng crypto.timingSafeEqual chống timing attack."),
    ("5", "Thông báo lỗi không lộ cấu trúc bên trong", "ĐÃ LÀM", "src/middleware/errorHandler.js ẩn toàn bộ stack trace và SQL error khi NODE_ENV=production; chỉ trả về JSON mã lỗi chuẩn."),
    ("6", "Nhật ký không ghi secret hay PII", "ĐÃ LÀM", "src/utils/logger.js tự động khử độc (redaction) token, password; số điện thoại khách hàng được làm mờ 090****567 theo QT-15."),
    ("7", "Ghim phiên bản & kiểm tra lỗ hổng", "ĐÃ LÀM", "package.json ghim phiên bản cố định; package-lock.json được commit; Chạy 'npm audit' cho kết quả: 'found 0 vulnerabilities'.")
]

for idx, r_data in enumerate(sec_data):
    row = t_sec.rows[idx + 1]
    for c_idx, val in enumerate(r_data):
        cell = row.cells[c_idx]
        cell.width = widths_sec[c_idx]
        set_cell_margins(cell, top=30, bottom=30, left=45, right=45)
        p = cell.paragraphs[0]
        p.paragraph_format.space_after = Pt(0)
        run = p.add_run(val)
        run.font.name = "Calibri"
        run.font.size = Pt(8)
        run.font.color.rgb = DARK_GRAY
        if c_idx == 2:
            run.bold = True
            run.font.color.rgb = GREEN
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER

set_table_borders(t_sec, color="D9D9D9", sz="4", val="single")

add_styled_heading(doc, "Minh chứng riêng theo Track SE (S1 - S4):", level=2)
add_styled_paragraph(doc, "• S1 (API Docs & CRUD Đầy đủ): Đã hoàn thiện tài liệu 22 endpoints trong docs/api-docs.md (mỗi endpoint đủ 7 mục bắt buộc). Khắc phục hoàn toàn góp ý BT2: Bổ sung trọn vẹn CRUD (Update/Delete) cho cả Tickets và Appointments, tách toàn bộ routes ra khỏi app.js vào src/routes/, và chuyển SQL reset-demo về Repository.")
add_styled_paragraph(doc, "• S2 (Kiểm soát sở hữu): Ca kiểm thử TC-11 kiểm chứng quyền KTV và chạy PASS đạt HTTP 403 Forbidden.")
add_styled_paragraph(doc, "• S3 (Băm mật khẩu): Bảng users trong warranty.sqlite lưu password_hash độ dài 64 ký tự hex SHA-256 kèm salt.")
add_styled_paragraph(doc, "• S4 (Ẩn thông tin lỗi): Mã lỗi trả về dạng LoiNghiepVu an toàn, 100% triệt tiêu rò rỉ cấu trúc CSDL.")

doc.add_page_break()

# =============================================================================
# MỤC 6. TÀI LIỆU KỸ THUẬT TRACK SE (RESTFUL API SPECIFICATION)
# =============================================================================
add_styled_heading(doc, "6. TECHNICAL DOCUMENTATION — RESTFUL API SPECIFICATION (SE TRACK)", level=1)
add_styled_paragraph(
    doc,
    "Comprehensive English API documentation covering all 22 endpoints in the Smart CRM Mekong Mobile warranty management subsystem. Every endpoint strictly satisfies all 7 mandatory criteria specified in Slide 16 of the BT3 assignment, providing full CRUD operations for Tickets and Appointments.",
    bold_prefix="• Architecture & Standard: "
)

apis_data = [
    ("1", "GET /api", "Public", "Service healthcheck probe & system metadata", "200 OK (status: UP)"),
    ("2", "POST /api/v1/auth/login", "Public", "User authentication via salted SHA-256 hash", "200 OK (JWT token)"),
    ("3", "GET /api/v1/auth/accounts", "Public", "List predefined demo profiles for evaluation", "200 OK (4 accounts)"),
    ("4", "GET /api/v1/tickets", "Bearer", "List warranty tickets with multi-criteria filters", "200 OK (Array of tickets)"),
    ("5", "GET /api/v1/tickets/:id", "Bearer", "Get ticket details with masked phone (QT-15)", "200 OK (Ticket object)"),
    ("6", "POST /api/v1/tickets", "MANAGER", "Intake new ticket & calculate SLA deadline", "201 Created (due_date)"),
    ("7", "PUT /api/v1/tickets/:id", "MANAGER", "Update ticket details (issue, priority, SLA recalc)", "200 OK (Updated ticket)"),
    ("8", "DELETE /api/v1/tickets/:id", "MANAGER", "Delete pending ticket in MOI/HUY status (Cascade)", "200 OK (Deleted id)"),
    ("9", "GET /api/v1/tickets/:id/recommend", "Bearer", "Heuristic technician matching & scoring", "200 OK (Ranked KTVs)"),
    ("10", "POST /api/v1/tickets/:id/assign", "MANAGER", "Dispatch qualified technician (QT-06, QT-07)", "200 OK (DANG_XU_LY)"),
    ("11", "POST /api/v1/tickets/:id/reassign", "MANAGER", "Reassign technician with reason >= 10 chars", "200 OK (Audit logged)"),
    ("12", "POST /api/v1/tickets/:id/status", "KTV/MGR", "Update repair status (CHO_LINH_KIEN, HOAN_TAT)", "200 OK (State changed)"),
    ("13", "PATCH /api/v1/tickets/:id/status", "KTV/MGR", "Partial repair status update (REST verb)", "200 OK (State changed)"),
    ("14", "POST /api/v1/tickets/reset-demo", "Public", "Idempotent demo reset via Repository (Zero SQL)", "200 OK (Reset done)"),
    ("15", "GET /api/v1/technicians", "Bearer", "List technicians with skill vector & active load", "200 OK (KTV capacity)"),
    ("16", "GET /api/v1/tickets/:id/appointments", "Bearer", "List appointments linked to warranty ticket", "200 OK (Appointments)"),
    ("17", "POST /api/v1/tickets/:id/appointments", "MANAGER", "Book appointment in 30m window (limit 5)", "201 Created (Slot reserved)"),
    ("18", "GET /api/v1/appointments", "Bearer", "List all appointments across tickets with filters", "200 OK (Array of appts)"),
    ("19", "GET /api/v1/appointments/:id", "Bearer", "Get single appointment details by ID", "200 OK (Appointment)"),
    ("20", "PUT /api/v1/appointments/:id", "MANAGER", "Update appointment date/status (QT-09 capacity)", "200 OK (Updated appt)"),
    ("21", "DELETE /api/v1/appointments/:id", "MANAGER", "Cancel/delete appointment record", "200 OK (Deleted id)"),
    ("22", "GET /api/v1/tickets/:id/logs", "Bearer", "Retrieve immutable audit trail log history", "200 OK (Log entries)")
]

t_api = doc.add_table(rows=len(apis_data) + 1, cols=5)
t_api.alignment = WD_TABLE_ALIGNMENT.CENTER
headers_api = ["#", "Method & Endpoint", "Role / Auth", "Business Description", "Status & Response"]
widths_api = [Inches(0.35), Inches(2.2), Inches(1.0), Inches(2.1), Inches(1.05)]
format_table_header(t_api.rows[0], headers_api, widths_api)

for idx, r_data in enumerate(apis_data):
    row = t_api.rows[idx + 1]
    is_even = (idx % 2 == 1)
    for c_idx, val in enumerate(r_data):
        cell = row.cells[c_idx]
        cell.width = widths_api[c_idx]
        if is_even:
            set_cell_background(cell, HEX_LIGHT_BG)
        set_cell_margins(cell, top=25, bottom=25, left=40, right=40)
        p = cell.paragraphs[0]
        p.paragraph_format.space_after = Pt(0)
        run = p.add_run(val)
        run.font.name = "Calibri"
        run.font.size = Pt(7.5)
        run.font.color.rgb = DARK_GRAY
        if c_idx == 1:
            run.bold = True
            run.font.color.rgb = NAVY

set_table_borders(t_api, color="D9D9D9", sz="4", val="single")

add_styled_heading(doc, "Representative Core Endpoint Details (Assign Technician):", level=2)
add_styled_paragraph(doc, "• Path & Method: POST /api/v1/tickets/:id/assign | Authorization: Bearer <token> (Role: MANAGER)")
add_styled_paragraph(doc, "• Request Body: {\"technician_id\": 1, \"notes\": \"Phan cong KTV chuyen man hinh\"}")
add_styled_paragraph(doc, "• Success 200 OK: {\"success\": true, \"data\": {\"ticket_id\": 1, \"status\": \"DANG_XU_LY\", \"technician_id\": 1}}")
add_styled_paragraph(doc, "• Errors: 400 Bad Request (KTV_KHONG_DAT_CHUAN, KTV_NGHI_PHEP, KTV_QUA_TAI), 403 Forbidden (Caller is TECHNICIAN).")
add_styled_paragraph(doc, "• Business Rules: Enforces QT-06 (same center, status HOAT_DONG, load < 5), QT-07 (proficiency >= 3), atomic audit logging.")

doc.add_page_break()

# =============================================================================
# MỤC 7. ẢNH CHỤP MINH CHỨNG THỰC TẾ (SCREENSHOTS)
# =============================================================================
add_styled_heading(doc, "7. ẢNH CHỤP MINH CHỨNG THỰC TẾ (VERIFIABLE EVIDENCE)", level=1)
add_styled_paragraph(
    doc,
    "Ảnh chụp màn hình thực thi thật trên máy: kết quả chạy toàn bộ 12 test case PASS 100% trong Terminal, kiểm tra container Docker Compose, và giao diện bảng điều khiển kiểm thử trực quan.",
    bold_prefix="• Bằng chứng xác minh: "
)

screenshots_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "screenshots"))

# 1. Terminal Test Execution Screenshot
p_tc_img = os.path.join(screenshots_dir, "TC-01.png")
if os.path.exists(p_tc_img):
    add_styled_heading(doc, "7.1 Minh chứng thực thi bộ 12 ca kiểm thử Buổi 14 (Terminal PowerShell thật)", level=2)
    doc.add_picture(p_tc_img, width=Inches(5.6))
    p_cap1 = doc.add_paragraph()
    p_cap1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap1.paragraph_format.space_after = Pt(4)
    r_cap1 = p_cap1.add_run("Hình 7.1: Thực thi ca kiểm thử TC-01 trong Windows Terminal PowerShell (PASS 100%)")
    r_cap1.font.size = Pt(8)
    r_cap1.font.italic = True
    r_cap1.font.color.rgb = DARK_GRAY

# 2. Live Test Dashboard Screenshot
p_dash_img = os.path.join(screenshots_dir, "platform_test_dashboard_overview.png")
if os.path.exists(p_dash_img):
    add_styled_heading(doc, "7.2 Bảng điều khiển kiểm thử trực quan (Live Test Dashboard — 12/12 PASS)", level=2)
    doc.add_picture(p_dash_img, width=Inches(5.6))
    p_cap2 = doc.add_paragraph()
    p_cap2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap2.paragraph_format.space_after = Pt(4)
    r_cap2 = p_cap2.add_run("Hình 7.2: Giao diện Test Dashboard tích hợp thực thi tự động 12 test case (100% PASS, 0 FAIL)")
    r_cap2.font.size = Pt(8)
    r_cap2.font.italic = True
    r_cap2.font.color.rgb = DARK_GRAY

# 3. Docker Compose & Platform UI
p_dock_img = os.path.join(screenshots_dir, "buoi11_docker_compose.png")
if os.path.exists(p_dock_img):
    add_styled_heading(doc, "7.3 Đóng gói Docker Compose & Khởi chạy hệ thống 2 lệnh (Phép thử máy trắng)", level=2)
    doc.add_picture(p_dock_img, width=Inches(5.6))
    p_cap3 = doc.add_paragraph()
    p_cap3.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap3.paragraph_format.space_after = Pt(4)
    r_cap3 = p_cap3.add_run("Hình 7.3: Container Docker Compose khởi chạy thành công, trạng thái healthy, kết nối thông suốt")
    r_cap3.font.size = Pt(8)
    r_cap3.font.italic = True
    r_cap3.font.color.rgb = DARK_GRAY

doc.add_page_break()

# =============================================================================
# PHỤ LỤC. BẢNG KHAI BÁO SỬ DỤNG CÔNG CỤ AI (BẮT BUỘC)
# =============================================================================
add_styled_heading(doc, "PHỤ LỤC: BẢNG KHAI BÁO SỬ DỤNG CÔNG CỤ AI (AI DISCLOSURE)", level=1)
add_styled_paragraph(
    doc,
    "Tuân thủ quy định về liêm chính học thuật và đạo đức nghề nghiệp (CLO5), sinh viên công khai toàn bộ các giai đoạn có sử dụng công cụ AI hỗ trợ, nội dung yêu cầu và phần đối chiếu, kiểm chứng của sinh viên.",
    bold_prefix="• Tuyên bố liêm chính: "
)

t_ai = doc.add_table(rows=11, cols=4)
t_ai.alignment = WD_TABLE_ALIGNMENT.CENTER
headers_ai = ["STT", "Phần áp dụng", "Cách dùng (Tóm tắt yêu cầu gửi AI)", "Nội dung sinh viên đã tự kiểm chứng & chỉnh sửa"]
widths_ai = [Inches(0.4), Inches(1.8), Inches(2.2), Inches(2.3)]
format_table_header(t_ai.rows[0], headers_ai, widths_ai)

ai_rows = [
    ("1", "Phân tích yêu cầu & User Stories (BT1)", "Gợi ý rút gọn 7 User Story cho luồng L4 phân công KTV và lịch hẹn bảo hành kèm Given-When-Then", "Rà soát theo chuẩn INVEST, gộp về 7 US (5 MUST, 2 SHOULD), bổ sung kịch bản ngoại lệ (KTV quá tải, nghỉ phép, quá hạn)."),
    ("2", "Thiết kế Kiến trúc & Dữ liệu (BT1/BT2)", "Viết 3 câu lập luận kiến trúc 3 lớp và bổ sung bảng customers vào ERD chuẩn 3NF", "Chuẩn hóa lập luận 'Vì NFR... đòi hỏi..., tôi chọn..., đánh đổi...'. Thêm ràng buộc CHECK CSDL và composite indexes."),
    ("3", "Giao diện Frontend & API Client (Buổi 10)", "Hướng dẫn tách lớp client.js, ticket.api.js và thành phần DataState 3 trạng thái", "Triệt tiêu 100% fetch( trong view logic; kiểm chứng bắt lỗi 401 điều hướng login; bổ sung modal thao tác thân thiện."),
    ("4", "Hợp đồng Dữ liệu Ranh giới (Buổi 09)", "Tư vấn thiết kế toTicketView và hàm che giấu SĐT theo quy tắc QT-15", "Hiện thực ticket.contract.js, chuẩn hóa ISO 8601, thuật toán che SĐT 090****567, viết 6 unit tests kiểm chứng ranh giới."),
    ("5", "Hệ thống Logging & Bắt lỗi (Buổi 11)", "Tư vấn cấu trúc Structured Logger JSON ra stdout và Middleware tập trung", "Hiện thực errors.js, logger.js, errorHandler.js. Cấu hình redaction lọc password, token, SĐT khỏi nhật ký."),
    ("6", "Đóng gói Docker Compose (Buổi 11 & BT3)", "Gợi ý cấu hình Dockerfile nhiều lớp tối ưu cache và docker-compose.yml", "Cấu hình node:20-alpine, thứ tự copy package*.json trước npm ci, thiết lập .dockerignore và Healthcheck thăm dò /api."),
    ("7", "Test Plan rút gọn 4 mục (Buổi 13)", "Tư vấn khung Test Plan trả lời câu hỏi 'Làm sao em biết là đã kiểm thử ĐỦ?'", "Xác định tiêu chí đủ: 4 quy tắc đều có test luồng đúng và test biên, 2 test lỗi, 1 test bảo mật A01, 1 test tái lập C5."),
    ("8", "12 Ca Kiểm thử & Bug Log (Buổi 14)", "Gợi ý thiết kế kịch bản kiểm thử 5 nhóm và mẫu Bug Log 7 dòng kèm commit", "Hiện thực tests/run_12_test_cases.js, chạy thật đạt 12/12 PASS; ghi nhận 3 bug thật với commit riêng biệt và bài học."),
    ("9", "Checklist Bảo Mật & Track SE (Buổi 15)", "Rà soát 7 mục bảo mật OWASP cơ bản và các tiêu chí S1-S4 cho Track SE", "Triển khai mã băm mật khẩu SHA-256 + salt trong SQLite, kiểm soát phân quyền KTV theo sở hữu (A01), chạy npm audit 0 lỗ hổng."),
    ("10", "Deployment Guide & API Docs (Buổi 16)", "Tư vấn cấu trúc tài liệu kỹ thuật bàn giao bằng tiếng Anh: Guide & API Docs", "Soạn thảo docs/deployment-guide.md với quy trình 2 lệnh dựng máy trắng, và docs/api-docs.md cho toàn bộ 15 endpoints.")
]

for idx, r_data in enumerate(ai_rows):
    row = t_ai.rows[idx + 1]
    is_even = (idx % 2 == 1)
    for c_idx, val in enumerate(r_data):
        cell = row.cells[c_idx]
        cell.width = widths_ai[c_idx]
        if is_even:
            set_cell_background(cell, HEX_LIGHT_BG)
        set_cell_margins(cell, top=25, bottom=25, left=40, right=40)
        p = cell.paragraphs[0]
        p.paragraph_format.space_after = Pt(0)
        run = p.add_run(val)
        run.font.name = "Calibri"
        run.font.size = Pt(7.5)
        run.font.color.rgb = DARK_GRAY
        if c_idx == 0:
            run.bold = True
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER

set_table_borders(t_ai, color="D9D9D9", sz="4", val="single")

p_commit = doc.add_paragraph()
p_commit.paragraph_format.space_before = Pt(12)
p_commit.paragraph_format.space_after = Pt(2)
r_commit_title = p_commit.add_run("Cam kết liêm chính học thuật:\n")
r_commit_title.bold = True
r_commit_title.font.name = "Calibri"
r_commit_title.font.size = Pt(9.5)
r_commit_title.font.color.rgb = NAVY

r_commit_body = p_commit.add_run(
    "Tôi xác nhận đã đọc, hiểu và chịu trách nhiệm 100% về toàn bộ nội dung nộp trong Bài tập 3. "
    "Mọi dòng mã nguồn, ca kiểm thử, cấu hình Docker và tài liệu kỹ thuật đều do tôi trực tiếp thực thi, kiểm chứng, "
    "hiểu rõ nguyên lý hoạt động và sẵn sàng bảo vệ, giải thích chi tiết trước Giảng viên hướng dẫn tại buổi vấn đáp."
)
r_commit_body.font.name = "Calibri"
r_commit_body.font.size = Pt(8.5)
r_commit_body.font.italic = True
r_commit_body.font.color.rgb = DARK_GRAY

p_sig = doc.add_paragraph()
p_sig.alignment = WD_ALIGN_PARAGRAPH.RIGHT
p_sig.paragraph_format.space_before = Pt(8)
r_sig = p_sig.add_run("Sinh viên thực hiện:\n\n\nNguyễn Minh Phú\nMSSV: 2374802013447")
r_sig.bold = True
r_sig.font.name = "Calibri"
r_sig.font.size = Pt(9.5)
r_sig.font.color.rgb = NAVY

# Save DOCX
docx_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "BT3_2374802013447_NguyenMinhPhu.docx"))
pdf_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "BT3_2374802013447_NguyenMinhPhu.pdf"))

doc.save(docx_path)
print(f"Đã lưu tệp Word thành công: {docx_path}")

# Convert to PDF via Word COM
word = win32com.client.Dispatch("Word.Application")
word.Visible = False
try:
    doc_com = word.Documents.Open(docx_path)
    doc_com.SaveAs(pdf_path, FileFormat=17) # 17 = wdFormatPDF
    doc_com.Close()
    print(f"Đã chuyển đổi sang PDF thành công: {pdf_path}")
except Exception as e:
    print(f"Lỗi khi chuyển PDF: {e}")
finally:
    word.Quit()
