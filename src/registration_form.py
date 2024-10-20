import tkinter as tk
from tkinter import messagebox

from src.models.player import Player


def open_registration_form(connection):
    registration_window = tk.Toplevel()
    registration_window.title("Registration Form")

    # Configure window
    screen_width = registration_window.winfo_screenwidth()
    screen_height = registration_window.winfo_screenheight()
    window_width = screen_width // 2
    window_height = screen_height // 2
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    registration_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

    font_size = 16

    # First name entry
    label_first_name = tk.Label(registration_window, text="First Name:", font=("Arial", font_size))
    label_first_name.pack(pady=10)
    entry_first_name = tk.Entry(registration_window, font=("Arial", font_size), width=30)
    entry_first_name.pack(pady=10)

    # Last name entry
    label_last_name = tk.Label(registration_window, text="Last Name:", font=("Arial", font_size))
    label_last_name.pack(pady=10)
    entry_last_name = tk.Entry(registration_window, font=("Arial", font_size), width=30)
    entry_last_name.pack(pady=10)

    # Student no. entry
    label_student_no = tk.Label(registration_window, text="Student Number:", font=("Arial", font_size))
    label_student_no.pack(pady=10)
    entry_student_no = tk.Entry(registration_window, font=("Arial", font_size), width=30)
    entry_student_no.pack(pady=10)

    # Free/Paid table selection
    def activate_button1():
        button1.config(state=tk.DISABLED)  # Disable button 1
        button2.config(state=tk.NORMAL)  # Enable button 2
        table_type = "Free"

    def activate_button2():
        button2.config(state=tk.DISABLED)  # Disable button 2
        button1.config(state=tk.NORMAL)  # Enable button 1
        table_type = "Paid"

    button_frame = tk.Frame(registration_window)
    button_frame.pack(pady=10)  # Add some vertical padding

    button1 = tk.Button(button_frame, text="Free", command=activate_button1, width=6, height=2)
    button1.pack(side=tk.LEFT, padx=5)  # Place button1 to the left with padding
    button2 = tk.Button(button_frame, text="Paid", command=activate_button2, width=6, height=2)
    button2.pack(side=tk.LEFT, padx=5)  # Place button2 to the left with padding

    # Submit function for the registration form
    def submit():
        first_name = entry_first_name.get()
        last_name = entry_last_name.get()
        student_no = entry_student_no.get()


        if button1.cget("state") == tk.NORMAL:
            table_type = 5
        else:
            table_type = 0


        if first_name and last_name and student_no and not (button1.cget("state") == tk.DISABLED and button2.cget("state") == tk.DISABLED):
            try:
                # Create a Player instance
                new_player = Player(first_name=first_name, last_name=last_name, student_no=student_no)

                # Save the player to the database using the Player class method
                new_player.save_to_db(connection)

                new_player.increment_total_spent(connection,table_type)

                messagebox.showinfo("Registration Successful", f"Welcome, {first_name} {last_name}!")
                registration_window.destroy()  # Close the registration window
            except Exception as e:
                messagebox.showerror("Database Error", f"Failed to save to the database: {e}")
                connection.rollback()
        else:
            messagebox.showwarning("Input Error", "Please enter all fields")

    # Create and place the submit button
    submit_button = tk.Button(registration_window, text="Submit", font=("Arial", font_size), command=submit)
    submit_button.pack(pady=20)
