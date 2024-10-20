from src.models.player import Player
import tkinter as tk


def show_all_members(connection):
    all_members_window = tk.Toplevel()
    all_members_window.title("All Members")

    # Create a frame for the league table
    table_frame = tk.Frame(all_members_window)
    table_frame.pack(padx=10, pady=10)

    # Function to populate the table with member data
    def populate_table():
        # Clear previous table content
        for widget in table_frame.winfo_children():
            widget.destroy()

        # Create header labels
        headers = ["Student Number", "First Name", "Last Name", "Points", "Times Played", "Total Won", "Total Spent",
                   "Membership Status", "Actions"]
        for col, header in enumerate(headers):
            header_label = tk.Label(table_frame, text=header, font=("Arial", 12, "bold"))
            header_label.grid(row=0, column=col, padx=10, pady=5)

        # Retrieve all members from the database
        all_members = Player.get_all_members(connection)

        # Populate the league table with standings
        for row, standing in enumerate(all_members, start=1):
            # Extract the player's details
            student_no, first_name, last_name, points, times_played, total_won, total_spent, membership_status = standing

            # Create labels for each column
            student_no_label = tk.Label(table_frame, text=student_no)
            student_no_label.grid(row=row, column=0, padx=10, pady=5)

            first_name_label = tk.Label(table_frame, text=first_name)
            first_name_label.grid(row=row, column=1, padx=10, pady=5)

            last_name_label = tk.Label(table_frame, text=last_name)
            last_name_label.grid(row=row, column=2, padx=10, pady=5)

            points_label = tk.Label(table_frame, text=points)
            points_label.grid(row=row, column=3, padx=10, pady=5)

            times_played_label = tk.Label(table_frame, text=times_played)
            times_played_label.grid(row=row, column=4, padx=10, pady=5)

            total_won_label = tk.Label(table_frame, text=f"£{total_won:.2f}")
            total_won_label.grid(row=row, column=5, padx=10, pady=5)

            total_spent_label = tk.Label(table_frame, text=f"£{total_spent:.2f}")
            total_spent_label.grid(row=row, column=6, padx=10, pady=5)

            membership_var = tk.BooleanVar(value=bool(membership_status))  # Convert 1 or 0 to True or False

            # Display the membership status as "True" or "False"
            membership_status_label = tk.Label(table_frame,
                                               text=str(membership_var.get()))  # Show boolean value as text
            membership_status_label.grid(row=row, column=7, padx=10, pady=5)

            # Add "Edit" and "Delete" buttons
            edit_button = tk.Button(table_frame, text="Edit", command=lambda p=standing, r=row: edit_member(p, r))
            edit_button.grid(row=row, column=8, padx=5, pady=5)

            delete_button = tk.Button(table_frame, text="Delete",
                                      command=lambda p=Player(student_no=student_no): delete_member(p))
            delete_button.grid(row=row, column=9, padx=5, pady=5)

    # Function to delete a member
    def delete_member(player):
        # Perform deletion from the database here
        player.delete_member(connection)
        # Refresh the table to reflect the changes
        populate_table()

    def edit_member(member, row):
        # Extract the player's details
        student_no, first_name, last_name, points, times_played, total_won, total_spent, membershipstatus = member

        # Clear existing widgets in the row
        for widget in table_frame.grid_slaves(row=row):
            widget.destroy()

        # Create entry fields for editing
        student_no_entry = tk.Entry(table_frame)
        student_no_entry.insert(0, student_no)
        student_no_entry.grid(row=row, column=0, padx=10, pady=5)

        first_name_entry = tk.Entry(table_frame)
        first_name_entry.insert(0, first_name)
        first_name_entry.grid(row=row, column=1, padx=10, pady=5)

        last_name_entry = tk.Entry(table_frame)
        last_name_entry.insert(0, last_name)
        last_name_entry.grid(row=row, column=2, padx=10, pady=5)

        points_entry = tk.Entry(table_frame)
        points_entry.insert(0, points)
        points_entry.grid(row=row, column=3, padx=10, pady=5)

        times_played_entry = tk.Entry(table_frame)
        times_played_entry.insert(0, times_played)
        times_played_entry.grid(row=row, column=4, padx=10, pady=5)

        total_won_entry = tk.Entry(table_frame)
        total_won_entry.insert(0, total_won)
        total_won_entry.grid(row=row, column=5, padx=10, pady=5)

        total_spent_entry = tk.Entry(table_frame)
        total_spent_entry.insert(0, total_spent)
        total_spent_entry.grid(row=row, column=6, padx=10, pady=5)

        # Entry field for Membership Status
        membership_status_entry = tk.Entry(table_frame)
        membership_status_entry.insert(0, "True" if membershipstatus else "False")  # Set to "True" or "False"
        membership_status_entry.grid(row=row, column=7, padx=10, pady=5)

        def update_member():
            # Update the Player object with new values
            updated_player = Player(
                student_no=student_no_entry.get(),
                first_name=first_name_entry.get(),
                last_name=last_name_entry.get(),
                points=int(points_entry.get()),
                total_won=float(total_won_entry.get()),
                total_spent=float(total_spent_entry.get()),
                membership_status=membership_status_entry.get()  # Add membership status
            )

            updated_player.edit_member(connection)

            # Refresh the table to show updated values
            populate_table()

        # Update button
        update_button = tk.Button(table_frame, text="Save", command=update_member)
        update_button.grid(row=row, column=8, padx=5, pady=5)  # Adjusted column index for the button


    # Initially populate the table
    populate_table()

    # Optionally, you can add a close button
    close_button = tk.Button(all_members_window, text="Close", command=all_members_window.destroy)
    close_button.pack(pady=10)
