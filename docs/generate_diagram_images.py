import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os

docs_dir = r"D:\CDTN 1\docs"
os.makedirs(docs_dir, exist_ok=True)

# ----------------------------------------------------------------------
# 1. USE CASE DIAGRAM (usecase.png)
# ----------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(12, 8), dpi=300)
ax.set_xlim(0, 1200)
ax.set_ylim(0, 800)
ax.axis('off')

# Title
ax.text(600, 770, "USE CASE DIAGRAM - LUỒNG L4: PHÂN CÔNG KỸ THUẬT VIÊN & LỊCH HẸN", 
        fontsize=14, fontweight='bold', ha='center', color='#1F4E78')

# System Boundary
sys_rect = patches.FancyBboxPatch((280, 70), 620, 670, boxstyle="round,pad=10", 
                                  edgecolor="#1F4E78", facecolor="#F9FBFD", linewidth=2)
ax.add_patch(sys_rect)
ax.text(310, 720, "Hệ thống: Phân công KTV & Quản lý lịch hẹn", fontsize=11, fontweight='bold', color='#1F4E78')

# Actors
def draw_actor(x, y, label):
    # Head
    head = patches.Circle((x, y+35), 15, edgecolor='#1F4E78', facecolor='#D9E1F2', linewidth=2)
    ax.add_patch(head)
    # Body
    ax.plot([x, x], [y+20, y-15], color='#1F4E78', linewidth=2)
    # Arms
    ax.plot([x-25, x+25], [y+10, y+10], color='#1F4E78', linewidth=2)
    # Legs
    ax.plot([x, x-20], [y-15, y-45], color='#1F4E78', linewidth=2)
    ax.plot([x, x+20], [y-15, y-45], color='#1F4E78', linewidth=2)
    # Label
    ax.text(x, y-65, label, fontsize=10, fontweight='bold', ha='center', color='#333333')

draw_actor(140, 480, "Quản lý\ntrung tâm")
draw_actor(1040, 360, "Kỹ thuật\nviên")
draw_actor(1040, 580, "Hệ thống SLA\n(Timer)")

# Use Cases
use_cases = [
    (590, 660, "UC1: Xem d/s chờ phân công & tải KTV", "#DAE8FC", "#6C8EBF"),
    (590, 570, "UC2: Gợi ý và phân công KTV cho phiếu", "#D5E8D4", "#82B366"),
    (590, 480, "UC3: Đặt và quản lý/dời lịch hẹn", "#FFE6CC", "#D79B00"),
    (590, 390, "UC4: Xem phiếu gán xếp theo SLA (due_date)", "#E1D5E7", "#9673A6"),
    (590, 300, "UC5: Cập nhật trạng thái phiếu & lưu log", "#E1D5E7", "#9673A6"),
    (590, 210, "UC6: Chuyển phiếu sang KTV khác (nhập lý do)", "#FFF2CC", "#D6B656"),
    (590, 120, "UC7: Tra cứu lịch sử sửa chữa (IMEI/Serial)", "#F8CECC", "#B85450")
]

for xc, yc, text, bg, border in use_cases:
    ellipse = patches.Ellipse((xc, yc), 360, 55, edgecolor=border, facecolor=bg, linewidth=1.8)
    ax.add_patch(ellipse)
    ax.text(xc, yc, text, fontsize=9.5, fontweight='bold', ha='center', va='center', color='#111111')

# Actor connections
# QLTT connects to UC1, UC2, UC3, UC6, UC7
for yc in [660, 570, 480, 210, 120]:
    ax.plot([180, 410], [480, yc], color='#555555', linewidth=1.2)

# KTV connects to UC4, UC5, UC7
for yc in [390, 300, 120]:
    ax.plot([1000, 770], [360, yc], color='#555555', linewidth=1.2)

# Timer connects to UC4, UC5
for yc in [390, 300]:
    ax.plot([1000, 770], [580, yc], color='#888888', linestyle='--', linewidth=1.2)

# <<include>> UC2 -> UC1
ax.annotate("", xy=(590, 630), xytext=(590, 600),
            arrowprops=dict(arrowstyle="->", linestyle="dashed", color="#1F4E78", lw=1.5))
ax.text(600, 615, "<<include>>", fontsize=8.5, fontstyle='italic', color='#1F4E78')

# <<extend>> UC6 -> UC2
ax.annotate("", xy=(540, 545), xytext=(540, 240),
            arrowprops=dict(arrowstyle="->", linestyle="dashed", color="#B85450", lw=1.5))
ax.text(475, 400, "<<extend>>", fontsize=8.5, fontstyle='italic', color='#B85450')

# LEGEND BOX (CHÚ THÍCH KÝ HIỆU)
leg_rect = patches.FancyBboxPatch((30, 30), 220, 170, boxstyle="square,pad=5", 
                                 edgecolor="#666666", facecolor="#FFFFFF", linewidth=1.2)
ax.add_patch(leg_rect)
ax.text(40, 185, "BẢNG CHÚ THÍCH KÝ HIỆU:", fontsize=9, fontweight='bold', color='#1F4E78')
ax.text(40, 160, "• Hình chữ nhật lớn: Ranh giới hệ thống", fontsize=8, color='#333333')
ax.text(40, 135, "• Hình người: Tác nhân ngoài (Actor)", fontsize=8, color='#333333')
ax.text(40, 110, "• Hình Oval: Trường hợp sử dụng (Use Case)", fontsize=8, color='#333333')
ax.text(40, 85, "• Đường nét liền: Tương tác giữa Actor & UC", fontsize=8, color='#333333')
ax.text(40, 60, "• Mũi tên nét đứt: <<include>> / <<extend>>", fontsize=8, color='#333333')
ax.text(40, 40, "• Timer: Tác nhân thời gian tự động", fontsize=8, color='#333333')

plt.tight_layout()
plt.savefig(os.path.join(docs_dir, "usecase.png"), dpi=300, bbox_inches='tight')
plt.close()

print("Created usecase.png")

# ----------------------------------------------------------------------
# 2. ARCHITECTURE DIAGRAM (architecture.png)
# ----------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(12, 8), dpi=300)
ax.set_xlim(0, 1200)
ax.set_ylim(0, 800)
ax.axis('off')

ax.text(600, 770, "SƠ ĐỒ KIẾN TRÚC PHÂN LỚP (LAYERED ARCHITECTURE - 4 LỚP)", 
        fontsize=14, fontweight='bold', ha='center', color='#1F4E78')

# Layer 1: Presentation
l1 = patches.FancyBboxPatch((150, 610), 900, 110, boxstyle="round,pad=8", edgecolor="#6C8EBF", facecolor="#DAE8FC", linewidth=2)
ax.add_patch(l1)
ax.text(170, 700, "1. LỚP TRÌNH BÀY (Presentation Layer) - Controllers & Views", fontsize=11, fontweight='bold', color='#1F4E78')
m_boxes = [
    (200, 630, 240, 45, "[M1: D/s chờ & Tải KTV]"),
    (480, 630, 240, 45, "[M2: Phân công & Re-assign]"),
    (760, 630, 240, 45, "[M3: Đặt & Dời lịch hẹn]")
]
for x, y, w, h, t in m_boxes:
    bx = patches.Rectangle((x, y), w, h, edgecolor="#6C8EBF", facecolor="#FFFFFF", linewidth=1.2)
    ax.add_patch(bx)
    ax.text(x+w/2, y+h/2, t, fontsize=9.5, ha='center', va='center', fontweight='bold', color='#333333')

# Arrow L1 -> L2
ax.annotate("", xy=(600, 500), xytext=(600, 600),
            arrowprops=dict(arrowstyle="->", color="#1F4E78", lw=2))
ax.text(615, 550, "HTTP REST / JSON (api-contract.md)", fontsize=9.5, fontstyle='italic', fontweight='bold', color='#1F4E78')

# Layer 2: Business / Service
l2 = patches.FancyBboxPatch((150, 390), 900, 110, boxstyle="round,pad=8", edgecolor="#D79B00", facecolor="#FFE6CC", linewidth=2)
ax.add_patch(l2)
ax.text(170, 480, "2. LỚP NGHIỆP VỤ (Business / Service Layer) - 100% Business Rules (QT-04, QT-06, QT-07, QT-08, QT-09)", 
        fontsize=10.5, fontweight='bold', color='#995400')
s_boxes = [
    (200, 410, 240, 45, "AssignService\n(Gợi ý & Phân công)"),
    (480, 410, 240, 45, "TicketService\n(Trạng thái & SLA Log)"),
    (760, 410, 240, 45, "AppointmentService\n(Đặt & Dời lịch hẹn)")
]
for x, y, w, h, t in s_boxes:
    bx = patches.Rectangle((x, y), w, h, edgecolor="#D79B00", facecolor="#FFFFFF", linewidth=1.2)
    ax.add_patch(bx)
    ax.text(x+w/2, y+h/2, t, fontsize=9, ha='center', va='center', fontweight='bold', color='#333333')

# Arrow L2 -> L3
ax.annotate("", xy=(600, 280), xytext=(600, 380),
            arrowprops=dict(arrowstyle="->", color="#1F4E78", lw=2))
ax.text(615, 330, "Gọi qua giao diện Repository (Phụ thuộc 1 chiều)", fontsize=9.5, fontstyle='italic', fontweight='bold', color='#1F4E78')

# Layer 3: Data Access
l3 = patches.FancyBboxPatch((150, 180), 900, 100, boxstyle="round,pad=8", edgecolor="#82B366", facecolor="#D5E8D4", linewidth=2)
ax.add_patch(l3)
ax.text(170, 260, "3. LỚP TRUY CẬP DỮ LIỆU (Repository Layer) - Che giấu chi tiết SQL", fontsize=10.5, fontweight='bold', color='#2D662D')
r_boxes = [
    (200, 200, 240, 40, "ITicketRepository"),
    (480, 200, 240, 40, "ITechnicianRepository"),
    (760, 200, 240, 40, "IAppointmentRepository")
]
for x, y, w, h, t in r_boxes:
    bx = patches.Rectangle((x, y), w, h, edgecolor="#82B366", facecolor="#FFFFFF", linewidth=1.2)
    ax.add_patch(bx)
    ax.text(x+w/2, y+h/2, t, fontsize=9.5, ha='center', va='center', fontweight='bold', color='#333333')

# Arrow L3 -> L4
ax.annotate("", xy=(600, 105), xytext=(600, 175),
            arrowprops=dict(arrowstyle="->", color="#1F4E78", lw=2))
ax.text(615, 140, "SQL Queries (schema.sql)", fontsize=9.5, fontstyle='italic', fontweight='bold', color='#1F4E78')

# Layer 4: Storage
l4 = patches.FancyBboxPatch((150, 15), 900, 90, boxstyle="round,pad=8", edgecolor="#9673A6", facecolor="#E1D5E7", linewidth=2)
ax.add_patch(l4)
ax.text(170, 85, "4. LỚP LƯU TRỮ (Data Store Layer) - PostgreSQL / SQLite", fontsize=10.5, fontweight='bold', color='#4C2666')
ax.text(600, 45, "Bảng CSDL: customers | service_centers | technicians | technician_skills | tickets | ticket_status_log | appointments", 
        fontsize=9.5, ha='center', fontweight='bold', color='#222222')

# Notes
ax.text(150, 2, "CHÚ THÍCH: Mũi tên chỉ chiều phụ thuộc (lớp trên gọi lớp dưới, KHÔNG gọi ngược). NGOÀI PHẠM VI (WON'T): Gửi SMS, Mua linh kiện tự động.", 
        fontsize=8.5, fontstyle='italic', color='#555555')

plt.tight_layout()
plt.savefig(os.path.join(docs_dir, "architecture.png"), dpi=300, bbox_inches='tight')
plt.close()

print("Created architecture.png")

# ----------------------------------------------------------------------
# 3. ERD DIAGRAM (erd.png) - 7 TABLES INCL. CUSTOMERS
# ----------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(13, 9), dpi=300)
ax.set_xlim(0, 1300)
ax.set_ylim(0, 900)
ax.axis('off')

ax.text(650, 875, "MÔ HÌNH DỮ LIỆU QUAN HỆ (ERD CHUẨN 3NF - 7 BẢNG)", 
        fontsize=14, fontweight='bold', ha='center', color='#1F4E78')

def draw_entity(x, y, w, h, name, pk_list, fk_list, attr_list):
    # Header
    hdr = patches.Rectangle((x, y+h-28), w, 28, edgecolor="#1F4E78", facecolor="#1F4E78")
    ax.add_patch(hdr)
    ax.text(x+w/2, y+h-14, name, fontsize=9.5, fontweight='bold', color='#FFFFFF', ha='center', va='center')
    # Body
    body = patches.Rectangle((x, y), w, h-28, edgecolor="#1F4E78", facecolor="#FFFFFF", linewidth=1.2)
    ax.add_patch(body)
    
    cur_y = y + h - 45
    for pk in pk_list:
        ax.text(x+8, cur_y, f"PK  {pk}", fontsize=8.5, fontweight='bold', color='#B85450')
        cur_y -= 18
    for fk in fk_list:
        ax.text(x+8, cur_y, f"FK  {fk}", fontsize=8.5, fontweight='bold', color='#2D662D')
        cur_y -= 18
    for attr in attr_list:
        ax.text(x+8, cur_y, f"•   {attr}", fontsize=8, color='#333333')
        cur_y -= 17

# 1. service_centers
draw_entity(50, 640, 220, 190, "service_centers", 
            ["center_id : SERIAL"], [], 
            ["center_code : VARCHAR (UQ)", "center_name : VARCHAR", "address : TEXT", "phone : VARCHAR", "created_at : TIMESTAMP"])

# 2. customers (Bổ sung theo TD-05)
draw_entity(50, 390, 220, 190, "customers", 
            ["customer_id : SERIAL"], [], 
            ["customer_code : VARCHAR (UQ)", "full_name : VARCHAR", "phone : VARCHAR (UQ)", "address : TEXT", "created_at : TIMESTAMP"])

# 3. technicians
draw_entity(390, 640, 240, 200, "technicians", 
            ["technician_id : SERIAL"], ["center_id : INT"], 
            ["technician_code : VARCHAR (UQ)", "full_name : VARCHAR", "phone : VARCHAR (UQ)", "status : VARCHAR", "created_at : TIMESTAMP"])

# 4. technician_skills
draw_entity(740, 670, 240, 150, "technician_skills", 
            ["technician_id : INT", "issue_category : VARCHAR"], [], 
            ["proficiency : INT (1-5)"])

# 5. tickets
draw_entity(380, 280, 260, 270, "tickets", 
            ["ticket_id : SERIAL"], 
            ["customer_id : INT", "center_id : INT", "technician_id : INT (Null)"], 
            ["ticket_code : VARCHAR (UQ)", "issue_category : VARCHAR", "issue_desc : TEXT", "priority : VARCHAR", "status : VARCHAR [IDX]", "received_at : TIMESTAMP", "due_date : TIMESTAMP [IDX]", "closed_at : TIMESTAMP"])

# 6. ticket_status_log
draw_entity(740, 320, 250, 220, "ticket_status_log", 
            ["log_id : BIGSERIAL"], ["ticket_id : INT"], 
            ["from_status : VARCHAR", "to_status : VARCHAR", "from_technician_id : INT", "to_technician_id : INT", "reason : TEXT", "note : TEXT", "changed_by : INT", "changed_at : TIMESTAMP"])

# 7. appointments
draw_entity(380, 50, 260, 180, "appointments", 
            ["appointment_id : SERIAL"], ["ticket_id : INT"], 
            ["appointment_type : VARCHAR", "appointment_date : TIMESTAMP", "status : VARCHAR", "notes : TEXT", "created_at : TIMESTAMP"])

# Connectors
# sc (1) -> tech (N)
ax.plot([270, 390], [740, 740], color="#1F4E78", lw=1.5)
ax.text(285, 745, "1", fontsize=8.5, fontweight='bold', color="#1F4E78")
ax.text(370, 745, "N", fontsize=8.5, fontweight='bold', color="#1F4E78")

# tech (1) -> skill (N)
ax.plot([630, 740], [740, 740], color="#1F4E78", lw=1.5)
ax.text(645, 745, "1", fontsize=8.5, fontweight='bold', color="#1F4E78")
ax.text(725, 745, "N", fontsize=8.5, fontweight='bold', color="#1F4E78")

# sc (1) -> tickets (N)
ax.plot([160, 160, 380], [640, 360, 360], color="#1F4E78", lw=1.5)
ax.text(170, 620, "1", fontsize=8.5, fontweight='bold', color="#1F4E78")
ax.text(360, 365, "N", fontsize=8.5, fontweight='bold', color="#1F4E78")

# customers (1) -> tickets (N)
ax.plot([270, 380], [480, 480], color="#1F4E78", lw=1.5)
ax.text(285, 485, "1", fontsize=8.5, fontweight='bold', color="#1F4E78")
ax.text(360, 485, "N", fontsize=8.5, fontweight='bold', color="#1F4E78")

# tech (0..1) -> tickets (N)
ax.plot([510, 510], [640, 550], color="#1F4E78", lw=1.5)
ax.text(515, 620, "1", fontsize=8.5, fontweight='bold', color="#1F4E78")
ax.text(515, 560, "N", fontsize=8.5, fontweight='bold', color="#1F4E78")

# tickets (1) -> status_log (N)
ax.plot([640, 740], [430, 430], color="#1F4E78", lw=1.5)
ax.text(655, 435, "1", fontsize=8.5, fontweight='bold', color="#1F4E78")
ax.text(725, 435, "N", fontsize=8.5, fontweight='bold', color="#1F4E78")

# tickets (1) -> appointments (N)
ax.plot([510, 510], [280, 230], color="#1F4E78", lw=1.5)
ax.text(515, 260, "1", fontsize=8.5, fontweight='bold', color="#1F4E78")
ax.text(515, 240, "N", fontsize=8.5, fontweight='bold', color="#1F4E78")

# LEGEND BOX (CHÚ THÍCH KÝ HIỆU ERD)
leg_rect = patches.FancyBboxPatch((740, 40), 250, 190, boxstyle="square,pad=5", 
                                 edgecolor="#666666", facecolor="#F9FBFD", linewidth=1.2)
ax.add_patch(leg_rect)
ax.text(750, 210, "BẢNG CHÚ THÍCH KÝ HIỆU ERD:", fontsize=9, fontweight='bold', color='#1F4E78')
ax.text(750, 185, "• PK: Khóa chính (Primary Key)", fontsize=8, color='#B85450', fontweight='bold')
ax.text(750, 160, "• FK: Khóa ngoại (Foreign Key)", fontsize=8, color='#2D662D', fontweight='bold')
ax.text(750, 135, "• UQ: Thuộc tính duy nhất (Unique)", fontsize=8, color='#333333')
ax.text(750, 110, "• [IDX]: Cột được đánh Composite Index", fontsize=8, color='#1F4E78')
ax.text(750, 85, "• Đường nối 1 - N: Quan hệ Một - Nhiều", fontsize=8, color='#333333')
ax.text(750, 60, "• Không có bảng cô lập trong mô hình", fontsize=8, color='#2D662D')

plt.tight_layout()
plt.savefig(os.path.join(docs_dir, "erd.png"), dpi=300, bbox_inches='tight')
plt.close()

print("Created erd.png")

# ----------------------------------------------------------------------
# 4. WIREFRAME 3 MÀN HÌNH (wireframe.png)
# ----------------------------------------------------------------------
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 8), dpi=300)

for ax, title, bg in zip([ax1, ax2, ax3], 
                         ["M1: Danh sách chờ & Tải KTV", "M2: Phân công & Re-assign", "M3: Đặt & Dời lịch hẹn"],
                         ["#F4F6F9", "#F4F6F9", "#F4F6F9"]):
    ax.set_xlim(0, 360)
    ax.set_ylim(0, 500)
    ax.axis('off')
    # Window Frame
    win = patches.FancyBboxPatch((10, 10), 340, 480, boxstyle="round,pad=5", edgecolor="#333333", facecolor=bg, lw=1.5)
    ax.add_patch(win)
    # Window Title bar
    tbar = patches.Rectangle((10, 455), 340, 35, facecolor="#1F4E78", edgecolor="#333333")
    ax.add_patch(tbar)
    ax.text(180, 472, title, fontsize=9.5, fontweight='bold', color="#FFFFFF", ha='center', va='center')

# M1 Content
ax1.text(25, 430, "Lọc Trung tâm: [ Trung tâm Cần Thơ V ]", fontsize=8.5, fontweight='bold', color="#1F4E78")
ax1.text(25, 395, "D/S PHIẾU CHỜ PHÂN CÔNG (MOI):", fontsize=8.5, fontweight='bold', color="#333333")
ax1.text(30, 370, "• #BH-001 | KH: Nguyễn Văn An (0901234567)", fontsize=7.5, color="#111111")
ax1.text(35, 355, "  Sự cố: Màn hình sọc xanh | Ưu tiên: CAO", fontsize=7.5, color="#555555")
ax1.text(30, 330, "• #BH-002 | KH: Trần Thị Bình (0912345678)", fontsize=7.5, color="#111111")
ax1.text(35, 315, "  Sự cố: Pin chai tụt nhanh | Ưu tiên: TB", fontsize=7.5, color="#555555")

ax1.text(25, 275, "TẢI CÔNG VIỆC KTV TRUNG TÂM:", fontsize=8.5, fontweight='bold', color="#333333")
ax1.text(30, 250, "• KTV Trần Văn Bình   | Đang giữ: 1 phiếu | Rank: 5/5", fontsize=7.5, color="#111111")
ax1.text(30, 230, "• KTV Lê Văn Cường    | Đang giữ: 2 phiếu | Rank: 3/5", fontsize=7.5, color="#111111")
ax1.text(30, 210, "• KTV Nguyễn Thị Dung | Đang giữ: 0 phiếu (Nghỉ phép)", fontsize=7.5, color="#888888")

btn_g = patches.Rectangle((30, 140), 200, 30, facecolor="#1F4E78", edgecolor="#1F4E78")
ax1.add_patch(btn_g)
ax1.text(130, 155, "Gợi ý KTV tự động (US2)", fontsize=8, fontweight='bold', color="#FFFFFF", ha='center', va='center')

# M2 Content
ax2.text(25, 430, "CHI TIẾT PHIẾU #BH-001", fontsize=9, fontweight='bold', color="#1F4E78")
ax2.text(25, 405, "• Khách hàng: Nguyễn Văn An - 0901234567", fontsize=8, color="#222222")
ax2.text(25, 385, "• Thiết bị: Samsung A52 | Lỗi: MÀN HÌNH", fontsize=8, color="#222222")
ax2.text(25, 360, "BẢNG GỢI Ý KTV (Proficiency >= 3):", fontsize=8.5, fontweight='bold', color="#333333")
ax2.text(30, 335, "[X] KTV Trần Văn Bình (Tay nghề: 5/5 - Tải: 1 phiếu)", fontsize=7.5, color="#2D662D", fontweight='bold')
ax2.text(30, 315, "[ ] KTV Lê Văn Cường (Tay nghề: 3/5 - Tải: 2 phiếu)", fontsize=7.5, color="#444444")
ax2.text(25, 280, "Hạn cam kết SLA (QT-04): 2026-10-16 (+24h)", fontsize=8, fontstyle='italic', color="#1F4E78")

ax2.text(25, 245, "CHUYỂN PHIẾU (RE-ASSIGN - US6):", fontsize=8.5, fontweight='bold', color="#B85450")
ax2.text(25, 225, "Lý do chuyển: [KTV cũ nghỉ đột xuất.........]", fontsize=7.5, color="#333333")
ax2.text(25, 205, "(Bắt buộc tối thiểu 10 ký tự - QT-08)", fontsize=7, fontstyle='italic', color="#888888")

btn_m2 = patches.Rectangle((30, 130), 160, 30, facecolor="#2D662D", edgecolor="#2D662D")
ax2.add_patch(btn_m2)
ax2.text(110, 145, "Xác nhận phân công", fontsize=8, fontweight='bold', color="#FFFFFF", ha='center', va='center')

# M3 Content
ax3.text(25, 430, "ĐẶT LỊCH HẸN CHO PHIẾU #BH-001", fontsize=8.5, fontweight='bold', color="#1F4E78")
ax3.text(25, 395, "• Loại lịch hẹn: (X) GIAO MÁY  ( ) NHẬN MÁY", fontsize=8, color="#222222")
ax3.text(25, 365, "• Ngày hẹn: [ 2026-10-16 ]", fontsize=8, color="#222222")
ax3.text(25, 335, "• Khung giờ: [ 09:30 - 10:00 V ]", fontsize=8, color="#222222")

alrt = patches.Rectangle((25, 240), 310, 65, facecolor="#F8CECC", edgecolor="#B85450")
ax3.add_patch(alrt)
ax3.text(30, 285, "CẢNH BÁO QUY TẮC LỊCH HẸN (QT-09):", fontsize=7.5, fontweight='bold', color="#900")
ax3.text(30, 265, "Khung giờ 09:30 ngày 2026-10-16 đã đầy 5/5 lịch.", fontsize=7.5, color="#900")
ax3.text(30, 250, "Đề nghị chọn khung giờ khác!", fontsize=7.5, color="#900")

ax3.text(25, 210, "Ghi chú: [Khách hẹn mang máy đến kiểm tra...]", fontsize=7.5, color="#333333")

btn_m3 = patches.Rectangle((30, 130), 150, 30, facecolor="#1F4E78", edgecolor="#1F4E78")
ax3.add_patch(btn_m3)
ax3.text(105, 145, "Lưu lịch hẹn (US3)", fontsize=8, fontweight='bold', color="#FFFFFF", ha='center', va='center')

plt.tight_layout()
plt.savefig(os.path.join(docs_dir, "wireframe.png"), dpi=300, bbox_inches='tight')
plt.close()

print("Created wireframe.png")
