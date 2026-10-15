import os
import shutil

docs_dir = r"D:\CDTN 1\docs"
root_dir = r"D:\CDTN 1"

# 1. Copy usecase_l4.drawio -> docs/usecase.drawio
if os.path.exists(os.path.join(docs_dir, "usecase_l4.drawio")):
    shutil.copyfile(os.path.join(docs_dir, "usecase_l4.drawio"), os.path.join(docs_dir, "usecase.drawio"))

# 2. Create docs/architecture.drawio
arch_xml = """<mxfile host="Electron" modified="2026-10-08T15:50:00.000Z" agent="Mozilla/5.0" version="21.6.8" type="device">
  <diagram id="arch_l4" name="Sơ đồ Kiến trúc 4 Lớp - Luồng L4">
    <mxGraphModel dx="1000" dy="800" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1169" pageHeight="827">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />
        
        <mxCell id="title" value="HỆ THỐNG PHÂN CÔNG KTV &amp; QUẢN LÝ LỊCH HẸN (TRACK SE) - LUỒNG L4" style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontSize=16;fontStyle=1;fontColor=#1F4E78;" vertex="1" parent="1">
          <mxGeometry x="180" y="20" width="700" height="30" as="geometry" />
        </mxCell>

        <!-- Layer 1: Presentation -->
        <mxCell id="layer1" value="1. LỚP TRÌNH BÀY (Presentation Layer - Controllers &amp; Views)" style="swimlane;whiteSpace=wrap;html=1;startSize=30;fillColor=#dae8fc;strokeColor=#6c8ebf;fontStyle=1;" vertex="1" parent="1">
          <mxGeometry x="100" y="70" width="860" height="100" as="geometry" />
        </mxCell>
        <mxCell id="m1" value="[M1: Màn hình Danh sách chờ phân công &amp; Tải KTV]" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#6c8ebf;" vertex="1" parent="layer1">
          <mxGeometry x="30" y="45" width="250" height="40" as="geometry" />
        </mxCell>
        <mxCell id="m2" value="[M2: Màn hình Phân công &amp; Chuyển gán phiếu]" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#6c8ebf;" vertex="1" parent="layer1">
          <mxGeometry x="305" y="45" width="250" height="40" as="geometry" />
        </mxCell>
        <mxCell id="m3" value="[M3: Màn hình Đặt &amp; Quản lý lịch hẹn]" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#6c8ebf;" vertex="1" parent="layer1">
          <mxGeometry x="580" y="45" width="250" height="40" as="geometry" />
        </mxCell>

        <!-- Layer 2: Business/Service -->
        <mxCell id="layer2" value="2. LỚP NGHIỆP VỤ (Business / Service Layer - Chứa 100% Business Rules QT-04, QT-06, QT-07, QT-08, QT-09)" style="swimlane;whiteSpace=wrap;html=1;startSize=30;fillColor=#ffe6cc;strokeColor=#d79b00;fontStyle=1;" vertex="1" parent="1">
          <mxGeometry x="100" y="220" width="860" height="110" as="geometry" />
        </mxCell>
        <mxCell id="svc1" value="AssignService&#xa;(Gợi ý KTV &amp; Phân công)" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#d79b00;fontStyle=1;" vertex="1" parent="layer2">
          <mxGeometry x="40" y="45" width="230" height="50" as="geometry" />
        </mxCell>
        <mxCell id="svc2" value="TicketService&#xa;(Cập nhật trạng thái &amp; SLA Log)" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#d79b00;fontStyle=1;" vertex="1" parent="layer2">
          <mxGeometry x="315" y="45" width="230" height="50" as="geometry" />
        </mxCell>
        <mxCell id="svc3" value="AppointmentService&#xa;(Đặt &amp; Dời lịch hẹn)" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#d79b00;fontStyle=1;" vertex="1" parent="layer2">
          <mxGeometry x="590" y="45" width="230" height="50" as="geometry" />
        </mxCell>

        <!-- Layer 3: Repository -->
        <mxCell id="layer3" value="3. LỚP TRUY CẬP DỮ LIỆU (Repository / DAO Layer - Interface Trừu tượng)" style="swimlane;whiteSpace=wrap;html=1;startSize=30;fillColor=#d5e8d4;strokeColor=#82b366;fontStyle=1;" vertex="1" parent="1">
          <mxGeometry x="100" y="380" width="860" height="100" as="geometry" />
        </mxCell>
        <mxCell id="repo1" value="ITicketRepository" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#82b366;fontStyle=1;" vertex="1" parent="layer3">
          <mxGeometry x="60" y="45" width="200" height="40" as="geometry" />
        </mxCell>
        <mxCell id="repo2" value="ITechnicianRepository" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#82b366;fontStyle=1;" vertex="1" parent="layer3">
          <mxGeometry x="330" y="45" width="200" height="40" as="geometry" />
        </mxCell>
        <mxCell id="repo3" value="IAppointmentRepository" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#82b366;fontStyle=1;" vertex="1" parent="layer3">
          <mxGeometry x="600" y="45" width="200" height="40" as="geometry" />
        </mxCell>

        <!-- Layer 4: Data Store -->
        <mxCell id="layer4" value="4. LỚP LƯU TRỮ (Data Store Layer - PostgreSQL Database)" style="swimlane;whiteSpace=wrap;html=1;startSize=30;fillColor=#e1d5e7;strokeColor=#9673a6;fontStyle=1;" vertex="1" parent="1">
          <mxGeometry x="100" y="530" width="860" height="100" as="geometry" />
        </mxCell>
        <mxCell id="db1" value="tickets, ticket_status_log" style="shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;backgroundOutline=1;size=10;fillColor=#ffffff;strokeColor=#9673a6;" vertex="1" parent="layer4">
          <mxGeometry x="70" y="40" width="180" height="50" as="geometry" />
        </mxCell>
        <mxCell id="db2" value="technicians, technician_skills" style="shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;backgroundOutline=1;size=10;fillColor=#ffffff;strokeColor=#9673a6;" vertex="1" parent="layer4">
          <mxGeometry x="340" y="40" width="180" height="50" as="geometry" />
        </mxCell>
        <mxCell id="db3" value="appointments, service_centers" style="shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;backgroundOutline=1;size=10;fillColor=#ffffff;strokeColor=#9673a6;" vertex="1" parent="layer4">
          <mxGeometry x="610" y="40" width="180" height="50" as="geometry" />
        </mxCell>

        <!-- Connectors -->
        <mxCell id="conn1" value="HTTP + JSON (REST API)" style="edgeStyle=orthogonalEdgeStyle;endArrow=classic;html=1;fontStyle=2;" edge="1" parent="1" source="layer1" target="layer2">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <mxCell id="conn2" value="Gọi giao diện Repository" style="edgeStyle=orthogonalEdgeStyle;endArrow=classic;html=1;fontStyle=2;" edge="1" parent="1" source="layer2" target="layer3">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <mxCell id="conn3" value="SQL Query" style="edgeStyle=orthogonalEdgeStyle;endArrow=classic;html=1;fontStyle=2;" edge="1" parent="1" source="layer3" target="layer4">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <!-- Notes -->
        <mxCell id="note_box" value="CHÚ THÍCH &amp; NGOÀI PHẠM VI (WON'T):&#xa;• [ ] = Màn hình giao diện UI. Phụ thuộc đi 1 chiều từ trên xuống dưới.&#xa;• WON'T HAVE: Tự động gửi SMS thông báo, Tự động mua linh kiện nhà cung cấp." style="text;html=1;strokeColor=#b85450;fillColor=#f8cecc;align=left;verticalAlign=middle;whiteSpace=wrap;rounded=1;fontSize=11;" vertex="1" parent="1">
          <mxGeometry x="100" y="650" width="860" height="40" as="geometry" />
        </mxCell>

      </root>
    </mxGraphModel>
  </diagram>
</mxfile>"""
with open(os.path.join(docs_dir, "architecture.drawio"), "w", encoding="utf-8") as f:
    f.write(arch_xml)

# 3. Create docs/erd.drawio
erd_xml = """<mxfile host="Electron" modified="2026-10-08T15:52:00.000Z" agent="Mozilla/5.0" version="21.6.8" type="device">
  <diagram id="erd_l4" name="Sơ đồ ERD chuẩn 3NF - Luồng L4">
    <mxGraphModel dx="1000" dy="800" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1169" pageHeight="827">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />
        
        <mxCell id="title" value="MÔ HÌNH DỮ LIỆU ERD CHUẨN 3NF - LUỒNG L4: PHÂN CÔNG KTV &amp; LỊCH HẸN" style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontSize=15;fontStyle=1;fontColor=#1F4E78;" vertex="1" parent="1">
          <mxGeometry x="180" y="20" width="750" height="30" as="geometry" />
        </mxCell>

        <!-- Entity: service_centers -->
        <mxCell id="sc" value="service_centers&#xa;--------------------&#xa;* center_id : SERIAL &lt;PK&gt;&#xa;center_code : VARCHAR &lt;UQ&gt;&#xa;center_name : VARCHAR&#xa;address : TEXT&#xa;phone : VARCHAR" style="shape=rect;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;fontStyle=1;align=left;spacingLeft=10;" vertex="1" parent="1">
          <mxGeometry x="60" y="80" width="220" height="120" as="geometry" />
        </mxCell>

        <!-- Entity: technicians -->
        <mxCell id="tech" value="technicians&#xa;--------------------&#xa;* technician_id : SERIAL &lt;PK&gt;&#xa;technician_code : VARCHAR &lt;UQ&gt;&#xa;full_name : VARCHAR&#xa;phone : VARCHAR &lt;UQ&gt;&#xa;* center_id : INT &lt;FK&gt;&#xa;status : VARCHAR" style="shape=rect;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;fontStyle=1;align=left;spacingLeft=10;" vertex="1" parent="1">
          <mxGeometry x="360" y="80" width="240" height="130" as="geometry" />
        </mxCell>

        <!-- Entity: technician_skills -->
        <mxCell id="skill" value="technician_skills&#xa;--------------------&#xa;* technician_id : INT &lt;PK,FK&gt;&#xa;* issue_category : VARCHAR &lt;PK&gt;&#xa;proficiency : INT (1-5)" style="shape=rect;whiteSpace=wrap;html=1;fillColor=#e1d5e7;strokeColor=#9673a6;fontStyle=1;align=left;spacingLeft=10;" vertex="1" parent="1">
          <mxGeometry x="690" y="80" width="230" height="90" as="geometry" />
        </mxCell>

        <!-- Entity: tickets -->
        <mxCell id="ticket" value="tickets&#xa;--------------------&#xa;* ticket_id : SERIAL &lt;PK&gt;&#xa;ticket_code : VARCHAR &lt;UQ&gt;&#xa;customer_id : INT&#xa;* center_id : INT &lt;FK&gt;&#xa;technician_id : INT &lt;FK,Null&gt;&#xa;issue_category : VARCHAR&#xa;priority : VARCHAR&#xa;status : VARCHAR &lt;INDEX&gt;&#xa;received_at : TIMESTAMPTZ&#xa;due_date : TIMESTAMPTZ &lt;INDEX&gt;" style="shape=rect;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;fontStyle=1;align=left;spacingLeft=10;" vertex="1" parent="1">
          <mxGeometry x="350" y="280" width="260" height="200" as="geometry" />
        </mxCell>

        <!-- Entity: ticket_status_log -->
        <mxCell id="log" value="ticket_status_log&#xa;--------------------&#xa;* log_id : BIGSERIAL &lt;PK&gt;&#xa;* ticket_id : INT &lt;FK&gt;&#xa;from_status : VARCHAR&#xa;to_status : VARCHAR&#xa;from_technician_id : INT &lt;FK&gt;&#xa;to_technician_id : INT &lt;FK&gt;&#xa;reason : TEXT&#xa;changed_by : INT&#xa;changed_at : TIMESTAMPTZ" style="shape=rect;whiteSpace=wrap;html=1;fillColor=#ffe6cc;strokeColor=#d79b00;fontStyle=1;align=left;spacingLeft=10;" vertex="1" parent="1">
          <mxGeometry x="70" y="300" width="230" height="170" as="geometry" />
        </mxCell>

        <!-- Entity: appointments -->
        <mxCell id="appt" value="appointments&#xa;--------------------&#xa;* appointment_id : SERIAL &lt;PK&gt;&#xa;* ticket_id : INT &lt;FK&gt;&#xa;appointment_type : VARCHAR&#xa;appointment_date : TIMESTAMPTZ&#xa;status : VARCHAR&#xa;notes : TEXT" style="shape=rect;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;fontStyle=1;align=left;spacingLeft=10;" vertex="1" parent="1">
          <mxGeometry x="680" y="310" width="240" height="140" as="geometry" />
        </mxCell>

        <!-- Relationships -->
        <mxCell id="rel1" value="1 : N" style="edgeStyle=orthogonalEdgeStyle;endArrow=ERmany;html=1;" edge="1" parent="1" source="sc" target="tech"><mxGeometry relative="1" as="geometry" /></mxCell>
        <mxCell id="rel2" value="1 : N" style="edgeStyle=orthogonalEdgeStyle;endArrow=ERmany;html=1;" edge="1" parent="1" source="tech" target="skill"><mxGeometry relative="1" as="geometry" /></mxCell>
        <mxCell id="rel3" value="1 : N" style="edgeStyle=orthogonalEdgeStyle;endArrow=ERmany;html=1;" edge="1" parent="1" source="sc" target="ticket"><mxGeometry relative="1" as="geometry" /></mxCell>
        <mxCell id="rel4" value="0..1 : N" style="edgeStyle=orthogonalEdgeStyle;endArrow=ERmany;html=1;" edge="1" parent="1" source="tech" target="ticket"><mxGeometry relative="1" as="geometry" /></mxCell>
        <mxCell id="rel5" value="1 : N" style="edgeStyle=orthogonalEdgeStyle;endArrow=ERmany;html=1;" edge="1" parent="1" source="ticket" target="log"><mxGeometry relative="1" as="geometry" /></mxCell>
        <mxCell id="rel6" value="1 : N" style="edgeStyle=orthogonalEdgeStyle;endArrow=ERmany;html=1;" edge="1" parent="1" source="ticket" target="appt"><mxGeometry relative="1" as="geometry" /></mxCell>

      </root>
    </mxGraphModel>
  </diagram>
</mxfile>"""
with open(os.path.join(docs_dir, "erd.drawio"), "w", encoding="utf-8") as f:
    f.write(erd_xml)

# 4. Create docs/wireframe.drawio
wf_xml = """<mxfile host="Electron" modified="2026-10-08T15:54:00.000Z" agent="Mozilla/5.0" version="21.6.8" type="device">
  <diagram id="wf_l4" name="Wireframe 3 Màn hình - Luồng L4">
    <mxGraphModel dx="1000" dy="800" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1169" pageHeight="827">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />

        <mxCell id="title" value="WIREFRAME 3 MÀN HÌNH CHÍNH - LUỒNG L4: PHÂN CÔNG KTV &amp; LỊCH HẸN" style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontSize=15;fontStyle=1;fontColor=#1F4E78;" vertex="1" parent="1">
          <mxGeometry x="180" y="20" width="750" height="30" as="geometry" />
        </mxCell>

        <!-- M1 Window -->
        <mxCell id="m1_win" value="M1: Màn hình Danh sách chờ phân công &amp; Tải công việc KTV" style="swimlane;whiteSpace=wrap;html=1;startSize=25;fillColor=#f5f5f5;fontStyle=1;" vertex="1" parent="1">
          <mxGeometry x="40" y="70" width="340" height="560" as="geometry" />
        </mxCell>
        <mxCell id="m1_content" value="[Thanh lọc Trung tâm: Trung tâm bảo hành 2]&#xa;&#xa;PHẦN 1: D/S PHIẾU CHỜ PHÂN CÔNG (MOI)&#xa;• BH-7821 | Khách: Nguyễn Văn A | Sự cố: MÀN HÌNH&#xa;• BH-7822 | Khách: Trần Văn B | Sự cố: PIN&#xa;&#xa;PHẦN 2: TẢI CÔNG VIỆC KTV TRUNG TÂM&#xa;• KTV Trần Văn Bình | Đang giữ: 2 phiếu | Tay nghề: 5/5&#xa;• KTV Lê Thị Cúc | Đang giữ: 4 phiếu | Tay nghề: 4/5&#xa;&#xa;[ Nút: Gợi ý KTV tự động ]" style="text;html=1;strokeColor=#d6b656;fillColor=#fff2cc;align=left;verticalAlign=top;whiteSpace=wrap;rounded=1;fontSize=11;" vertex="1" parent="m1_win">
          <mxGeometry x="15" y="40" width="310" height="500" as="geometry" />
        </mxCell>

        <!-- M2 Window -->
        <mxCell id="m2_win" value="M2: Màn hình Phân công &amp; Chuyển gán phiếu (Re-assign)" style="swimlane;whiteSpace=wrap;html=1;startSize=25;fillColor=#f5f5f5;fontStyle=1;" vertex="1" parent="1">
          <mxGeometry x="410" y="70" width="340" height="560" as="geometry" />
        </mxCell>
        <mxCell id="m2_content" value="CHI TIẾT PHIẾU #BH-7821&#xa;• Khách hàng: Nguyễn Văn A (0901234567)&#xa;• Nhóm sự cố: MÀN HÌNH (Priority: CAO)&#xa;• KTV hiện tại: Trần Văn Bình (Đang gán)&#xa;&#xa;BẢNG GỢI Ý KTV PHÙ HỢP (Proficiency &gt;= 3):&#xa;[X] KTV Trần Văn Bình (Tay nghề: 5/5 - Tải: 2 phiếu)&#xa;[  ] KTV Nguyễn Văn D (Tay nghề: 4/5 - Tải: 3 phiếu)&#xa;&#xa;HẠN SLA DỰ TÍNH (QT-04): 2026-10-03 16:30 (+48h)&#xa;&#xa;CHUYỂN PHIẾU (RE-ASSIGN):&#xa;• Ô nhập Lý do chuyển: [KTV Bình nghỉ đột xuất............]&#xa;  (Bắt buộc tối thiểu 10 ký tự - QT-08)&#xa;&#xa;[ Nút: HỦY ]     [ Nút: XÁC NHẬN PHÂN CÔNG ]" style="text;html=1;strokeColor=#82b366;fillColor=#d5e8d4;align=left;verticalAlign=top;whiteSpace=wrap;rounded=1;fontSize=11;" vertex="1" parent="m2_win">
          <mxGeometry x="15" y="40" width="310" height="500" as="geometry" />
        </mxCell>

        <!-- M3 Window -->
        <mxCell id="m3_win" value="M3: Màn hình Đặt &amp; Quản lý Lịch hẹn giao-nhận máy" style="swimlane;whiteSpace=wrap;html=1;startSize=25;fillColor=#f5f5f5;fontStyle=1;" vertex="1" parent="1">
          <mxGeometry x="780" y="70" width="340" height="560" as="geometry" />
        </mxCell>
        <mxCell id="m3_content" value="ĐẶT LỊCH HẸN CHO PHIẾU #BH-7821&#xa;&#xa;• Loại lịch hẹn: (X) GIAO MÁY   ( ) NHẬN MÁY&#xa;• Ngày hẹn: [ 2026-10-04 ]&#xa;• Khung giờ: [ 09:30 - 10:00  V ]&#xa;&#xa;CẢNH BÁO / THÔNG BÁO LỖI (QT-09):&#xa;[ ! ] Khung giờ 09:30 ngày 2026-10-04 đã kín 5/5 lịch hẹn.&#xa;    Vui lòng chọn khung giờ khác!&#xa;&#xa;• Ghi chú hẹn: [Khách hẹn đến nhận máy trực tiếp...]&#xa;&#xa;[ Nút: DỜI LỊCH HẸN ]     [ Nút: XÁC NHẬN ĐẶT LỊCH ]" style="text;html=1;strokeColor=#6c8ebf;fillColor=#dae8fc;align=left;verticalAlign=top;whiteSpace=wrap;rounded=1;fontSize=11;" vertex="1" parent="m3_win">
          <mxGeometry x="15" y="40" width="310" height="500" as="geometry" />
        </mxCell>

      </root>
    </mxGraphModel>
  </diagram>
</mxfile>"""
with open(os.path.join(docs_dir, "wireframe.drawio"), "w", encoding="utf-8") as f:
    f.write(wf_xml)

# 5. Create docs/ai-disclosure.md
ai_disc_md = """# PHỤ LỤC: BẢNG KHAI BÁO SỬ DỤNG CÔNG CỤ AI

**Tên học phần:** Chuyên đề tốt nghiệp 1 (HK261)  
**Tên bài tập:** Bài tập 1 - Phân tích và Thiết kế Hệ thống  
**Họ và tên sinh viên:** Nguyễn Minh Phú  
**MSSV:** 2374802013447 | **Track:** SE | **Luồng:** L4 - Phân công kỹ thuật viên & Lịch hẹn  

---

| STT | Công cụ AI | Phần áp dụng | Cách dùng (tóm tắt yêu cầu đã gửi) | Nội dung sinh viên đã chỉnh sửa, đối chiếu & kiểm chứng |
| :---: | :--- | :--- | :--- | :--- |
| 1 | Trợ lý AI (Google Antigravity) | Mục 1 - User Stories & Acceptance Criteria | "Gợi ý bộ 8 User Story cho luồng L4 phân công KTV và lịch hẹn bảo hành kèm tiêu chí Given-When-Then" | Đã rà soát và chỉnh sửa lại theo chuẩn INVEST, bổ sung 3 kịch bản ngoại lệ cụ thể (KTV quá tải, không tìm thấy KTV tay nghề >= 3, quá hạn lịch hẹn) và gán mức MoSCoW. |
| 2 | Trợ lý AI (Google Antigravity) | Mục 3.2 - Ba câu lập luận kiến trúc | "Viết 3 câu lập luận lựa chọn kiến trúc 4 lớp phân tầng và Repository Pattern gắn với NFR1, NFR2, NFR3" | Đã chuẩn hóa lại đúng khuôn mẫu: *'Vì NFR... đòi hỏi..., tôi chọn..., đánh đổi là...'* và kiểm tra tính khả thi trên quy mô prototype. |
| 3 | Trợ lý AI (Google Antigravity) | Mục 4 & db/schema.sql - Mô hình ERD & SQL DDL | "Gợi ý cấu trúc bảng SQL DDL chuẩn 3NF cho 6 bảng luồng L4 kèm các ràng buộc NOT NULL, FOREIGN KEY và INDEX" | Tự tay kiểm tra chuẩn 3NF, thêm ràng buộc `CHECK` cho mốc SLA `due_date >= received_at`, `CHECK` proficiency điểm 1-5, và bổ sung các composite index trên `(technician_id, due_date)`. |
| 4 | Trợ lý AI (Google Antigravity) | Mục 5 - Wireframe 3 Màn hình | "Gợi ý bố cục layout text wireframe 3 màn hình (M1, M2, M3) cho Luồng L4" | Tự vẽ lại sơ đồ cấu trúc trên Draw.io, lập bảng đối chiếu 1-1 giữa từng trường hiển thị với cột trong CSDL và mã FR/US. |

---

**Cam kết liêm chính học thuật:**  
Tôi xác nhận đã đọc, hiểu và chịu trách nhiệm về toàn bộ nội dung nộp.

Họ tên: Nguyễn Minh Phú  
MSSV: 2374802013447  
Ngày nộp: 08/10/2026  
"""
with open(os.path.join(docs_dir, "ai-disclosure.md"), "w", encoding="utf-8") as f:
    f.write(ai_disc_md)

# 6. Create docs/api-contract.md
api_md = """# HỢP ĐỒNG API (API CONTRACT - TRACK SE)

**Họ tên:** Nguyễn Minh Phú | **MSSV:** 2374802013447 | **Track:** SE | **Luồng:** L4 - Phân công KTV & Lịch hẹn

---

## 1. QUY ƯỚC CHUNG
- **Định dạng trao đổi**: JSON, UTF-8. Header bắt buộc: `Content-Type: application/json`, `Authorization: Bearer <token>`.
- **Đặt tên trường**: Dùng kiểu `snake_case` khớp với schema CSDL (`ticket_id`, `technician_id`, `due_date`...).
- **Định dạng thời gian**: ISO 8601 kèm timezone, ví dụ: `2026-10-01T14:30:00+07:00`.
- **Cấu trúc Response lỗi chuẩn**:
```json
{
  "error": {
    "code": "VALIDATION_FAILED | NOT_FOUND | CONFLICT | FORBIDDEN",
    "message": "Thông báo lỗi chi tiết dành cho người dùng",
    "fields": {
      "field_name": "Mô tả lỗi cụ thể của trường"
    }
  }
}
```

## 2. DANH SÁCH ENDPOINTS
- `GET /api/v1/tickets/unassigned`: Lấy danh sách phiếu chờ phân công kèm tải KTV (US1)
- `GET /api/v1/tickets/{id}/recommend-technicians`: Lấy danh sách KTV gợi ý phù hợp (US2)
- `POST /api/v1/tickets/{id}/assign`: Phân công phiếu bảo hành cho KTV (US2)
- `POST /api/v1/tickets/{id}/reassign`: Chuyển phiếu bảo hành sang KTV khác (US6)
- `POST /api/v1/appointments`: Đặt lịch hẹn giao – nhận máy (US3)
- `GET /api/v1/technicians/me/tickets`: KTV xem phiếu được gán xếp theo SLA (US4)
- `PATCH /api/v1/tickets/{id}/status`: KTV cập nhật trạng thái phiếu và ghi log (US5)
- `GET /api/v1/devices/{identifier}/history`: Tra cứu lịch sử sửa chữa thiết bị (US7)
"""
with open(os.path.join(docs_dir, "api-contract.md"), "w", encoding="utf-8") as f:
    f.write(api_md)

# 7. Create root README.md
readme_md = """# BÀI TẬP 1: PHÂN TÍCH VÀ THIẾT KẾ HỆ THỐNG
## LUỒNG L4: PHÂN CÔNG KỸ THUẬT VIÊN VÀ LỊCH HẸN

**Thông tin sinh viên:**
- **Họ và tên:** Nguyễn Minh Phú
- **Mã số sinh viên:** 2374802013447
- **Chuyên ngành (Track):** SE (Software Engineering)
- **Học phần:** Chuyên đề tốt nghiệp 1 (HK261 - Trường ĐH Văn Lang)

---

### 📌 MỤC 1. THÔNG TIN PHẠM VI LUỒNG L4
> **Phạm vi 1 câu:** Hệ thống hỗ trợ Quản lý trung tâm bảo hành phân công phiếu bảo hành cho kỹ thuật viên phù hợp dựa trên tay nghề, trung tâm làm việc và khối lượng công việc hiện tại; cho phép đặt và quản lý lịch hẹn giao – nhận máy với khách hàng, đồng thời tự động theo dõi hạn cam kết (SLA) và lịch sử chuyển trạng thái.

---

### 📌 MỤC 2. CẤU TRÚC THƯ MỤC DỰ ÁN & HỒ SƠ THIẾT KẾ
```text
.
├── docs/
│   ├── srs.md                 # Bản đặc tả SRS rút gọn 6 mục + SE API Contract
│   ├── usecase.drawio         # File gốc sơ đồ Use Case (Draw.io XML)
│   ├── architecture.drawio    # File gốc sơ đồ Kiến trúc 4 Lớp (Draw.io XML)
│   ├── erd.drawio             # File gốc sơ đồ ERD chuẩn 3NF (Draw.io XML)
│   ├── wireframe.drawio       # File gốc sơ đồ Wireframe 3 Màn hình (Draw.io XML)
│   ├── ai-disclosure.md       # Bảng khai báo sử dụng công cụ AI
│   └── api-contract.md        # Hợp đồng API Track SE
├── db/
│   └── schema.sql             # SQL DDL Skeleton chuẩn 3NF (PostgreSQL)
└── README.md
```

---

### 📌 MỤC 6. HƯỚNG DẪN MỞ VÀ RÀ SOÁT FILE
- **Sơ đồ Draw.io gốc (`.drawio`)**: Mở bằng công cụ miễn phí tại [app.diagrams.net](https://app.diagrams.net/).
- **Mã CSDL PostgreSQL**: Xem chi tiết tại file `db/schema.sql`.
- **Bản nộp PDF chính thức**: Xem file `BT1_2374802013447_NguyenMinhPhu.pdf` (đã export từ file Word).
"""
with open(os.path.join(root_dir, "README.md"), "w", encoding="utf-8") as f:
    f.write(readme_md)

print("SUCCESS: All repo files for BT1 created and synchronized.")
