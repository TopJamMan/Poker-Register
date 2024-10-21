import math
import tkinter as tk

from src.models.player import Player
from src.models.playerTable import PlayerTable
from src.models.table import Table
from src.models.week import Week

class TableManagement:
    def __init__(self, master, connection):
        self.master = master
        self.connection = connection  # Store the database connection for later use
        self.master.title("Table Layout")

        # Set the window size
        self.master.geometry("800x600")  # Increase window size for more space

        # Center the window on the screen
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        x = (screen_width - 800) // 2
        y = (screen_height - 600) // 2
        self.master.geometry(f"+{x}+{y}")

        # Create a frame to hold the tables and seats
        self.main_frame = tk.Frame(self.master)
        self.main_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)

        # Initialize the UI with current table data
        self.update_table_ui()

    def update_table_ui(self):
        """Update the table UI by fetching the latest table details from the database."""
        # Clear the existing content in the main frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        # Get the current week number
        current_week_no = Week.get_current_week_number(self.connection)

        # Get table details from the database
        table_list_detailed = Table.get_table_details(self.connection, current_week_no)

        # Create a frame for each table
        for table in table_list_detailed:
            self.create_table_frame(self.main_frame, table)

    def create_table_frame(self, parent_frame, table):
        # Create a frame for this table
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

        # Create seat labels based on the calculated positions
        for i in range(table.seat_count):
            x_pos, y_pos = positions[i]

            # Check if the seat is taken
            seat_info = next((seat for seat in taken_seats if seat['seat'] == i + 1), None)
            seat_color = "red" if seat_info else "lightgreen"

            # Create a label for the seat
            seat_label = tk.Label(table_frame, text=f"Seat {i + 1}", bg=seat_color, width=10, height=2)
            seat_label.place(relx=x_pos, rely=y_pos, anchor=tk.CENTER)

            # If the seat is taken, display player information below the seat
            if seat_info:
                # Fetch player information using the student number
                player = Player.get_player_info(self.connection, seat_info['student_number'])
                if player:
                    # Use 0.00 as default if total_buy_in is None
                    total_buy_in = seat_info['total_buy_in'] if seat_info['total_buy_in'] is not None else 0.00
                    info_text = f"Taken by: {player.first_name} {player.last_name}\nBuy-in: ${total_buy_in:.2f}"
                    info_label = tk.Label(table_frame, text=info_text, bg="red", fg="white", wraplength=100)
                    # Position the info label slightly lower to avoid overlap with the seat label
                    info_label.place(relx=x_pos, rely=y_pos + 0.15, anchor=tk.CENTER)

        # Pot and buy-in labels
        pot_label = tk.Label(table_frame, text=f"Pot: ${table.pot:.2f}", bg="lightgreen")
        pot_label.pack(side=tk.BOTTOM, pady=5)

        buy_in_label = tk.Label(table_frame, text=f"Buy-in: ${table.buy_in:.2f}", bg="lightblue")
        buy_in_label.pack(side=tk.BOTTOM, pady=5)

