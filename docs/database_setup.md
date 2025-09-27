# Database Setup Using SQLTools - Restaurant Ordering System

## Step 1: Install Required Extensions

1. Open VS Code
2. Go to Extensions (Ctrl+Shift+X)
3. Search and install these extensions:
   - **SQLTools** by Matheus Teixeira
   - **SQLTools MySQL/MariaDB** by Matheus Teixeira

## Step 2: Set up MySQL Connection

1. **Open SQLTools Panel:**
   - Look for the SQLTools icon in the left sidebar (database icon)
   - Click on it to open the SQLTools panel

2. **Add New Connection:**
   - Click the '+' button next to "SQLTools: Connections (0)"
   - Select **MySQL/MariaDB** from the driver list

3. **Fill in Connection Details:**
   ```
   Connection Name: Restaurant Database
   Connection group: [leave blank]
   Connect using: Server and Port
   Server Address: localhost
   Port: 3306
   Database: mysql
   Username: root
   Password mode: Ask on connect (root most likely)
   ```

4. **MySQL Driver Options:**
   - Authentication Protocol: default
   - SSL: Disabled
   - Over SSH: Disabled

5. **Click "SAVE CONNECTION"**

## Step 3: Connect to MySQL

1. Click **"Connect Now"** when prompted
2. Enter your MySQL password when asked
3. You should see "Restaurant Database" appear in your SQLTools connections

## Step 4: Create Database and Tables

1. **Right-click on "Restaurant Database"** and select "New SQL File"
2. **Copy and paste this SQL code:**

```sql
-- Create the restaurant database
CREATE DATABASE IF NOT EXISTS restaurant_ordering;
USE restaurant_ordering;

-- Create menu_items table
CREATE TABLE IF NOT EXISTS menu_items (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    category VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert sample menu items
INSERT INTO menu_items (name, description, price, category) VALUES
('Classic Cheeseburger', 'Juicy beef patty with cheddar cheese, lettuce, tomato, and our special sauce', 12.99, 'burgers'),
('Chicken Caesar Salad', 'Fresh romaine lettuce with grilled chicken, parmesan cheese, croutons, and caesar dressing', 10.99, 'salads'),
('Margherita Pizza', 'Traditional pizza with tomato sauce, fresh mozzarella, basil, and olive oil', 14.99, 'pizza'),
('Fish and Chips', 'Beer-battered cod with golden fries and tartar sauce', 16.99, 'seafood'),
('Chocolate Brownie', 'Warm chocolate brownie served with vanilla ice cream', 6.99, 'desserts'),
('Coca Cola', 'Ice-cold Coca Cola served in a chilled glass', 2.99, 'drinks'),
('BBQ Bacon Burger', 'Beef patty with crispy bacon, BBQ sauce, onion rings, and cheddar cheese', 15.99, 'burgers'),
('Greek Salad', 'Mixed greens with feta cheese, olives, tomatoes, cucumbers, and olive oil dressing', 9.99, 'salads');

-- Verify the data
SELECT * FROM menu_items;
```

3. **Run the SQL:**
   - Press Ctrl+Shift+E to run all queries
   - Or click "Run on active connection" at the top of the file

## Step 5: Verify Database Setup

You should see results showing:
- Database created successfully
- Table created successfully  
- 8 menu items inserted
- Final SELECT showing all your menu data with IDs 1-8

## Step 6: Update Backend Configuration

# In backend/app.py, update this section with your MySQL credentials:
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'your_mysql_password',  # Change this to your actual password
    'database': 'restaurant_ordering',
    'port': 3306
}

## Step 7: Install Python Dependencies

Open terminal in VS Code and run:

```bash
cd backend
pip install flask flask-cors mysql-connector-python
```

## Step 8: Test the Setup

1. **Start the Backend:**
   ```bash
   cd backend
   python app.py
   ```
   You should see:
   ```
   Starting Restaurant Menu API...
   Available at: http://localhost:5000
   ```

2. **Test the API:**
   - Open browser and go to: http://localhost:5000/api/menu
   - You should see JSON data with your 8 menu items

3. **Test the Frontend:**
   - Open `frontend/index.html` in your browser
   - You should see the restaurant menu with category filters
   - All 8 items should display with names, descriptions, and prices
   - Can also launch with Live Server and should work

## Troubleshooting

**If connection fails:**
- Make sure MySQL is running on your system
- Verify your username and password are correct
- Try connecting to MySQL command line first: `mysql -u root -p`

**If database creation fails:**
- Check that you have permission to create databases
- Make sure you're connected to MySQL server (not a specific database)

**If backend can't connect:**
- Double-check the password in `backend/config.py`
- Ensure the database name matches exactly: `restaurant_ordering`

**If frontend shows errors:**
- Make sure the Flask backend is running first
- Check browser console for specific error messages
- Verify the API endpoint returns data: http://localhost:5000/api/menu

## Success Checklist

- [ ] SQLTools extensions installed
- [ ] MySQL connection established  
- [ ] Database `restaurant_ordering` created
- [ ] Table `menu_items` created with 8 sample items
- [ ] Backend config updated with correct credentials
- [ ] Python dependencies installed
- [ ] Backend API running and returning JSON data
- [ ] Frontend displaying menu items with filtering

Your restaurant menu system should now be fully functional!