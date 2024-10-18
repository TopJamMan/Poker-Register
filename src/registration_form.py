import tkinter as tk
from tkinter import messagebox

def submit():
    first_name = entry_first_name.get()
    last_name = entry_last_name.get()
    if first_name and last_name:
        messagebox.showinfo("Registration Successful", f"Welcome, {first_name} {last_name}!")
    else:
        messagebox.showwarning("Input Error", "Please enter both first and last names.")

# Create the main window
root = tk.Tk()
root.title("Registration Form")

# Get the screen dimensions
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Set the window size to half the screen
window_width = screen_width // 2
window_height = screen_height // 2

# Calculate the position to center the window
x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2

# Set the geometry to the calculated size and position
root.geometry(f"{window_width}x{window_height}+{x}+{y}")

# Set the font size for input fields
font_size = 16

# Create and place the first name label and entry
label_first_name = tk.Label(root, text="First Name:", font=("Arial", font_size))
label_first_name.pack(pady=10)
entry_first_name = tk.Entry(root, font=("Arial", font_size), width=30)
entry_first_name.pack(pady=10)

# Create and place the last name label and entry
label_last_name = tk.Label(root, text="Last Name:", font=("Arial", font_size))
label_last_name.pack(pady=10)
entry_last_name = tk.Entry(root, font=("Arial", font_size), width=30)
entry_last_name.pack(pady=10)

# Create and place the submit button
submit_button = tk.Button(root, text="Submit", font=("Arial", font_size), command=submit)
submit_button.pack(pady=20)

# Start the Tkinter event loop
root.mainloop()
