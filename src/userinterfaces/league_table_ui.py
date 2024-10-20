from src.models.player import Player
import tkinter as tk
from tkinter import messagebox

def show_league_table(connection):
    standings = Player.get_league_standing(connection)

    league_table_window = tk.Toplevel()
    league_table_window.title("League Table")

    # Create a frame for the league table
    table_frame = tk.Frame(league_table_window)
    table_frame.pack(padx=10, pady=10)

    # Create header labels
    headers = ["Rank", "First Name", "Last Name", "Points", "Times Played", "Total Won", "Total Spent"]
    for col, header in enumerate(headers):
        header_label = tk.Label(table_frame, text=header, font=("Arial", 12, "bold"))
        header_label.grid(row=0, column=col, padx=10, pady=5)

    # Populate the league table with standings and calculate ranks
    for row, standing in enumerate(standings, start=1):
        rank = row  # Since the standings are sorted, the row number can be the rank
        first_name, last_name, points, times_played, total_won, total_spent = standing

        # Create labels for each column
        rank_label = tk.Label(table_frame, text=rank)
        rank_label.grid(row=row, column=0, padx=10, pady=5)

        player_name_label = tk.Label(table_frame, text=first_name)
        player_name_label.grid(row=row, column=1, padx=10, pady=5)

        last_name_label = tk.Label(table_frame, text=last_name)
        last_name_label.grid(row=row, column=2, padx=10, pady=5)

        points_label = tk.Label(table_frame, text=points)
        points_label.grid(row=row, column=3, padx=10, pady=5)

        times_played_label = tk.Label(table_frame, text=times_played)
        times_played_label.grid(row=row, column=4, padx=10, pady=5)

        # Add the total_won and total_spent labels with currency symbol
        total_won_label = tk.Label(table_frame, text=f"£{total_won:.2f}")  # Format as currency
        total_won_label.grid(row=row, column=5, padx=10, pady=5)

        total_spent_label = tk.Label(table_frame, text=f"£{total_spent:.2f}")  # Format as currency
        total_spent_label.grid(row=row, column=6, padx=10, pady=5)

    # Optionally, you can add a close button
    close_button = tk.Button(league_table_window, text="Close", command=league_table_window.destroy)
    close_button.pack(pady=10)