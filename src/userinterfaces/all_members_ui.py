from src.models.player import Player
import tkinter as tk

def show_all_members(connection):
    all_members = Player.get_all_members(connection)

    all_members_window = tk.Toplevel()
    all_members_window.title("All Members")

    # Create a frame for the league table
    table_frame = tk.Frame(all_members_window)
    table_frame.pack(padx=10, pady=10)

    # Create header labels
    headers = ["Student Number", "First Name", "Last Name", "Points", "Times Played", "Total Won", "Total Spent",
               "Actions"]
    for col, header in enumerate(headers):
        header_label = tk.Label(table_frame, text=header, font=("Arial", 12, "bold"))
        header_label.grid(row=0, column=col, padx=10, pady=5)

    # Function to delete a member
    def delete_member(member_id):
        # Perform deletion from the database here
        Player.delete_member(connection=self.connection, member_id=member_id)
        # Refresh the list to reflect the changes
        all_members_window.destroy()
        self.show_all_members()

    # Function to edit a member's details
    def edit_member(member):
        # Open a new window or a popup to edit the member's details
        edit_window = tk.Toplevel(all_members_window)
        edit_window.title("Edit Member")

        # Create input fields for each member detail
        first_name_entry = tk.Entry(edit_window)
        first_name_entry.insert(0, member[0])  # Assuming first_name is the first value in the tuple
        first_name_entry.grid(row=0, column=1, padx=5, pady=5)

        last_name_entry = tk.Entry(edit_window)
        last_name_entry.insert(0, member[1])
        last_name_entry.grid(row=1, column=1, padx=5, pady=5)

        # Add other fields as needed...

        # Update function
        def update_member():
            # Implement the update in the database
            Player.update_member(connection=self.connection, member_id=member[6],
                                 first_name=first_name_entry.get(), last_name=last_name_entry.get())
            # Refresh the list
            edit_window.destroy()
            all_members_window.destroy()
            self.show_all_members()

        # Update button
        update_button = tk.Button(edit_window, text="Update", command=update_member)
        update_button.grid(row=2, column=0, columnspan=2, pady=10)

    # Populate the league table with standings
    for row, standing in enumerate(all_members, start=1):
        # Extract the player's details
        first_name, last_name, points, times_played, total_won, total_spent, member_id = standing

        # Create labels for each column
        player_name_label = tk.Label(table_frame, text=first_name)
        player_name_label.grid(row=row, column=0, padx=10, pady=5)

        last_name_label = tk.Label(table_frame, text=last_name)
        last_name_label.grid(row=row, column=1, padx=10, pady=5)

        points_label = tk.Label(table_frame, text=points)
        points_label.grid(row=row, column=2, padx=10, pady=5)

        times_played_label = tk.Label(table_frame, text=times_played)
        times_played_label.grid(row=row, column=3, padx=10, pady=5)

        total_won_label = tk.Label(table_frame, text=f"£{total_won:.2f}")
        total_won_label.grid(row=row, column=4, padx=10, pady=5)

        total_spent_label = tk.Label(table_frame, text=f"£{total_spent:.2f}")
        total_spent_label.grid(row=row, column=5, padx=10, pady=5)

        # Add "Edit" and "Delete" buttons
        edit_button = tk.Button(table_frame, text="Edit", command=lambda m=standing: edit_member(m))
        edit_button.grid(row=row, column=6, padx=5, pady=5)

        delete_button = tk.Button(table_frame, text="Delete", command=lambda m_id=member_id: delete_member(m_id))
        delete_button.grid(row=row, column=7, padx=5, pady=5)

    # Optionally, you can add a close button
    close_button = tk.Button(all_members_window, text="Close", command=all_members_window.destroy)
    close_button.pack(pady=10)