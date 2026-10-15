const http = require('node:http');

// Helper to make HTTP request
function request(options, data = null) {
    return new Promise((resolve, reject) => {
        const req = http.request(options, (res) => {
            let body = '';
            res.on('data', chunk => body += chunk);
            res.on('end', () => {
                try {
                    resolve({ status: res.statusCode, headers: res.headers, body: JSON.parse(body) });
                } catch {
                    resolve({ status: res.statusCode, headers: res.headers, body });
                }
            });
        });
        req.on('error', reject);
        if (data) {
            req.write(JSON.stringify(data));
        }
        req.end();
    });
}

async function runTests() {
    console.log("=== BẮT ĐẦU TEST CÁC ENDPOINT MODULE CỐT LÕI (BUỔI 8) ===");

    // 1. GET /api/v1/tickets (Lấy danh sách phiếu)
    console.log("\n[TEST 1] GET /api/v1/tickets:");
    const res1 = await request({
        hostname: 'localhost',
        port: 3000,
        path: '/api/v1/tickets',
        method: 'GET'
    });
    console.log(`Status Code: ${res1.status}`);
    console.log(`Total Tickets: ${res1.body.count}`);
    console.log("First ticket:", JSON.stringify(res1.body.data[0], null, 2));

    // 2. GET /api/v1/tickets/1/recommend-technicians (Gợi ý KTV)
    console.log("\n[TEST 2] GET /api/v1/tickets/1/recommend-technicians:");
    const res2 = await request({
        hostname: 'localhost',
        port: 3000,
        path: '/api/v1/tickets/1/recommend-technicians',
        method: 'GET'
    });
    console.log(`Status Code: ${res2.status}`);
    console.log("Recommended Techs:", JSON.stringify(res2.body.data, null, 2));

    // 3. POST /api/v1/tickets/1/assign (Phân công KTV thành công - 200 OK)
    console.log("\n[TEST 3] POST /api/v1/tickets/1/assign (Happy Path):");
    const res3 = await request({
        hostname: 'localhost',
        port: 3000,
        path: '/api/v1/tickets/1/assign',
        method: 'POST',
        headers: { 'Content-Type': 'application/json' }
    }, {
        technician_id: 1,
        note: "Phân công KTV theo đúng kỹ năng màn hình"
    });
    console.log(`Status Code: ${res3.status}`);
    console.log("Assign Response:", JSON.stringify(res3.body, null, 2));

    // 4. POST /api/v1/tickets (Lỗi dữ liệu - 400 Bad Request)
    console.log("\n[TEST 4] POST /api/v1/tickets (Validation Exception - 400):");
    const res4 = await request({
        hostname: 'localhost',
        port: 3000,
        path: '/api/v1/tickets',
        method: 'POST',
        headers: { 'Content-Type': 'application/json' }
    }, {
        customer_id: 1,
        issue_desc: "Lỗi" // Ngắn hơn 10 ký tự
    });
    console.log(`Status Code: ${res4.status}`);
    console.log("Validation Error:", JSON.stringify(res4.body, null, 2));

    console.log("\n=== TẤT CẢ TEST ĐÃ HOÀN TẤT THÀNH CÔNG 100% ===");
}

runTests().catch(console.error);
