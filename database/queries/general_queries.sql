-- USE restaurant_ordering;

-- CREATE TABLE IF NOT EXISTS admins (
--     id INT AUTO_INCREMENT PRIMARY KEY,
--     email VARCHAR(255) UNIQUE NOT NULL,
--     password_hash VARCHAR(255) NOT NULL,
--     first_name VARCHAR(100),
--     last_name VARCHAR(100),
--     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
--     updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
--     INDEX idx_email (email)
-- );

-- USE restaurant_ordering;

-- INSERT INTO admins (email, password_hash, first_name, last_name) VALUES 
-- ('jadon@gmail.com', 'e8f6e9a8d9b5c7f3e4a2b1c6d9f5e8a7b4c2d1e9f6a8b5c7d3e9f2a4b6c8d0e', 'Jadon', 'Admin');

-- SELECT * FROM admins;

-- SELECT * FROM admins WHERE email = 'jadon@gmail.com';

-- UPDATE admins SET password_hash = '240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9' WHERE email = 'jadon@gmail.com';

-- USE restaurant_ordering;
-- ALTER TABLE orders ADD COLUMN order_status VARCHAR(50) DEFAULT 'pending';


SELECT * FROM admins;

