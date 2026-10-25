import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn
import os
import win32com.client

doc = docx.Document()

# Margins: 0.75 inch for optimal 7-8 page fit
for section in doc.sections:
    section.top_margin = Inches(0.7)
    section.bottom_margin = Inches(0.7)
    section.left_margin = Inches(0.75)
    section.right_margin = Inches(0.75)

# Color Palette
NAVY = RGBColor(31, 78, 120)     # #1F4E78 Primary
DARK_GRAY = RGBColor(51, 51, 51) # Body text
WHITE = RGBColor(255, 255, 255)

HEX_NAVY = "1F4E78"
HEX_LIGHT_BG = "F4F6F9"
HEX_BORDER = "D9D9D9"

def set_cell_background(cell, fill_hex):
    shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    cell._tc.get_or_add_tcPr().append(shading_elm)

def set_cell_margins(cell, top=60, bottom=60, left=80, right=80):
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
        set_cell_margins(cell, top=70, bottom=70, left=70, right=70)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(header_text)
        run.bold = True
        run.font.color.rgb = WHITE
        run.font.name = "Calibri"
        run.font.size = Pt(9)

def add_styled_heading(doc, text, level):
    h = doc.add_heading(text, level=level)
    h.paragraph_format.space_before = Pt(10)
    h.paragraph_format.space_after = Pt(2)
    run = h.runs[0]
    run.font.name = "Calibri"
    if level == 1:
        run.font.size = Pt(13)
        run.font.bold = True
        run.font.color.rgb = NAVY
    elif level == 2:
        run.font.size = Pt(11)
        run.font.bold = True
        run.font.color.rgb = NAVY
    elif level == 3:
        run.font.size = Pt(10)
        run.font.bold = True
        run.font.color.rgb = DARK_GRAY
    return h

def add_styled_paragraph(doc, text="", bold_prefix=None, space_after=3):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.15
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.bold = True
        r_pre.font.name = "Calibri"
        r_pre.font.size = Pt(9.5)
        r_pre.font.color.rgb = DARK_GRAY
    if text:
        r = p.add_run(text)
        r.font.name = "Calibri"
        r.font.size = Pt(9.5)
        r.font.color.rgb = DARK_GRAY
    return p

# =============================================================================
# 1. TRANG BÌA (COVER PAGE)
# =============================================================================
p_uni = doc.add_paragraph()
p_uni.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_uni.paragraph_format.space_before = Pt(24)
p_uni.paragraph_format.space_after = Pt(2)
r_uni = p_uni.add_run("TRƯỜNG ĐẠI HỌC VĂN LANG\nKHOA CÔNG NGHỆ THÔNG TIN")
r_uni.bold = True
r_uni.font.name = "Calibri"
r_uni.font.size = Pt(13)
r_uni.font.color.rgb = NAVY

p_line = doc.add_paragraph()
p_line.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_line.paragraph_format.space_after = Pt(40)
r_l = p_line.add_run("———————————————")
r_l.font.color.rgb = NAVY

p_rep = doc.add_paragraph()
p_rep.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_rep.paragraph_format.space_after = Pt(8)
r_rep = p_rep.add_run("BÁO CÁO KẾT THÚC GIAI ĐOẠN 2 — BÀI TẬP 2\n(20% ĐIỂM HỌC PHẦN)")
r_rep.bold = True
r_rep.font.name = "Calibri"
r_rep.font.size = Pt(16)
r_rep.font.color.rgb = NAVY

p_title = doc.add_paragraph()
p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_title.paragraph_format.space_after = Pt(40)
r_title = p_title.add_run("HIỆN THỰC PROTOTYPE, TÍCH HỢP HỆ THỐNG\nVÀ KIỂM THỬ XUYÊN LỚP\n\nĐỀ TÀI: SMART CRM — MEKONG MOBILE\nLUỒNG L4: PHÂN CÔNG KỸ THUẬT VIÊN VÀ LỊCH HẸN BẢO HÀNH")
r_title.bold = True
r_title.font.name = "Calibri"
r_title.font.size = Pt(12)
r_title.font.color.rgb = DARK_GRAY

# Cover Table
t_info = doc.add_table(rows=6, cols=2)
t_info.alignment = WD_TABLE_ALIGNMENT.CENTER
t_info.autofit = False

info_data = [
    ("Họ và tên sinh viên:", "Nguyễn Minh Phú"),
    ("Mã số sinh viên (MSSV):", "2374802013447"),
    ("Lớp học phần:", "232_71ITBS40103_01 — HK261"),
    ("Chuyên ngành đào tạo (Track):", "Kỹ thuật phần mềm (Software Engineering - SE)"),
    ("Mã nguồn GitHub (Public Repo):", "https://github.com/P-HUBcode/cdtn1-NGUYEN-MINH-PHU-l4"),
    ("Phiên bản phát hành (Tag nộp bài):", "v0.2 (Commit mới nhất, verified clean clone)")
]

col_w = [Inches(2.5), Inches(4.2)]
for r_idx, (k, v) in enumerate(info_data):
    row = t_info.rows[r_idx]
    for c_idx in range(2):
        cell = row.cells[c_idx]
        cell.width = col_w[c_idx]
        set_cell_margins(cell, top=50, bottom=50, left=80, right=80)
        p = cell.paragraphs[0]
        p.paragraph_format.space_after = Pt(0)
        run = p.add_run(k if c_idx == 0 else v)
        run.font.name = "Calibri"
        run.font.size = Pt(10)
        if c_idx == 0:
            run.bold = True
            run.font.color.rgb = NAVY
        else:
            run.font.color.rgb = DARK_GRAY
            if "http" in v or "v0.2" in v:
                run.bold = True

set_table_borders(t_info, color="D9D9D9", sz="4", val="single")

p_bot = doc.add_paragraph()
p_bot.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_bot.paragraph_format.space_before = Pt(60)
r_bot = p_bot.add_run("TP. HỒ CHÍ MINH, THÁNG 10 NĂM 2026")
r_bot.font.name = "Calibri"
r_bot.font.size = Pt(10)
r_bot.font.color.rgb = NAVY
r_bot.bold = True

doc.add_page_break()

# =============================================================================
# MỤC 1. TÓM TẮT HỆ THỐNG
# =============================================================================
add_styled_heading(doc, "1. TÓM TẮT HỆ THỐNG (SYSTEM SUMMARY)", level=1)
add_styled_paragraph(
    doc,
    "Hệ thống hỗ trợ Quản lý trung tâm bảo hành phân công phiếu bảo hành cho kỹ thuật viên phù hợp dựa trên tay nghề (proficiency >= 3 theo QT-07), cùng trung tâm (QT-06) và tải công việc hiện tại; cho phép tiếp nhận đặt và quản lý lịch hẹn giao – nhận máy với khách hàng (tối đa 5 lịch/khung giờ 30 phút theo QT-09), đồng thời tự động tính toán hạn cam kết SLA (QT-04) và lưu vết toàn diện nhật ký thay đổi trạng thái (Audit Log).",
    bold_prefix="• Phạm vi nghiệp vụ luồng L4 (1 câu tóm tắt): "
)
add_styled_paragraph(
    doc,
    "Giải quyết triệt để tình trạng phân công thủ công, cảm tính và quá tải cục bộ tại các chi nhánh Mekong Mobile miền Tây; loại bỏ nguy cơ trễ hạn cam kết khách hàng thông qua cơ chế tự động hóa gợi ý và bảo đảm tính minh bạch bằng nhật ký kiểm toán.",
    bold_prefix="• Mục tiêu cốt lõi: "
)
add_styled_paragraph(
    doc,
    "Node.js (v20 LTS), Express.js 4, SQLite 3 (node:sqlite chuẩn ACID), Docker & Docker Compose v2, HTML5/CSS3/Vanilla JS theo kiến trúc Client Adapter không dùng framework nặng.",
    bold_prefix="• Ngăn xếp công nghệ đã hiện thực (Tech Stack): "
)

# =============================================================================
# MỤC 2. KIẾN TRÚC ĐÃ HIỆN THỰC
# =============================================================================
add_styled_heading(doc, "2. KIẾN TRÚC ĐÃ HIỆN THỰC (IMPLEMENTED ARCHITECTURE)", level=1)
add_styled_paragraph(
    doc,
    "Hệ thống tuân thủ nghiêm ngặt mô hình kiến trúc 3 lớp phân tầng tách bạch ranh giới trách nhiệm, đáp ứng trọn vẹn tiêu chí cốt lõi C2 của Bài tập 2:"
)

arch_bullets = [
    ("Lớp Trình bày (Presentation Layer): ", "Giao diện Web 3 màn hình M1, M2, M3 tại src/public/. Toàn bộ giao tiếp mạng được bao đóng trong API Client (src/api/client.js, src/api/ticket.api.js). Hoàn toàn không có lệnh fetch( trực tiếp trong mã view. Bộ điều khiển ticketController.js chỉ làm nhiệm vụ parse HTTP request, gọi Service và trả về JSON chuẩn."),
    ("Lớp Nghiệp vụ (Business Service Layer): ", "src/services/ticketService.js hoàn toàn độc lập với giao thức HTTP (không chứa req, res, hay mã HTTP status). Đóng gói 100% logic của các quy tắc: QT-04 (SLA), QT-06 (Trung tâm), QT-07 (Tay nghề >= 3), QT-08 (Lý do chuyển gán >= 10 ký tự), QT-09 (Tải lịch hẹn <= 5). Khi vi phạm, Service ném LoiNghiepVu mang mã máy đọc và thông điệp tiếng Việt."),
    ("Lớp Truy cập Dữ liệu (Repository Layer): ", "src/repositories/ticketRepository.js phụ trách 100% câu truy vấn SQL trên SQLite. Dịch toàn bộ lỗi kỹ thuật hạ tầng thành LoiTruyCapDuLieu. Tuyệt đối không chứa mã HTTP và không log tại đây."),
    ("Logging tập trung & Xử lý lỗi xuyên lớp (Buổi 11): ", "src/errors.js, src/utils/logger.js và src/middleware/errorHandler.js. Ghi log JSON có cấu trúc ra stdout, tự động khử độc (Data Redaction) che giấu password, token, SĐT; gán requestId duy nhất theo dõi xuyên suốt.")
]
for pfx, txt in arch_bullets:
    add_styled_paragraph(doc, txt, bold_prefix=f"• {pfx}")

# =============================================================================
# MỤC 3. MODULE CỐT LÕI (KÈM ẢNH CHỤP CHẠY THẬT)
# =============================================================================
add_styled_heading(doc, "3. MODULE CỐT LÕI (CORE MODULE EXECUTION)", level=1)
add_styled_paragraph(
    doc,
    "Module cốt lõi của Luồng L4 đã được hiện thực đầy đủ cho 2 thực thể chính (Tickets và Appointments) cùng các thực thể liên quan (Customers, Technicians, ServiceCenters, TicketStatusLog) đảm bảo trọn vẹn CRUD, tuân thủ mô hình CSDL quan hệ 7 bảng chuẩn 3NF:"
)

crud_items = [
    ("Quản lý Phiếu bảo hành (Tickets): ", "Tiếp nhận tạo mới (POST /api/v1/tickets), tra cứu lọc theo chi nhánh/trạng thái (GET /api/v1/tickets), xem chi tiết (GET /api/v1/tickets/:id), gợi ý phân công KTV (POST /api/v1/tickets/:id/assign) và chuyển gán (POST /api/v1/tickets/:id/reassign)."),
    ("Quản lý Lịch hẹn (Appointments): ", "Lấy danh sách lịch hẹn của phiếu (GET /api/v1/tickets/:id/appointments), đặt lịch hẹn giao - nhận máy (POST /api/v1/tickets/:id/appointments) kèm kiểm soát tải 30 phút theo QT-09."),
    ("Truy vết Lịch sử (Audit Log): ", "Tự động ghi nhận mọi sự kiện chuyển trạng thái và thay đổi KTV vào bảng ticket_status_log với đầy đủ thời điểm, người thực hiện và lý do nghiệp vụ.")
]
for pfx, txt in crud_items:
    add_styled_paragraph(doc, txt, bold_prefix=f"• {pfx}")

p_cap1 = add_styled_paragraph(doc, "Hình 3.1: Minh chứng chạy thực tế Module cốt lõi qua kiểm thử tích hợp API (Sprint 1 & Sprint 2)", bold_prefix="Minh chứng chạy thật: ")
p_cap1.runs[0].font.color.rgb = NAVY

img_core = r"D:\CDTN 1\docs\screenshots\api_test_result.png"
if os.path.exists(img_core):
    doc.add_picture(img_core, width=Inches(6.5))
    doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER

# =============================================================================
# MỤC 4. BỘ KIỂM THỬ (KÈM ẢNH CHỤP TEST PASS 100%)
# =============================================================================
add_styled_heading(doc, "4. BỘ KIỂM THỬ TỰ ĐỘNG (AUTOMATED TEST SUITE)", level=1)
add_styled_paragraph(
    doc,
    "Hệ thống tích hợp bộ 22 Unit Tests tự động thực thi qua lệnh 'npm test' (sử dụng thư viện chuẩn node:test & node:assert/strict). Bộ test bao phủ trọn vẹn 3 nhóm tiêu chuẩn của Bài tập 2 (tiêu chí C4) và nhóm Regression Tests cho Bug Log (Buổi 11):"
)

# Table for test coverage
t_test = doc.add_table(rows=5, cols=4)
t_test.alignment = WD_TABLE_ALIGNMENT.CENTER
t_test.autofit = False

test_headers = ["Nhóm kiểm thử", "Số lượng", "Quy tắc kiểm tra", "Kết quả thực tế"]
format_table_header(t_test.rows[0], test_headers)

test_rows_data = [
    ("1. Luồng đúng (Happy Path)", "6 tests", "SLA CAO/TRUNG_BINH/THAP; KTV hợp lệ 5/5; Lý do chuyển gán chuẩn; Slot hẹn 2/5", "PASS (100%)"),
    ("2. Trường hợp Biên (Boundary)", "4 tests", "Tay nghề đúng bằng 3 (QT-07); Lý do đúng 10 ký tự (QT-08); Khung giờ hẹn đúng 4/5 (QT-09)", "PASS (100%)"),
    ("3. Dữ liệu sai & Ngoại lệ", "7 tests", "Priority sai; ngày rỗng; KTV tay nghề < 3; KTV khác chi nhánh; KTV nghỉ; Lý do < 10 ký tự; Slot đầy 5/5", "PASS (100%)"),
    ("4. Test hồi quy (Bug Log)", "5 tests", "BUG-001 (LY_DO_QUA_NGAN); BUG-002 (LICH_HEN_QUA_TAI); BUG-003 (KTV_KHAC_TRUNG_TAM); BUG-004 (toTicketView)", "PASS (100%)")
]

col_w_test = [Inches(1.8), Inches(0.8), Inches(3.2), Inches(1.0)]
for r_idx, r_data in enumerate(test_rows_data):
    row = t_test.rows[r_idx + 1]
    bg_color = HEX_LIGHT_BG if r_idx % 2 == 1 else "FFFFFF"
    for c_idx, val in enumerate(r_data):
        cell = row.cells[c_idx]
        cell.width = col_w_test[c_idx]
        set_cell_background(cell, bg_color)
        set_cell_margins(cell, top=50, bottom=50, left=60, right=60)
        p = cell.paragraphs[0]
        p.paragraph_format.space_after = Pt(0)
        run = p.add_run(val)
        run.font.name = "Calibri"
        run.font.size = Pt(8.5)
        if c_idx == 3:
            run.bold = True
            run.font.color.rgb = RGBColor(39, 201, 63)
        elif c_idx == 0:
            run.bold = True

set_table_borders(t_test, color="D9D9D9", sz="4", val="single")

p_cap2 = add_styled_paragraph(doc, "Hình 4.1: Minh chứng chạy thành công 22/22 Unit Tests (100% PASS) qua lệnh 'npm test'", bold_prefix="Minh chứng kết quả Test: ")
p_cap2.runs[0].font.color.rgb = NAVY

img_test = r"D:\CDTN 1\docs\screenshots\buoi11_unit_tests.png"
if os.path.exists(img_test):
    doc.add_picture(img_test, width=Inches(6.5))
    doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER

# =============================================================================
# MỤC 5. TRÌNH BÀY KẾT QUẢ & 3 TRẠNG THÁI GIAO DIỆN
# =============================================================================
add_styled_heading(doc, "5. TRÌNH BÀY KẾT QUẢ & BA TRẠNG THÁI GIAO DIỆN", level=1)
add_styled_paragraph(
    doc,
    "Giao diện Frontend được hiện thực đúng theo Wireframe BT1 gồm 3 màn hình tương tác thực tế kết nối API backend, xử lý trọn vẹn 3 trạng thái dữ liệu (tiêu chí S4 & C7):"
)

ui_screens = [
    ("Màn hình M1 (Danh sách chờ tiếp nhận & Tải KTV): ", "Bộ lọc theo Chi nhánh và Trạng thái; bảng danh sách phiếu hiển thị đầy đủ thông tin khách hàng, sự cố, hạn SLA; bảng theo dõi tải công việc hiện hành của từng KTV; nút thao tác 'Tiếp nhận phiếu mới' và 'Khôi phục mẫu MOI'."),
    ("Màn hình M2 (Chi tiết phiếu & Gợi ý phân công / Re-assign): ", "Hiển thị chi tiết thông tin sự cố, khách hàng, SLA; tự động gợi ý danh sách KTV cùng trung tâm có tay nghề >= 3 xếp tăng dần theo số phiếu đang xử lý; hỗ trợ phân công mới và chuyển gán (Re-assign) bắt buộc nhập lý do >= 10 ký tự; kèm bảng Audit Log truy vết."),
    ("Màn hình M3 (Đặt và dời lịch hẹn giao – nhận máy): ", "Cho phép hẹn giao/nhận máy; tự động kiểm tra tải khung giờ 30 phút theo QT-09, từ chối khi đã đủ 5 lịch; hiển thị danh sách lịch hẹn hiện có của phiếu."),
    ("Bao đóng 3 trạng thái (DataState Component): ", "Cài đặt tại src/public/js/components/DataState.js gồm: (1) Đang tải (Loading Spinner); (2) Danh sách rỗng (Empty Icon); (3) Lỗi kết nối (Error Banner màu đỏ kèm mã requestId và nút 'Thử lại ngay - Retry'). Ngoài ra, nút 'Thử mã 401' kiểm chứng cơ chế tự động xóa token và chuyển về modal đăng nhập.")
]
for pfx, txt in ui_screens:
    add_styled_paragraph(doc, txt, bold_prefix=f"• {pfx}")

p_cap3 = add_styled_paragraph(doc, "Hình 5.1: Minh chứng thành phần DataState xử lý trọn vẹn 3 trạng thái (Đang tải, Rỗng, Lỗi kèm Thử lại)", bold_prefix="Minh chứng 3 trạng thái: ")
p_cap3.runs[0].font.color.rgb = NAVY

img_ds = r"D:\CDTN 1\docs\screenshots\buoi11_datastate_3states.png"
if os.path.exists(img_ds):
    doc.add_picture(img_ds, width=Inches(6.5))
    doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER

# =============================================================================
# MỤC 6. CÁCH DỰNG LẠI HỆ THỐNG
# =============================================================================
add_styled_heading(doc, "6. CÁCH DỰNG LẠI HỆ THỐNG (REPRODUCIBILITY GUIDE)", level=1)
add_styled_paragraph(
    doc,
    "Tuân thủ nguyên tắc TÁI LẬP ĐƯỢC của học phần: người chấm clone về thư mục mới và chạy đúng các bước sau là ra chính xác kết quả. Tệp khóa package-lock.json đã được commit đầy đủ."
)

add_styled_paragraph(doc, "Cách 1: Chạy trực tiếp trên máy cục bộ (Node.js 20 LTS)", bold_prefix="6.1. ")
steps_code = [
    "git clone --branch v0.2 https://github.com/P-HUBcode/cdtn1-NGUYEN-MINH-PHU-l4.git",
    "cd cdtn1-NGUYEN-MINH-PHU-l4",
    "npm ci                     # Cài đặt chính xác các gói đã khóa phiên bản",
    "cp .env.example .env        # Tạo tệp cấu hình môi trường",
    "npm test                   # Chạy 22 Unit Tests (PASS 100%)",
    "npm run test:e2e           # Chạy kịch bản tích hợp toàn luồng",
    "npm start                  # Khởi chạy server tại http://localhost:3000"
]
for sc in steps_code:
    p_code = doc.add_paragraph()
    p_code.paragraph_format.left_indent = Inches(0.3)
    p_code.paragraph_format.space_after = Pt(2)
    r_c = p_code.add_run(sc)
    r_c.font.name = "Consolas"
    r_c.font.size = Pt(8.5)
    r_c.font.color.rgb = NAVY

add_styled_paragraph(doc, "Cách 2: Đóng gói và chạy bằng Docker Compose (≤ 2 lệnh từ máy sạch — Buổi 11)", bold_prefix="6.2. ")
docker_steps = [
    "cp .env.example .env        # Bước 1: Khởi tạo biến môi trường",
    "docker compose up -d --build # Bước 2: Dựng image và chạy container ở chế độ nền"
]
for ds in docker_steps:
    p_code = doc.add_paragraph()
    p_code.paragraph_format.left_indent = Inches(0.3)
    p_code.paragraph_format.space_after = Pt(2)
    r_c = p_code.add_run(ds)
    r_c.font.name = "Consolas"
    r_c.font.size = Pt(8.5)
    r_c.font.color.rgb = NAVY

p_cap4 = add_styled_paragraph(doc, "Hình 6.1: Minh chứng hệ thống đóng gói chạy bằng Docker Compose và kiểm tra Healthcheck healthy", bold_prefix="Minh chứng Docker: ")
p_cap4.runs[0].font.color.rgb = NAVY

img_dk = r"D:\CDTN 1\docs\screenshots\buoi11_docker_compose.png"
if os.path.exists(img_dk):
    doc.add_picture(img_dk, width=Inches(6.5))
    doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER

# =============================================================================
# MỤC 7. THAY ĐỔI SO VỚI BÀI TẬP 1
# =============================================================================
add_styled_heading(doc, "7. THAY ĐỔI SO VỚI BÀI TẬP 1 (DESIGN CHANGE LOG)", level=1)
add_styled_paragraph(
    doc,
    "Toàn bộ 10 quyết định thay đổi thiết kế (TD-01 đến TD-10) đã được ghi chép và lưu vết chi tiết trong tệp docs/thay-doi-thiet-ke.md:"
)

# Table for Design Changes
t_td = doc.add_table(rows=11, cols=4)
t_td.alignment = WD_TABLE_ALIGNMENT.CENTER
t_td.autofit = False

td_headers = ["Mã TD", "Giai đoạn", "Nội dung phản hồi / Yêu cầu cải tiến", "Kết quả thực hiện"]
format_table_header(t_td.rows[0], td_headers)

td_data = [
    ("TD-01", "Sau BT1", "File PDF không có hình; trang 14 bị trắng", "Chèn ảnh sơ đồ độ phân giải cao; xóa 100% trang trắng"),
    ("TD-02", "Sau BT1", "usecase.drawio và erd.drawio thiếu bảng chú thích (Legend)", "Bổ sung khung chú thích ký hiệu chuẩn trực tiếp vào file vẽ"),
    ("TD-03", "Sau BT1", "Có 8 User Story, đề bài yêu cầu phạm vi 5-7", "Gộp US3 & US8 thành đúng 7 User Story (5 MUST, 2 SHOULD)"),
    ("TD-04", "Sau BT1", "Luồng ngoại lệ 9a của UC2 tham chiếu bước 9, luồng chính có 7 bước", "Chuẩn hóa bảng UC2 đủ 9 bước tuần tự khớp hoàn toàn 9a"),
    ("TD-05", "Sau BT1", "tickets.customer_id không nối tới bảng nào; wireframe có tên khách", "Thêm bảng thực thể customers chuẩn 3NF và khóa ngoại liên kết"),
    ("TD-06", "Sau BT1", "Dòng cam kết liêm chính AI thiếu họ tên, MSSV, ngày", "Bổ sung đầy đủ thông tin định danh vào cuối mọi tài liệu nộp"),
    ("TD-07", "Sau BT1", "Repo nằm lồng trong thư mục con, thiếu .gitignore, README trống", "Đưa mã nguồn ra thư mục gốc, bổ sung .gitignore, README chuẩn"),
    ("TD-08", "Sprint 2", "Tích hợp Frontend 3 màn hình, API Client, DataState, 17 Unit Tests", "Hoàn thiện Web UI, tách client.js, bọc 3 trạng thái, test PASS"),
    ("TD-09", "Buổi 11", "Logging có cấu trúc, Redaction dữ liệu nhạy cảm, lỗi xuyên lớp", "Tạo logger JSON, requestId, errorHandler, toTicketView, 22 tests"),
    ("TD-10", "Buổi 11-12", "Đóng gói Dockerfile tối ưu cache và docker-compose.yml", "Tạo Dockerfile node:20-alpine, .dockerignore, compose có volume")
]

col_w_td = [Inches(0.7), Inches(0.9), Inches(3.2), Inches(2.1)]
for r_idx, r_data in enumerate(td_data):
    row = t_td.rows[r_idx + 1]
    bg_color = HEX_LIGHT_BG if r_idx % 2 == 1 else "FFFFFF"
    for c_idx, val in enumerate(r_data):
        cell = row.cells[c_idx]
        cell.width = col_w_td[c_idx]
        set_cell_background(cell, bg_color)
        set_cell_margins(cell, top=40, bottom=40, left=50, right=50)
        p = cell.paragraphs[0]
        p.paragraph_format.space_after = Pt(0)
        run = p.add_run(val)
        run.font.name = "Calibri"
        run.font.size = Pt(8.5)
        if c_idx == 0:
            run.bold = True
            run.font.color.rgb = NAVY

set_table_borders(t_td, color="D9D9D9", sz="4", val="single")

# =============================================================================
# PHỤ LỤC. BẢNG KHAI BÁO SỬ DỤNG CÔNG CỤ AI
# =============================================================================
add_styled_heading(doc, "PHỤ LỤC. BẢNG KHAI BÁO SỬ DỤNG CÔNG CỤ AI (BẮT BUỘC)", level=1)
add_styled_paragraph(
    doc,
    "Tuân thủ chính sách liêm chính học thuật của Trường Đại học Văn Lang và hướng dẫn của Buổi 1, sinh viên công khai minh bạch toàn bộ các tác vụ có sự hỗ trợ của công cụ AI:"
)

t_ai = doc.add_table(rows=7, cols=4)
t_ai.alignment = WD_TABLE_ALIGNMENT.CENTER
t_ai.autofit = False

ai_headers = ["STT", "Công cụ AI", "Phần áp dụng & Yêu cầu", "Nội dung SV chỉnh sửa & kiểm chứng"]
format_table_header(t_ai.rows[0], ai_headers)

ai_rows_data = [
    ("1", "Google Antigravity", "Phân tích yêu cầu & User Story (BT1 & BT2)", "Rà soát chuẩn INVEST, gộp về đúng 7 User Story, bổ sung 3 ca ngoại lệ cụ thể."),
    ("2", "Google Antigravity", "Thiết kế Kiến trúc & ERD 3NF (BT1 & Sprint 1)", "Chuẩn hóa 3 câu lập luận kiến trúc theo NFR; tự kiểm 3NF và bổ sung composite index."),
    ("3", "Google Antigravity", "Giao diện Frontend & API Client (Buổi 10)", "Tách client.js và ticket.api.js, xóa 100% lệnh fetch trong view, bắt mã 401 tự động."),
    ("4", "Google Antigravity", "Logging có cấu trúc & Xử lý lỗi (Buổi 11)", "Tạo logger JSON, requestId, errorHandler, khử độc password/token/SĐT nhạy cảm."),
    ("5", "Google Antigravity", "Đóng gói Docker & Docker Compose (Buổi 11-12)", "Cấu hình Dockerfile tối ưu cache, .dockerignore bảo mật, compose volume CSDL."),
    ("6", "Google Antigravity", "Bộ kiểm thử tự động & Bug Log (Buổi 10-12)", "Viết 22 unit tests (Happy path, Biên, Ngoại lệ, Hồi quy) & E2E; lập Bug Log 4 bước.")
]

col_w_ai = [Inches(0.4), Inches(1.4), Inches(2.5), Inches(2.6)]
for r_idx, r_data in enumerate(ai_rows_data):
    row = t_ai.rows[r_idx + 1]
    bg_color = HEX_LIGHT_BG if r_idx % 2 == 1 else "FFFFFF"
    for c_idx, val in enumerate(r_data):
        cell = row.cells[c_idx]
        cell.width = col_w_ai[c_idx]
        set_cell_background(cell, bg_color)
        set_cell_margins(cell, top=45, bottom=45, left=50, right=50)
        p = cell.paragraphs[0]
        p.paragraph_format.space_after = Pt(0)
        run = p.add_run(val)
        run.font.name = "Calibri"
        run.font.size = Pt(8.5)
        if c_idx == 0:
            run.bold = True
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER

set_table_borders(t_ai, color="D9D9D9", sz="4", val="single")

p_com = doc.add_paragraph()
p_com.paragraph_format.space_before = Pt(12)
p_com.paragraph_format.space_after = Pt(2)
r_com_title = p_com.add_run("Cam kết liêm chính học thuật:\n")
r_com_title.bold = True
r_com_title.font.name = "Calibri"
r_com_title.font.size = Pt(9.5)
r_com_title.font.color.rgb = NAVY

r_com_body = p_com.add_run(
    "\"Tôi xác nhận đã đọc, hiểu và chịu trách nhiệm về toàn bộ nội dung nộp. "
    "Mọi dòng mã, cấu hình và báo cáo đều được tôi trực tiếp kiểm chứng, hiểu rõ logic hoạt động và sẵn sàng giải thích chi tiết trước Giảng viên tại buổi đánh giá.\"\n\n"
    "• Họ và tên sinh viên: Nguyễn Minh Phú\n"
    "• Mã số sinh viên (MSSV): 2374802013447\n"
    "• Ngày hoàn thành: 26/10/2026"
)
r_com_body.font.name = "Calibri"
r_com_body.font.size = Pt(9.5)
r_com_body.font.color.rgb = DARK_GRAY

# Lưu tài liệu Word
out_docx = r"D:\CDTN 1\docs\BT2_2374802013447_NguyenMinhPhu.docx"
out_pdf = r"D:\CDTN 1\docs\BT2_2374802013447_NguyenMinhPhu.pdf"

doc.save(out_docx)
print("Saved DOCX:", out_docx)

# Chuyển đổi sang PDF bằng Word COM Interface
word = win32com.client.Dispatch("Word.Application")
word.Visible = False

try:
    wdoc = word.Documents.Open(os.path.abspath(out_docx))
    wdoc.SaveAs(os.path.abspath(out_pdf), FileFormat=17) # 17 = wdFormatPDF
    page_count = wdoc.ComputeStatistics(2) # 2 = wdStatisticPages
    wdoc.Close()
    print(f"SUCCESS: Exported PDF with {page_count} pages at {out_pdf}")
except Exception as e:
    print("Error during conversion:", e)
finally:
    word.Quit()
