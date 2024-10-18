# table.py
import tkinter as tk

def open_table_window():
    table_window = tk.Toplevel()
    table_window.title("Table Layout")

    # Set the window size
    table_window.geometry("600x400")

    # Center the window on the screen
    screen_width = table_window.winfo_screenwidth()
    screen_height = table_window.winfo_screenheight()
    x = (screen_width - 600) // 2
    y = (screen_height - 400) // 2
    table_window.geometry(f"+{x}+{y}")

    # Create a frame to hold the table and seats
    frame = tk.Frame(table_window)
    frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)

    # Example of creating a table with seats
    num_seats = 8
    seat_labels = []

    # Create seat labels around a table
    for i in range(num_seats):
        seat = tk.Label(frame, text=f"Seat {i + 1}", bg="lightgray", width=10, height=2)
        seat.grid(row=i // 4, column=i % 4, padx=10, pady=10)
        seat_labels.append(seat)

    # Add a label for the table itself
    table_label = tk.Label(frame, text="Table", bg="brown", fg="white", width=10, height=2)
    table_label.grid(row=1, column=1, columnspan=2, padx=10, pady=10)

    # Run the table window event loop
    table_window.mainloop()
