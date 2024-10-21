import math
import tkinter as tk
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
        """
        Create a frame to display the details of a single table with seats arranged in a rectangular pattern.

        :param parent_frame: The parent frame to add this table frame to.
        :param table: The Table instance containing the table's details.
        """
        # Create a frame for this table
        table_frame = tk.Frame(parent_frame, bd=2, relief=tk.SOLID)
        table_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Center frame to hold the table number
        center_frame = tk.Frame(table_frame, width=100, height=100, bg="brown")
        center_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Table header label (table number)
        header_label = tk.Label(center_frame, text=f"Table {table.table_number}", bg="brown", fg="white")
        header_label.pack(expand=True)

        # Maximum of 8 seats in total (2 seats per side)
        num_seats = table.seat_count

        # Positions for 2 seats on each side
        positions = [
            (0.4, 0.1), (0.6, 0.1),  # Top (left and right)
            (0.9, 0.3), (0.9, 0.7),  # Right (top and bottom)
            (0.6, 0.9), (0.4, 0.9),  # Bottom (right and left)
            (0.1, 0.7), (0.1, 0.3),  # Left (bottom and top)
        ]

        # Create seat labels based on the calculated positions
        for i in range(num_seats):
            x_pos, y_pos = positions[i]  # Get the (x, y) position for this seat
            seat_label = tk.Label(table_frame, text=f"Seat {i + 1}", bg="lightgreen", width=10, height=2)
            seat_label.place(relx=x_pos, rely=y_pos, anchor=tk.CENTER)

        # Pot and buy-in labels (optional, if you want to display them)
        display_pot = table.pot
        if display_pot >= 50:
            display_pot -= 5

        pot_label = tk.Label(table_frame, text=f"Pot: ${display_pot:.2f}", bg="lightgreen")
        pot_label.pack(side=tk.BOTTOM, pady=5)

        buy_in_label = tk.Label(table_frame, text=f"Buy-in: ${table.buy_in:.2f}", bg="lightblue")
        buy_in_label.pack(side=tk.BOTTOM, pady=5)