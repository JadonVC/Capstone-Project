# Database Setup - Restaurant Ordering System

This guide covers setting up the MySQL database using a fast command-line import, then configuring SQLTools for easy database viewing and management within VS Code.

## Prerequisites

- MySQL Server installed on your machine
- MySQL root password

---

## Part 1: Quick Database Import (Fast Setup)

### Step 1: Find Your MySQL Installation Path

The MySQL executable location varies depending on your installation. Run this command in **Command Prompt (CMD)** or **Git Bash**:

```cmd
dir "C:\Program Files\MySQL" /s /b | findstr mysql.exe
```

You should see output like:
```
C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe
```

**Note:** Your version number (8.0, 9.0, etc.) may differ. Use the path that shows `MySQL Server X.X\bin\mysql.exe`.

### Step 2: Import the Database

1. Open **Command Prompt (CMD)** or **Git Bash** in VS Code terminal (**not PowerShell**)
2. Navigate to the project root directory:
   ```cmd
   cd path\to\Capstone-Project-main
   ```

3. Run the import command using YOUR MySQL path from Step 1:
   ```cmd
   "C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe" -u root -p restaurant_ordering < database/restaurant_ordering.sql
   ```
   
   **Important:** Replace the path in quotes with your actual MySQL path from Step 1!

4. Enter your MySQL root password when prompted

That's it! The database, tables, and sample data are now imported.

### Step 3: Verify the Import

Quick verification:

```cmd
"C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe" -u root -p
```

Then in the MySQL prompt:
```sql
SHOW DATABASES;
USE restaurant_ordering;
SHOW TABLES;
EXIT;
```

---

## Part 2: SQLTools Setup (For Easy Database Management)

Now let's set up SQLTools so you can view and work with your database directly in VS Code without switching to MySQL Workbench.

### Step 1: Install Required Extensions

1. Open VS Code Extensions (Ctrl+Shift+X)
2. Search and install:
   - **SQLTools** by Matheus Teixeira
   - **SQLTools MySQL/MariaDB** by Matheus Teixeira

### Step 2: Set up MySQL Connection

1. **Open SQLTools Panel:**
   - Look for the SQLTools icon in the left sidebar (database icon)
   - Click on it to open the SQLTools panel

2. **Add New Connection:**
   - Click the '+' button next to "Connections"
   - Select **MySQL** from the driver list

3. **Fill in Connection Details:**
   ```
   Connection Name: Restaurant Database
   Connect using: Server and Port
   Server Address: localhost
   Port: 3306
   Database: restaurant_ordering
   Username: root
   Password mode: Ask on connect (or Save as plaintext if preferred)
   ```

4. **MySQL Driver Options:**
   - Authentication Protocol: default
   - SSL: Disabled

5. **Click "SAVE CONNECTION"**

### Step 3: Connect and Explore

1. Click the connection to connect (enter password if prompted)
2. You should now see:
   - **restaurant_ordering** database
   - All tables (menu_items, orders, order_items, users, etc.)

### Step 4: Working with SQLTools

**View Table Data:**
- Right-click any table → "Show Table Records"
- Browse your data in a clean interface

**Run SQL Queries:**
- Right-click connection → "New SQL File"
- Write queries and press Ctrl+E to run
- Results appear in a formatted table

**Example queries to try:**
```sql
-- View all menu items
SELECT * FROM menu_items;

-- View orders with customer info
SELECT * FROM orders ORDER BY created_at DESC LIMIT 10;

-- View specific order details
SELECT o.id, o.customer_name, oi.item_name, oi.quantity, oi.subtotal
FROM orders o
JOIN order_items oi ON o.id = oi.order_id
WHERE o.id = 1;
```

## Part 3: Backend Configuration

Update your backend configuration file with your MySQL credentials:

```python
# In your backend config file
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'your_mysql_password',  # Change this
    'database': 'restaurant_ordering',
    'port': 3306
}
```

## Part 4: Install Python Dependencies

```bash
cd backend
pip install flask flask-cors mysql-connector-python
```

## Part 5: Test the Application

1. **Start the Backend:**
   ```bash
   cd backend
   python app.py
   ```

2. **Test the API:**
   - Open browser: http://localhost:5000/api/menu
   - You should see JSON data with menu items

3. **Test the Frontend:**
   - Open `frontend/index.html` with Live Server or in your browser
   - Menu items should display with category filters

---

## Troubleshooting

### PowerShell Issues (Part 1)
If you see an error about `<` operator being reserved:
- **Switch to Command Prompt or Git Bash** using the dropdown next to the `+` in VS Code terminal
- PowerShell doesn't support `<` redirection the same way

### MySQL Not Found (Part 1)
If you get `'mysql' is not recognized`:
- You need to use the **full path** to mysql.exe (follow Step 1)
- OR add MySQL to your system PATH (see Optional Setup below)

### Database Already Exists (Part 1)
If the database already exists and you want to start fresh:
```cmd
"C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe" -u root -p -e "DROP DATABASE IF EXISTS restaurant_ordering;"
```
Then re-run the import command.

### SQLTools Connection Failed (Part 2)
- Make sure MySQL Server is running
- Verify your username and password are correct
- Try port 3306 (default) or check your MySQL configuration
- Ensure you selected the correct database name: `restaurant_ordering`

### Authentication Error
- Verify your MySQL root password is correct
- Try connecting via command line first to confirm credentials work

---

## Optional: Add MySQL to System PATH

To use `mysql` command directly without the full path:

1. Search for **"Environment Variables"** in Windows Start Menu
2. Click **"Environment Variables"** button
3. Under **System variables**, select **Path**, then click **Edit**
4. Click **New** and add: `C:\Program Files\MySQL\MySQL Server 8.0\bin`
5. Click **OK** on all windows
6. **Restart VS Code**

After this, you can simply run:
```cmd
mysql -u root -p restaurant_ordering < database/restaurant_ordering.sql
```
