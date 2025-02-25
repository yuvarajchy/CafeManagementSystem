from tkinter import *
from tkinter import messagebox
import sqlite3
from PIL import Image, ImageTk  # Import PIL for image handling

def login():
    username = entry_username.get().strip()  # Remove leading/trailing spaces
    password = entry_password.get().strip()

    # Hardcoded Admin Login
    if username == "admin" and password == "admin12":
        messagebox.showinfo("Success", "Welcome, Admin!")
        root.destroy()
        import adminaccount  # Open the admin panel
        return

    # Check Database for User Credentials
    conn = sqlite3.connect("cafe_management.db")
    cursor = conn.cursor()

    # Debugging: Check if inputs are being captured correctly
    print(f"Debug Input -> Username: {username}, Password: {password}")

    # Case-insensitive username comparison
    cursor.execute("""
        SELECT role FROM users WHERE LOWER(username) = LOWER(?) AND password = ?
    """, (username, password))

    user = cursor.fetchone()
    conn.close()

    # Debugging: Check the query result
    print(f"Debug Result -> User: {user}")

    # Redirect Based on User Role
    if user:
        role = user[0]
        if role == 'admin':
            messagebox.showinfo("Success", "Welcome, Admin!")
            root.destroy()
            import adminaccount  # Open the admin panel
        elif role == 'employee':
            messagebox.showinfo("Success", f"Welcome, {username}!")
            root.destroy()
            import employee  # Open the employee panel
    else:
        messagebox.showerror("Error", "Invalid username or password")

def show_password():
    if entry_password.cget('show') == '*':
        entry_password.config(show='')
    else:
        entry_password.config(show='*')

def open_signup():
    root.destroy()
    import signup  # Assuming you have a signup.py file

root = Tk()
root.title("Login")

# Make window open in full screen and allow resizing
root.state("zoomed")  # Full screen
root.resizable(True, True)  # Allow resizing

# Split screen into two parts (left for image and text, right for form)
frame_left = Frame(root, width=1050, height=600, bg="#f5f5f5")
frame_left.pack(side=LEFT, fill=Y)

frame_right = Frame(root, width=500, height=500, bg="white")
frame_right.pack(side=RIGHT, fill=Y)

# Left frame content (Image and overlay text)
image = Image.open("images/home_bg.jpg")  # Adjust the image path as needed
# image = image.resize((1600, 870), Image.LANCZOS)
image_tk = ImageTk.PhotoImage(image)

label_image = Label(frame_left, image=image_tk, bg="#f5f5f5")
label_image.image = image_tk  # Keep a reference to avoid garbage collection
label_image.place(relwidth=1, relheight=1)  # Ensure the image fills the frame

# Heading and description overlayed on the image
heading_label = Label(frame_left, text="Cafe Management System", font=("Arial", 18, "bold"), fg="#fab706", bg="#f5f5f5")
heading_label.place(relx=0.5, rely=0.3, anchor="center")

description_label = Label(frame_left, text="Welcome to our cafe! Enjoy the finest coffee and a cozy atmosphere.", font=("Arial", 12), fg="black", bg="#f5f5f5")
description_label.place(relx=0.5, rely=0.4, anchor="center")

# Right frame content (login form centered)
frame_right_content = Frame(frame_right, bg="white")
frame_right_content.place(relx=0.5, rely=0.5, anchor="center")

# Username Label and Input
Label(frame_right_content, text="Username", font=("Arial", 12)).grid(row=0, column=0, pady=10, padx=20, sticky="w")
entry_username = Entry(frame_right_content, font=("Arial", 12))
entry_username.grid(row=1, column=0, pady=10, padx=20)

# Password Label and Input
Label(frame_right_content, text="Password", font=("Arial", 12)).grid(row=2, column=0, pady=10, padx=20, sticky="w")
entry_password = Entry(frame_right_content, font=("Arial", 12), show="*")
entry_password.grid(row=3, column=0, pady=10, padx=20)

# Show Password Checkbox and Label
show_password_var = BooleanVar()
show_password_checkbox = Checkbutton(frame_right_content, text="Show Password", variable=show_password_var, command=show_password)
show_password_checkbox.grid(row=4, column=0, pady=5, padx=20, sticky="w")

# Login Button
login_button = Button(frame_right_content, text="Login", font=("Arial", 12), bg="#ff6600", fg="white", command=login)
login_button.grid(row=5, column=0, pady=10, padx=20)

# Don't have an account? Sign up (Clickable label like a link) no

# signup_label = Label(frame_right_content, text="Don't have an account? Sign up", font=("Arial", 10), fg="blue", cursor="hand2")
# signup_label.grid(row=6, column=0, pady=5, padx=20)

# Bind the click event to the signup function no
# signup_label.bind("<Button-1>", lambda event: open_signup())

root.mainloop()