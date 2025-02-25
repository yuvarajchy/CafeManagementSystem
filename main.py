from tkinter import *
from PIL import Image, ImageTk
import os

def open_login():
    root.destroy()
    os.system("python login.py")

# Initialize Tkinter window
root = Tk()
root.title("Cafe Management System")
root.state("zoomed")  # Open in full screen
root.resizable(True, True)  # Allow resizing

# Load background image
bg_image = Image.open("images/home_bg.jpg")
bg_image = bg_image.resize((1366, 768), Image.LANCZOS)  # Resize to fit screen
bg_photo = ImageTk.PhotoImage(bg_image)

# Create Canvas for background
canvas = Canvas(root, width=1366, height=768)
canvas.place(x=0, y=0, relwidth=1, relheight=1)  # Place it at (0,0) and expand
canvas.create_image(0, 0, image=bg_photo, anchor="nw")

# Navbar frame (Now Visible!)
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

# Cafe Management System Label (Now second)
title_label = Label(navbar, text="Cafe Management System", font=("Arial", 16, "bold"), bg='#ffffff', fg='#fab706')
title_label.pack(side="left", padx=20, pady=10)

# Login Button (Right side)
login_button = Button(navbar, text="Login", font=("Arial", 12), bg="#ff6600", fg="white", command=open_login)
login_button.pack(side="right", padx=20, pady=10)

# "Our Latest Trending" heading
heading_label = Label(root, text="Our Latest Trending", font=("Arial", 20, "bold"), fg="#fab706", bg="black")
heading_label.place(relx=0.5, rely=0.2, anchor="center")

# Load Menu Images
menu_items = [
    ("images/menu-1.png", "Black Coffee with milk"),
    ("images/menu-2.png", "Espresso"),
    ("images/menu-3.png", "Cafe' Latte"),
    ("images/menu-4.png", "Piccolo Latte"),
    ("images/menu-5.png", "Mocha"),
    ("images/menu-6.png", "Cappuccino")
]

menu_frame = Frame(root, bg="white")
menu_frame.place(relx=0.5, rely=0.4, anchor="center")

for idx, (image_file, name) in enumerate(menu_items):
    img = Image.open(image_file)
    img = img.resize((100, 100), Image.LANCZOS)
    img_photo = ImageTk.PhotoImage(img)

    # Add shadow effect by placing the image in a frame with relief
    image_frame = Frame(menu_frame, bg="black", bd=5, relief="raised", highlightthickness=3, highlightbackground="grey")
    image_frame.grid(row=0, column=idx, padx=20, pady=10)

    img_label = Label(image_frame, image=img_photo, bg="white")
    img_label.image = img_photo
    img_label.pack()

    name_label = Label(menu_frame, text=name, font=("Arial", 12, "bold"), bg="white")
    name_label.grid(row=1, column=idx, padx=20, pady=5)

root.mainloop()