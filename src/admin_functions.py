import tkinter as tk
from tkinter import messagebox
from src.userinterfaces import all_members_ui as all_members, league_table_ui as league_table

from src.models.table import Table
from src.models.week import Week

class AdminFunctions:
    def __init__(self, master, connection):
        self.master = master
        self.connection = connection  # Store the connection in the class
        self.master.title("Admin Functions")

        # Add a button for starting a new week
        self.start_week_button = tk.Button(master, text="Start New Week", command=self.start_new_week)
        self.start_week_button.pack(pady=20)

        self.show_league_table_button = tk.Button(master, text="Show League Table",
                                                  command=lambda: league_table.show_league_table(connection))
        self.show_league_table_button.pack(pady=20)

        self.show_all_members_button = tk.Button(master, text="Show All Members", command=lambda: all_members.show_all_members(connection))
        self.show_all_members_button.pack(pady=20)

    def start_new_week(self):
        # Create a new popup window for starting a new week
        new_week_window = tk.Toplevel(self.master)
        new_week_window.title("Start New Week")

        # Label and entry for the week number
        label_week_number = tk.Label(new_week_window, text="Enter Week Number:")
        label_week_number.pack(pady=10)

        self.entry_week_number = tk.Entry(new_week_window, width=20)
        self.entry_week_number.pack(pady=10)

        # Label and entry for £5 tables
        label_5_pound = tk.Label(new_week_window, text="How many £5 tables?")
        label_5_pound.pack(pady=10)

        self.entry_5_pound = tk.Entry(new_week_window, width=20)
        self.entry_5_pound.pack(pady=10)

        # Label and entry for free tables
        label_free = tk.Label(new_week_window, text="How many free tables?")
        label_free.pack(pady=10)

        self.entry_free = tk.Entry(new_week_window, width=20)
        self.entry_free.pack(pady=10)

        # Submit button for the popup window
        submit_button = tk.Button(new_week_window, text="Submit", command=lambda: self.submit_new_week(new_week_window))
        submit_button.pack(pady=20)

    def submit_new_week(self, new_week_window):
        # Retrieve the input values
        week_no = self.entry_week_number.get()
        fiver_count = self.entry_5_pound.get()
        free_count = self.entry_free.get()

        # Validate inputs
        if not (week_no.isdigit() and fiver_count.isdigit() and free_count.isdigit()):
            messagebox.showwarning("Input Error", "Please enter valid numbers for all fields.")
            return

        try:
            # Convert input strings to integers
            week_no = int(week_no)
            fiver_count = int(fiver_count)
            free_count = int(free_count)

            # Create a Week instance
            week = Week(week_no, fiver_count, free_count)

            # Save to the database
            week.save_to_db(self.connection)

            table_counter = 1

            for i in range(fiver_count):  # Loop from 0 to fiver_count - 1
                table = Table(week_no=week_no,seat_count=8,buy_in=5,table_number=table_counter)
                table_counter = table_counter + 1
                table.create_table(self.connection)

            for i in range(free_count):  # Loop from 0 to free_count - 1
                table = Table(week_no=week_no,seat_count=8,buy_in=0,table_number=table_counter)
                table_counter = table_counter + 1
                table.create_table(self.connection)

            messagebox.showinfo("Success",
                                f"Week {week_no} has been started with {fiver_count} £5 tables and {free_count} free tables.")
            new_week_window.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start the new week: {e}")
