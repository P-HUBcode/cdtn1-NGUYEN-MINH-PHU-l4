# Deployment & Setup Guide — Smart CRM Mekong Mobile (Flow L4)

**Student:** Nguyễn Minh Phú — **Student ID:** 2374802013447  
**Track:** Software Engineering (SE) — **Academic Year:** HK261, Van Lang University  
**Topic:** Flow L4 — Technician Assignment & Warranty Appointments Dispatching  
**Release Tag:** `v1.0`

---

## 1. Environment Requirements

Before running the prototype, ensure your host environment meets the following specifications:

| Component | Minimum Specification | Recommended Specification | Notes |
| :--- | :--- | :--- | :--- |
| **Operating System** | Ubuntu 22.04 LTS / macOS 13+ / Windows 10/11 (WSL2) | Ubuntu 24.04 LTS / macOS 14+ / Windows 11 | Cross-platform container runtime |
| **Docker Engine** | `v24.0.0` or higher | `v27.0.0` or higher | Required for containerized build |
| **Docker Compose** | `v2.20.0` or higher (`compose-plugin`) | `v2.29.0` or higher | Uses `docker compose` syntax (Compose V2) |
| **Node.js (Host Bare-metal)** | Node.js `v20.0.0` LTS (Alpine/Debian) | Node.js `v20.18.0` LTS | Only required if running without Docker |
| **Memory (RAM)** | 2.0 GB RAM available | 4.0 GB RAM available | Application runtime footprint is ~80MB |
| **Disk Space** | 1.5 GB available storage | 3.0 GB available storage | For Docker base image and dependencies |
| **Port Availability** | Port `3000` (TCP) free | Port `3000` (TCP) free | Configurable via `PORT` variable |

---

## 2. Step-by-Step Setup (Zero-Configuration White-box Test)

The entire system is containerized and conforms to the two-command zero-configuration white-box test standard.

### Step 1: Clone Repository
Clone the repository using release tag `v1.0`:
```bash
git clone --branch v1.0 https://github.com/P-HUBcode/cdtn1-NGUYEN-MINH-PHU-l4.git
cd cdtn1-NGUYEN-MINH-PHU-l4
```

### Step 2: Initialize Configuration
Copy the provided environment template file:
```bash
cp .env.example .env
```

### Step 3: Launch System via Docker Compose
Build the container image and launch all background services in detached mode:
```bash
docker compose up -d --build
```
> **White-box Test Note:** Step 2 and Step 3 constitute the exact **two commands** required to initialize and run the prototype on an empty machine.

---

### Alternative: Bare-Metal Local Development Setup
If Docker is unavailable, the application can be executed directly on the host using Node.js:

```bash
# 1. Install dependencies
npm ci

# 2. Initialize environment configuration
npm run setup

# 3. Start application
npm start
```

---

## 3. Environment Variables Configuration

The application reads runtime configurations from `.env`. The table below outlines all available parameters:

| Variable Name | Default Value | Required | Business Purpose & Description |
| :--- | :--- | :---: | :--- |
| `PORT` | `3000` | No | Listening TCP port for the Express application server and REST API. |
| `NODE_ENV` | `production` | No | Application environment mode (`development`, `test`, `production`). Suppresses verbose stack traces in production. |
| `DATABASE_TYPE` | `sqlite` | No | Embedded database engine. SQLite requires zero external server setup. |
| `DATABASE_URL` | `db/warranty.sqlite` | No | Relative or absolute path to the persistent SQLite database file. |
| `LOG_LEVEL` | `INFO` | No | Structured logger threshold (`DEBUG`, `INFO`, `WARN`, `ERROR`). |
| `JWT_SECRET` | `smart-crm-warranty-hub-se-hk261-secret-key-2026` | No | Secret key used for cryptographic signature of mock JWT authorization tokens. |

---

## 4. Sample Data Verification

The SQLite database is automatically seeded upon application startup (`initDatabase()` in `src/config/database.js`). Seeding is **strictly idempotent** (running multiple times or restarting containers never duplicates or corrupts rows).

### Seeded Entities Summary:
- **Warranty Tickets:** 5 seeded tickets (ID `#1` to `#5`), spanning statuses `MOI`, `DA_TIEP_NHAN`, `DANG_SUA`, `CHO_LINH_KIEN`.
- **Technicians:** 4 active technicians with verified skill vectors and current workload counters:
  - `Trần Văn Bình` (ID: 1): Specializes in Screen repairs (`MAN_HINH` proficiency 5/5, Battery 4/5).
  - `Lê Văn Cường` (ID: 2): Specializes in Software and Motherboard (`PHAN_MEM` 5/5, Screen 3/5).
  - `Phạm Minh Đức` (ID: 3): Hardware technician (`PHAN_CUNG` 5/5, Camera 4/5).
  - `Hoàng Kim Oanh` (ID: 4): Senior diagnostic technician (`MAN_HINH` 4/5, `CAMERA` 5/5).
- **Appointments:** 3 scheduled customer pickup/inspection appointments.

### Demo User Accounts for Testing:
| Username | Password | Role | Assigned Profile | Permission Boundary |
| :--- | :--- | :--- | :--- | :--- |
| `quanly` | `123456` | `MANAGER` | Nguyễn Minh Phú (Dispatch Manager) | Full access: Assign, reassign, schedule, oversee |
| `ktv_binh` | `123456` | `TECHNICIAN` | Trần Văn Bình (KTV-001) | Restricted: Only updates status of self-assigned tickets |
| `ktv_cuong` | `123456` | `TECHNICIAN` | Lê Văn Cường (KTV-002) | Restricted: Only updates status of self-assigned tickets |
| `admin` | `123456` | `ADMIN` | System Administrator | Full administrative system oversight |

### Verification Command:
Verify that sample tickets and technicians exist:
```bash
curl -s http://localhost:3000/api/v1/tickets | grep -o '"count":[0-9]*'
# Expected output: "count":5
```

---

## 5. Health Check & Test Suite Execution

### 5.1 Container Health Check Verification
Execute the following commands to ensure all container services are healthy:

```bash
# 1. Inspect Docker container status
docker compose ps
# Expected output: smartcrm_warranty_hub ... Up ... (healthy)

# 2. Query REST API Healthcheck endpoint
curl -s http://localhost:3000/api
```

**Expected JSON Response:**
```json
{
  "name": "Smart CRM Warranty Hub API - Luồng L4",
  "version": "1.0.0",
  "author": "Nguyễn Minh Phú - 2374802013447",
  "status": "UP",
  "timestamp": "2026-11-11T04:30:00.000Z"
}
```

### 5.2 Single-Command Test Suite Execution
Execute the automated test suite verifying all 12 test cases across 5 test categories:

```bash
# Inside running container:
docker compose exec app npm test

# Or on host:
npm run test:report
```

**Expected Result:**
```
================================================================================
           BÁO CÁO THỰC THI 12 CA KIỂM THỬ BÀI TẬP 3 (TRACK SE)
================================================================================
 TỔNG SỐ TEST CASE ĐÃ CHẠY: 12
 SỐ CA KIỂM THỬ ĐẠT (PASS): 12 (100.0%)
 SỐ CA KIỂM THỬ HỎNG (FAIL): 0 (0.0%)
 ĐỦ 5 LOẠI: CÓ (Luồng đúng: 5, Giá trị biên: 3, Dữ liệu sai: 2, Bảo mật: 1, Tái lập: 1)
 KẾT LUẬN: ĐẠT TIÊU CHÍ BÀI TẬP 3
================================================================================
```

### 5.3 Web GUI & Interactive Test Dashboard Access
Open any modern web browser to access:
- **Platform Web UI:** `http://localhost:3000`
- **Interactive Live Test Dashboard:** `http://localhost:3000/test-dashboard.html`

---

## 6. Optional Cloud Deployment (Bonus Points — Rubric 3.3)

To qualify for optional bonus points (+0.5 to +1.0 marks), the system can be deployed to a cloud platform (e.g., Render.com or Railway.app) directly from the public GitHub repository.

### Step-by-Step Deployment on Render.com:
1. **Create Account:** Sign up or log in to [https://render.com](https://render.com) using your GitHub account.
2. **New Web Service:**
   - In Dashboard, click **New +** -> **Web Service**.
   - Select **Build and deploy from a Git repository**.
   - Paste the public repository URL: `https://github.com/P-HUBcode/cdtn1-NGUYEN-MINH-PHU-l4`.
3. **Configure Service Settings:**
   - **Name:** `smartcrm-warranty-hub-l4`
   - **Region:** Singapore (Southeast Asia - closest latency)
   - **Branch:** `main` (or Tag `v1.0`)
   - **Runtime:** `Node`
   - **Build Command:** `npm ci --omit=dev`
   - **Start Command:** `npm start`
   - **Plan Type:** `Free`
4. **Environment Variables Configuration:**
   Add the following environment variables in the **Environment** tab:
   - `NODE_ENV` = `production`
   - `NODE_VERSION` = `22.14.0`
   - `JWT_SECRET` = `smart-crm-warranty-hub-se-hk261-secret-key-2026`
   - `LOG_LEVEL` = `INFO`
5. **Deploy & Verification:**
   - Click **Deploy Web Service**.
   - Wait 1–2 minutes for the build to complete.
   - Once the service status displays **Live**, test the public healthcheck URL:
     `https://<your-service-name>.onrender.com/api`
   - Verify the Web UI in any browser:
     `https://<your-service-name>.onrender.com`

