import sqlite3
import tkinter as tk
from tkinter import ttk , messagebox
import live_image_blink
from new_user import ImageCaptureApp
def fetch_all_users():
    conn = sqlite3.connect('your_database.db')
    cursor = conn.cursor()
    x = []
    cursor.execute('SELECT Username FROM Usernames')
    result = cursor.fetchall()
    if result is not None:
        for i in [row[0] for row in result]:
             x.append(i)
    return x

def on_next(username_entry,  window):

    username = username_entry.get()
    if len(username)==0:
        messagebox.showinfo("warning", "enter the user name")
    else:
        if username in fetch_all_users():
            window.destroy()
            live_image_blink.main(username)
        else:
            messagebox.showinfo("warning", "Username not found")


def create_username_entry_window():
        root = tk.Tk()
        root.title("Username Entry")
        root.geometry('300x150')
        username_var = tk.StringVar()
        username_label = ttk.Label(root, text="Enter Username:")
        username_label.pack(pady=10)

        username_entry = ttk.Entry(root, width=30, textvariable=username_var)
        username_entry.pack(pady=10)

        quick_button = ttk.Button(root, text="Back", command=lambda: on_back(root))
        quick_button.pack(pady=10, side=tk.LEFT)
        next_button = ttk.Button(root, text="Next", command=lambda: on_next(username_entry, root), state=tk.NORMAL)
        next_button.pack(pady=10, side=tk.RIGHT)

        # Add a trace to call validate_username whenever the username entry changes
        root.mainloop()
def on_back(root):
     root.destroy()
     main_page()
     
def main_page():
        root = tk.Tk()
        root.title("Face Authentication App")
        root.geometry("400x300")
        root.resizable(False, False)

        # Connect to SQLite database

        style = ttk.Style()
        style.theme_use("clam")  # Use the clam theme for a modern appearance
        style.configure('TButton', font=('Helvetica', 12), background='#3498db', foreground='white')
        style.configure('TLabel', font=('Helvetica', 12), background='#ecf0f1')
        style.configure('TEntry', font=('Helvetica', 12), fieldbackground='#ecf0f1')

        label = ttk.Label(root, text="", font=("Helvetica", 16), background='#ecf0f1')
        label.pack(pady=20)

        btn_login = ttk.Button(root, text="Login", command=lambda: show_login_form(root))

        btn_login.pack(pady=10, ipadx=10)

        btn_signup = ttk.Button(root, text="Signup", command =lambda: show_signup_form(root))
        btn_signup.pack(pady=10, ipadx=10)

        btn_quit = ttk.Button(root, text="Quit", command = root.destroy)
        btn_quit.pack(pady=10, ipadx=10)
        root.mainloop()
def show_login_form(root):
    root.destroy()
    create_username_entry_window()
def show_signup_form(root):
    root.destroy()
    ImageCaptureApp()


# main_page()