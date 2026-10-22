const { db } = require('../src/config/database');

db.prepare(`UPDATE tickets SET status = 'MOI', technician_id = NULL WHERE ticket_id IN (1, 2)`).run();

console.log('Current tickets:');
console.table(db.prepare('SELECT ticket_id, ticket_code, status, technician_id, customer_id, priority FROM tickets').all());
