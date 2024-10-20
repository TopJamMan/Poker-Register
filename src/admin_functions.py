import tkinter as tk
from tkinter import messagebox
from venv import create

from src.models.player import Player
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

        self.show_league_table_button = tk.Button(master, text="Show League Table", command=self.show_league_table)
        self.show_league_table_button.pack(pady=20)

        self.show_all_members_button = tk.Button(master, text="Show All Members", command=self.show_all_members)
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

    def show_league_table(self):
        standings = Player.get_league_standing(connection=self.connection)

        league_table_window = tk.Toplevel(self.master)
        league_table_window.title("League Table")

        # Create a frame for the league table
        table_frame = tk.Frame(league_table_window)
        table_frame.pack(padx=10, pady=10)

        # Create header labels
        headers = ["Rank", "First Name", "Last Name", "Points", "Times Played", "Total Won", "Total Spent"]
        for col, header in enumerate(headers):
            header_label = tk.Label(table_frame, text=header, font=("Arial", 12, "bold"))
            header_label.grid(row=0, column=col, padx=10, pady=5)

        # Populate the league table with standings and calculate ranks
        for row, standing in enumerate(standings, start=1):
            rank = row  # Since the standings are sorted, the row number can be the rank
            first_name, last_name, points, times_played, total_won, total_spent = standing

            # Create labels for each column
            rank_label = tk.Label(table_frame, text=rank)
            rank_label.grid(row=row, column=0, padx=10, pady=5)

            player_name_label = tk.Label(table_frame, text=first_name)
            player_name_label.grid(row=row, column=1, padx=10, pady=5)

            last_name_label = tk.Label(table_frame, text=last_name)
            last_name_label.grid(row=row, column=2, padx=10, pady=5)

            points_label = tk.Label(table_frame, text=points)
            points_label.grid(row=row, column=3, padx=10, pady=5)

            times_played_label = tk.Label(table_frame, text=times_played)
            times_played_label.grid(row=row, column=4, padx=10, pady=5)

            # Add the total_won and total_spent labels with currency symbol
            total_won_label = tk.Label(table_frame, text=f"£{total_won:.2f}")  # Format as currency
            total_won_label.grid(row=row, column=5, padx=10, pady=5)

            total_spent_label = tk.Label(table_frame, text=f"£{total_spent:.2f}")  # Format as currency
            total_spent_label.grid(row=row, column=6, padx=10, pady=5)

        # Optionally, you can add a close button
        close_button = tk.Button(league_table_window, text="Close", command=league_table_window.destroy)
        close_button.pack(pady=10)

    def show_all_members(self):
        all_members = Player.get_all_members(connection=self.connection)

        all_members_window = tk.Toplevel(self.master)
        all_members_window.title("All Members")

        # Create a frame for the league table
        table_frame = tk.Frame(all_members_window)
        table_frame.pack(padx=10, pady=10)

        # Create header labels
        headers = ["Student Number","First Name", "Last Name", "Points", "Times Played", "Total Won", "Total Spent", "Actions"]
        for col, header in enumerate(headers):
            header_label = tk.Label(table_frame, text=header, font=("Arial", 12, "bold"))
            header_label.grid(row=0, column=col, padx=10, pady=5)

        # Function to delete a member
        def delete_member(member_id):
            # Perform deletion from the database here
            Player.delete_member(connection=self.connection, member_id=member_id)
            # Refresh the list to reflect the changes
            all_members_window.destroy()
            self.show_all_members()

        # Function to edit a member's details
        def edit_member(member):
            # Open a new window or a popup to edit the member's details
            edit_window = tk.Toplevel(all_members_window)
            edit_window.title("Edit Member")

            # Create input fields for each member detail
            first_name_entry = tk.Entry(edit_window)
            first_name_entry.insert(0, member[0])  # Assuming first_name is the first value in the tuple
            first_name_entry.grid(row=0, column=1, padx=5, pady=5)

            last_name_entry = tk.Entry(edit_window)
            last_name_entry.insert(0, member[1])
            last_name_entry.grid(row=1, column=1, padx=5, pady=5)

            # Add other fields as needed...

            # Update function
            def update_member():
                # Implement the update in the database
                Player.update_member(connection=self.connection, member_id=member[6],
                                     first_name=first_name_entry.get(), last_name=last_name_entry.get())
                # Refresh the list
                edit_window.destroy()
                all_members_window.destroy()
                self.show_all_members()

            # Update button
            update_button = tk.Button(edit_window, text="Update", command=update_member)
            update_button.grid(row=2, column=0, columnspan=2, pady=10)

        # Populate the league table with standings
        for row, standing in enumerate(all_members, start=1):
            # Extract the player's details
            first_name, last_name, points, times_played, total_won, total_spent, member_id = standing

            # Create labels for each column
            player_name_label = tk.Label(table_frame, text=first_name)
            player_name_label.grid(row=row, column=0, padx=10, pady=5)

            last_name_label = tk.Label(table_frame, text=last_name)
            last_name_label.grid(row=row, column=1, padx=10, pady=5)

            points_label = tk.Label(table_frame, text=points)
            points_label.grid(row=row, column=2, padx=10, pady=5)

            times_played_label = tk.Label(table_frame, text=times_played)
            times_played_label.grid(row=row, column=3, padx=10, pady=5)

            total_won_label = tk.Label(table_frame, text=f"£{total_won:.2f}")
            total_won_label.grid(row=row, column=4, padx=10, pady=5)

            total_spent_label = tk.Label(table_frame, text=f"£{total_spent:.2f}")
            total_spent_label.grid(row=row, column=5, padx=10, pady=5)

            # Add "Edit" and "Delete" buttons
            edit_button = tk.Button(table_frame, text="Edit", command=lambda m=standing: edit_member(m))
            edit_button.grid(row=row, column=6, padx=5, pady=5)

            delete_button = tk.Button(table_frame, text="Delete", command=lambda m_id=member_id: delete_member(m_id))
            delete_button.grid(row=row, column=7, padx=5, pady=5)

        # Optionally, you can add a close button
        close_button = tk.Button(all_members_window, text="Close", command=all_members_window.destroy)
        close_button.pack(pady=10)
