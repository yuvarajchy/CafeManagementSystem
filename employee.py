from tkinter import *
import sqlite3
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk
import subprocess

# Logout function
def logout():
    root.destroy()
    subprocess.run(["python", "login.py"])

# Initialize Tkinter window
root = Tk()
root.title("Employee Panel")
root.state("zoomed")  # Open in full screen
root.resizable(True, True)  # Allow resizing

# Fetch logged-in employee's name from the database or login
employee_name = "Subharaj"  # Example, replace with dynamic login data

# Navbar frame (Visible)
navbar = Frame(root, bg="#fefefe", height=50)
navbar.place(relx=0, rely=0, relwidth=1)  # Place navbar at top with full width

# Load coffee shop logo
logo_image = Image.open("images/CoffeeShop-brand-logo.png")
logo_image = logo_image.resize((40, 40), Image.LANCZOS)  # Resize logo to fit
logo_photo = ImageTk.PhotoImage(logo_image)

# Add logo image first
logo_label = Label(navbar, image=logo_photo, bg="#fefefe")
logo_label.image = logo_photo  # Keep a reference to avoid garbage collection
logo_label.pack(side="left", padx=5, pady=10)

# Cafe Management System Label
title_label = Label(navbar, text="Cafe Management System", font=("Arial", 16, "bold"), bg='#ffffff', fg='#fab706')
title_label.pack(side="left", padx=20, pady=10)

# Dynamic employee name label (e.g., "Welcome Subharaj")
welcome_label = Label(navbar, text=f"Welcome {employee_name}", font=("Arial", 12), bg="#fefefe", fg="#555555")
welcome_label.pack(side="left", padx=20, pady=10)

# Login Button (Right side)
login_button = Button(navbar, text="LogOut", font=("Arial", 12), bg="#ff6600", fg="white", command=logout)
login_button.pack(side="right", padx=20, pady=10)

# Load background image
bg_image = Image.open("images/home_bg.jpg")
bg_image = bg_image.resize((1366, 768), Image.LANCZOS)  # Resize to fit screen
bg_photo = ImageTk.PhotoImage(bg_image)

# Create Canvas for background
canvas = Canvas(root, width=1366, height=768)
canvas.place(x=0, y=0, relwidth=1, relheight=1)  # Place it at (0,0) and expand
canvas.create_image(0, 0, image=bg_photo, anchor="nw")

# Orders Button to open order window
def open_orders_window():
    # Remove any previous frames from the window
    for widget in root.winfo_children():
        if widget != navbar:
            widget.destroy()

    # Create the frame to hold order form and menu
    order_window = Frame(root, bg="#f4f4f9")
    order_window.place(relx=0, rely=0.08, relheight=0.92, relwidth=1)

    # Left Frame for Order Form
    left_frame = Frame(order_window, bg="white", width=600)
    left_frame.pack(side="left", padx=10, pady=10, fill="both", expand=True)

    # Customer Name Text Field
    Label(left_frame, text="Customer Name", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=5)
    customer_name_entry = Entry(left_frame, font=("Arial", 12))
    customer_name_entry.grid(row=0, column=1, padx=10, pady=5)

    # Table Number Dropdown (up to 5 tables)
    Label(left_frame, text="Table Number", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=5)
    table_number_entry = ttk.Combobox(left_frame, font=("Arial", 12))
    table_number_entry['values'] = (1, 2, 3, 4, 5)  # Table numbers 1 to 5
    table_number_entry.grid(row=1, column=1, padx=10, pady=5)

    # Quantity Entry
    Label(left_frame, text="Quantity", font=("Arial", 12)).grid(row=2, column=0, padx=10, pady=5)
    quantity_entry = Entry(left_frame, font=("Arial", 12))
    quantity_entry.grid(row=2, column=1, padx=10, pady=5)

    # Total Price Label (calculated based on quantity and menu item)
    Label(left_frame, text="Total Price", font=("Arial", 12)).grid(row=3, column=0, padx=10, pady=5)
    total_price_label = Label(left_frame, text="0", font=("Arial", 12))
    total_price_label.grid(row=3, column=1, padx=10, pady=5)

    # Menu Item Dropdown
    Label(left_frame, text="Menu Item", font=("Arial", 12)).grid(row=4, column=0, padx=10, pady=5)
    menu_item_entry = ttk.Combobox(left_frame, font=("Arial", 12))
    
    # Connect to the database and fetch menu items
    def load_menu_items():
        conn = sqlite3.connect("cafe_management.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, price FROM menu")  # Fetch menu items (ID, Name, Price)
        items = cursor.fetchall()
        conn.close()
        return items

    menu_items = load_menu_items()
    menu_item_names = [item[1] for item in menu_items]
    menu_item_prices = {item[1]: item[2] for item in menu_items}  # {item_name: price}

    menu_item_entry['values'] = menu_item_names  # Populate with menu items
    menu_item_entry.grid(row=4, column=1, padx=10, pady=5)

    # Function to update total price based on selected item and quantity
    def update_total_price():
        selected_item = menu_item_entry.get()
        if selected_item:
            try:
                quantity = int(quantity_entry.get())
                price = menu_item_prices[selected_item]
                total_price = price * quantity
                total_price_label.config(text=f"{total_price:.2f}")
            except ValueError:
                total_price_label.config(text="Invalid Quantity")

    # Bind event to update total price when menu item or quantity is changed
    menu_item_entry.bind("<<ComboboxSelected>>", lambda e: update_total_price())
    quantity_entry.bind("<KeyRelease>", lambda e: update_total_price())

    # CRUD Operations

    # Add Order
    def create_order():
        customer_name = customer_name_entry.get()
        table_number = table_number_entry.get()
        quantity = quantity_entry.get()

        if not customer_name or not table_number or not quantity:
            messagebox.showerror("Input Error", "Please fill all fields.")
            return

        selected_item = menu_item_entry.get()
        if selected_item:
            item_id = menu_item_names.index(selected_item) + 1  # Get the item ID based on its index
            try:
                quantity = int(quantity)
                total_price = float(total_price_label.cget("text"))
                user_id = 1  # Example employee ID, replace with dynamic employee login

                conn = sqlite3.connect("cafe_management.db")
                cursor = conn.cursor()
                cursor.execute(''' 
                    INSERT INTO orders (customer_name, user_id, table_number, item_id, quantity, total_price)
                    VALUES (?, ?, ?, ?, ?, ?) 
                ''', (customer_name, user_id, table_number, item_id, quantity, total_price))
                conn.commit()
                conn.close()

                messagebox.showinfo("Order Placed", "The order has been successfully placed!")
                clear_form()  # Clear the form after placing the order
                load_employee_orders()  # Reload the orders table to show updated orders
            except ValueError:
                messagebox.showerror("Input Error", "Invalid input for quantity or price.")
        else:
            messagebox.showerror("Selection Error", "Please select a menu item.")

    # Update Order
    def update_order():
        selected_item = orders_treeview.selection()
        if selected_item:
            order_data = orders_treeview.item(selected_item, "values")
            order_id = order_data[0]
            customer_name = customer_name_entry.get()
            table_number = table_number_entry.get()
            quantity = quantity_entry.get()

            if not customer_name or not table_number or not quantity:
                messagebox.showerror("Input Error", "Please fill all fields.")
                return

            selected_item_name = menu_item_entry.get()
            if selected_item_name:
                item_id = menu_item_names.index(selected_item_name) + 1
                total_price = float(total_price_label.cget("text"))
                user_id = 1

                conn = sqlite3.connect("cafe_management.db")
                cursor = conn.cursor()
                cursor.execute(''' 
                    UPDATE orders
                    SET customer_name = ?, table_number = ?, item_id = ?, quantity = ?, total_price = ?
                    WHERE id = ?
                ''', (customer_name, table_number, item_id, quantity, total_price, order_id))
                conn.commit()
                conn.close()

                messagebox.showinfo("Order Updated", "The order has been updated successfully!")
                load_employee_orders()
                clear_form()

    # Delete Order
    def delete_order():
        selected_item = orders_treeview.selection()
        if selected_item:
            order_data = orders_treeview.item(selected_item, "values")
            order_id = order_data[0]

            conn = sqlite3.connect("cafe_management.db")
            cursor = conn.cursor()
            cursor.execute(''' 
                DELETE FROM orders WHERE id = ? 
            ''', (order_id,))
            conn.commit()
            conn.close()
            messagebox.showinfo("Order Deleted", "The order has been deleted.")
            load_employee_orders()

    # Load Orders
    def load_employee_orders():
        for item in orders_treeview.get_children():
            orders_treeview.delete(item)

        conn = sqlite3.connect("cafe_management.db")
        cursor = conn.cursor()
        cursor.execute(''' 
            SELECT orders.id, orders.customer_name, orders.table_number, menu.name, orders.quantity, orders.total_price
            FROM orders
            JOIN menu ON orders.item_id = menu.id
        ''')
        orders = cursor.fetchall()
        conn.close()

        for order in orders:
            orders_treeview.insert("", "end", values=order)

    # Clear form
    def clear_form():
        customer_name_entry.delete(0, END)
        table_number_entry.set("")
        quantity_entry.delete(0, END)
        menu_item_entry.set("")
        total_price_label.config(text="0")

    # Create Treeview for Orders List (display orders)
    orders_frame = Frame(order_window, bg="white", height=400)
    orders_frame.pack(side="right", padx=10, pady=10, fill="both", expand=True)

    columns = ("ID", "Customer Name", "Table", "Item", "Quantity", "Total Price")
    orders_treeview = ttk.Treeview(orders_frame, columns=columns, show="headings")
    for col in columns:
        orders_treeview.heading(col, text=col)
        orders_treeview.column(col, width=150, anchor="center")
    orders_treeview.pack(fill="both", expand=True)

    def on_order_select(event):
        selected_item = orders_treeview.selection()  # Get the selected row
        if selected_item:
            order_data = orders_treeview.item(selected_item, "values")  # Fetch order data
            # Fill the form fields with the selected order's data
            customer_name_entry.delete(0, END)
            customer_name_entry.insert(0, order_data[1])  # Customer Name
            table_number_entry.set(order_data[2])  # Table Number
            quantity_entry.delete(0, END)
            quantity_entry.insert(0, order_data[4])  # Quantity
            menu_item_entry.set(order_data[3])  # Menu Item (Item Name)
        total_price_label.config(text=f"{float(order_data[5]):.2f}")  # Total Price (ensure it's a float)


    orders_treeview.bind("<ButtonRelease-1>", on_order_select)  # Bind the select event

    # Load orders when the page loads
    load_employee_orders()

    # Create Add, Update, Delete buttons
    Button(left_frame, text="Add Order", font=("Arial", 12), bg="#4CAF50", fg="white", command=create_order).grid(row=6, column=0, padx=10, pady=10)
    Button(left_frame, text="Update Order", font=("Arial", 12), bg="#ff9900", fg="white", command=update_order).grid(row=6, column=1, padx=10, pady=10)
    Button(left_frame, text="Delete Order", font=("Arial", 12), bg="#ff3333", fg="white", command=delete_order).grid(row=7, column=0, padx=10, pady=10)

# Open Orders Window when the program starts
open_orders_window()

root.mainloop()