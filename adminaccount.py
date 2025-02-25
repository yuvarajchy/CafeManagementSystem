import sqlite3
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import os
import sys
import subprocess

# Function to clear the content frame
def clear_content():
    for widget in content_frame.winfo_children():
        widget.destroy()

# Function to manage coffee (CRUD operations)
import tkinter.messagebox as MessageBox

def manage_coffee():
    clear_content()  # Clear the content frame

    def load_coffee():
        conn = sqlite3.connect("cafe_management.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM menu")
        coffee_items = cursor.fetchall()
        conn.close()
        
        # Clear existing data in the table
        for row in treeview.get_children():
            treeview.delete(row)
        
        # Insert the coffee data into the table
        for coffee in coffee_items:
            treeview.insert("", "end", values=(coffee[0], coffee[1], coffee[2], coffee[3], coffee[4]))

    def add_coffee():
        coffee_name = coffee_name_entry.get()
        description = description_entry.get()
        discount = discount_entry.get()
        price = price_entry.get()

        if not coffee_name or not description or not discount or not price:
            MessageBox.showwarning("Input Error", "All fields are required!")
            return

        conn = sqlite3.connect("cafe_management.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO menu (name, description, discount, price) VALUES (?, ?, ?, ?)", 
                       (coffee_name, description, discount, price))
        conn.commit()
        conn.close()

        coffee_name_entry.delete(0, END)
        description_entry.delete(0, END)
        discount_entry.delete(0, END)
        price_entry.delete(0, END)
        load_coffee()

    def delete_coffee():
        selected_item = treeview.selection()
        if selected_item:
            coffee_id = treeview.item(selected_item, "values")[0]
            conn = sqlite3.connect("cafe_management.db")
            cursor = conn.cursor()
            cursor.execute("DELETE FROM menu WHERE id=?", (coffee_id,))
            conn.commit()
            conn.close()
            load_coffee()

    def update_coffee():
        selected_item = treeview.selection()
        if selected_item:
            coffee_id = treeview.item(selected_item, "values")[0]
            coffee_name = coffee_name_entry.get()
            description = description_entry.get()
            discount = discount_entry.get()
            price = price_entry.get()

            if not coffee_name or not description or not discount or not price:
                MessageBox.showwarning("Input Error", "All fields are required!")
                return

            conn = sqlite3.connect("cafe_management.db")
            cursor = conn.cursor()
            cursor.execute("UPDATE menu SET name=?, description=?, discount=?, price=? WHERE id=?", 
                           (coffee_name, description, discount, price, coffee_id))
            conn.commit()
            conn.close()

            coffee_name_entry.delete(0, END)
            description_entry.delete(0, END)
            discount_entry.delete(0, END)
            price_entry.delete(0, END)
            load_coffee()

    def clear_form():
        coffee_name_entry.delete(0, END)
        description_entry.delete(0, END)
        discount_entry.delete(0, END)
        price_entry.delete(0, END)

    # Add content to the content_frame
    Label(content_frame, text="Coffee Name:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
    coffee_name_entry = Entry(content_frame)
    coffee_name_entry.grid(row=0, column=1, padx=10, pady=5)

    Label(content_frame, text="Coffee Description:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
    description_entry = Entry(content_frame)
    description_entry.grid(row=1, column=1, padx=10, pady=5)

    Label(content_frame, text="Discount (%):").grid(row=2, column=0, padx=10, pady=5, sticky="w")
    discount_entry = Entry(content_frame)
    discount_entry.grid(row=2, column=1, padx=10, pady=5)

    Label(content_frame, text="Price:").grid(row=3, column=0, padx=10, pady=5, sticky="w")
    price_entry = Entry(content_frame)
    price_entry.grid(row=3, column=1, padx=10, pady=5)

    # Buttons in the same row as requested:
    Button(content_frame, text="Add Coffee", command=add_coffee).grid(row=4, column=0, padx=10, pady=10)
    Button(content_frame, text="Update Coffee", command=update_coffee).grid(row=4, column=1, padx=10, pady=10)

    # Buttons in the row below:
    Button(content_frame, text="Clear Coffee", command=clear_form).grid(row=5, column=0, padx=10, pady=10)
    Button(content_frame, text="Delete Coffee", command=delete_coffee).grid(row=5, column=1, padx=10, pady=10)

    # Treeview for coffee data (table format)
    columns = ("ID", "Coffee Name", "Description", "Discount (%)", "Price")
    treeview = ttk.Treeview(content_frame, columns=columns, show="headings", height=10)
    treeview.grid(row=0, column=2, rowspan=6, padx=10, pady=10)

    # Define column headings
    treeview.heading("ID", text="ID")
    treeview.heading("Coffee Name", text="Coffee Name")
    treeview.heading("Description", text="Description")
    treeview.heading("Discount (%)", text="Discount (%)")
    treeview.heading("Price", text="Price")
    
    # Set column widths
    treeview.column("ID", width=50)
    treeview.column("Coffee Name", width=200)
    treeview.column("Description", width=200)
    treeview.column("Discount (%)", width=100)
    treeview.column("Price", width=100)

    # Select item in the table
    def on_select(event):
        selected_item = treeview.selection()
        if selected_item:
            coffee_data = treeview.item(selected_item, "values")
            coffee_name_entry.delete(0, END)
            coffee_name_entry.insert(0, coffee_data[1])
            description_entry.delete(0, END)
            description_entry.insert(0, coffee_data[2])
            discount_entry.delete(0, END)
            discount_entry.insert(0, coffee_data[3])
            price_entry.delete(0, END)
            price_entry.insert(0, coffee_data[4])  # Make sure this matches the expected column

    treeview.bind("<ButtonRelease-1>", on_select)

    load_coffee()  # Load the coffee items initially

# Function to manage employees (CRUD operations)
def manage_employees():
    clear_content()  # Clear the content frame

    # Form fields for employee management
    Label(content_frame, text="Full Name:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
    fullname_entry = Entry(content_frame)
    fullname_entry.grid(row=0, column=1, padx=10, pady=5)

    Label(content_frame, text="Age:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
    age_entry = Entry(content_frame)
    age_entry.grid(row=1, column=1, padx=10, pady=5)

    Label(content_frame, text="Gender:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
    gender_entry = Entry(content_frame)
    gender_entry.grid(row=2, column=1, padx=10, pady=5)

    Label(content_frame, text="Username:").grid(row=3, column=0, padx=10, pady=5, sticky="w")
    username_entry = Entry(content_frame)
    username_entry.grid(row=3, column=1, padx=10, pady=5)

    Label(content_frame, text="Position:").grid(row=4, column=0, padx=10, pady=5, sticky="w")
    position_entry = Entry(content_frame)
    position_entry.grid(row=4, column=1, padx=10, pady=5)

    Label(content_frame, text="Salary:").grid(row=5, column=0, padx=10, pady=5, sticky="w")
    salary_entry = Entry(content_frame)
    salary_entry.grid(row=5, column=1, padx=10, pady=5)

    Label(content_frame, text="Password:").grid(row=6, column=0, padx=10, pady=5, sticky="w")
    password_entry = Entry(content_frame, show="*")  # Hide password input
    password_entry.grid(row=6, column=1, padx=10, pady=5)

    # Default role to 'employee'
    role = 'employee'

    # Buttons for CRUD operations
    Button(content_frame, text="Add Employee", command=lambda: add_employee()).grid(row=7, column=0, padx=10, pady=10)
    Button(content_frame, text="Update Employee", command=lambda: update_employee()).grid(row=7, column=1, padx=10, pady=10)
    Button(content_frame, text="Clear Form", command=lambda: clear_form()).grid(row=8, column=0, padx=10, pady=10)
    Button(content_frame, text="Delete Employee", command=lambda: delete_employee()).grid(row=8, column=1, padx=10, pady=10)

    # Treeview to display employee records
    columns = ("ID", "Full Name", "Username", "Age", "Gender", "Position", "Salary", "Role")
    treeview = ttk.Treeview(content_frame, columns=columns, show="headings", height=10)
    treeview.grid(row=0, column=2, rowspan=9, padx=10, pady=10)

    # Define column headings
    treeview.heading("ID", text="ID")
    treeview.heading("Full Name", text="Full Name")
    treeview.heading("Username", text="Username")
    treeview.heading("Age", text="Age")
    treeview.heading("Gender", text="Gender")
    treeview.heading("Position", text="Position")
    treeview.heading("Salary", text="Salary")
    treeview.heading("Role", text="Role")

    # Set column widths
    treeview.column("ID", width=50)
    treeview.column("Full Name", width=150)
    treeview.column("Username", width=120)
    treeview.column("Age", width=80)
    treeview.column("Gender", width=80)
    treeview.column("Position", width=100)
    treeview.column("Salary", width=100)
    treeview.column("Role", width=100)

    # Select item in the table
    def on_select(event):
        selected_item = treeview.selection()
        if selected_item:
            employee_data = treeview.item(selected_item, "values")
            fullname_entry.delete(0, END)
            fullname_entry.insert(0, employee_data[1])
            username_entry.delete(0, END)
            username_entry.insert(0, employee_data[2])
            age_entry.delete(0, END)
            age_entry.insert(0, employee_data[3])
            gender_entry.delete(0, END)
            gender_entry.insert(0, employee_data[4])
            position_entry.delete(0, END)
            position_entry.insert(0, employee_data[5])
            salary_entry.delete(0, END)
            salary_entry.insert(0, employee_data[6])

    treeview.bind("<ButtonRelease-1>", on_select)

    # Load employee data from the database
    def load_employees():
        conn = sqlite3.connect("cafe_management.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE role='employee'")  # Load only employees
        employees = cursor.fetchall()
        conn.close()

        # Clear existing data in the table
        for row in treeview.get_children():
            treeview.delete(row)

        # Insert employee data into the table
        for employee in employees:
            treeview.insert("", "end", values=(employee[0], employee[1], employee[4], employee[2], employee[3], employee[5], employee[6], employee[7]))

    # Add an employee to the database
    def add_employee():
        fullname = fullname_entry.get()
        username = username_entry.get()
        age = age_entry.get()
        gender = gender_entry.get()
        position = position_entry.get()
        salary = salary_entry.get()
        password = password_entry.get()

        conn = sqlite3.connect("cafe_management.db")
        cursor = conn.cursor()

        # Insert employee with default role 'employee'
        cursor.execute("INSERT INTO users (fullname, age, gender, username, password, position, salary, role) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                       (fullname, age, gender, username, password, position, salary, role))
        conn.commit()
        conn.close()

        # Clear form fields after adding
        fullname_entry.delete(0, END)
        username_entry.delete(0, END)
        age_entry.delete(0, END)
        gender_entry.delete(0, END)
        position_entry.delete(0, END)
        salary_entry.delete(0, END)
        password_entry.delete(0, END)

        load_employees()

    # Delete selected employee from the database
    def delete_employee():
        selected_item = treeview.selection()
        if selected_item:
            employee_id = treeview.item(selected_item, "values")[0]
            conn = sqlite3.connect("cafe_management.db")
            cursor = conn.cursor()
            cursor.execute("DELETE FROM users WHERE id=?", (employee_id,))
            conn.commit()
            conn.close()
            load_employees()

    # Update selected employee details in the database
    def update_employee():
        selected_item = treeview.selection()
        if selected_item:
            employee_id = treeview.item(selected_item, "values")[0]
            fullname = fullname_entry.get()
            username = username_entry.get()
            age = age_entry.get()
            gender = gender_entry.get()
            position = position_entry.get()
            salary = salary_entry.get()
            password = password_entry.get()

            conn = sqlite3.connect("cafe_management.db")
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET fullname=?, age=?, gender=?, username=?, password=?, position=?, salary=? WHERE id=?",
                           (fullname, age, gender, username, password, position, salary, employee_id))
            conn.commit()
            conn.close()

            # Clear form fields after updating
            fullname_entry.delete(0, END)
            username_entry.delete(0, END)
            age_entry.delete(0, END)
            gender_entry.delete(0, END)
            position_entry.delete(0, END)
            salary_entry.delete(0, END)
            password_entry.delete(0, END)

            load_employees()

    # Clear form fields
    def clear_form():
        fullname_entry.delete(0, END)
        username_entry.delete(0, END)
        age_entry.delete(0, END)
        gender_entry.delete(0, END)
        position_entry.delete(0, END)
        salary_entry.delete(0, END)
        password_entry.delete(0, END)

    load_employees()  # Load the employees initially

def manage_orders():
    clear_content()  # Clear the content frame

    # Function to load order data into the Treeview
    def load_orders():
        conn = sqlite3.connect("cafe_management.db")
        cursor = conn.cursor()
        cursor.execute('''
        SELECT o.id, o.customer_name, m.name AS item_name, o.quantity, o.total_price, o.order_date, e.fullname AS employee_name, o.table_number
        FROM orders o
        JOIN menu m ON o.item_id = m.id
        JOIN users e ON o.user_id = e.id
        ''')
        orders = cursor.fetchall()
        conn.close()

        # Clear existing data in the table
        for row in treeview.get_children():
            treeview.delete(row)

        # Insert the orders data into the table
        for order in orders:
            treeview.insert("", "end", values=order)

    # Treeview for order data (table format)
    columns = ("Order ID", "Customer Name", "Item Name", "Quantity", "Total Price", "Order Date", "Employee Name", "Table Number")
    treeview = ttk.Treeview(content_frame, columns=columns, show="headings", height=10)
    treeview.grid(row=0, column=0, padx=10, pady=10)

    # Define column headings
    treeview.heading("Order ID", text="Order ID")
    treeview.heading("Customer Name", text="Customer Name")
    treeview.heading("Item Name", text="Item Name")
    treeview.heading("Quantity", text="Quantity")
    treeview.heading("Total Price", text="Total Price")
    treeview.heading("Order Date", text="Order Date")
    treeview.heading("Employee Name", text="Employee Name")
    treeview.heading("Table Number", text="Table Number")

    # Set column widths
    treeview.column("Order ID", width=100)
    treeview.column("Customer Name", width=150)
    treeview.column("Item Name", width=150)
    treeview.column("Quantity", width=80)
    treeview.column("Total Price", width=100)
    treeview.column("Order Date", width=150)
    treeview.column("Employee Name", width=150)
    treeview.column("Table Number", width=100)

    load_orders()  # Load the orders initially

# Function to log out and redirect to login.py
def logout():
    root.destroy()
    subprocess.run(["python", "login.py"])

# Root window setup
root = Tk()
root.title("Cafe Management System")
# root.geometry("800x600")
# Make window open in full screen and allow resizing
root.state("zoomed")  # Full screen
root.resizable(True, True)  # Allow resizing

# Navbar frame (Fixed at the top)
navbar = Frame(root, bg="#fefefe", height=50)
navbar.place(relx=0, rely=0, relwidth=1, relheight=0.08)  # Adjust height as needed

# Load coffee shop logo
logo_image = Image.open("images/CoffeeShop-brand-logo.png")
logo_image = logo_image.resize((40, 40), Image.LANCZOS)  # Resize logo to fit
logo_photo = ImageTk.PhotoImage(logo_image)

# Add logo image first
logo_label = Label(navbar, image=logo_photo, bg="#fefefe")
logo_label.image = logo_photo  # Keep a reference to avoid garbage collection
logo_label.pack(side="left", padx=5, pady=10)

# Cafe Management System Label (Now second)
title_label = Label(navbar, text="Cafe Management System", font=("Arial", 16, "bold"), bg='#ffffff', fg='#fab706')
title_label.pack(side="left", padx=20, pady=10)

# Welcome Admin label
welcome_label = Label(navbar, text="Welcome Admin", font=("Arial", 12, "bold"), bg='#ffffff', fg='black')
welcome_label.pack(side="right", padx=20, pady=10)

# Logout button
logout_button = Button(navbar, text="Logout", command=logout, bg="#dc3545", fg="white")
logout_button.pack(side="right", padx=10, pady=10)

# Sidebar setup (Fixed on the left side)
sidebar = Frame(root, width=300, bg="#2e3d4f", height=600)
sidebar.place(relx=0, rely=0.08, relheight=0.92)  # Sidebar below the navbar, adjusts height dynamically

# Content frame (Right side for content)
# content_frame = Frame(root, bg="#f4f4f9", width=600, height=600)
# content_frame.place(relx=0.25, rely=0.08, relheight=0.92, relwidth=0.75)  # Adjust width and height as needed
# Content frame (Right side for content)
content_frame = Frame(root, bg="#f4f4f9", width=850, height=850)
content_frame.place(relx=0.12, rely=0.09, relheight=0.9, relwidth=0.85)  # Adjust width and height as needed


# Sidebar buttons
Button(sidebar, text="Manage", command=manage_coffee, width=20, bg="#3c8dbc", fg="white").pack(pady=10)
Button(sidebar, text="Manage Employees", command=manage_employees, width=20, bg="#3c8dbc", fg="white").pack(pady=10)
Button(sidebar, text="View Orders", command=manage_orders, width=20, bg="#3c8dbc", fg="white").pack(pady=10)

root.mainloop()