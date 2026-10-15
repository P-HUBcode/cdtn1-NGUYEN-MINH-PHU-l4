import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn
import os

doc = docx.Document()

# Margins: 0.8 inch for clean layout
for section in doc.sections:
    section.top_margin = Inches(0.8)
    section.bottom_margin = Inches(0.8)
    section.left_margin = Inches(0.8)
    section.right_margin = Inches(0.8)

# Color Palette
NAVY = RGBColor(31, 78, 120)     # #1F4E78 Primary
DARK_GRAY = RGBColor(51, 51, 51) # Body text
WHITE = RGBColor(255, 255, 255)

HEX_NAVY = "1F4E78"
HEX_LIGHT_BG = "F2F4F7"
HEX_BORDER = "D9D9D9"

def set_cell_background(cell, fill_hex):
    shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    cell._tc.get_or_add_tcPr().append(shading_elm)

def set_cell_margins(cell, top=70, bottom=70, left=100, right=100):
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

def format_table_header(row, headers):
    for i, header_text in enumerate(headers):
        cell = row.cells[i]
        set_cell_background(cell, HEX_NAVY)
        set_cell_margins(cell, top=90, bottom=90, left=90, right=90)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(header_text)
        run.bold = True
        run.font.color.rgb = WHITE
        run.font.name = "Calibri"
        run.font.size = Pt(9.5)

def add_styled_heading(doc, text, level):
    h = doc.add_heading(text, level=level)
    h.paragraph_format.space_before = Pt(11)
    h.paragraph_format.space_after = Pt(3)
    run = h.runs[0]
    run.font.name = "Calibri"
    if level == 1:
        run.font.size = Pt(13.5)
        run.font.bold = True
        run.font.color.rgb = NAVY
    elif level == 2:
        run.font.size = Pt(11.5)
        run.font.bold = True
        run.font.color.rgb = NAVY
    elif level == 3:
        run.font.size = Pt(10)
        run.font.bold = True
        run.font.color.rgb = DARK_GRAY
    return h

def add_body_p(doc, text, bold_prefix=None, italic=False):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(2.5)
    p.paragraph_format.line_spacing = 1.15
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.bold = True
        r_pre.font.name = "Calibri"
        r_pre.font.size = Pt(9.5)
        r_pre.font.color.rgb = DARK_GRAY
    run = p.add_run(text)
    run.italic = italic
    run.font.name = "Calibri"
    run.font.size = Pt(9.5)
    run.font.color.rgb = DARK_GRAY
    return p

def add_callout(doc, text, title="PHẠM VI DIỄN ĐẠT BẰNG MỘT CÂU:"):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    set_cell_background(cell, HEX_LIGHT_BG)
    set_cell_margins(cell, top=100, bottom=100, left=130, right=130)
    
    tcPr = cell._tc.get_or_add_tcPr()
    borders = parse_xml(
        f'<w:tcBorders {nsdecls("w")}>'
        f'  <w:left w:val="single" w:sz="24" w:space="0" w:color="{HEX_NAVY}"/>'
        f'  <w:top w:val="none"/>'
        f'  <w:right w:val="none"/>'
        f'  <w:bottom w:val="none"/>'
        f'</w:tcBorders>'
    )
    tcPr.append(borders)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_after = Pt(2)
    r_t = p.add_run(title + "\n")
    r_t.bold = True
    r_t.font.name = "Calibri"
    r_t.font.size = Pt(10)
    r_t.font.color.rgb = NAVY
    
    r_body = p.add_run(text)
    r_body.italic = True
    r_body.font.name = "Calibri"
    r_body.font.size = Pt(9.5)
    r_body.font.color.rgb = DARK_GRAY

def add_code_block(doc, code_text):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    set_cell_background(cell, "272822")
    set_cell_margins(cell, top=70, bottom=70, left=100, right=100)
    p = cell.paragraphs[0]
    p.paragraph_format.space_after = Pt(0)
    r = p.add_run(code_text)
    r.font.name = "Consolas"
    r.font.size = Pt(8)
    r.font.color.rgb = RGBColor(248, 248, 242)

# ==========================================
# TRANG BÌA
# ==========================================
p_inst = doc.add_paragraph()
p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p_inst.add_run("TRƯỜNG ĐẠI HỌC VĂN LANG - KHOA CÔNG NGHỆ THÔNG TIN\n")
r.bold = True
r.font.size = Pt(11)
r.font.color.rgb = NAVY

r2 = p_inst.add_run("CHUYÊN ĐỀ TỐT NGHIỆP 1 (HK261)\n\n")
r2.font.size = Pt(10)
r2.italic = True

p_main = doc.add_paragraph()
p_main.alignment = WD_ALIGN_PARAGRAPH.CENTER
r_m = p_main.add_run("BÀI TẬP 1: PHÂN TÍCH VÀ THIẾT KẾ HỆ THỐNG\n")
r_m.bold = True
r_m.font.size = Pt(16)
r_m.font.color.rgb = NAVY

r_sub = p_main.add_run("LUỒNG L4: PHÂN CÔNG KỸ THUẬT VIÊN VÀ LỊCH HẸN\n\n")
r_sub.bold = True
r_sub.font.size = Pt(12)
r_sub.font.color.rgb = DARK_GRAY

p_info = doc.add_paragraph()
p_info.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_info.paragraph_format.space_after = Pt(20)
r_i = p_info.add_run(
    "Họ và tên sinh viên: Nguyễn Minh Phú\n"
    "Mã số sinh viên: 2374802013447\n"
    "Chuyên ngành (Track): SE (Software Engineering)\n"
    "Link GitHub Repo: https://github.com/phu47/cdtn-warranty-hub\n"
    "(Đã mời giảng viên làm Collaborator / Repo Public)"
)
r_i.font.size = Pt(10.5)

# ==========================================
# MỤC 1. BẢN SRS RÚT GỌN
# ==========================================
add_styled_heading(doc, "MỤC 1. BẢN SRS RÚT GỌN", 1)

add_styled_heading(doc, "1.1 Bối cảnh doanh nghiệp & Phạm vi hệ thống", 2)
add_body_p(doc, "Hệ thống bảo hành dịch vụ kỹ thuật quản lý việc tiếp nhận, sửa chữa, phân công và bàn giao thiết bị bảo hành cho khách hàng qua chuỗi trung tâm. Việc phân công kỹ thuật viên (KTV) trước đây chủ yếu thực hiện thủ công, dễ dẫn đến tình trạng quá tải cục bộ (Vấn đề V3), phiếu bảo hành bị trễ hạn cam kết SLA (Vấn đề V2) và thiếu minh bạch trong lịch sử xử lý.")
add_callout(doc, "Hệ thống hỗ trợ Quản lý trung tâm bảo hành phân công phiếu bảo hành cho kỹ thuật viên phù hợp dựa trên tay nghề, trung tâm làm việc và khối lượng công việc hiện tại; cho phép đặt và quản lý lịch hẹn giao – nhận máy với khách hàng, đồng thời tự động theo dõi hạn cam kết (SLA) và lịch sử chuyển trạng thái.")

add_styled_heading(doc, "1.2 Điều CHỦ Ý KHÔNG LÀM (WON'T Have)", 2)
t_wont = doc.add_table(rows=4, cols=3)
t_wont.alignment = WD_TABLE_ALIGNMENT.CENTER
set_table_borders(t_wont)
format_table_header(t_wont.rows[0], ["Mã", "Nội dung chủ ý không làm", "Ghi chú phạm vi"])
wont_data = [
    ("WON'T-01", "Không tự động mua sắm hoặc đặt hàng linh kiện tự động từ nhà cung cấp bên ngoài.", "Thuộc hệ thống quản lý chuỗi cung ứng độc lập"),
    ("WON'T-02", "Không tích hợp thanh toán trực tuyến chi phí ngoài bảo hành trong phiên bản này.", "Xử lý thủ công tại quầy thu ngân trung tâm"),
    ("WON'T-03", "Không tự động điều phối KTV di chuyển sửa chữa tại nhà khách hàng.", "Chỉ áp dụng với bảo hành tại trung tâm")
]
for idx, data in enumerate(wont_data, 1):
    row = t_wont.rows[idx]
    if idx % 2 == 1:
        for c in row.cells: set_cell_background(c, HEX_LIGHT_BG)
    for c_idx, val in enumerate(data):
        cell = row.cells[c_idx]
        set_cell_margins(cell)
        p = cell.paragraphs[0]
        r = p.add_run(val)
        r.font.name = "Calibri"
        r.font.size = Pt(8.5)
        if c_idx == 0:
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r.bold = True

add_styled_heading(doc, "1.3 Bảng thuật ngữ nghiệp vụ", 2)
terms_data = [
    ("Phiếu bảo hành (Ticket)", "Yêu cầu bảo hành/sửa chữa thiết bị do khách hàng gửi, có mã định danh duy nhất."),
    ("Kỹ thuật viên (KTV)", "Nhân viên kỹ thuật thực hiện chẩn đoán và sửa chữa thiết bị tại trung tâm."),
    ("Hạn cam kết (SLA / Due Date)", "Thời hạn tối đa hệ thống/trung tâm cam kết hoàn thành sửa chữa cho khách hàng."),
    ("Tay nghề (Proficiency)", "Mức độ thành thạo của KTV với nhóm kỹ năng/thiết bị cụ thể (thang điểm 1–5)."),
    ("Lịch hẹn (Appointment)", "Khung thời gian hẹn trước giữa khách hàng và trung tâm để giao máy hoặc nhận lại máy."),
    ("Nhật ký trạng thái (Status Log)", "Bản ghi lịch sử ghi nhận mỗi lần phiếu bảo hành thay đổi trạng thái, KTV hoặc lịch hẹn.")
]
t_terms = doc.add_table(rows=len(terms_data)+1, cols=3)
t_terms.alignment = WD_TABLE_ALIGNMENT.CENTER
set_table_borders(t_terms)
format_table_header(t_terms.rows[0], ["STT", "Thuật ngữ", "Khái niệm / Giải thích nghiệp vụ"])
for idx, (term, exp) in enumerate(terms_data, 1):
    row = t_terms.rows[idx]
    if idx % 2 == 1:
        for c in row.cells: set_cell_background(c, HEX_LIGHT_BG)
    row.cells[0].paragraphs[0].add_run(str(idx)).font.size = Pt(8.5)
    row.cells[0].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_t = row.cells[1].paragraphs[0].add_run(term)
    r_t.bold = True
    r_t.font.size = Pt(8.5)
    r_e = row.cells[2].paragraphs[0].add_run(exp)
    r_e.font.size = Pt(8.5)
    for c in row.cells: set_cell_margins(c)

add_styled_heading(doc, "1.4 Danh sách Các bên liên quan & Actor", 2)
actors_data = [
    ("Quản lý trung tâm bảo hành", "Human", "Người điều hành công việc tại 1 trung tâm bảo hành cụ thể.", "• Xem danh sách phiếu chờ phân công & tải KTV\n• Phân công & chuyển gán phiếu cho KTV\n• Đặt & quản lý lịch hẹn giao – nhận máy"),
    ("Kỹ thuật viên (KTV)", "Human", "Nhân viên trực tiếp thao tác sửa chữa thiết bị.", "• Xem phiếu gán cho mình xếp theo SLA\n• Cập nhật trạng thái tiến độ xử lý phiếu\n• Tra cứu lịch sử thiết bị theo IMEI/Serial"),
    ("Hệ thống cảnh báo SLA", "Timer", "Actor tự động chạy theo lịch định kỳ.", "• Tự động tính hạn SLA khi phân công phiếu\n• Phát cảnh báo khi phiếu sắp quá hạn hoặc quá hạn SLA")
]
t_act = doc.add_table(rows=len(actors_data)+1, cols=4)
t_act.alignment = WD_TABLE_ALIGNMENT.CENTER
set_table_borders(t_act)
format_table_header(t_act.rows[0], ["Vai trò / Tác nhân", "Loại Actor", "Mô tả vai trò", "Quyền hạn & Trách nhiệm chính"])
for idx, (name, atype, desc, resp) in enumerate(actors_data, 1):
    row = t_act.rows[idx]
    if idx % 2 == 1:
        for c in row.cells: set_cell_background(c, HEX_LIGHT_BG)
    row.cells[0].paragraphs[0].add_run(name).bold = True
    row.cells[1].paragraphs[0].add_run(atype).alignment = WD_ALIGN_PARAGRAPH.CENTER
    row.cells[2].paragraphs[0].add_run(desc)
    row.cells[3].paragraphs[0].add_run(resp)
    for c in row.cells:
        set_cell_margins(c)
        c.paragraphs[0].runs[0].font.size = Pt(8.5)

add_styled_heading(doc, "1.5 Danh sách Yêu cầu Chức năng (FR)", 2)
frs_list = [
    ("FR1", "Hệ thống cho phép Quản lý trung tâm xem danh sách phiếu chờ phân công kèm số lượng phiếu đang xử lý của từng KTV trong cùng trung tâm."),
    ("FR2", "Hệ thống cung cấp tính năng tự động gợi ý danh sách KTV phù hợp dựa trên tay nghề (proficiency >= 3), trung tâm hoạt động và tải công việc thấp nhất."),
    ("FR3", "Hệ thống cho phép Quản lý trung tâm thực hiện gán phiếu bảo hành hoặc chuyển gán phiếu (re-assign) sang KTV khác kèm lý do bắt buộc."),
    ("FR4", "Hệ thống hỗ trợ khởi tạo và quản lý lịch hẹn giao – nhận máy với khách hàng (chọn khung giờ, loại hẹn, dời lịch hẹn)."),
    ("FR5", "Hệ thống cho phép KTV xem danh sách công việc được gán, tự động sắp xếp theo hạn cam kết SLA (due_date) tăng dần."),
    ("FR6", "Hệ thống cho phép KTV cập nhật trạng thái xử lý phiếu bảo hành và ghi nhận tự động vào lịch sử log (ticket_status_log)."),
    ("FR7", "Hệ thống hỗ trợ tra cứu lịch sử sửa chữa thiết bị theo IMEI / Serial.")
]
for code, desc in frs_list:
    add_body_p(doc, desc, bold_prefix=f"• {code}: ")

# ==========================================
# 1.6 BẢNG DẠNG RÚT GỌN CHO USER STORIES (CHÍNH XÁC 7 STORIES)
# ==========================================
add_styled_heading(doc, "1.6 Danh sách 7 User Story đạt chuẩn INVEST & MoSCoW (Đã rút gọn theo TD-03)", 2)

us_table_data = [
    ("US1", "Quản lý trung tâm", "Xem danh sách phiếu chờ phân công kèm số phiếu đang giữ của các KTV trung tâm để nắm tổng quan và phân công hợp lý.", "MUST", 
     "• AC1.1 (Happy): GIVEN Quản lý chọn trung tâm, THEN hiển thị phiếu MỚI và tải công việc từng KTV.\n• AC1.2 (Exception): GIVEN Không có phiếu chờ, THEN hiển thị 'Không có phiếu bảo hành nào đang chờ phân công'."),

    ("US2", "Quản lý trung tâm", "Tự động gợi ý KTV phù hợp theo tay nghề (proficiency >= 3), cùng trung tâm & tải ít nhất để phân công đúng người, tránh quá tải (V3).", "MUST", 
     "• AC2.1 (Happy): GIVEN Nhóm 'MAN_HINH', WHEN nhấn 'Gợi ý KTV', THEN trả về KTV proficiency >= 3 xếp theo số phiếu đang giữ tăng dần.\n• AC2.2 (Happy): GIVEN Chọn KTV & bấm Phân công, THEN đổi status='DANG_XU_LY', tính SLA due_date và ghi log.\n• AC2.3 (Exception): GIVEN Không có KTV proficiency >= 3, THEN cảnh báo 'Không có KTV phù hợp đạt chuẩn tay nghề, đề nghị chọn thủ công'."),

    ("US3", "Quản lý trung tâm", "Đặt và quản lý/dời lịch hẹn giao – nhận máy với khách hàng theo khung giờ 30 phút để tối ưu lịch làm việc trung tâm.", "MUST", 
     "• AC3.1 (Happy): GIVEN Phiếu hợp lệ, WHEN chọn ngày, khung giờ (09:00-09:30) & loại hẹn, THEN lưu lịch hẹn mới vào appointments.\n• AC3.2 (Exception): GIVEN Chọn ngày quá khứ hoặc khung giờ hẹn đã đủ 5 lịch, THEN báo lỗi 'Khung giờ hẹn đã kín hoặc thời gian không hợp lệ'.\n• AC3.3 (Dời hẹn): GIVEN Lịch hẹn đã xác nhận, WHEN chọn mốc thời gian mới, THEN lưu cập nhật và đổi trạng thái thành 'DA_DOI_LICH'."),

    ("US4", "Kỹ thuật viên", "Xem danh sách phiếu bảo hành được gán sắp xếp ưu tiên theo hạn cam kết SLA (due_date) để ưu tiên phiếu sắp quá hạn trước (V2).", "MUST", 
     "• AC4.1 (Happy): GIVEN KTV đăng nhập, WHEN mở 'Phiếu của tôi', THEN hiển thị các phiếu gán sắp xếp theo due_date tăng dần.\n• AC4.2 (Exception): GIVEN KTV không giữ phiếu nào, THEN hiển thị 'Hiện tại bạn không có phiếu bảo hành nào cần xử lý'."),

    ("US5", "Kỹ thuật viên", "Cập nhật chuyển trạng thái xử lý phiếu kèm ghi chú lý do để minh bạch tiến độ sửa chữa và tự động lưu log (ticket_status_log).", "MUST", 
     "• AC5.1 (Happy): GIVEN Phiếu 'DANG_XU_LY', WHEN đổi sang 'CHO_LINH_KIEN' kèm ghi chú, THEN hệ thống lưu trạng thái mới và ghi log.\n• AC5.2 (Exception): GIVEN Phiếu trạng thái 'MOI', WHEN KTV cố bấm 'HOAN_TAT', THEN hệ thống chặn và thông báo 'Phiếu chưa được phân công KTV'."),

    ("US6", "Quản lý trung tâm", "Chuyển phiếu bảo hành sang KTV khác kèm bắt buộc nhập lý do chuyển để đảm bảo phiếu xử lý đúng SLA.", "SHOULD", 
     "• AC6.1 (Happy): GIVEN KTV A nghỉ phép, WHEN chọn KTV B & nhập lý do >= 10 ký tự, THEN hệ thống đổi technician_id và ghi chú log."),

    ("US7", "KTV / Quản lý", "Tra cứu lịch sử sửa chữa trước đó của thiết bị theo IMEI / Serial để phát hiện lỗi lặp lại và có phương án kỹ thuật phù hợp.", "SHOULD", 
     "• AC7.1 (Happy): GIVEN Nhập IMEI/Serial hợp lệ, WHEN bấm Tra cứu, THEN hiển thị toàn bộ lịch sử các phiếu bảo hành quá khứ.")
]

t_us = doc.add_table(rows=len(us_table_data)+1, cols=5)
t_us.alignment = WD_TABLE_ALIGNMENT.CENTER
set_table_borders(t_us)
format_table_header(t_us.rows[0], ["Mã US", "Vai trò (Role)", "Mục tiêu & Giá trị (User Story)", "MoSCoW", "Tiêu chí chấp nhận (Given-When-Then)"])

for idx, (code, role, goal_val, moscow, ac_text) in enumerate(us_table_data, 1):
    row = t_us.rows[idx]
    if idx % 2 == 1:
        for c in row.cells: set_cell_background(c, HEX_LIGHT_BG)
    row.cells[0].paragraphs[0].add_run(code).bold = True
    row.cells[0].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
    row.cells[1].paragraphs[0].add_run(role).alignment = WD_ALIGN_PARAGRAPH.CENTER
    row.cells[2].paragraphs[0].add_run(goal_val)
    row.cells[3].paragraphs[0].add_run(moscow).bold = True
    row.cells[3].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
    row.cells[4].paragraphs[0].add_run(ac_text)
    for c in row.cells:
        set_cell_margins(c)
        c.paragraphs[0].runs[0].font.size = Pt(8)

add_styled_heading(doc, "1.7 Danh sách Yêu cầu Phi chức năng (NFR)", 2)
nfrs_data = [
    ("NFR1", "Performance (Hiệu năng)", "Màn hình danh sách phiếu chờ phân công và khối lượng KTV phải load và hiển thị hoàn tất trong thời gian DƯỚI 1.5 GIÂY với cơ sở dữ liệu thử nghiệm 10.000 phiếu bảo hành và 50 KTV.", "Đo thời gian response API bằng Postman/JMeter trên máy chủ RAM 8GB."),
    ("NFR2", "Security (Bảo mật & Phân quyền)", "100% các thao tác phân công KTV (/assign, /reassign) chỉ được thực hiện bởi tài khoản có role SERVICE_CENTER_MANAGER. KTV thông thường gọi API phải nhận mã HTTP 403 Forbidden.", "Viết Unit Test / Integration Test kiểm tra RBAC middleware."),
    ("NFR3", "Reliability (Tin cậy & Vẹn toàn dữ liệu)", "100% thao tác chuyển trạng thái phiếu, phân công KTV và tạo lịch hẹn phải được thực hiện trong Database Transaction. Nếu ghi log thất bại, toàn bộ quá trình cập nhật phải Rollback.", "Kiểm tra cơ chế Transaction rollback khi cố tình ngắt kết nối CSDL."),
    ("NFR4", "Usability (Khả dụng)", "Quản lý trung tâm bảo hành thao tác phân công 1 phiếu dựa trên gợi ý tự động của hệ thống hoàn tất trong DƯỚI 30 GIÂY (tối đa 3 lượt click chuột).", "Thực hiện User Acceptance Testing (UAT) bấm giờ thao tác thực tế.")
]
t_nfr = doc.add_table(rows=len(nfrs_data)+1, cols=4)
t_nfr.alignment = WD_TABLE_ALIGNMENT.CENTER
set_table_borders(t_nfr)
format_table_header(t_nfr.rows[0], ["Mã NFR", "Phân loại NFR", "Nội dung Yêu cầu & Ngưỡng số đo được", "Phương pháp kiểm chứng"])
for idx, (code, ntype, req, test_mth) in enumerate(nfrs_data, 1):
    row = t_nfr.rows[idx]
    if idx % 2 == 1:
        for c in row.cells: set_cell_background(c, HEX_LIGHT_BG)
    row.cells[0].paragraphs[0].add_run(code).bold = True
    row.cells[0].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
    row.cells[1].paragraphs[0].add_run(ntype).alignment = WD_ALIGN_PARAGRAPH.CENTER
    row.cells[2].paragraphs[0].add_run(req)
    row.cells[3].paragraphs[0].add_run(test_mth)
    for c in row.cells:
        set_cell_margins(c)
        c.paragraphs[0].runs[0].font.size = Pt(8.5)

add_styled_heading(doc, "1.8 Ràng buộc và Quy tắc nghiệp vụ (Business Rules)", 2)
brs_data = [
    ("QT-04", "Quy tắc SLA", "Hạn cam kết SLA (due_date) được tự động tính tại thời điểm phân công phiếu:\n• Ưu tiên CAO = received_at + 24h\n• Ưu tiên TRUNG_BÌNH = received_at + 48h\n• Ưu tiên THẤP = received_at + 72h"),
    ("QT-06", "Quy tắc Gán KTV duy nhất & Cùng trung tâm", "Tại một thời điểm, một phiếu bảo hành chỉ được gán cho duy nhất 1 KTV. KTV được gán BẮT BUỘC phải làm việc tại đúng Trung tâm bảo hành (center_id) tiếp nhận phiếu đó."),
    ("QT-07", "Quy tắc Tay nghề gợi ý", "Hệ thống chỉ đưa KTV vào danh sách gợi ý phân công nếu điểm tay nghề của KTV đó đối với nhóm sự cố của phiếu (issue_category) đạt điểm proficiency >= 3."),
    ("QT-08", "Quy tắc Chuyển phiếu bắt buộc lý do", "Thao tác re-assign phiếu từ KTV cũ sang KTV mới yêu cầu bắt buộc nhập reason (chuỗi ký tự >= 10 ký tự) và ghi lại log trong ticket_status_log."),
    ("QT-09", "Quy tắc Lịch hẹn", "Lịch hẹn giao/nhận máy không được chọn mốc thời gian trong quá khứ (appointment_date >= current_timestamp). Mỗi khung giờ 30 phút tại 1 trung tâm tối đa nhận 5 lịch hẹn.")
]
for code, name, desc in brs_data:
    add_body_p(doc, desc, bold_prefix=f"• {code} ({name}): ")

add_styled_heading(doc, "1.9 Bảng truy vết yêu cầu (Traceability Matrix)", 2)
matrix_data = [
    ("FR1", "Xem danh sách chờ phân công & khối lượng KTV", "US1", "UC1", "MUST", "TC_FR1_01, TC_FR1_02"),
    ("FR2", "Gợi ý & phân công KTV dựa trên tay nghề & tải", "US2", "UC2", "MUST", "TC_FR2_01, TC_FR2_02, TC_FR2_03"),
    ("FR3", "Phân công / Chuyển gán KTV kèm bắt buộc nhập lý do", "US2, US6", "UC2, UC6", "MUST / SHOULD", "TC_FR3_01, TC_FR3_02"),
    ("FR4", "Đặt & quản lý lịch hẹn giao – nhận máy với khách", "US3", "UC3", "MUST", "TC_FR4_01, TC_FR4_02"),
    ("FR5", "Xem danh sách phiếu của KTV sắp xếp theo SLA", "US4", "UC4", "MUST", "TC_FR5_01, TC_FR5_02"),
    ("FR6", "Cập nhật trạng thái phiếu & tự động lưu nhật ký log", "US5", "UC5", "MUST", "TC_FR6_01, TC_FR6_02"),
    ("FR7", "Tra cứu lịch sử sửa chữa thiết bị theo IMEI / Serial", "US7", "UC7", "SHOULD", "TC_FR7_01")
]
t_mat = doc.add_table(rows=len(matrix_data)+1, cols=6)
t_mat.alignment = WD_TABLE_ALIGNMENT.CENTER
set_table_borders(t_mat)
format_table_header(t_mat.rows[0], ["Mã FR", "Yêu cầu chức năng", "User Story", "Use Case", "MoSCoW", "Test Case (BT3)"])
for idx, row_data in enumerate(matrix_data, 1):
    row = t_mat.rows[idx]
    if idx % 2 == 1:
        for c in row.cells: set_cell_background(c, HEX_LIGHT_BG)
    for c_idx, val in enumerate(row_data):
        cell = row.cells[c_idx]
        cell.paragraphs[0].add_run(val)
        set_cell_margins(cell)
        cell.paragraphs[0].runs[0].font.size = Pt(8.5)
        if c_idx in [0, 2, 3, 4]:
            cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
            if c_idx == 0: cell.paragraphs[0].runs[0].bold = True

# ==========================================
# MỤC 2. USE CASE VÀ ĐẶC TẢ CHI TIẾT
# ==========================================
add_styled_heading(doc, "MỤC 2. USE CASE VÀ ĐẶC TẢ CHI TIẾT", 1)

add_styled_heading(doc, "2.1 Sơ đồ Use Case Diagram Luồng L4 (Có chú thích ký hiệu)", 2)
uc_img_path = r"D:\CDTN 1\docs\usecase.png"
if os.path.exists(uc_img_path):
    p_img = doc.add_paragraph()
    p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
    doc.add_picture(uc_img_path, width=Inches(6.2))
    p_cap = doc.add_paragraph()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_c = p_cap.add_run("Hình 2.1: Sơ đồ Use Case Luồng L4 - Phân công KTV & Lịch hẹn (File gốc: docs/usecase.drawio)")
    r_c.font.size = Pt(8.5)
    r_c.font.italic = True

add_styled_heading(doc, "2.2 Đặc tả chi tiết Use Case quan trọng nhất: UC2 (Đủ 9 bước chuẩn hóa theo TD-04)", 2)
add_body_p(doc, "UC2 - GỢI Ý VÀ PHÂN CÔNG KỸ THUẬT VIÊN CHO PHIẾU BẢO HÀNH", bold_prefix="• Tên Use Case: ")
add_body_p(doc, "Quản lý trung tâm bảo hành", bold_prefix="• Actor chính: ")
add_body_p(doc, "Phân công phiếu bảo hành cho KTV phù hợp nhất thuộc trung tâm để tiến hành sửa chữa đúng hạn SLA.", bold_prefix="• Mục tiêu: ")
add_body_p(doc, "Quản lý đã đăng nhập với quyền SERVICE_CENTER_MANAGER. Phiếu bảo hành ở trạng thái MỚI và thuộc trung tâm quản lý.", bold_prefix="• Điều kiện trước: ")
add_body_p(doc, "Phiếu bảo hành được cập nhật technician_id, đổi status='DANG_XU_LY', có SLA due_date và ghi log ticket_status_log.", bold_prefix="• Điều kiện sau: ")

add_styled_heading(doc, "Luồng chính (Happy Path) - Đủ 9 bước tuần tự:", 3)
happy_data = [
    ("1", "Quản lý chọn 1 phiếu bảo hành chờ phân công từ danh sách phiếu MỚI.", "Hệ thống hiển thị thông tin chi tiết phiếu bảo hành."),
    ("2", "Quản lý nhấn nút 'Gợi ý KTV phù hợp'.", "Hệ thống kích hoạt dịch vụ gợi ý phân công."),
    ("3", "---", "Hệ thống xác định category_id và center_id của phiếu bảo hành."),
    ("4", "---", "Hệ thống truy vấn KTV thuộc cùng center_id có điểm tay nghề proficiency >= 3."),
    ("5", "---", "Hệ thống đếm số phiếu ĐANG_XU_LY của từng KTV hợp lệ và sắp xếp tăng dần theo tải."),
    ("6", "---", "Hệ thống hiển thị danh sách KTV gợi ý kèm điểm tay nghề và số phiếu đang giữ."),
    ("7", "Quản lý chọn 1 KTV từ danh sách gợi ý.", "Hệ thống làm nổi bật KTV được chọn và kiểm tra giới hạn tải."),
    ("8", "---", "Hệ thống tính hạn cam kết SLA due_date theo quy tắc QT-04 dựa trên độ ưu tiên."),
    ("9", "Quản lý nhấn 'Xác nhận phân công'.", "Hệ thống cập nhật tickets (technician_id, status='DANG_XU_LY', due_date), ghi log ticket_status_log và báo thành công.")
]
t_hp = doc.add_table(rows=len(happy_data)+1, cols=3)
t_hp.alignment = WD_TABLE_ALIGNMENT.CENTER
set_table_borders(t_hp)
format_table_header(t_hp.rows[0], ["Bước", "Hành động của Actor (Quản lý)", "Phản hồi / Xử lý của Hệ thống"])
for idx, (st, act, sys_act) in enumerate(happy_data, 1):
    row = t_hp.rows[idx]
    if idx % 2 == 1:
        for c in row.cells: set_cell_background(c, HEX_LIGHT_BG)
    row.cells[0].paragraphs[0].add_run(st).bold = True
    row.cells[0].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
    row.cells[1].paragraphs[0].add_run(act)
    row.cells[2].paragraphs[0].add_run(sys_act)
    for c in row.cells: set_cell_margins(c); c.paragraphs[0].runs[0].font.size = Pt(8.5)

add_styled_heading(doc, "Luồng ngoại lệ (Exception Paths) - Đánh số khớp chính xác bước luồng chính:", 3)
exc_data = [
    ("4a", "Không có KTV nào thuộc trung tâm đạt proficiency >= 3.", "Hệ thống hiển thị cảnh báo 'Không tìm thấy KTV đạt tay nghề >= 3'. Gợi ý toàn bộ KTV trung tâm để Quản lý chọn thủ công hoặc chuyển trung tâm."),
    ("7a", "KTV được chọn đang giữ > 10 phiếu bảo hành.", "Hệ thống cảnh báo 'KTV này đang giữ 11 phiếu. Bạn có chắc muốn phân công?'. Quản lý bấm 'Tiếp tục' để gán hoặc 'Hủy' để chọn KTV khác."),
    ("9a", "Lỗi kết nối CSDL khi lưu thông tin phân công.", "Hệ thống Rollback giao dịch, giữ nguyên trạng thái phiếu là MOI. Hiển thị thông báo 'Không thể lưu phân công. Vui lòng thử lại'.")
]
t_exc = doc.add_table(rows=len(exc_data)+1, cols=3)
t_exc.alignment = WD_TABLE_ALIGNMENT.CENTER
set_table_borders(t_exc)
format_table_header(t_exc.rows[0], ["Mã Ngoại lệ", "Điều kiện phát sinh ngoại lệ", "Xử lý của Hệ thống & Kết quả"])
for idx, (code, cond, sys_res) in enumerate(exc_data, 1):
    row = t_exc.rows[idx]
    if idx % 2 == 1:
        for c in row.cells: set_cell_background(c, HEX_LIGHT_BG)
    row.cells[0].paragraphs[0].add_run(code).bold = True
    row.cells[0].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
    row.cells[1].paragraphs[0].add_run(cond)
    row.cells[2].paragraphs[0].add_run(sys_res)
    for c in row.cells: set_cell_margins(c); c.paragraphs[0].runs[0].font.size = Pt(8.5)

# ==========================================
# MỤC 3. THIẾT KẾ KIẾN TRÚC HỆ THỐNG
# ==========================================
add_styled_heading(doc, "MỤC 3. THIẾT KẾ KIẾN TRÚC HỆ THỐNG", 1)

add_styled_heading(doc, "3.1 Sơ đồ Kiến trúc Phân lớp (4 Lớp - Có chú thích)", 2)
arch_img_path = r"D:\CDTN 1\docs\architecture.png"
if os.path.exists(arch_img_path):
    p_img = doc.add_paragraph()
    p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
    doc.add_picture(arch_img_path, width=Inches(6.2))
    p_cap = doc.add_paragraph()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_c = p_cap.add_run("Hình 3.1: Sơ đồ Kiến trúc Phân lớp 4 Tầng & Repository Pattern (File gốc: docs/architecture.drawio)")
    r_c.font.size = Pt(8.5)
    r_c.font.italic = True

add_styled_heading(doc, "3.2 Ba câu Lập luận Lựa chọn Kiến trúc", 2)
add_body_p(doc, "Vì NFR1 yêu cầu danh sách phiếu chờ phân công và tải KTV hiển thị dưới 1.5 giây với 10.000 bản ghi, tôi chọn phân trang tại tầng CSDL và đánh Composite Index (technician_id, due_date ASC) trên bảng tickets thay vì tải toàn bộ phiếu về lớp trình bày rồi mới sắp xếp; đánh đổi là mỗi lần Insert/Update phiếu phải tốn thêm một khoảng chi phí ghi nhỏ để cập nhật cây Index, chấp nhận được vì tần suất đọc/truy vấn danh sách cao hơn nhiều tần suất ghi.", bold_prefix="• Câu lập luận 1 (Hiệu năng - NFR1): ")
add_body_p(doc, "Vì NFR2 yêu cầu 100% thao tác phân công phiếu (/assign, /reassign) chỉ được thực hiện bởi Quản lý trung tâm, tôi chọn kiểm tra vai trò (RBAC Middleware) và phân quyền chặt chẽ ngay tại Lớp Nghiệp vụ (AssignService) thay vì chỉ ẩn nút bấm trên giao diện người dùng; đánh đổi là mọi lời gọi hàm Service bắt buộc phải truyền kèm ngữ cảnh người dùng (user_id, role, center_id) làm tăng nhẹ độ phức tạp tham số.", bold_prefix="• Câu lập luận 2 (Bảo mật - NFR2): ")
add_body_p(doc, "Vì NFR3 yêu cầu 100% các thao tác gán phiếu, cập nhật trạng thái và lưu log lịch sử phải vẹn toàn dữ liệu, tôi chọn bao bọc các thao tác đổi phiếu và insert log trong Database Transaction tại Lớp Nghiệp vụ và giao tiếp qua Lớp Repository; đánh đổi là nếu 1 bước ghi log thất bại thì toàn bộ phiếu bị Rollback, khiến quy trình xử lý khắt khe hơn nhưng đảm bảo không bao giờ bị mất vết lịch sử.", bold_prefix="• Câu lập luận 3 (Tin cậy/Vẹn toàn - NFR3): ")

# ==========================================
# MỤC 4. MÔ HÌNH DỮ LIỆU & SQL DDL SKELETON
# ==========================================
add_styled_heading(doc, "MỤC 4. MÔ HÌNH DỮ LIỆU & SQL DDL SKELETON", 1)

add_styled_heading(doc, "4.1 Sơ đồ ERD chuẩn 3NF (7 Bảng - Đã bổ sung bảng customers theo TD-05)", 2)
erd_img_path = r"D:\CDTN 1\docs\erd.png"
if os.path.exists(erd_img_path):
    p_img = doc.add_paragraph()
    p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
    doc.add_picture(erd_img_path, width=Inches(6.2))
    p_cap = doc.add_paragraph()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_c = p_cap.add_run("Hình 4.1: Mô hình Dữ liệu Quan hệ Chuẩn 3NF (File gốc: docs/erd.drawio)")
    r_c.font.size = Pt(8.5)
    r_c.font.italic = True

add_styled_heading(doc, "4.2 Đối chiếu và Giải thích tránh 5 lỗi ERD phổ biến", 2)
add_body_p(doc, "Mọi bảng trong ERD đều nối với nhau (customers -> tickets; service_centers -> technicians -> skills -> tickets -> log / appointments). Bảng customers đã được bổ sung giải quyết hoàn toàn lỗi cô lập.", bold_prefix="• 1. Không có bảng cô lập: ")
add_body_p(doc, "Bảng ticket_status_log được thiết kế riêng để lưu vết mọi lần thay đổi trạng thái, KTV cũ/mới và lý do chuyển gán, không bị lỗi ghi đè trạng thái.", bold_prefix="• 2. Có bảng log lịch sử: ")
add_body_p(doc, "KHÔNG lưu số ngày xử lý hay trạng thái trễ hạn vào cột riêng (tính trực tiếp từ closed_at - received_at và due_date), tránh sai lệch dữ liệu.", bold_prefix="• 3. Không lưu giá trị tính toán thừa: ")
add_body_p(doc, "Đã khởi tạo Composite Index idx_tickets_technician_due trên (technician_id, due_date ASC) đáp ứng NFR1 (< 1.5s).", bold_prefix="• 4. Tạo Index phục vụ NFR1: ")
add_body_p(doc, "Tất cả các bảng dùng khóa chính nhân tạo tự tăng (SERIAL / BIGSERIAL); các mã nghiệp vụ (ticket_code, phone) chỉ đặt ràng buộc UNIQUE.", bold_prefix="• 5. Dùng khóa nhân tạo (Surrogate Key): ")

add_styled_heading(doc, "4.3 SQL DDL Skeleton (Track SE - File gốc db/schema.sql)", 2)
sql_code = (
    "-- BẢNG KHÁCH HÀNG (BỔ SUNG THEO TD-05)\n"
    "CREATE TABLE customers (\n"
    "    customer_id SERIAL PRIMARY KEY,\n"
    "    customer_code VARCHAR(30) NOT NULL UNIQUE,\n"
    "    full_name VARCHAR(100) NOT NULL,\n"
    "    phone VARCHAR(15) NOT NULL UNIQUE,\n"
    "    address TEXT, created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP\n"
    ");\n\n"
    "-- BẢNG TRUNG TÂM BẢO HÀNH\n"
    "CREATE TABLE service_centers (\n"
    "    center_id SERIAL PRIMARY KEY, center_code VARCHAR(20) NOT NULL UNIQUE,\n"
    "    center_name VARCHAR(100) NOT NULL, address TEXT NOT NULL, phone VARCHAR(15) NOT NULL\n"
    ");\n\n"
    "-- BẢNG KỸ THUẬT VIÊN & TAY NGHỀ\n"
    "CREATE TABLE technicians (\n"
    "    technician_id SERIAL PRIMARY KEY, technician_code VARCHAR(20) NOT NULL UNIQUE,\n"
    "    full_name VARCHAR(100) NOT NULL, phone VARCHAR(15) NOT NULL UNIQUE,\n"
    "    center_id INT NOT NULL REFERENCES service_centers(center_id), status VARCHAR(20) DEFAULT 'HOAT_DONG'\n"
    ");\n"
    "CREATE TABLE technician_skills (\n"
    "    technician_id INT REFERENCES technicians(technician_id) ON DELETE CASCADE,\n"
    "    issue_category VARCHAR(50) NOT NULL, proficiency INT NOT NULL CHECK (proficiency BETWEEN 1 AND 5),\n"
    "    PRIMARY KEY (technician_id, issue_category)\n"
    ");\n\n"
    "-- BẢNG PHIẾU BẢO HÀNH (CÓ FK customer_id)\n"
    "CREATE TABLE tickets (\n"
    "    ticket_id SERIAL PRIMARY KEY, ticket_code VARCHAR(30) NOT NULL UNIQUE,\n"
    "    customer_id INT NOT NULL REFERENCES customers(customer_id),\n"
    "    center_id INT NOT NULL REFERENCES service_centers(center_id),\n"
    "    technician_id INT REFERENCES technicians(technician_id),\n"
    "    issue_category VARCHAR(50) NOT NULL, priority VARCHAR(20) DEFAULT 'TRUNG_BINH',\n"
    "    status VARCHAR(30) DEFAULT 'MOI', received_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,\n"
    "    due_date TIMESTAMPTZ NOT NULL, CONSTRAINT check_due CHECK (due_date >= received_at)\n"
    ");\n\n"
    "-- BẢNG NHẬT KÝ TRẠNG THÁI & LỊCH HẸN\n"
    "CREATE TABLE ticket_status_log (\n"
    "    log_id BIGSERIAL PRIMARY KEY, ticket_id INT REFERENCES tickets(ticket_id) ON DELETE CASCADE,\n"
    "    from_status VARCHAR(30), to_status VARCHAR(30) NOT NULL, from_technician_id INT, to_technician_id INT,\n"
    "    reason TEXT, note TEXT, changed_by INT NOT NULL, changed_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP\n"
    ");\n"
    "CREATE TABLE appointments (\n"
    "    appointment_id SERIAL PRIMARY KEY, ticket_id INT REFERENCES tickets(ticket_id) ON DELETE CASCADE,\n"
    "    appointment_type VARCHAR(20) NOT NULL, appointment_date TIMESTAMPTZ NOT NULL, status VARCHAR(30) DEFAULT 'DA_XAC_NHAN'\n"
    ");\n\n"
    "-- INDEXES TỐI ƯU HIỆU NĂNG NFR1\n"
    "CREATE INDEX idx_tickets_technician_due ON tickets (technician_id, due_date ASC);\n"
    "CREATE INDEX idx_tickets_center_status ON tickets (center_id, status);\n"
    "CREATE INDEX idx_tickets_customer ON tickets (customer_id);"
)
add_code_block(doc, sql_code)

# ==========================================
# MỤC 5. WIREFRAME 3 MÀN HÌNH CHÍNH
# ==========================================
add_styled_heading(doc, "MỤC 5. WIREFRAME 3 MÀN HÌNH CHÍNH & BẢNG ĐỐI CHIẾU", 1)

add_styled_heading(doc, "5.1 Hình ảnh Wireframe 3 Màn hình chính (M1, M2, M3)", 2)
wf_img_path = r"D:\CDTN 1\docs\wireframe.png"
if os.path.exists(wf_img_path):
    p_img = doc.add_paragraph()
    p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
    doc.add_picture(wf_img_path, width=Inches(6.2))
    p_cap = doc.add_paragraph()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_c = p_cap.add_run("Hình 5.1: Wireframe 3 Màn hình chính Luồng L4 (File gốc: docs/wireframe.drawio)")
    r_c.font.size = Pt(8.5)
    r_c.font.italic = True

add_styled_heading(doc, "5.2 Bảng đối chiếu 1-1 giữa Trường trên Wireframe với CSDL và FR/US", 2)
wire_data = [
    ("M1", "Mã phiếu bảo hành", "tickets.ticket_code", "FR1, US1"),
    ("M1", "Tên & SĐT khách hàng", "customers.full_name, customers.phone", "FR1, US1, TD-05"),
    ("M1", "Tải công việc KTV (Số phiếu giữ)", "COUNT(tickets.status='DANG_XU_LY')", "FR1, US1"),
    ("M2", "Thông tin khách hàng chi tiết", "customers.full_name, customers.phone", "FR2, US2, TD-05"),
    ("M2", "KTV gợi ý & Điểm tay nghề", "technician_skills.proficiency (>=3)", "FR2, US2"),
    ("M2", "Ô lý do chuyển KTV", "ticket_status_log.reason (>=10 ký tự)", "FR3, US6, QT-08"),
    ("M2", "Hạn cam kết SLA tự sinh", "tickets.due_date", "FR2, US2, QT-04"),
    ("M3", "Khung giờ hẹn giao/nhận", "appointments.appointment_date", "FR4, US3, QT-09"),
    ("M3", "Thông báo lỗi khung giờ đầy", "--- (Hiển thị UI khi vi phạm QT-09)", "FR4, US3, AC3.2")
]
t_wire = doc.add_table(rows=len(wire_data)+1, cols=4)
t_wire.alignment = WD_TABLE_ALIGNMENT.CENTER
set_table_borders(t_wire)
format_table_header(t_wire.rows[0], ["Màn hình", "Trường / Thao tác trên Wireframe", "Cột tương ứng trong CSDL (ERD)", "Nguồn Yêu cầu (FR / US / QT)"])
for idx, (m, fld, col, src) in enumerate(wire_data, 1):
    row = t_wire.rows[idx]
    if idx % 2 == 1:
        for c in row.cells: set_cell_background(c, HEX_LIGHT_BG)
    row.cells[0].paragraphs[0].add_run(m).bold = True
    row.cells[0].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
    row.cells[1].paragraphs[0].add_run(fld)
    row.cells[2].paragraphs[0].add_run(col)
    row.cells[3].paragraphs[0].add_run(src).alignment = WD_ALIGN_PARAGRAPH.CENTER
    for c in row.cells: set_cell_margins(c); c.paragraphs[0].runs[0].font.size = Pt(8.5)

# ==========================================
# PHỤ LỤC: KHAI BÁO CÔNG CỤ AI
# ==========================================
add_styled_heading(doc, "PHỤ LỤC. BẢNG KHAI BÁO SỬ DỤNG CÔNG CỤ AI", 1)
ai_data = [
    ("Trợ lý AI (Google Antigravity)", "Mục 1 - User Stories & AC", "Gợi ý rút gọn 7 User Story cho luồng L4 phân công KTV và lịch hẹn", "Rà soát chuẩn INVEST, gộp US lịch hẹn về 7 story, kiểm chứng kịch bản ngoại lệ và gán MoSCoW."),
    ("Trợ lý AI (Google Antigravity)", "Mục 3.2 - Ba câu lập luận", "Viết 3 câu lập luận lựa chọn kiến trúc 4 lớp gắn với NFR1, NFR2, NFR3", "Chuẩn hóa đúng khuôn 'Vì NFR... đòi hỏi..., tôi chọn..., đánh đổi là...' và kiểm chứng tính khả thi."),
    ("Trợ lý AI (Google Antigravity)", "Mục 4 - ERD & SQL DDL", "Bổ sung bảng customers và khóa ngoại tickets.customer_id theo phản hồi BT1", "Kiểm tra chuẩn 3NF, thêm CHECK constraint, Composite Index trên (technician_id, due_date)."),
    ("Trợ lý AI (Google Antigravity)", "Mục 5 - Wireframe 3 Màn hình", "Bố cục layout wireframe 3 màn hình và bảng đối chiếu dữ liệu", "Đối chiếu 1-1 từng trường UI với cột CSDL và mã FR/US.")
]
t_ai = doc.add_table(rows=len(ai_data)+1, cols=4)
t_ai.alignment = WD_TABLE_ALIGNMENT.CENTER
set_table_borders(t_ai)
format_table_header(t_ai.rows[0], ["Công cụ AI", "Phần áp dụng", "Cách dùng (tóm tắt yêu cầu)", "Nội dung em đã chỉnh sửa & kiểm chứng"])
for idx, (tool, sec, usage, verification) in enumerate(ai_data, 1):
    row = t_ai.rows[idx]
    if idx % 2 == 1:
        for c in row.cells: set_cell_background(c, HEX_LIGHT_BG)
    row.cells[0].paragraphs[0].add_run(tool).bold = True
    row.cells[1].paragraphs[0].add_run(sec)
    row.cells[2].paragraphs[0].add_run(usage)
    row.cells[3].paragraphs[0].add_run(verification)
    for c in row.cells: set_cell_margins(c); c.paragraphs[0].runs[0].font.size = Pt(8.5)

p_com = doc.add_paragraph()
p_com.paragraph_format.space_before = Pt(8)
r_com = p_com.add_run(
    "Dòng cam kết bắt buộc:\n"
    "Tôi xác nhận đã đọc, hiểu và chịu trách nhiệm về toàn bộ nội dung nộp.\n"
    "Họ và tên: Nguyễn Minh Phú | MSSV: 2374802013447 | Ngày nộp: 15/10/2026"
)
r_com.bold = True
r_com.italic = True
r_com.font.size = Pt(9.5)
r_com.font.color.rgb = NAVY

# Save docx
out_docx = r"D:\CDTN 1\docs\BT1_2374802013447_NguyenMinhPhu.docx"
doc.save(out_docx)
print("SUCCESS: Updated Word document saved at", out_docx)
