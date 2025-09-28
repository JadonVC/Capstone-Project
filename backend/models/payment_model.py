import _mysql_connector
from mysql.connector import connect
from mysql.connector import Error

DB_CONFIG = {
    "host": "127.0.0.1",
    "user": "root",            # change if your teammate uses another user
    "password": "root",# replace with your MySQL password
    "database": "restaurant_ordering"
}

def get_connection():
    return _mysql_connector.connect(**DB_CONFIG)

def create_payment_table():
    connect = get_connection()
    cursor = connect.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS payments (
            id INT PRIMARY KEY AUTO_INCREMENT,
            order_id INT NOT NULL,
            transaction_id VARCHAR(100) NOT NULL,
            status ENUM('success','failed') NOT NULL DEFAULT 'Pending',
            amount DECIMAL(10,2) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    connect.commit()
    cursor.close()
    connect.close()

def insert_payment(order_id, status, amount):

    connect = get_connection
    cursor = connect.cursor()
    try:
        cursor.execute("""
        INSERT INTO payments (order_id, transaction_id, status, amount)
        VALUES (%s, %s, %s, %s)
        """, (order_id, transaction_id, status, amount)) # type: ignore
    except Error as e:
        print("Error inserting payment:", e)
    finally:
        cursor.close()
        connect.close()



def get_all_payments():
    """Fetch all payment records"""
    connect = get_connection()
    cursor = connect.cursor(dictionary=True)
    cursor.execute("SELECT order_id, transaction_id, status, amount, created_at FROM payments")
    rows = cursor.fetchall()
    cursor.close()
    connect.close()
    return rows
 