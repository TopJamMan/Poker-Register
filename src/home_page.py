import tkinter as tk
from tkinter import simpledialog, messagebox
from registration_form import open_registration_form
from admin_functions import AdminFunctions
from database import Database
from src.userinterfaces.table_ui import TableManagement  # Assuming table_ui.py has a TableManagement class
from dotenv import load_dotenv
import os

class AdminCodeDialog(simpledialog.Dialog):
    def body(self, master):
        tk.Label(master, text="Please enter the admin code:").grid(row=0)
        self.entry = tk.Entry(master, show="*")  # Mask input characters
        self.entry.grid(row=1)
        return self.entry  # Focus on this entry

    def apply(self):
        self.result = self.entry.get()  # Store the entered value

class HomePage:
    def __init__(self, master, connection):
        self.master = master
        self.connection = connection  # Store the connection in the class
        self.master.title("Home Page")
        self.master.geometry("400x300")

        # Load environment variables from .env file
        load_dotenv()
        self.admin_code = os.getenv("ADMIN_CODE")  # Get the admin code from the environment

        # Welcome label
        self.welcome_label = tk.Label(master, text="Welcome to the Poker Register", font=("Arial", 14))
        self.welcome_label.pack(pady=20)

        # Button to open registration form
        self.registration_button = tk.Button(master, text="Register", command=self.open_registration_form)
        self.registration_button.pack(pady=10)

        # Button to open admin functions
        self.admin_button = tk.Button(master, text="Admin Functions", command=self.open_admin_code_dialog)
        self.admin_button.pack(pady=10)

        # Button to open table management
        self.table_button = tk.Button(master, text="Tables View", command=self.open_table_management)
        self.table_button.pack(pady=10)

        self.welcome_label = tk.Label(master, text="Licenced for RHUL Poker Society by \n Tom Gyorffy and Jasper Mansfield", font=("Arial", 11))
        self.welcome_label.pack(pady=20)

    def open_registration_form(self):
        open_registration_form(self.connection)

    def open_admin_code_dialog(self):
        dialog = AdminCodeDialog(self.master)  # Create the custom dialog
        if dialog.result:  # Check if a result was entered
            entered_code = dialog.result
            self.check_admin_code(entered_code)

    def check_admin_code(self, entered_code):
        if entered_code == self.admin_code:
            admin_window = tk.Toplevel(self.master)
            AdminFunctions(admin_window, self.connection)  # Pass the connection
        else:
            messagebox.showerror("Access Denied", "Incorrect admin code. Please try again.")

    def open_table_management(self):
        table_window = tk.Toplevel(self.master)
        TableManagement(table_window, self.connection)

if __name__ == "__main__":
    root = tk.Tk()
    # Create a database connection
    db = Database()
    connection = db.get_connection()  # Get the active connection
    home_app = HomePage(root, connection)  # Pass the connection to HomePage

    # Start the main loop
    root.mainloop()

    # Close the connection when the app is closed
    db.close_connection()
