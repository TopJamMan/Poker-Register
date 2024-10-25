import math
import tkinter as tk
from tkinter import messagebox

from src.models.player import Player
from src.models.player_seat import PlayerTable
from src.models.table import Table
from src.models.week import Week

class TableManagement:
    def __init__(self, master, connection):
        self.master = master
        self.connection = connection  # Store the database connection for later use
        self.master.title("Table Layout")

        # Set the window size
        self.master.geometry("800x600")  # Increase window size for more space
        self.center_window()  # Center the window on the screen

        # Create a frame to hold the tables and seats
        self.main_frame = tk.Frame(self.master)
        self.main_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)

        # Initialize the UI with current table data
        self.update_table_ui()

    def center_window(self):
        """Center the window on the screen."""
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        x = (screen_width - 800) // 2
        y = (screen_height - 600) // 2
        self.master.geometry(f"+{x}+{y}")

    def update_table_ui(self):
        """Update the table UI by fetching the latest table details from the database."""
        # Clear the existing content in the main frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        # Get the current week number and table details from the database
        current_week_no = Week.get_current_week_number(self.connection)
        table_list_detailed = Table.get_table_details(self.connection, current_week_no)

        # Configure the grid layout in the main frame to allow resizing
        self.main_frame.grid_rowconfigure(0, weight=1)  # Make the first row resizable
        self.main_frame.grid_columnconfigure(0, weight=1)  # Make the first column resizable
        self.main_frame.grid_columnconfigure(1, weight=1)  # Make the second column resizable

        # Iterate over the table list to create table frames in two columns
        for index, table in enumerate(table_list_detailed):
            # Calculate row and column indices for grid layout (2 columns)
            row = index // 2  # Every two tables go in a new row
            column = index % 2  # 0 for first column, 1 for second column

            # Create the table frame and place it in the grid
            table_frame = tk.Frame(self.main_frame, bd=2, relief=tk.SOLID)
            table_frame.grid(row=row, column=column, padx=10, pady=10, sticky="nsew")  # Use grid instead of pack

            # Configure the current row to be resizable
            self.main_frame.grid_rowconfigure(row, weight=1)  # Ensure the rows expand

            # Create the table frame using the existing method
            self.create_table_frame(table_frame, table)

        # Ensure the main window can resize both columns and rows dynamically
        for i in range((len(table_list_detailed) + 1) // 2):  # Configure all the created rows
            self.main_frame.grid_rowconfigure(i, weight=1)

        self.main_frame.grid_columnconfigure(0, weight=1)  # First column scales with window resize
        self.main_frame.grid_columnconfigure(1, weight=1)  # Second column scales with window resize

    def create_table_frame(self, parent_frame, table):
        """Create a frame to display the table and its seats."""
        table_frame = tk.Frame(parent_frame, bd=2, relief=tk.SOLID)
        table_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Center frame to hold the table number
        center_frame = tk.Frame(table_frame, width=1500, height=1500, bg="brown")
        center_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Table header label (table number)
        header_label = tk.Label(center_frame, text=f"Table {table.table_number}", bg="brown", fg="white")
        header_label.pack(expand=True)

        # Get occupied seats from the PlayerSeat table
        taken_seats = PlayerTable.get_taken_seats(self.connection, table.table_id)

        # Positions for seats
        positions = [
            (0.4, 0.1), (0.6, 0.1),  # Top (left and right)
            (0.9, 0.3), (0.9, 0.7),  # Right (top and bottom)
            (0.6, 0.7), (0.4, 0.7),  # Bottom (right and left)
            (0.1, 0.7), (0.1, 0.3),  # Left (bottom and top)
        ]

        # Create seat labels and display player details along with additional buy-in buttons
        for i in range(table.seat_count):
            x_pos, y_pos = positions[i]
            seat_info = next((seat for seat in taken_seats if seat['seat'] == i + 1), None)
            seat_color = "red" if seat_info else "lightgreen"

            if not seat_info:
                # Create a label for the unoccupied seat
                seat_label = tk.Label(table_frame, text=f"Seat {i + 1}", bg=seat_color, width=10, height=2)
                seat_label.place(relx=x_pos, rely=y_pos, anchor=tk.CENTER)

            # If the seat is occupied, display player information and "Additional Buy In" button
            else:
                self.display_player_info(seat_info, table, x_pos, y_pos, table_frame)

        # Pot and buy-in labels
        pot_label = tk.Label(table_frame, text=f"Pot: £{table.pot:.2f}", bg="lightgreen")
        pot_label.pack(side=tk.BOTTOM, pady=5)

        buy_in_label = tk.Label(table_frame, text=f"Buy-in: £{table.buy_in:.2f}", bg="lightblue")
        buy_in_label.pack(side=tk.BOTTOM, pady=5)

    def display_player_info(self, seat_info, table, x_pos, y_pos, table_frame):
        """Display player information and create an additional buy-in button."""
        player = Player.get_player_info(self.connection, seat_info['student_number'])
        if player:
            total_buy_in = seat_info['total_buy_in'] if seat_info['total_buy_in'] is not None else 0.00
            info_text = f"{player.first_name} {player.last_name}\nTotal Buy-In: £{total_buy_in:.2f}"

            # Create a label to show player information
            info_label = tk.Label(table_frame, text=info_text, bg="red", fg="white", wraplength=100)
            info_label.place(relx=x_pos, rely=y_pos, anchor=tk.CENTER)

            # Create the "Additional Buy In" button
            buy_in_button = tk.Button(table_frame, text="Additional Buy In",
                                      command=lambda: self.additional_buy_in_action(player, table))
            buy_in_button.place(relx=x_pos, rely=y_pos + 0.25, anchor=tk.CENTER)

    def additional_buy_in_action(self, player, table):
        """Handle the additional buy-in action for a player."""
        try:
            # Increment the pot and player's total spent
            table.increment_pot(self.connection)
            player.increment_total_spent(self.connection, table.buy_in)
            PlayerTable.increment_total_spent(self.connection, player.student_no, table.buy_in)

            # Update the UI to reflect the new pot value
            self.update_table_ui()

            # Show a success message
            messagebox.showinfo(
                "Success",
                f"{player.first_name} {player.last_name} rebought for £{table.buy_in:.2f} "
                f"at Table {table.table_number}"
            )
        except Exception as e:
            messagebox.showerror("Error", f"Failed to increment the pot: {e}")


    def move_player(self, player, player_seat, old_table, new_table):
        try:
            old_table.move_table(self.connection, player_seat, new_table)

            player_seat

            # Update the UI to reflect the new pot value
            self.update_table_ui()

            # Show a success message
            messagebox.showinfo(
                "Success",
                f"{player.first_name} {player.last_name} was moved to {new_table.table_number:.2f} "
            )
        except Exception as e:
            messagebox.showerror("Error", f"Failed to move player to the table: {e}")


