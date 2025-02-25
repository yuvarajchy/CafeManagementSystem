import sqlite3

def create_database():
    conn = sqlite3.connect("cafe_management.db")
    cursor = conn.cursor()

    # Drop tables if they exist (optional, for development/testing purposes)
    cursor.execute("DROP TABLE IF EXISTS users")
    cursor.execute("DROP TABLE IF EXISTS menu")
    cursor.execute("DROP TABLE IF EXISTS orders")
    cursor.execute("DROP TABLE IF EXISTS employees")
    cursor.execute("DROP TABLE IF EXISTS feedback")

    # Create users table
    cursor.execute('''
    CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fullname TEXT NOT NULL,
        age INTEGER NOT NULL,
        gender TEXT NOT NULL,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        position TEXT NOT NULL,
        salary REAL NOT NULL,
                   
        role TEXT NOT NULL CHECK (role IN ('admin', 'employee'))
    )
    ''')

    # Insert default admin user
    cursor.execute("INSERT INTO users (fullname, age, gender, username, password, position, salary, role) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                   ("Admin User", 30, "Other", "admin", "admin12", "admin", 50000, "admin"))

    # Create menu table
    cursor.execute('''
    CREATE TABLE menu (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT,
        discount REAL,
        price REAL NOT NULL
    )
    ''')

    # Insert sample menu items
    cursor.executemany("INSERT INTO menu (name, description, discount, price) VALUES (?, ?, ?, ?)", [
        ("Espresso", "Strong black coffee", 2.50, 2.50),
        ("Cappuccino", "Espresso with steamed milk and foam", 3.50, 3.50),
        ("Latte", "Espresso with steamed milk", 3.00, 3.00),
        ("Mocha", "Chocolate-flavored coffee drink", 3.75, 3.75)
    ])

    # Create orders table (updated with employee_id and table_number)
    cursor.execute('''
    CREATE TABLE orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_name TEXT NOT NULL,
        user_id INTEGER NOT NULL,  -- References employee who took the order
        table_number INTEGER NOT NULL,  -- Table number where the order was placed
        item_id INTEGER NOT NULL,       -- Reference to menu item
        quantity INTEGER NOT NULL,      -- Quantity of the item ordered
        order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        total_price REAL NOT NULL,      -- Total price of the order
        FOREIGN KEY (user_id) REFERENCES users (id),
        FOREIGN KEY (item_id) REFERENCES menu (id)
    )
    ''')

    # Create employees table
    cursor.execute('''
    CREATE TABLE employees (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fullname TEXT NOT NULL,
        age INTEGER NOT NULL,
        gender TEXT NOT NULL,
        position TEXT NOT NULL,
        password TEXT NOT NULL,
        salary REAL NOT NULL
    )
    ''')

    # Insert sample employees
    cursor.executemany("INSERT INTO employees (fullname, age, gender, position, password, salary) VALUES (?, ?, ?, ?, ?, ?)", [
        ("John Doe", 28, "Male", "Barista", "barista123", 2500),
        ("Jane Smith", 25, "Female", "Cashier", "cashier123", 2200)
    ])

    # Create feedback table
    cursor.execute('''
    CREATE TABLE feedback (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_name TEXT NOT NULL,
        feedback_text TEXT NOT NULL,
        feedback_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    conn.commit()
    conn.close()
    print("Database tables created and sample data inserted successfully.")

# Call the function to create the database and tables
if __name__ == "__main__":
    create_database()