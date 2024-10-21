import random
from tkinter import messagebox

from src.models.table import Table


class PlayerTable:
    def __init__(self, student_no,total_buy_in, table_id = None, placement=None, seat=None):
        """
        Initialize a PlayerTable object with required parameters.

        :param student_no: The player's ID (Primary Key, Foreign Key).
        :param table_id: The table's ID (Primary Key, Foreign Key).
        :param placement: The player's placement in the table.
        :param seat: The seat number occupied by the player.
        :param total_buy_in: The total buy-in amount for the player at this table.
        """
        self.student_no = student_no
        self.table_id = table_id
        self.placement = placement
        self.seat = seat
        self.total_buy_in = total_buy_in



    def seat_allocation(self, connection, week_no, buy_in):
        #we know player id, and total buy in
        tables = Table.get_tables_by_type(connection, week_no, buy_in)
        ##getting all the tables based if the player is free or paid

        not_found_free_table = True
        current_attempt_table = 0
        random_number = None
        taken_seats = []# Initialize the variable outside the loop

        while not_found_free_table:
            random_number = random.randint(0, len(tables) - 1)  # Generates a random index

            taken_seats = count_seats_allocated(connection, tables[random_number].table_id)

            if len(taken_seats) < tables[random_number].seat_count:
                self.table_id = tables[random_number].table_id
                not_found_free_table = False

            if current_attempt_table == len(tables):
                messagebox.showerror("Couldn't find any table with free seats!")
                break

            current_attempt_table = current_attempt_table + 1


        taken_seat_numbers = []
        for seat in taken_seats:
            taken_seat_numbers.append(seat.seat)

        chosen_table = Table.get_table_by_id(connection, self.table_id)

        not_found_random_seat = True
        while not_found_random_seat:
            random_seat_number = random.randint(1, chosen_table.seat_count)

            if random_seat_number not in taken_seat_numbers:
                not_found_random_seat = False
                self.seat = random_seat_number

        self.save_seat(connection)

        chosen_table.increment_pot(connection)


    def save_seat(self, connection):
        """
        Save the PlayerTable instance to the database.

        :param connection: The active database connection.
        """
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO playerseat (studentnumber, tableId, seat, totalBuyIn)
                    VALUES (%s, %s, %s, %s)
                    """,
                    (self.student_no, self.table_id, self.seat, self.total_buy_in)
                )
            connection.commit()  # Commit the transaction
        except Exception as e:
            connection.rollback()  # Rollback in case of error
            print(f"Error saving player table: {e}")
            raise e

    @staticmethod
    def get_taken_seats(connection, table_id):
        """
        Fetch all the taken seats for the specified table.

        :param connection: The active database connection.
        :param table_id: The ID of the table.
        :return: A list of dictionaries, each containing the seat information.
        """
        taken_seats = []
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT seat, studentnumber, tableid, totalbuyin, placement
                    FROM PlayerSeat WHERE tableId = %s
                """, (table_id,))
                results = cursor.fetchall()
                # Convert each row into a dictionary
                taken_seats = [
                    {
                        'seat': row[0],
                        'student_number': row[1],
                        'table_id': row[2],
                        'total_buy_in': row[3],
                        'placement': row[4]
                    }
                    for row in results
                ]
        except Exception as e:
            print(f"Error fetching taken seats: {e}")
        return taken_seats


def count_seats_allocated(connection, table_id):
    """
    Get all PlayerTable instances for a specific table based on the table_id.

    :param connection: The active database connection.
    :param table_id: The table ID to filter the PlayerTable records.
    :return: A list of PlayerTable instances associated with the given table_id.
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                    SELECT studentnumber, totalBuyIn, tableId, placement, seat
                    FROM playerseat
                    WHERE tableId = %s
                """, (table_id,))

            results = cursor.fetchall()  # Fetch all results

        player_tables = []  # Initialize an empty list to hold PlayerTable instances
        if results:
            # Convert each row to a PlayerTable instance
            for row in results:
                player_table = PlayerTable(
                    student_no=row[0],
                    total_buy_in=row[1],
                    table_id=row[2],
                    placement=row[3],
                    seat=row[4]
                )
                player_tables.append(player_table)  # Add the PlayerTable instance to the list

        return player_tables  # Return the list of PlayerTable instances
    except Exception as e:
        print(f"Error fetching PlayerTable records for table ID {table_id}: {e}")
        return []  # Return an empty list on error

