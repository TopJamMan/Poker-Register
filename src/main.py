import tkinter as tk
from tkinter import messagebox

def open_registration_form():
    # Create a new window for the registration form
    registration_window = tk.Toplevel(root)
    registration_window.title("Registration Form")

    # Get the screen dimensions
    screen_width = registration_window.winfo_screenwidth()
    screen_height = registration_window.winfo_screenheight()

    # Set the window size to half the screen
    window_width = screen_width // 2
    window_height = screen_height // 2

    # Calculate the position to center the window
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2

    # Set the geometry to the calculated size and position
    registration_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

    # Set the font size for input fields
    font_size = 16

    # Create and place the first name label and entry
    label_first_name = tk.Label(registration_window, text="First Name:", font=("Arial", font_size))
    label_first_name.pack(pady=10)
    entry_first_name = tk.Entry(registration_window, font=("Arial", font_size), width=30)
    entry_first_name.pack(pady=10)

    # Create and place the last name label and entry
    label_last_name = tk.Label(registration_window, text="Last Name:", font=("Arial", font_size))
    label_last_name.pack(pady=10)
    entry_last_name = tk.Entry(registration_window, font=("Arial", font_size), width=30)
    entry_last_name.pack(pady=10)

    # Submit function for the registration form
    def submit():
        first_name = entry_first_name.get()
        last_name = entry_last_name.get()
        if first_name and last_name:
            messagebox.showinfo("Registration Successful", f"Welcome, {first_name} {last_name}!")
        else:
            messagebox.showwarning("Input Error", "Please enter both first and last names.")

    # Create and place the submit button
    submit_button = tk.Button(registration_window, text="Submit", font=("Arial", font_size), command=submit)
    submit_button.pack(pady=20)

# Create the main home window
root = tk.Tk()
root.title("Home Panel")

# Set the main window size
root.geometry("400x300")

# Center the main window on the screen
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width - 400) // 2
y = (screen_height - 300) // 2
root.geometry(f"+{x}+{y}")

# Add a button to open the registration form
open_form_button = tk.Button(root, text="Open Registration Form", font=("Arial", 14), command=open_registration_form)
open_form_button.pack(pady=100)

# Start the Tkinter event loop
root.mainloop()
