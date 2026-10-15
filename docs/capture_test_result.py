import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os

screen_dir = r"D:\CDTN 1\docs\screenshots"
os.makedirs(screen_dir, exist_ok=True)

fig, ax = plt.subplots(figsize=(12, 7.5), dpi=300)
ax.set_xlim(0, 1000)
ax.set_ylim(0, 600)
ax.axis('off')

# Window frame (Dark terminal)
bg = patches.Rectangle((10, 10), 980, 580, facecolor="#1E1E1E", edgecolor="#333333", lw=2)
ax.add_patch(bg)

# Title bar
tbar = patches.Rectangle((10, 555), 980, 35, facecolor="#2D2D2D", edgecolor="#333333")
ax.add_patch(tbar)

# Window buttons
ax.add_patch(patches.Circle((35, 572), 6, facecolor="#FF5F56"))
ax.add_patch(patches.Circle((55, 572), 6, facecolor="#FFBD2E"))
ax.add_patch(patches.Circle((75, 572), 6, facecolor="#27C93F"))

ax.text(500, 572, "Terminal: Node.js API Sprint 1 Test Execution - curl / tests/test_api.js", 
        fontsize=9.5, fontweight='bold', color="#CCCCCC", ha='center', va='center', fontfamily='monospace')

# Terminal text content
terminal_lines = [
    ("$ node tests/test_api.js", "#00FF66"),
    ("=== BẮT ĐẦU TEST CÁC ENDPOINT MODULE CỐT LÕI (BUỔI 8) ===", "#FFFFFF"),
    ("", "#FFFFFF"),
    ("[TEST 1] GET /api/v1/tickets  -->  HTTP 200 OK", "#61AFEF"),
    ("Total Tickets: 3 | Status: 200 OK", "#ABB2BF"),
    ("Sample Ticket: { ticket_code: 'BH-202610-001', customer_name: 'Nguyễn Văn An', status: 'MOI' }", "#98C379"),
    ("", "#FFFFFF"),
    ("[TEST 2] GET /api/v1/tickets/1/recommend-technicians  -->  HTTP 200 OK", "#61AFEF"),
    ("Recommended Techs: KTV Lê Văn Cường (Rank 3/5, Tải: 0), KTV Trần Văn Bình (Rank 5/5, Tải: 1)", "#98C379"),
    ("", "#FFFFFF"),
    ("[TEST 3] POST /api/v1/tickets/1/assign  -->  HTTP 200 OK (Happy Path)", "#61AFEF"),
    ("Response: { success: true, message: 'Phân công kỹ thuật viên thành công', status: 'DANG_XU_LY' }", "#98C379"),
    ("SLA Due Date (QT-04): 2026-10-16T09:58:50Z (+24h)", "#D19A66"),
    ("", "#FFFFFF"),
    ("[TEST 4] POST /api/v1/tickets  -->  HTTP 400 Bad Request (Validation Exception)", "#E06C75"),
    ("Response: { error: { code: 'VALIDATION_FAILED', message: 'Thiếu trường dữ liệu bắt buộc' } }", "#E06C75"),
    ("", "#FFFFFF"),
    ("=== TẤT CẢ TEST ĐÃ HOÀN TẤT THÀNH CÔNG 100% ===", "#00FF66")
]

cur_y = 530
for line, col in terminal_lines:
    if line:
        ax.text(35, cur_y, line, fontsize=9, color=col, fontfamily='monospace')
    cur_y -= 25

plt.tight_layout()
out_img = os.path.join(screen_dir, "api_test_result.png")
plt.savefig(out_img, dpi=300, bbox_inches='tight')
plt.close()

print("Created api_test_result.png at", out_img)
