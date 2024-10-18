class Table:
    def __init__(self, table_id=None, week_id=None, seat_count=0, pot=0.00, buy_in=0.00, table_number=0):
        """
        Initialize a Table object with optional parameters.

        :param table_id: The unique identifier for the table (Primary Key).
        :param week_id: The foreign key referencing the Week table.
        :param seat_count: The number of seats available at the table.
        :param pot: The current pot amount at the table.
        :param buy_in: The buy-in amount for the table.
        :param table_number: The number assigned to the table.
        """
        self.table_id = table_id
        self.week_id = week_id
        self.seat_count = seat_count
        self.pot = pot
        self.buy_in = buy_in
        self.table_number = table_number

    def save_to_db(self, connection):
        """
        Save the Table instance to the database.

        :param connection: The active database connection.
        """
        try:
            with connection.cursor() as cursor:
                if self.table_id is None:
                    # Insert new table if table_id is not set
                    cursor.execute(
                        """
                        INSERT INTO Table (weekId, seatCount, pot, buyIn, tableNumber)
                        VALUES (%s, %s, %s, %s, %s) RETURNING tableId
                        """,
                        (self.week_id, self.seat_count, self.pot, self.buy_in, self.table_number)
                    )
                    self.table_id = cursor.fetchone()[0]  # Get the generated table ID
                else:
                    # Update existing table if table_id is set
                    cursor.execute(
                        """
                        UPDATE Table
                        SET weekId = %s, seatCount = %s, pot = %s, buyIn = %s, tableNumber = %s
                        WHERE tableId = %s
                        """,
                        (self.week_id, self.seat_count, self.pot, self.buy_in, self.table_number, self.table_id)
                    )
            connection.commit()
        except Exception as e:
            connection.rollback()
            raise e

    def delete_from_db(self, connection):
        """
        Delete the Table instance from the database.

        :param connection: The active database connection.
        """
        try:
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM Table WHERE tableId = %s", (self.table_id,))
            connection.commit()
        except Exception as e:
            connection.rollback()
            raise e

    @classmethod
    def load_from_db(cls, connection, table_id):
        """
        Load a Table instance from the database.

        :param connection: The active database connection.
        :param table_id: The ID of the table to load.
        :return: A Table object if found, otherwise None.
        """
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT tableId, weekId, seatCount, pot, buyIn, tableNumber FROM Table WHERE tableId = %s", (table_id,))
                row = cursor.fetchone()
                if row:
                    return cls(table_id=row[0], week_id=row[1], seat_count=row[2], pot=row[3], buy_in=row[4], table_number=row[5])
                else:
                    return None
        except Exception as e:
            raise e
