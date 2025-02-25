from tkinter import *
from tkinter import messagebox
import sqlite3

def fetch_menu():
    listbox.delete(0, END)
    conn = sqlite3.connect("cafe.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM menu")
    items = cursor.fetchall()
    conn.close()
    for item in items:
        listbox.insert(END, f"{item[0]} - {item[1]} : ${item[2]}")

def add_item():
    name = entry_name.get()
    price = entry_price.get()
    
    if name and price:
        conn = sqlite3.connect("cafe.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO menu (name, price) VALUES (?, ?)", (name, float(price)))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Item added!")
        fetch_menu()
    else:
        messagebox.showerror("Error", "All fields are required")

def delete_item():
    try:
        selected = listbox.get(listbox.curselection())
        item_id = selected.split(" - ")[0]
        conn = sqlite3.connect("cafe.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM menu WHERE id=?", (item_id,))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Item deleted!")
        fetch_menu()
    except:
        messagebox.showerror("Error", "Select an item to delete")

root = Tk()
root.title("Admin Panel")
root.geometry("400x400")

Label(root, text="Item Name").pack()
entry_name = Entry(root)
entry_name.pack()

Label(root, text="Price").pack()
entry_price = Entry(root)
entry_price.pack()

Button(root, text="Add Item", command=add_item).pack()
Button(root, text="Delete Item", command=delete_item).pack()

listbox = Listbox(root)
listbox.pack(fill=BOTH, expand=True)

fetch_menu()

root.mainloop()
