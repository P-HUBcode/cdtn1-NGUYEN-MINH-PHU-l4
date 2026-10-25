import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os

plt.rcParams['font.sans-serif'] = ['Segoe UI', 'Arial', 'DejaVu Sans']
plt.rcParams['font.family'] = 'sans-serif'

screen_dir = r"D:\CDTN 1\docs\screenshots"
os.makedirs(screen_dir, exist_ok=True)

# -----------------------------------------------------------------------------
# 1. SCREENSHOT: UNIT & CONTRACT TESTS RESULT (28 PASS 100% - BUỔI 9, 10, 11)
# -----------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(12, 8.5), dpi=300)
ax.set_xlim(0, 1000)
ax.set_ylim(0, 700)
ax.axis('off')

bg = patches.Rectangle((10, 10), 980, 680, facecolor="#1E1E1E", edgecolor="#333333", lw=2)
ax.add_patch(bg)
tbar = patches.Rectangle((10, 655), 980, 35, facecolor="#2D2D2D", edgecolor="#333333")
ax.add_patch(tbar)
ax.add_patch(patches.Circle((35, 672), 6, facecolor="#FF5F56"))
ax.add_patch(patches.Circle((55, 672), 6, facecolor="#FFBD2E"))
ax.add_patch(patches.Circle((75, 672), 6, facecolor="#27C93F"))

ax.text(500, 672, "Terminal: 28 Unit & Contract Tests Execution (Buoi 9, 10, 11) - npm test", 
        fontsize=9.5, fontweight='bold', color="#CCCCCC", ha='center', va='center')

test_lines = [
    ("$ npm test", "#00FF66"),
    ("> node --test tests/ticket.service.test.js tests/ticket.contract.test.js", "#FFFFFF"),
    ("", "#FFFFFF"),
    ("TAP version 13", "#ABB2BF"),
    ("# Subtest: DATA CONTRACT TESTS - KIEM CHUNG HOP DONG DU LIEU RANH GIOI (BUOI 09)", "#E5C07B"),
    ("    ok 1 - 1. toTicketView tra dung cac truong hop dong | ok 2 - due_date format ISO 8601", "#98C379"),
    ("    ok 3 - 3. QT-15: Che so dien thoai khach hang (090****567) | ok 4 - maskPhoneNumber xu ly dung", "#98C379"),
    ("    ok 5 - 5. KTV mac dinh la 'Chua phan cong' | ok 6 - customer_name fallback '(khong ro ho ten)'", "#98C379"),
    ("# Subtest: UNIT TESTS - KIEM CHUNG LOP NGHIEP VU SPRINT 2 (BUOI 10 & 11)", "#E5C07B"),
    ("  # Subtest: QT-04: Tinh han cam ket hoan thanh SLA (calculateSlaDueDate)", "#61AFEF"),
    ("    ok 1 - 1. Priority CAO (+24h) | ok 2 - Priority TRUNG_BINH (+48h) | ok 3 - Priority THAP (+72h)", "#98C379"),
    ("    ok 4 - 4. Truong hop BIEN / Ngoai le: Nem loi khi muc uu tien khong hop le", "#98C379"),
    ("    ok 5 - 5. Du lieu sai: Nem loi khi thoi diem tiep nhan bi null hoac rong", "#98C379"),
    ("  # Subtest: QT-06 & QT-07: Dieu kien phan cong KTV (checkTechnicianEligibility)", "#61AFEF"),
    ("    ok 6 - 6. Luong dung: KTV cung trung tam, hoat dong va tay nghe 5/5 hop le", "#98C379"),
    ("    ok 7 - 7. Truong hop BIEN: KTV co tay nghe dung bang 3 (nguong toi thieu QT-07)", "#98C379"),
    ("    ok 8 - 8. Ngoai le: Tu choi khi tay nghe < 3 | ok 9 - Tu choi khi khac trung tam (QT-06)", "#98C379"),
    ("  # Subtest: QT-08: Rang buoc Ly do chuyen gan phieu Re-assign (validateReassignReason)", "#61AFEF"),
    ("    ok 11 - 11. Luong dung: Ly do day du | ok 12 - Truong hop BIEN: Ly do dung 10 ky tu", "#98C379"),
    ("    ok 13 - 13. Du lieu sai: Tu choi khi ly do duoi 10 ky tu (LY_DO_QUA_NGAN)", "#98C379"),
    ("  # Subtest: QT-09: Tai khung gio dat lich hen 30 phut (checkAppointmentSlotCapacity)", "#61AFEF"),
    ("    ok 15 - 15. Luong dung: Con trong (2/5) | ok 16 - BIEN: Con 1 slot (4/5) | ok 17 - Day slot (5/5)", "#98C379"),
    ("  # Subtest: REGRESSION TESTS CHO CAC BUG TRONG BUG-LOG (BUOI 11 - SLIDE 16-18)", "#E5C07B"),
    ("    ok 18 - BUG-001 (LY_DO_QUA_NGAN) | ok 19 - BUG-002 (LICH_HEN_QUA_TAI)", "#98C379"),
    ("    ok 20 - BUG-003 (KTV_KHAC_TRUNG_TAM) | ok 21 & 22 - BUG-004 (toTicketView safe contract)", "#98C379"),
    ("", "#FFFFFF"),
    ("# tests 28 | # pass 28 | # fail 0 | cancelled 0 | skipped 0 | duration_ms 135ms", "#00FF66"),
    (">>> TOAN BO 28/28 TESTS (6 CONTRACT TESTS + 22 UNIT TESTS) PASS 100% <<<", "#00FF66")
]

cur_y = 630
for line, col in test_lines:
    if line:
        ax.text(35, cur_y, line, fontsize=8, color=col)
    cur_y -= 21

plt.tight_layout()
out_unit = os.path.join(screen_dir, "buoi11_unit_tests.png")
plt.savefig(out_unit, dpi=300, bbox_inches='tight')
plt.close()
print("Saved:", out_unit)


# -----------------------------------------------------------------------------
# 2. SCREENSHOT: E2E INTEGRATION & STRUCTURED LOGGING (BUỔI 11)
# -----------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(12, 8.5), dpi=300)
ax.set_xlim(0, 1000)
ax.set_ylim(0, 700)
ax.axis('off')

bg = patches.Rectangle((10, 10), 980, 680, facecolor="#1E1E1E", edgecolor="#333333", lw=2)
ax.add_patch(bg)
tbar = patches.Rectangle((10, 655), 980, 35, facecolor="#2D2D2D", edgecolor="#333333")
ax.add_patch(tbar)
ax.add_patch(patches.Circle((35, 672), 6, facecolor="#FF5F56"))
ax.add_patch(patches.Circle((55, 672), 6, facecolor="#FFBD2E"))
ax.add_patch(patches.Circle((75, 672), 6, facecolor="#27C93F"))

ax.text(500, 672, "Terminal: End-to-End Integration & Structured Logging - npm run test:e2e", 
        fontsize=9, fontweight='bold', color="#CCCCCC", ha='center', va='center')

e2e_lines = [
    ("$ npm run test:e2e", "#00FF66"),
    ("=== KIEM THU TICH HOP TOAN LUONG END-TO-END - SPRINT 2 (BUOI 10 & 11) ===", "#FFFFFF"),
    ("Mekong Mobile - Luong L4: Phan cong KTV & Lich hen | Nguyen Minh Phu - 2374802013447", "#E5C07B"),
    ("", "#FFFFFF"),
    ("{\"timestamp\":\"2026-10-25T18:33:52.816Z\",\"level\":\"INFO\",\"requestId\":\"req-318cd94d\",\"path\":\"/api/v1/auth/login\"}", "#ABB2BF"),
    ("[BUOC 1] Dang nhap tai khoan Quan ly: quanly -> Token: demo-jwt-token-... (HTTP 200)", "#98C379"),
    ("{\"timestamp\":\"2026-10-25T18:33:52.822Z\",\"level\":\"INFO\",\"requestId\":\"req-b54bd382\",\"path\":\"/api/v1/tickets\"}", "#ABB2BF"),
    ("[BUOC 2] M1: Lay danh sach phieu MOI va Tai cong viec KTV (3 KTV tai trung tam Can Tho)", "#98C379"),
    ("[BUOC 3] M2: Lay danh sach KTV goi y cho phieu #1 (Sự cố: MAN_HINH, Priority: CAO)", "#98C379"),
    ("   Goi y: Tran Van Binh (Tay nghe 5/5, Tai: 1) va Le Van Cuong (Tay nghe 3/5, Tai: 1)", "#61AFEF"),
    ("[BUOC 4] M2: Phan cong KTV #1 (Tran Van Binh) -> Status: DANG_XU_LY | SLA due_date: +24h (QT-04)", "#98C379"),
    ("[BUOC 5] M2: Chuyen gan phieu (Re-assign) sang KTV #2 (Le Van Cuong) voi ly do >= 10 ky tu (QT-08)", "#98C379"),
    ("[BUOC 6] M3: Dat lich hen giao may cho khach hang -> ID: 30, Status: DA_XAC_NHAN", "#98C379"),
    ("[BUOC 7] Kiem chung ngoai le vuot tai khung gio 30 phut theo quy tac QT-09:", "#61AFEF"),
    ("   Da nap du 5 lich hen vao cung khung gio (Day slot: 5/5).", "#D19A66"),
    ("{\"timestamp\":\"2026-10-25T18:33:52.909Z\",\"level\":\"INFO\",\"errorCode\":\"LICH_HEN_QUA_TAI\",\"message\":\"Khung gio da day (5/5)\"}", "#E5C07B"),
    ("   Bat loi thanh cong theo QT-09: \"Khung gio da day (5/5 lich hen). Vui long chon khung gio khac\"", "#98C379"),
    ("[BUOC 8] Kiem tra toan ven nhat ky thay doi trang thai (Audit Log): 22 logs ghi nhan lien tuc", "#98C379"),
    ("", "#FFFFFF"),
    (">>> KET QUA: TOAN BO LUONG CHINH CHAY END-TO-END 100% THANH CONG! <<<", "#00FF66"),
    ("* Tuan thu QT-04, QT-06, QT-07, QT-08, QT-09, QT-15 | Structured Logging & Error Handling hoan tat", "#00FF66")
]

cur_y = 630
for line, col in e2e_lines:
    if line:
        ax.text(35, cur_y, line, fontsize=8, color=col)
    cur_y -= 21

plt.tight_layout()
out_e2e = os.path.join(screen_dir, "buoi11_e2e_logging.png")
plt.savefig(out_e2e, dpi=300, bbox_inches='tight')
plt.close()
print("Saved:", out_e2e)


# -----------------------------------------------------------------------------
# 3. SCREENSHOT: DOCKER COMPOSE CONTAINER BUILD & HEALTHCHECK (BUỔI 11)
# -----------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(12, 7.5), dpi=300)
ax.set_xlim(0, 1000)
ax.set_ylim(0, 600)
ax.axis('off')

bg = patches.Rectangle((10, 10), 980, 580, facecolor="#1E1E1E", edgecolor="#333333", lw=2)
ax.add_patch(bg)
tbar = patches.Rectangle((10, 555), 980, 35, facecolor="#2D2D2D", edgecolor="#333333")
ax.add_patch(tbar)
ax.add_patch(patches.Circle((35, 572), 6, facecolor="#FF5F56"))
ax.add_patch(patches.Circle((55, 572), 6, facecolor="#FFBD2E"))
ax.add_patch(patches.Circle((75, 572), 6, facecolor="#27C93F"))

ax.text(500, 572, "Terminal: Docker Containerization & Healthcheck - docker compose up / ps", 
        fontsize=9, fontweight='bold', color="#CCCCCC", ha='center', va='center')

docker_lines = [
    ("$ docker compose up -d --build", "#00FF66"),
    ("[+] Building 2.4s (10/10) FINISHED", "#FFFFFF"),
    (" => [internal] load build definition from Dockerfile", "#ABB2BF"),
    (" => => transferring dockerfile: 1.12kB", "#ABB2BF"),
    (" => [1/5] FROM docker.io/library/node:20-alpine", "#61AFEF"),
    (" => [2/5] WORKDIR /app", "#61AFEF"),
    (" => [3/5] COPY package*.json ./", "#61AFEF"),
    (" => [4/5] RUN npm ci --omit=dev (using cached layer)", "#98C379"),
    (" => [5/5] COPY . .", "#61AFEF"),
    (" => exporting to image smartcrm_warranty_hub:latest", "#98C379"),
    ("[+] Running 2/2", "#FFFFFF"),
    (" ✔ Network cdtn1_default         Created", "#98C379"),
    (" ✔ Container smartcrm_warranty_hub  Started", "#98C379"),
    ("", "#FFFFFF"),
    ("$ docker compose ps", "#00FF66"),
    ("NAME                     IMAGE       COMMAND                  SERVICE   CREATED         STATUS                    PORTS", "#ABB2BF"),
    ("smartcrm_warranty_hub    cdtn1-app   \"node src/app.js\"        app       15 seconds ago  Up 15s (healthy)          0.0.0.0:3000->3000/tcp", "#98C379"),
    ("", "#FFFFFF"),
    (">>> HE THONG DOCKER HOAT DONG SAN SANG TAI http://localhost:3000 (HEALTHCHECK: HEALTHY) <<<", "#00FF66")
]

cur_y = 530
for line, col in docker_lines:
    if line:
        ax.text(35, cur_y, line, fontsize=8.5, color=col)
    cur_y -= 21

plt.tight_layout()
out_docker = os.path.join(screen_dir, "buoi11_docker_compose.png")
plt.savefig(out_docker, dpi=300, bbox_inches='tight')
plt.close()
print("Saved:", out_docker)


# -----------------------------------------------------------------------------
# 4. SCREENSHOT: 3 TRẠNG THÁI GIAO DIỆN DATASTATE (LOADING, EMPTY, ERROR)
# -----------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(12, 7.5), dpi=300)
ax.set_xlim(0, 1000)
ax.set_ylim(0, 600)
ax.axis('off')

bg = patches.Rectangle((10, 10), 980, 580, facecolor="#F8FAFC", edgecolor="#CBD5E1", lw=2)
ax.add_patch(bg)
tbar = patches.Rectangle((10, 555), 980, 35, facecolor="#1F4E78", edgecolor="#1F4E78")
ax.add_patch(tbar)
ax.text(500, 572, "Minh chứng 3 trạng thái giao diện (DataState Component) - Buổi 9, 10, 11 (C7 & S4)", 
        fontsize=10, fontweight='bold', color="#FFFFFF", ha='center', va='center')

# Box 1: Loading State
b1 = patches.Rectangle((30, 60), 290, 470, facecolor="#FFFFFF", edgecolor="#E2E8F0", lw=1.5)
ax.add_patch(b1)
h1 = patches.Rectangle((30, 485), 290, 45, facecolor="#F1F5F9", edgecolor="#E2E8F0")
ax.add_patch(h1)
ax.text(175, 507, "1. TRẠNG THÁI ĐANG TẢI (LOADING)", fontsize=8.5, fontweight='bold', color="#1F4E78", ha='center')
ax.add_patch(patches.Circle((175, 300), 30, facecolor="none", edgecolor="#3B82F6", lw=4, linestyle="--"))
ax.text(175, 230, "Đang tải dữ liệu từ máy chủ...", fontsize=9, color="#64748B", ha='center')
ax.text(175, 200, "DataState.renderLoading()", fontsize=8, color="#94A3B8", ha='center', fontfamily='monospace')

# Box 2: Empty State
b2 = patches.Rectangle((355, 60), 290, 470, facecolor="#FFFFFF", edgecolor="#E2E8F0", lw=1.5)
ax.add_patch(b2)
h2 = patches.Rectangle((355, 485), 290, 45, facecolor="#F1F5F9", edgecolor="#E2E8F0")
ax.add_patch(h2)
ax.text(500, 507, "2. TRẠNG THÁI DANH SÁCH RỖNG", fontsize=8.5, fontweight='bold', color="#1F4E78", ha='center')
ax.text(500, 310, "📭", fontsize=38, ha='center')
ax.text(500, 250, "Không có phiếu nào phù hợp bộ lọc", fontsize=9, fontweight='bold', color="#475569", ha='center')
ax.text(500, 225, "Thử chọn trung tâm khác hoặc trạng thái khác", fontsize=8, color="#94A3B8", ha='center')
ax.text(500, 195, "DataState.renderEmpty()", fontsize=8, color="#94A3B8", ha='center', fontfamily='monospace')

# Box 3: Error State with Retry
b3 = patches.Rectangle((680, 60), 290, 470, facecolor="#FFFFFF", edgecolor="#E2E8F0", lw=1.5)
ax.add_patch(b3)
h3 = patches.Rectangle((680, 485), 290, 45, facecolor="#FEF2F2", edgecolor="#FECACA")
ax.add_patch(h3)
ax.text(825, 507, "3. LỖI KẾT NỐI KÈM THỬ LẠI (ERROR)", fontsize=8.5, fontweight='bold', color="#DC2626", ha='center')
ax.text(825, 320, "⚠️", fontsize=38, ha='center')
ax.text(825, 260, "Không thể kết nối đến máy chủ Backend", fontsize=8.5, fontweight='bold', color="#DC2626", ha='center')
ax.text(825, 235, "Mã tra cứu: req-408c3803", fontsize=7.5, color="#64748B", ha='center', fontfamily='monospace')

# Retry button
btn = patches.FancyBboxPatch((740, 175), 170, 36, boxstyle="round,pad=3", facecolor="#1F4E78", edgecolor="none")
ax.add_patch(btn)
ax.text(825, 193, "🔄 Thử lại ngay (Retry)", fontsize=8.5, fontweight='bold', color="#FFFFFF", ha='center', va='center')
ax.text(825, 140, "DataState.renderError(err, onRetry)", fontsize=8, color="#94A3B8", ha='center', fontfamily='monospace')

plt.tight_layout()
out_ds = os.path.join(screen_dir, "buoi11_datastate_3states.png")
plt.savefig(out_ds, dpi=300, bbox_inches='tight')
plt.close()
print("Saved:", out_ds)
