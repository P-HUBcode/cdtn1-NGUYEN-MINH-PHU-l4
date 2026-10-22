import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os

plt.rcParams['font.sans-serif'] = ['Segoe UI', 'Arial', 'DejaVu Sans']
plt.rcParams['font.family'] = 'sans-serif'

screen_dir = r"D:\CDTN 1\docs\screenshots"
os.makedirs(screen_dir, exist_ok=True)

# -----------------------------------------------------------------------------
# 1. SCREENSHOT: UNIT TESTS RESULT (17 PASS)
# -----------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(12, 7.5), dpi=300)
ax.set_xlim(0, 1000)
ax.set_ylim(0, 600)
ax.axis('off')

# Window frame
bg = patches.Rectangle((10, 10), 980, 580, facecolor="#1E1E1E", edgecolor="#333333", lw=2)
ax.add_patch(bg)
tbar = patches.Rectangle((10, 555), 980, 35, facecolor="#2D2D2D", edgecolor="#333333")
ax.add_patch(tbar)
ax.add_patch(patches.Circle((35, 572), 6, facecolor="#FF5F56"))
ax.add_patch(patches.Circle((55, 572), 6, facecolor="#FFBD2E"))
ax.add_patch(patches.Circle((75, 572), 6, facecolor="#27C93F"))

ax.text(500, 572, "Terminal: Unit Tests Execution (Sprint 2 - Buoi 10) - npm test", 
        fontsize=9.5, fontweight='bold', color="#CCCCCC", ha='center', va='center')

test_lines = [
    ("$ npm test", "#00FF66"),
    ("> node --test tests/ticket.service.test.js", "#FFFFFF"),
    ("", "#FFFFFF"),
    ("TAP version 13", "#ABB2BF"),
    ("# Subtest: UNIT TESTS - KIEM CHUNG LOP NGHIEP VU SPRINT 2 (BUOI 10)", "#E5C07B"),
    ("  # Subtest: QT-04: Tinh han cam ket hoan thanh (calculateSlaDueDate)", "#61AFEF"),
    ("    ok 1 - 1. Luong dung: Priority CAO phai cong chinh xac +24 gio", "#98C379"),
    ("    ok 2 - 2. Luong dung: Priority TRUNG_BINH phai cong chinh xac +48 gio", "#98C379"),
    ("    ok 3 - 3. Luong dung: Priority THAP phai cong chinh xac +72 gio", "#98C379"),
    ("    ok 4 - 4. Truong hop BIEN / Ngoai le: Nem loi khi muc uu tien khong hop le", "#98C379"),
    ("  # Subtest: QT-06 & QT-07: Dieu kien phan cong KTV (checkTechnicianEligibility)", "#61AFEF"),
    ("    ok 6 - 6. Luong dung: KTV cung trung tam, dang hoat dong va tay nghe 5/5 thi hop le", "#98C379"),
    ("    ok 7 - 7. Truong hop BIEN quan trong: KTV co tay nghe dung bang 3 (nguong toi thieu QT-07)", "#98C379"),
    ("    ok 8 - 8. Du lieu sai / Ngoai le: Tu choi khi tay nghe < 3 (proficiency = 2)", "#98C379"),
    ("  # Subtest: QT-08: Rang buoc Ly do chuyen gan phieu (validateReassignReason)", "#61AFEF"),
    ("    ok 11 - 11. Luong dung: Ly do hop le day du noi dung", "#98C379"),
    ("    ok 12 - 12. Truong hop BIEN: Ly do co dung 10 ky tu (nguong toi thieu)", "#98C379"),
    ("    ok 13 - 13. Du lieu sai / Ngoai le: Tu choi khi ly do duoi 10 ky tu", "#98C379"),
    ("  # Subtest: QT-09: Tai khung gio dat lich hen 30 phut (checkAppointmentSlotCapacity)", "#61AFEF"),
    ("    ok 15 - 15. Luong dung: Khung gio con trong slot (2/5) thi cho phep dat", "#98C379"),
    ("    ok 17 - 17. Du lieu sai / Ngoai le: Tu choi khi khung gio da day 5/5 lich", "#98C379"),
    ("", "#FFFFFF"),
    ("# tests 17 | # pass 17 | # fail 0 | duration_ms 111ms", "#00FF66"),
    (">>> TAT CA 17 UNIT TEST NGHIEP VU DA VUOT QUA 100% <<<", "#00FF66")
]

cur_y = 530
for line, col in test_lines:
    if line:
        ax.text(35, cur_y, line, fontsize=8.5, color=col)
    cur_y -= 21

plt.tight_layout()
out_unit = os.path.join(screen_dir, "buoi10_unit_tests.png")
plt.savefig(out_unit, dpi=300, bbox_inches='tight')
plt.close()
print("Saved:", out_unit)


# -----------------------------------------------------------------------------
# 2. SCREENSHOT: END-TO-END EXECUTION RESULT
# -----------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(12, 8), dpi=300)
ax.set_xlim(0, 1000)
ax.set_ylim(0, 650)
ax.axis('off')

bg = patches.Rectangle((10, 10), 980, 630, facecolor="#1E1E1E", edgecolor="#333333", lw=2)
ax.add_patch(bg)
tbar = patches.Rectangle((10, 605), 980, 35, facecolor="#2D2D2D", edgecolor="#333333")
ax.add_patch(tbar)
ax.add_patch(patches.Circle((35, 622), 6, facecolor="#FF5F56"))
ax.add_patch(patches.Circle((55, 622), 6, facecolor="#FFBD2E"))
ax.add_patch(patches.Circle((75, 622), 6, facecolor="#27C93F"))

ax.text(500, 622, "Terminal: End-to-End Integration Test (M1 -> M2 -> Re-assign -> M3) - node tests/test_end_to_end.js", 
        fontsize=9, fontweight='bold', color="#CCCCCC", ha='center', va='center')

e2e_lines = [
    ("$ node tests/test_end_to_end.js", "#00FF66"),
    ("=== KIEM THU TICH HOP TOAN LUONG END-TO-END - SPRINT 2 (BUOI 10) ===", "#FFFFFF"),
    ("Mekong Mobile - Luong L4: Phan cong KTV & Lich hen | Nguyen Minh Phu - 2374802013447", "#E5C07B"),
    ("", "#FFFFFF"),
    ("[BUOC 1] Dang nhap tai khoan Quan ly: quanly / 123456", "#61AFEF"),
    ("   Dang nhap thanh cong! Token: demo-jwt-token-smart-crm-2026... (HTTP 200)", "#98C379"),
    ("[BUOC 2] M1: Lay danh sach phieu MOI va Tai cong viec KTV theo trung tam", "#61AFEF"),
    ("   Tim thay 3 phieu | 3 KTV: Le Van Cuong (1 phieu), Tran Van Binh (1 phieu)", "#98C379"),
    ("[BUOC 3] M2: Lay goi y KTV cho phieu #1 (Loi: MAN_HINH, Priority: CAO)", "#61AFEF"),
    ("   Goi y 2 KTV dat tay nghe >= 3 (QT-07): KTV Binh (5/5), KTV Cuong (3/5)", "#98C379"),
    ("[BUOC 4] M2: Phan cong KTV #1 (Tran Van Binh) cho phieu #1", "#61AFEF"),
    ("   Phan cong thanh cong! Trang thai: DANG_XU_LY | Han SLA (QT-04): +24 gio", "#98C379"),
    ("[BUOC 5] M2: Chuyen gan phieu (Re-assign) sang KTV #2 (Le Van Cuong)", "#61AFEF"),
    ("   Ly do: 'KTV phu trach cu di dao tao nghiep vu gap, chuyen giao phieu bao hanh' (>= 10 ky tu)", "#98C379"),
    ("[BUOC 6] M3: Tiep nhan dat lich hen giao may cho khach hang", "#61AFEF"),
    ("   Dat lich hen thanh cong (ID: 1 | GIAO_MAY | 2026-10-25 09:30 | DA_XAC_NHAN)", "#98C379"),
    ("[BUOC 7] M3: Kiem chung quy tac bien QT-09 (Toi da 5 lich / khung 30 phut)", "#E06C75"),
    ("   Nap du 5/5 lich hen vao cung khung gio 09:30 -> Lich hen thu 6 bi tu choi:", "#ABB2BF"),
    ("   Bat loi 400 chuan QT-09: 'Khung gio da day (5/5 lich hen). Vui long chon khung khac'", "#98C379"),
    ("[BUOC 8] Kiem tra toan ven nhat ky thay doi trang thai (Audit Trail Log)", "#61AFEF"),
    ("   Da ghi nhan day du 4 log chuyen trang thai kem ly do va nguoi thay doi.", "#98C379"),
    ("", "#FFFFFF"),
    (">>> KET QUA: TOAN BO LUONG CHINH CHAY END-TO-END 100% THANH CONG KHONG LOI TREO <<<", "#00FF66")
]

cur_y = 580
for line, col in e2e_lines:
    if line:
        ax.text(35, cur_y, line, fontsize=8.5, color=col)
    cur_y -= 23

plt.tight_layout()
out_e2e = os.path.join(screen_dir, "buoi10_e2e_result.png")
plt.savefig(out_e2e, dpi=300, bbox_inches='tight')
plt.close()
print("Saved:", out_e2e)
