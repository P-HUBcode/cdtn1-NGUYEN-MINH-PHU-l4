# RESTful API Specification — Smart CRM Mekong Mobile Warranty Hub

**Course:** Graduation Internship / Capstone 1 (HK261) — Van Lang University  
**Student:** Nguyễn Minh Phú — **Student ID:** 2374802013447  
**Track:** Software Engineering (SE)  
**Flow L4:** Technician Assignment & Warranty Appointments Dispatching  
**Release Tag:** `v1.0`  
**Base URL:** `http://localhost:3000`

---

## 1. Overview & Architectural Standards

The Smart CRM Warranty Hub API adheres to modern RESTful design principles and software engineering best practices:
- **Data Exchange Format:** All requests and responses use `application/json; charset=utf-8`.
- **Idempotency & Correlation:** Every request is assigned a unique `X-Request-Id` (UUID v4) via middleware, propagated across logs and error payloads.
- **Data Boundary Protection (QT-15):** Customer phone numbers are masked as `090****567` at presentation boundary layer `toTicketView()`.
- **Role-Based Access Control (RBAC):** Authenticated endpoints inspect `Authorization: Bearer <token>` and `X-User-Role` headers.
- **Standard HTTP Status Codes:** `200 OK`, `201 Created`, `400 Bad Request`, `401 Unauthorized`, `403 Forbidden`, `404 Not Found`, `409 Conflict`, `500 Internal Server Error`.

---

## 2. Comprehensive Endpoint Specifications

### Endpoint 1: Service Health Check & System Metadata
- **1. Method & Path:** `GET /api`
- **2. Business Description:** Returns operational readiness status, version identifier, and server timestamp. Used by Docker Compose health checks and automated probes.
- **3. Auth Requirement:** Public (No authentication required).
- **4. Parameters & Request Body:** None.
- **5. Success Response:** `HTTP 200 OK`
  ```json
  {
    "name": "Smart CRM Warranty Hub API - Luồng L4",
    "version": "1.0.0",
    "author": "Nguyễn Minh Phú - 2374802013447",
    "status": "UP",
    "timestamp": "2026-11-11T04:30:00.000Z"
  }
  ```
- **6. Error Codes:** None.
- **7. Limitations & Rules:** Lightweight probe, guaranteed response time < 10ms.

---

### Endpoint 2: User Authentication & Token Issuance
- **1. Method & Path:** `POST /api/v1/auth/login`
- **2. Business Description:** Authenticates center managers, technicians, and administrators using salted SHA-256 cryptographic hashes.
- **3. Auth Requirement:** Public.
- **4. Request Body Schema:**
  | Field | Type | Required | Description |
  | :--- | :--- | :---: | :--- |
  | `username` | string | Yes | Account username (`quanly`, `ktv_binh`, `ktv_cuong`, `admin`). |
  | `password` | string | Yes | Plaintext password submitted for hashing and comparison (`123456`). |
- **5. Success Response:** `HTTP 200 OK`
  ```json
  {
    "success": true,
    "token": "demo-jwt-token-smart-crm-2026",
    "user": {
      "username": "quanly",
      "fullName": "Nguyễn Minh Phú (Quản lý)",
      "role": "MANAGER",
      "technicianId": null,
      "technicianName": null,
      "description": "Quản lý Trung tâm Cần Thơ — Toàn quyền điều phối, phân công & lịch hẹn"
    }
  }
  ```
- **6. Error Code Table:**
  | Status | Code | Description |
  | :--- | :--- | :--- |
  | `401 Unauthorized` | `UNAUTHORIZED` | Invalid credentials or inactive username. |
- **7. Limitations & Rules:** Timing-safe comparison prevents timing attacks (SE criterion S3).

---

### Endpoint 3: Retrieve Demo Accounts
- **1. Method & Path:** `GET /api/v1/auth/accounts`
- **2. Business Description:** Lists all seeded system user profiles for rapid evaluation in frontend demo pickers.
- **3. Auth Requirement:** Public.
- **4. Parameters:** None.
- **5. Success Response:** `HTTP 200 OK`
  ```json
  {
    "success": true,
    "count": 4,
    "data": [
      {
        "username": "quanly",
        "fullName": "Nguyễn Minh Phú (Quản lý)",
        "role": "MANAGER",
        "description": "Quản lý Trung tâm Cần Thơ"
      },
      {
        "username": "ktv_binh",
        "fullName": "Trần Văn Bình (KTV-001)",
        "role": "TECHNICIAN",
        "description": "Kỹ thuật viên chuyên Màn hình (Proficiency: 5/5, Pin: 4/5)"
      }
    ]
  }
  ```
- **6. Error Codes:** None.
- **7. Limitations:** Passwords and hashes are strictly excluded from output.

---

### Endpoint 4: List Warranty Tickets
- **1. Method & Path:** `GET /api/v1/tickets`
- **2. Business Description:** Retrieves warranty tickets with multi-criteria filtering (status, priority, center, technician).
- **3. Auth Requirement:** Authenticated (`Bearer <token>`).
- **4. Query Parameters:**
  | Parameter | Type | Required | Description |
  | :--- | :--- | :---: | :--- |
  | `status` | string | No | Filter by status (`MOI`, `DANG_XU_LY`, `CHO_LINH_KIEN`, `HOAN_TAT`). |
  | `center_id`| integer| No | Service center ID (e.g. `1` for Cần Thơ). |
  | `technician_id`| integer| No | Filter by assigned technician. |
- **5. Success Response:** `HTTP 200 OK`
  ```json
  {
    "success": true,
    "count": 5,
    "data": [
      {
        "ticket_id": 1,
        "ticket_code": "BH-202610-001",
        "customer_name": "Nguyễn Văn An",
        "customer_phone_masked": "090****567",
        "center_name": "Trung tâm Bảo hành Cần Thơ",
        "technician_name": "Chưa phân công",
        "issue_category": "MAN_HINH",
        "issue_desc": "Màn hình sọc xanh, nhấp nháy liên tục khi sử dụng",
        "priority": "CAO",
        "status": "MOI",
        "due_date": "2026-10-16T08:00:00.000Z"
      }
    ]
  }
  ```
- **6. Error Codes:**
  | Status | Code | Description |
  | :--- | :--- | :--- |
  | `401 Unauthorized` | `UNAUTHORIZED` | Missing or invalid Bearer token. |
- **7. Limitations:** Data contract compliance: `customer_phone_masked` conforms to QT-15.

---

### Endpoint 5: Get Warranty Ticket Details
- **1. Method & Path:** `GET /api/v1/tickets/:id`
- **2. Business Description:** Fetches complete ticket details including customer, center, assigned technician, and appointments.
- **3. Auth Requirement:** Authenticated (`Bearer <token>`).
- **4. Path Parameters:** `id` (integer, required) — Unique ticket identifier.
- **5. Success Response:** `HTTP 200 OK`
  ```json
  {
    "success": true,
    "data": {
      "ticket_id": 1,
      "ticket_code": "BH-202610-001",
      "customer_id": 1,
      "customer_name": "Nguyễn Văn An",
      "customer_phone_masked": "090****567",
      "center_id": 1,
      "center_name": "Trung tâm Bảo hành Cần Thơ",
      "technician_id": null,
      "technician_name": "Chưa phân công",
      "issue_category": "MAN_HINH",
      "issue_desc": "Màn hình sọc xanh, nhấp nháy liên tục khi sử dụng",
      "priority": "CAO",
      "status": "MOI",
      "received_at": "2026-10-15 08:00:00",
      "due_date": "2026-10-16T08:00:00.000Z"
    }
  }
  ```
- **6. Error Codes:**
  | Status | Code | Description |
  | :--- | :--- | :--- |
  | `400 Bad Request` | `VALIDATION_ERROR` | Ticket ID must be a positive integer. |
  | `404 Not Found` | `NOT_FOUND` | Ticket ID does not exist in database. |
- **7. Limitations:** Read-only operation.

---

### Endpoint 6: Create New Warranty Ticket (Intake)
- **1. Method & Path:** `POST /api/v1/tickets`
- **2. Business Description:** Records a new warranty intake ticket and calculates committed SLA resolution deadline.
- **3. Auth Requirement:** Role: `MANAGER` or `ADMIN`. Technicians receive `403 Forbidden`.
- **4. Request Body Schema:**
  | Field | Type | Required | Description |
  | :--- | :--- | :---: | :--- |
  | `customer_id` | integer | Yes | Existing registered customer ID. |
  | `center_id` | integer | Yes | Receiving service center ID. |
  | `issue_category`| string | Yes | `MAN_HINH`, `PIN`, `SAC`, `PHAN_MEM`, `NUOC_VAO`, `KHAC`. |
  | `issue_desc` | string | Yes | Fault description (minimum 5 characters). |
  | `priority` | string | Yes | `CAO` (+24h), `TRUNG_BINH` (+48h), `THAP` (+72h). |
- **5. Success Response:** `HTTP 201 Created`
  ```json
  {
    "success": true,
    "data": {
      "ticket_id": 6,
      "ticket_code": "BH-202611-006",
      "status": "MOI",
      "priority": "CAO",
      "due_date": "2026-11-12T08:00:00.000Z"
    }
  }
  ```
- **6. Error Codes:**
  | Status | Code | Description |
  | :--- | :--- | :--- |
  | `400 Bad Request` | `VALIDATION_ERROR` | Missing mandatory field or invalid priority enum. |
  | `403 Forbidden` | `FORBIDDEN` | Technicians are forbidden from creating tickets. |
- **7. Limitations:** SLA is computed automatically based on priority (rule QT-04).

---

### Endpoint 7: Intelligent Technician Recommendation
- **1. Method & Path:** `GET /api/v1/tickets/:id/recommend-technicians`
- **2. Business Description:** Executes the heuristic recommendation algorithm to score eligible technicians based on skill proficiency, active workload, and center affinity.
- **3. Auth Requirement:** Authenticated (`Bearer <token>`).
- **4. Path Parameters:** `id` (integer, required) — Ticket ID.
- **5. Success Response:** `HTTP 200 OK`
  ```json
  {
    "success": true,
    "ticket_id": 1,
    "category": "MAN_HINH",
    "recommendations": [
      {
        "technician_id": 1,
        "full_name": "Trần Văn Bình",
        "proficiency": 5,
        "active_workload": 0,
        "score": 100,
        "recommended": true,
        "reason": "Chuyên môn tối đa (5/5), khối lượng xử lý trống (0 phiếu)"
      },
      {
        "technician_id": 2,
        "full_name": "Lê Văn Cường",
        "proficiency": 3,
        "active_workload": 1,
        "score": 65,
        "recommended": false,
        "reason": "Trình độ đạt chuẩn (3/5), hiện đang nhận 1 phiếu"
      }
    ]
  }
  ```
- **6. Error Codes:**
  | Status | Code | Description |
  | :--- | :--- | :--- |
  | `404 Not Found` | `NOT_FOUND` | Ticket ID not found. |
- **7. Limitations:** Filter strictly eliminates technicians on leave (`NGHI_PHEP`) or below threshold `proficiency < 3` (QT-07).

---

### Endpoint 8: Assign Technician to Ticket
- **1. Method & Path:** `POST /api/v1/tickets/:id/assign`
- **2. Business Description:** Dispatches a qualified technician to a pending warranty ticket. Transitions status from `MOI` to `DANG_XU_LY`.
- **3. Auth Requirement:** Role: `MANAGER` or `ADMIN`. Technicians receive `403 Forbidden`.
- **4. Request Body Schema:**
  | Field | Type | Required | Description |
  | :--- | :--- | :---: | :--- |
  | `technician_id`| integer | Yes | Qualified technician ID. |
  | `notes` | string | No | Dispatch instructions or rationale. |
- **5. Success Response:** `HTTP 200 OK`
  ```json
  {
    "success": true,
    "message": "Phân công kỹ thuật viên thành công!",
    "data": {
      "ticket_id": 1,
      "technician_id": 1,
      "status": "DANG_XU_LY",
      "updated_at": "2026-11-11T04:35:00.000Z"
    }
  }
  ```
- **6. Error Codes:**
  | Status | Code | Description |
  | :--- | :--- | :--- |
  | `400 Bad Request` | `KTV_KHONG_DAT_CHUAN` | Technician proficiency < 3 or center mismatch (QT-06, QT-07). |
  | `400 Bad Request` | `KTV_NGHI_PHEP` | Technician is currently on leave (QT-06). |
  | `400 Bad Request` | `KTV_QUA_TAI` | Technician has reached the maximum capacity of 5 tickets (QT-06). |
  | `403 Forbidden` | `FORBIDDEN` | Caller lacks managerial authority. |
- **7. Limitations:** Creates an immutable record in `ticket_status_log`.

---

### Endpoint 9: Reassign Warranty Ticket
- **1. Method & Path:** `POST /api/v1/tickets/:id/reassign`
- **2. Business Description:** Reassigns an in-progress ticket to a different technician. Requires a justified business explanation (≥ 10 characters).
- **3. Auth Requirement:** Role: `MANAGER` or `ADMIN`.
- **4. Request Body Schema:**
  | Field | Type | Required | Description |
  | :--- | :--- | :---: | :--- |
  | `new_technician_id` | integer | Yes | Target technician ID. |
  | `reason` | string | Yes | Justification reason (minimum 10 characters). |
- **5. Success Response:** `HTTP 200 OK`
  ```json
  {
    "success": true,
    "message": "Chuyển gán kỹ thuật viên thành công!",
    "data": {
      "ticket_id": 1,
      "from_technician_id": 1,
      "to_technician_id": 2,
      "reason": "KTV Bình bận đột xuất, chuyển KTV Cường hỗ trợ hoàn thành đúng hạn"
    }
  }
  ```
- **6. Error Codes:**
  | Status | Code | Description |
  | :--- | :--- | :--- |
  | `400 Bad Request` | `LY_DO_QUA_NGAN` | Reason text contains fewer than 10 characters (QT-08). |
  | `400 Bad Request` | `TRUNG_KTV` | Target technician is identical to currently assigned technician. |
  | `403 Forbidden` | `FORBIDDEN` | Technicians cannot reassign tickets. |
- **7. Limitations:** Previous technician assignment is preserved in audit logs.

---

### Endpoint 10: Update Ticket Progress & Status
- **1. Method & Path:** `POST /api/v1/tickets/:id/status`
- **2. Business Description:** Updates warranty ticket lifecycle status (`CHO_LINH_KIEN`, `HOAN_TAT`).
- **3. Auth Requirement:** Authenticated (`MANAGER`, `ADMIN`, or assigned `TECHNICIAN`).
- **4. Request Body Schema:**
  | Field | Type | Required | Description |
  | :--- | :--- | :---: | :--- |
  | `status` | string | Yes | Target status: `CHO_LINH_KIEN`, `HOAN_TAT`. |
  | `note` | string | Yes | Work log progress details (minimum 3 characters). |
- **5. Success Response:** `HTTP 200 OK`
  ```json
  {
    "success": true,
    "message": "Cập nhật tiến độ xử lý phiếu thành công!",
    "data": {
      "ticket_id": 1,
      "status": "CHO_LINH_KIEN",
      "note": "Đang chờ linh kiện màn hình OLED từ kho trung tâm"
    }
  }
  ```
- **6. Error Codes:**
  | Status | Code | Description |
  | :--- | :--- | :--- |
  | `400 Bad Request` | `PHIEU_DA_HOAN_TAT` | Ticket is already completed (`HOAN_TAT`); further modifications locked. |
  | `400 Bad Request` | `TRANG_THAI_KHONG_HOP_LE` | Invalid transition according to state machine. |
  | `403 Forbidden` | `FORBIDDEN` | Technician attempting to edit a ticket assigned to someone else (OWASP A01). |
- **7. Limitations:** Once a ticket reaches `HOAN_TAT`, it is permanently immutable.

---

### Endpoint 11: Patch Ticket Workflow Status
- **1. Method & Path:** `PATCH /api/v1/tickets/:id/status`
- **2. Business Description:** Partial update equivalent to Endpoint 10 for HTTP REST verb consistency.
- **3. Auth Requirement:** Same as Endpoint 10.
- **4. Request Body Schema:** Same as Endpoint 10.
- **5. Success Response:** `HTTP 200 OK` (identical schema to Endpoint 10).
- **6. Error Codes:** Identical to Endpoint 10.
- **7. Limitations:** Same business state machine validation.

---

### Endpoint 12: List Technicians & Capacities
- **1. Method & Path:** `GET /api/v1/technicians`
- **2. Business Description:** Lists all registered technicians, their status, skill matrices, and real-time active ticket counts.
- **3. Auth Requirement:** Authenticated (`Bearer <token>`).
- **4. Parameters:** None.
- **5. Success Response:** `HTTP 200 OK`
  ```json
  {
    "success": true,
    "count": 4,
    "data": [
      {
        "technician_id": 1,
        "technician_code": "KTV-001",
        "full_name": "Trần Văn Bình",
        "status": "HOAT_DONG",
        "active_tickets_count": 1,
        "skills": {
          "MAN_HINH": 5,
          "PIN": 4
        }
      }
    ]
  }
  ```
- **6. Error Codes:** `401 Unauthorized`.
- **7. Limitations:** Real-time calculated aggregate for dispatch decision-making.

---

### Endpoint 13: List Ticket Appointments
- **1. Method & Path:** `GET /api/v1/tickets/:id/appointments`
- **2. Business Description:** Retrieves appointment history for customer intake inspection or repaired device pickup.
- **3. Auth Requirement:** Authenticated (`Bearer <token>`).
- **4. Path Parameters:** `id` (integer, required).
- **5. Success Response:** `HTTP 200 OK`
  ```json
  {
    "success": true,
    "count": 1,
    "data": [
      {
        "appointment_id": 101,
        "ticket_id": 1,
        "appointment_type": "GIAO_MAY",
        "appointment_date": "2026-11-20T09:00:00.000Z",
        "status": "DA_XAC_NHAN",
        "notes": "Khách hẹn nhận máy buổi sáng tại quầy 1"
      }
    ]
  }
  ```
- **6. Error Codes:** `404 Not Found`.
- **7. Limitations:** Read-only timeline view.

---

### Endpoint 14: Schedule Customer Appointment
- **1. Method & Path:** `POST /api/v1/tickets/:id/appointments`
- **2. Business Description:** Books an intake or return appointment in 30-minute intervals. Validates slot capacity limit (maximum 5 appointments per 30-minute window).
- **3. Auth Requirement:** Role: `MANAGER` or `ADMIN`.
- **4. Request Body Schema:**
  | Field | Type | Required | Description |
  | :--- | :--- | :---: | :--- |
  | `appointment_type` | string | Yes | `NHAN_MAY` (Intake) or `GIAO_MAY` (Return). |
  | `appointment_date` | string | Yes | ISO 8601 timestamp string (e.g. `2026-11-20T09:00:00Z`). |
  | `notes` | string | No | Optional appointment notes or service counter preferences. |
- **5. Success Response:** `HTTP 201 Created`
  ```json
  {
    "success": true,
    "message": "Đặt lịch hẹn thành công!",
    "data": {
      "appointment_id": 102,
      "ticket_id": 1,
      "appointment_type": "GIAO_MAY",
      "appointment_date": "2026-11-20T09:00:00.000Z",
      "status": "DA_XAC_NHAN",
      "notes": "Khách hẹn nhận máy buổi sáng tại quầy 1"
    }
  }
  ```
- **6. Error Codes:**
  | Status | Code | Description |
  | :--- | :--- | :--- |
  | `400 Bad Request` | `VALIDATION_ERROR` | Invalid appointment type or malformed date string. |
  | `409 Conflict` | `LICH_HEN_QUA_TAI` | Slot capacity exceeded (5/5 appointments in this 30-minute interval, QT-09). |
  | `403 Forbidden` | `FORBIDDEN` | Technicians lack authorization to schedule appointments. |
- **7. Limitations:** Enforces strict slot collision detection (Rule QT-09).

---

### Endpoint 15: Retrieve Ticket Audit Trail Logs
- **1. Method & Path:** `GET /api/v1/tickets/:id/logs`
- **2. Business Description:** Returns the tamper-evident chronological audit log recording every dispatch, reassignment, and status transition.
- **3. Auth Requirement:** Authenticated (`Bearer <token>`).
- **4. Path Parameters:** `id` (integer, required).
- **5. Success Response:** `HTTP 200 OK`
  ```json
  {
    "success": true,
    "count": 2,
    "data": [
      {
        "log_id": 1,
        "ticket_id": 1,
        "from_status": "MOI",
        "to_status": "DANG_XU_LY",
        "from_technician_id": null,
        "to_technician_id": 1,
        "reason": null,
        "note": "Phân công KTV Trần Văn Bình (tay nghề 5/5)",
        "changed_by": 1,
        "changed_at": "2026-11-11 04:35:00"
      }
    ]
  }
  ```
- **6. Error Codes:** `404 Not Found`.
- **7. Limitations:** Append-only log table; records cannot be updated or deleted.

---

### Endpoint 16: Update Warranty Ticket Information
- **1. Method & Path:** `PUT /api/v1/tickets/:id`
- **2. Business Description:** Updates mutable ticket fields (`issue_desc`, `priority`, `issue_category`). If the ticket is in `MOI` status and priority changes, the SLA due date is automatically recalculated. If the ticket is already completed (`HOAN_TAT`), updates are rejected.
- **3. Auth Requirement:** Authenticated (`Bearer <token>`, Manager or Admin role). Technicians receive `403 Forbidden`.
- **4. Parameters & Request Body Schema:**
  - Path Parameter: `id` (integer, required).
  - Body:
    | Field | Type | Required | Description |
    | :--- | :--- | :---: | :--- |
    | `issue_desc` | string | No | Description of the issue (min 10 characters). |
    | `priority` | string | No | Priority level (`CAO`, `TRUNG_BINH`, `THAP`). |
    | `issue_category` | string | No | Defect category (`MAN_HINH`, `PIN`, `SAC`, `PHAN_MEM`, `NUOC_VAO`, `KHAC`). |
    | `note` | string | No | Audit note explaining the change. |
- **5. Success Response:** `HTTP 200 OK`
  ```json
  {
    "success": true,
    "message": "Cập nhật thông tin phiếu bảo hành thành công",
    "data": {
      "ticket_id": 1,
      "ticket_code": "BH-202610-001",
      "customer_name": "Nguyễn Văn An",
      "customer_phone": "090****567",
      "center_name": "Trung tâm Cần Thơ",
      "issue_category": "MAN_HINH",
      "issue_desc": "Màn hình sọc xanh dọc thân máy, cảm ứng bị đơ góc trên bên phải sau khi va đập",
      "priority": "CAO",
      "status": "DANG_XU_LY",
      "technician_name": "Trần Văn Bình",
      "due_date": "2026-11-12T08:00:00.000Z"
    }
  }
  ```
- **6. Error Codes:**
  | Status | Code | Description |
  | :--- | :--- | :--- |
  | `400 Bad Request` | `MO_TA_SU_CO_QUA_NGAN` | Issue description has less than 10 characters. |
  | `400 Bad Request` | `MUC_UU_TIEN_KHONG_HOP_LE` | Priority value is not in `[CAO, TRUNG_BINH, THAP]`. |
  | `400 Bad Request` | `PHIEU_DA_HOAN_TAT` | Ticket is already completed (`HOAN_TAT`); modification forbidden. |
  | `403 Forbidden` | `FORBIDDEN` | Technicians lack authorization to update ticket general details. |
  | `404 Not Found` | `PHIEU_KHONG_TON_TAI` | Ticket ID does not exist. |
- **7. Limitations & Rules:** Only pending tickets can be edited; automatically registers a status audit log record.

---

### Endpoint 17: Delete Warranty Ticket
- **1. Method & Path:** `DELETE /api/v1/tickets/:id`
- **2. Business Description:** Deletes an erroneous ticket created at the reception desk. Only allowed for tickets in `MOI` (New) or `HUY` (Cancelled) status. Tickets in `DANG_XU_LY`, `CHO_LINH_KIEN`, or `HOAN_TAT` cannot be deleted.
- **3. Auth Requirement:** Authenticated (`Bearer <token>`, Manager or Admin role). Technicians receive `403 Forbidden`.
- **4. Path Parameters:** `id` (integer, required).
- **5. Success Response:** `HTTP 200 OK`
  ```json
  {
    "success": true,
    "message": "Đã xóa thành công phiếu bảo hành ID=10",
    "deleted_ticket_id": 10
  }
  ```
- **6. Error Codes:**
  | Status | Code | Description |
  | :--- | :--- | :--- |
  | `400 Bad Request` | `KHONG_THE_XOA_PHIEU` | Cannot delete ticket in processing (`DANG_XU_LY`, `CHO_LINH_KIEN`, `HOAN_TAT`). |
  | `403 Forbidden` | `FORBIDDEN` | Technicians are forbidden from deleting tickets. |
  | `404 Not Found` | `PHIEU_KHONG_TON_TAI` | Ticket ID does not exist. |
- **7. Limitations & Rules:** Cascade deletion deletes associated status logs and appointments.

---

### Endpoint 18: List All Appointments
- **1. Method & Path:** `GET /api/v1/appointments`
- **2. Business Description:** Retrieves all customer appointments across all tickets with optional filtering by status and ticket ID.
- **3. Auth Requirement:** Authenticated (`Bearer <token>`).
- **4. Query Parameters:**
  | Parameter | Type | Required | Description |
  | :--- | :--- | :---: | :--- |
  | `status` | string | No | Filter by appointment status (`CHO_XAC_NHAN`, `DA_XAC_NHAN`, `DA_HOAN_THANH`, `DA_HUY`). |
  | `ticket_id` | integer | No | Filter by specific ticket ID. |
- **5. Success Response:** `HTTP 200 OK`
  ```json
  {
    "success": true,
    "count": 2,
    "data": [
      {
        "appointment_id": 1,
        "ticket_id": 1,
        "appointment_type": "GIAO_MAY",
        "appointment_date": "2026-11-20T09:00:00.000Z",
        "status": "DA_XAC_NHAN",
        "notes": "Hẹn trả máy tại quầy tiếp nhận",
        "created_at": "2026-11-11 05:00:00"
      }
    ]
  }
  ```
- **6. Error Codes:** None.
- **7. Limitations & Rules:** Chronologically ordered by `appointment_date ASC`.

---

### Endpoint 19: Get Appointment Details by ID
- **1. Method & Path:** `GET /api/v1/appointments/:id`
- **2. Business Description:** Retrieves the detailed metadata of a specific appointment record.
- **3. Auth Requirement:** Authenticated (`Bearer <token>`).
- **4. Path Parameters:** `id` (integer, required).
- **5. Success Response:** `HTTP 200 OK`
  ```json
  {
    "success": true,
    "data": {
      "appointment_id": 1,
      "ticket_id": 1,
      "appointment_type": "GIAO_MAY",
      "appointment_date": "2026-11-20T09:00:00.000Z",
      "status": "DA_XAC_NHAN",
      "notes": "Hẹn trả máy tại quầy tiếp nhận",
      "created_at": "2026-11-11 05:00:00"
    }
  }
  ```
- **6. Error Codes:**
  | Status | Code | Description |
  | :--- | :--- | :--- |
  | `404 Not Found` | `LICH_HEN_KHONG_TON_TAI` | Appointment record not found. |
- **7. Limitations & Rules:** None.

---

### Endpoint 20: Update Customer Appointment
- **1. Method & Path:** `PUT /api/v1/appointments/:id`
- **2. Business Description:** Reschedules an appointment or updates its workflow status and dispatch notes. Enforces QT-09 capacity checking if `appointment_date` is moved to a new timeslot.
- **3. Auth Requirement:** Authenticated (`Bearer <token>`, Manager or Admin role). Technicians receive `403 Forbidden`.
- **4. Parameters & Request Body Schema:**
  - Path Parameter: `id` (integer, required).
  - Body:
    | Field | Type | Required | Description |
    | :--- | :--- | :---: | :--- |
    | `appointment_date` | string (ISO 8601) | No | New rescheduled time. |
    | `status` | string | No | New status (`CHO_XAC_NHAN`, `DA_XAC_NHAN`, `DA_HOAN_THANH`, `DA_DOI_LICH`, `DA_HUY`). |
    | `appointment_type` | string | No | `NHAN_MAY` or `GIAO_MAY`. |
    | `notes` | string | No | Detailed scheduling notes. |
- **5. Success Response:** `HTTP 200 OK`
  ```json
  {
    "success": true,
    "message": "Cập nhật lịch hẹn giao nhận thành công",
    "data": {
      "appointment_id": 1,
      "ticket_id": 1,
      "appointment_type": "GIAO_MAY",
      "appointment_date": "2026-11-21T10:00:00.000Z",
      "status": "DA_DOI_LICH",
      "notes": "Khách dời lịch hẹn sang sáng thứ Bảy",
      "created_at": "2026-11-11 05:00:00"
    }
  }
  ```
- **6. Error Codes:**
  | Status | Code | Description |
  | :--- | :--- | :--- |
  | `400 Bad Request` | `NGAY_HEN_KHONG_HOP_LE` | Invalid appointment timestamp. |
  | `400 Bad Request` | `TRANG_THAI_LICH_HEN_KHONG_HOP_LE` | Status string not in allowable set. |
  | `403 Forbidden` | `FORBIDDEN` | Technicians are forbidden from modifying appointments. |
  | `404 Not Found` | `LICH_HEN_KHONG_TON_TAI` | Appointment record not found. |
  | `409 Conflict` | `LICH_HEN_QUA_TAI` | The target timeslot already has 5 active bookings (QT-09). |
- **7. Limitations & Rules:** Enforces slot capacity rule QT-09 when changing dates.

---

### Endpoint 21: Delete Customer Appointment
- **1. Method & Path:** `DELETE /api/v1/appointments/:id`
- **2. Business Description:** Removes or cancels an appointment from the central calendar.
- **3. Auth Requirement:** Authenticated (`Bearer <token>`, Manager or Admin role). Technicians receive `403 Forbidden`.
- **4. Path Parameters:** `id` (integer, required).
- **5. Success Response:** `HTTP 200 OK`
  ```json
  {
    "success": true,
    "message": "Đã xóa thành công lịch hẹn ID=1",
    "deleted_appointment_id": 1
  }
  ```
- **6. Error Codes:**
  | Status | Code | Description |
  | :--- | :--- | :--- |
  | `403 Forbidden` | `FORBIDDEN` | Technicians lack permission to delete appointments. |
  | `404 Not Found` | `LICH_HEN_KHONG_TON_TAI` | Appointment record not found. |
- **7. Limitations & Rules:** Permanent deletion freeing up capacity in the 30-minute timeslot.

---

### Endpoint 22: Reset Demo State (Idempotent Test Helper)
- **1. Method & Path:** `POST /api/v1/tickets/reset-demo`
- **2. Business Description:** Resets demo tickets #1 and #2 back to `MOI` status and cleans test appointment slots. Implemented cleanly in `TicketRepository.resetDemoData()` without raw SQL in routes/controllers.
- **3. Auth Requirement:** Public (Development / Workshop verification).
- **4. Parameters & Body:** None.
- **5. Success Response:** `HTTP 200 OK`
  ```json
  {
    "success": true,
    "message": "Đã khôi phục các phiếu mẫu về trạng thái MOI!"
  }
  ```
- **6. Error Codes:** None.
- **7. Limitations & Rules:** Safe idempotent operation for workshop grading and reproducibility verification.
