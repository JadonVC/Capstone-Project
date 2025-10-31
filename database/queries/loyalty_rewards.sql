-- Loyalty Points Tables
CREATE TABLE loyalty_accounts (
    id INT PRIMARY KEY AUTO_INCREMENT,
    customer_id INT NOT NULL,
    total_points INT DEFAULT 0,
    lifetime_points INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers(id),
    UNIQUE KEY (customer_id)
);

CREATE TABLE loyalty_transactions (
    id INT PRIMARY KEY AUTO_INCREMENT,
    customer_id INT NOT NULL,
    order_id INT,
    points_change INT NOT NULL,
    transaction_type ENUM('earned', 'redeemed', 'expired', 'adjusted') NOT NULL,
    description VARCHAR(255),
    balance_after INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers(id),
    FOREIGN KEY (order_id) REFERENCES orders(id),
    INDEX idx_customer (customer_id),
    INDEX idx_order (order_id)
);

CREATE TABLE rewards (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    points_required INT NOT NULL,
    discount_type ENUM('percentage', 'fixed_amount') NOT NULL,
    discount_value DECIMAL(10,2) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert some default rewards
INSERT INTO rewards (name, description, points_required, discount_type, discount_value) VALUES
('5% Off Your Order', 'Get 5% off your next order', 100, 'percentage', 5.00),
('$5 Off', 'Save $5 on your order', 250, 'fixed_amount', 5.00),
('10% Off Your Order', 'Get 10% off your next order', 500, 'percentage', 10.00),
('$10 Off', 'Save $10 on your order', 750, 'fixed_amount', 10.00),
('Free Delivery', '$3 delivery credit', 200, 'fixed_amount', 3.00),
('15% Off Your Order', 'Get 15% off your next order', 1000, 'percentage', 15.00);

-- Receipt Related Tables
ALTER TABLE orders 
ADD COLUMN receipt_generated BOOLEAN DEFAULT FALSE,
ADD COLUMN receipt_pdf_path VARCHAR(255),
ADD COLUMN loyalty_points_earned INT DEFAULT 0,
ADD COLUMN loyalty_points_redeemed INT DEFAULT 0,
ADD COLUMN discount_type VARCHAR(50),
ADD COLUMN discount_amount DECIMAL(10,2) DEFAULT 0;

-- Store receipt items for historical accuracy
CREATE TABLE receipt_items (
    id INT PRIMARY KEY AUTO_INCREMENT,
    order_id INT NOT NULL,
    item_name VARCHAR(255) NOT NULL,
    quantity INT NOT NULL,
    unit_price DECIMAL(10,2) NOT NULL,
    subtotal DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(id)
);