# ===== Dockerfile — Track SE (Node.js 20 LTS Alpine) =====
# Dự án: Smart CRM Warranty Hub — Mekong Mobile (Luồng L4)
# Sinh viên: Nguyễn Minh Phú — MSSV: 2374802013447
# Tuân thủ Buổi 11 (Slide 30 - 32): Tối ưu lớp cache, chạy người dùng bảo mật, Healthcheck

FROM node:20-alpine

# Thiết lập thư mục làm việc trong container
WORKDIR /app

# 1. Chép tệp khai báo và tệp khoá phiên bản TRƯỚC
# Tận dụng triệt để bộ nhớ đệm (Layer Caching) của Docker
COPY package*.json ./

# 2. Cài đặt chính xác các phụ thuộc production theo package-lock.json
RUN npm ci --omit=dev

# 3. Chép toàn bộ mã nguồn ứng dụng (trừ các tệp trong .dockerignore)
COPY . .

# 4. Mở cổng mạng dịch vụ
EXPOSE 3000

# 5. Kiểm tra sức khỏe container định kỳ (Healthcheck)
HEALTHCHECK --interval=20s --timeout=5s --start-period=5s --retries=3 \
  CMD node -e "require('http').get('http://localhost:3000/api', (res) => process.exit(res.statusCode === 200 ? 0 : 1))"

# 6. Biến môi trường mặc định
ENV NODE_ENV=production \
    PORT=3000 \
    LOG_LEVEL=INFO

# 7. Khởi chạy ứng dụng
CMD ["node", "src/app.js"]
