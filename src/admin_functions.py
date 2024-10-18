import tkinter as tk
from tkinter import messagebox

class AdminFunctions:
    def __init__(self, master):
        self.master = master
        self.master.title("Admin Functions")

        # Create input for table number
        self.label = tk.Label(master, text="Set Table Number:")
        self.label.pack(pady=10)

        self.table_number_entry = tk.Entry(master, width=20)
        self.table_number_entry.pack(pady=10)

        self.submit_button = tk.Button(master, text="Submit", command=self.set_table_number)
        self.submit_button.pack(pady=20)

    def set_table_number(self):
        table_number = self.table_number_entry.get()

        if table_number.isdigit() and int(table_number) > 0:
            messagebox.showinfo("Success", f"Table number {table_number} has been set.")
            self.table_number_entry.delete(0, tk.END)  # Clear the input field
        else:
            messagebox.showwarning("Input Error", "Please enter a valid table number.")
