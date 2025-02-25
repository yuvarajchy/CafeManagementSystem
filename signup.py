from tkinter import *
from tkinter import messagebox
import sqlite3
from PIL import Image, ImageTk

def register():
    fullname = entry_fullname.get()
    age = entry_age.get()
    gender = gender_var.get()
    username = entry_username.get()
    password = entry_password.get()
    confirm_password = entry_confirm_password.get()
    role = "user"  # Default hidden role

    if fullname and age and gender and username and password and confirm_password:
        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match")
            return

        conn = sqlite3.connect("cafe.db")
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (fullname, age, gender, username, password, role) VALUES (?, ?, ?, ?, ?, ?)", 
                           (fullname, age, gender, username, password, role))
            conn.commit()
            messagebox.showinfo("Success", "User Registered!")
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Username already exists")
        finally:
            conn.close()
    else:
        messagebox.showerror("Error", "All fields are required")

def open_login():
    root.destroy()
    import login  # Assuming you have a login.py file

root = Tk()
root.title("Signup")
root.state("zoomed")  # Open in full screen
root.resizable(True, True)  # Allow resizing

# Split screen into two parts (left for image and text, right for form)
frame_left = Frame(root, width=700, height=500)
frame_left.pack(side=LEFT, fill=Y)

frame_right = Frame(root, width=500, height=500)
frame_right.pack(side=RIGHT, fill=Y)

# Left frame content (Image and overlay text)
image = Image.open("images/home_bg.jpg")  # Adjust the image path as needed
image_tk = ImageTk.PhotoImage(image)

label_image = Label(frame_left, image=image_tk, bg="#f5f5f5")
label_image.image = image_tk  # Keep a reference to avoid garbage collection
label_image.place(relwidth=1, relheight=1)  # Ensure the image fills the frame

# Heading and description overlayed on the image
heading_label = Label(frame_left, text="Cafe Management System", font=("Arial", 18, "bold"), fg="#fab706", bg="#f5f5f5")
heading_label.place(relx=0.5, rely=0.3, anchor="center")

description_label = Label(frame_left, text="Welcome to our cafe! Enjoy the finest coffee and a cozy atmosphere.", font=("Arial", 12), fg="black", bg="#f5f5f5")
description_label.place(relx=0.5, rely=0.4, anchor="center")

# Right frame content (signup form centered)
frame_right_content = Frame(frame_right)
frame_right_content.place(relx=0.5, rely=0.5, anchor="center")  # Center the form within the right frame

# Full Name
Label(frame_right_content, text="Full Name", font=("Arial", 12)).pack(pady=5)
entry_fullname = Entry(frame_right_content, font=("Arial", 12))
entry_fullname.pack(pady=5)

# Age
Label(frame_right_content, text="Age", font=("Arial", 12)).pack(pady=5)
entry_age = Entry(frame_right_content, font=("Arial", 12))
entry_age.pack(pady=5)

# Gender
Label(frame_right_content, text="Gender", font=("Arial", 12)).pack(pady=5)
gender_var = StringVar(value="Male")  # Default selection is Male

# Radio buttons for gender
Radiobutton(frame_right_content, text="Male", variable=gender_var, value="Male", font=("Arial", 12)).pack(pady=5)
Radiobutton(frame_right_content, text="Female", variable=gender_var, value="Female", font=("Arial", 12)).pack(pady=5)
Radiobutton(frame_right_content, text="Other", variable=gender_var, value="Other", font=("Arial", 12)).pack(pady=5)

# Username
Label(frame_right_content, text="Username", font=("Arial", 12)).pack(pady=5)
entry_username = Entry(frame_right_content, font=("Arial", 12))
entry_username.pack(pady=5)

# Password
Label(frame_right_content, text="Password", font=("Arial", 12)).pack(pady=5)
entry_password = Entry(frame_right_content, font=("Arial", 12), show="*")
entry_password.pack(pady=5)

# Confirm Password
Label(frame_right_content, text="Confirm Password", font=("Arial", 12)).pack(pady=5)
entry_confirm_password = Entry(frame_right_content, font=("Arial", 12), show="*")
entry_confirm_password.pack(pady=5)

# Register Button
Button(frame_right_content, text="Register", font=("Arial", 12), bg="#ff6600", fg="white", command=register).pack(pady=10)

# Already have an account? Sign In link
signup_label = Label(frame_right_content, text="Already have an account? Sign In", font=("Arial", 10), fg="blue", cursor="hand2")
signup_label.pack(pady=5)

# Bind click event to open login
signup_label.bind("<Button-1>", lambda event: open_login())

root.mainloop()