# home_page.py
import tkinter as tk
from registration_form import open_registration_form
from table import open_table_window

def main():
    root = tk.Tk()
    root.title("Home Panel")
    root.geometry("400x300")

    # Center the main window on the screen
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - 400) // 2
    y = (screen_height - 300) // 2
    root.geometry(f"+{x}+{y}")

    # Add a button to open the registration form
    open_form_button = tk.Button(root, text="Open Registration Form", font=("Arial", 14), command=open_registration_form)
    open_form_button.pack(pady=20)

    # Add a button to open the table layout
    open_table_button = tk.Button(root, text="Open Table Layout", font=("Arial", 14), command=open_table_window)
    open_table_button.pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    main()
