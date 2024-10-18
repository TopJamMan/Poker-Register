import tkinter as tk

class TableManagement:
    def __init__(self, master):
        self.master = master
        self.master.title("Table Layout")

        # Set the window size
        self.master.geometry("600x400")

        # Center the window on the screen
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        x = (screen_width - 600) // 2
        y = (screen_height - 400) // 2
        self.master.geometry(f"+{x}+{y}")

        # Create a frame to hold the table and seats
        frame = tk.Frame(self.master)
        frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)

        # Example of creating a table with seats
        num_seats = 8
        self.seat_labels = []

        # Create seat labels around a table
        for i in range(num_seats):
            seat = tk.Label(frame, text=f"Seat {i + 1}", bg="lightgray", width=10, height=2)
            seat.grid(row=i // 4, column=i % 4, padx=10, pady=10)
            self.seat_labels.append(seat)

        # Add a label for the table itself
        table_label = tk.Label(frame, text="Table", bg="brown", fg="white", width=10, height=2)
        table_label.grid(row=1, column=1, columnspan=2, padx=10, pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    table_app = TableManagement(root)
    root.mainloop()
