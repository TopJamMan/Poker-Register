import os
import tkinter as tk
from registration_form import open_registration_form
from admin_functions import AdminFunctions
from database import Database
from table_ui import TableManagement  # Assuming table_ui.py has a

class HomePage:
    def __init__(self, master):
        self.master = master
        self.master.title("Home Page")
        self.master.geometry("400x300")

        # Welcome label
        self.welcome_label = tk.Label(master, text="Welcome to the Game Environment", font=("Arial", 14))
        self.welcome_label.pack(pady=20)

        # Button to open registration form
        self.registration_button = tk.Button(master, text="Register", command=self.open_registration_form)
        self.registration_button.pack(pady=10)

        # Button to open admin functions
        self.admin_button = tk.Button(master, text="Admin Functions", command=self.open_admin_functions)
        self.admin_button.pack(pady=10)

        # Button to open table management
        self.table_button = tk.Button(master, text="Table Management", command=self.open_table_management)
        self.table_button.pack(pady=10)

    def open_registration_form(self):
        open_registration_form(connection)

    def open_admin_functions(self):
        admin_window = tk.Toplevel(self.master)
        AdminFunctions(admin_window)

    def open_table_management(self):
        table_window = tk.Toplevel(self.master)
        TableManagement(table_window)

if __name__ == "__main__":
    root = tk.Tk()
    # Create a database connection
    db = Database()
    connection = db.get_connection()  # Get the active connection
    home_app = HomePage(root)

    # Start the main loop
    root.mainloop()

    # Close the connection when the app is closed
    db.close_connection()
