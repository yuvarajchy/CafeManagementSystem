from tkinter import *
from tkinter import messagebox

def open_admin():
    root.destroy()
    import admin

def open_employee():
    root.destroy()
    import employee

root = Tk()
root.title("Dashboard")
root.geometry("300x200")

Label(root, text="Welcome to Cafe Management System").pack()

Button(root, text="Admin Panel", command=open_admin).pack()
Button(root, text="Employee Panel", command=open_employee).pack()

root.mainloop()
