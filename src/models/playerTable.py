from msilib.schema import tables
import random
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
        print(self.student_no, self.table_id, self.placement, self.seat,self.total_buy_in)
        #we know player id, and total buy in
        tables = Table.get_tables_by_type(connection, week_no, buy_in)
        ##getting all the tables based if the player is free or paid

        not_found_free_table = True
        random_number = None
        taken_seats = []# Initialize the variable outside the loop

        while not_found_free_table:
            random_number = random.randint(0, len(tables) - 1)  # Generates a random index

            taken_seats = count_seats_allocated(connection, tables[random_number].table_id)

            if len(taken_seats) < tables[random_number].seat_count:
                not_found_free_table = False

        self.table_id = random_number

        print(taken_seats)

        not_found_free_seat = True
        while not_found_free_seat:
            random_number = random.randint(1, tables[random_number].seat_count)

            if random_number != taken_seats[random_number].seat:
                not_found_free_table = False

        #megszamolni hany darab seat van mar allokalva minden asztalhoz minden tablehoz a Player tableben

        #selecting a seat that is not taken based on table id and free seats

        #saving it to the database with the details

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
                    FROM "playerseat"
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

