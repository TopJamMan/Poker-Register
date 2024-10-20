class Table:
    def __init__(self, table_id=None, week_no=None, pot = 0, seat_count=0, buy_in=0.0, table_number=0):
        """
        Initialize a Table instance.

        :param table_id: The table ID (optional).
        :param week_no: The week number the table belongs to.
        :param seat_count: The number of seats at the table.
        :param buy_in: The buy-in amount for the table.
        :param table_number: The identifier for the table.
        """
        self.table_id = table_id
        self.week_no = week_no
        self.seat_count = seat_count
        self.pot = pot  # Default pot value
        self.buy_in = buy_in
        self.table_number = table_number


    def create_table(self, connection):
        """
        Save the Table instance to the database.

        :param connection: The active database connection.
        :return: The ID of the created table.
        """
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO "table" (weekno, seatCount, pot, buyIn, tableNumber)
                    VALUES (%s, %s, %s, %s, %s) RETURNING tableId
                    """,
                    (self.week_no, self.seat_count, self.pot, self.buy_in, self.table_number)
                )
                self.table_id = cursor.fetchone()[0]  # Fetch the generated table ID
                connection.commit()
                return self.table_id  # Return the created table ID
        except Exception as e:
            connection.rollback()
            print(f"Error creating table: {e}")
            raise e

    def edit_table(self, connection):
        """
        Edit the Table instance in the database based on table_id.

        :param connection: The active database connection.
        """
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE "table"
                    SET pot = %s, buyIn = %s, seatCount = %s, tableNumber = %s
                    WHERE tableId = %s
                    """,
                    (self.pot, self.buy_in, self.seat_count, self.table_number, self.table_id)
                )
            connection.commit()
        except Exception as e:
            connection.rollback()
            raise e

    @staticmethod
    def get_table_details(connection, week_no):
        """
        Get table details as a list of Table instances from the database.

        :param connection: The active database connection.
        :param week_no: The week number to filter the tables.
        :return: A list of Table instances.
        """
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT tableId, weekno, seatCount, pot, buyIn, tableNumber 
                    FROM "table" 
                    WHERE weekno = %s
                """, (week_no,))
                results = cursor.fetchall()  # Fetch all results

            tables = []  # Initialize an empty list to hold the Table instances
            if results:
                # Convert each row to a Table instance
                for row in results:
                    table = Table(
                        table_id=row[0],
                        week_no=row[1],
                        seat_count=row[2],
                        pot = row[3],
                        buy_in=row[4],
                        table_number=row[5]
                    )
                    tables.append(table)  # Add the Table instance to the list

                return tables  # Return the list of Table instances
            else:
                return []  # Return an empty list if no results
        except Exception as e:
            print(f"Error fetching table details: {e}")
            return []  # Return an empty list on error

    @staticmethod
    def get_tables_by_type(connection, week_no, buy_in):
        """
        Get a list of free or paid tables based on the buy-in amount.

        :param connection: The active database connection.
        :param week_no: The week number to filter the tables.
        :param is_free: If True, get free tables (buy_in = 0). If False, get paid tables (buy_in > 0).
        :return: A list of Table instances matching the specified type.
        """
        try:
            with connection.cursor() as cursor:
                # Determine the condition for the query based on whether the tables are free or paid
                cursor.execute("""
                    SELECT tableId, weekno, seatCount, pot, buyIn, tableNumber
                    FROM "table"
                    WHERE weekno = %s AND buyIn = %s
                """, (week_no, buy_in))

                results = cursor.fetchall()  # Fetch all results

            tables = []  # Initialize an empty list to hold the Table instances
            if results:
                # Convert each row to a Table instance
                for row in results:
                    table = Table(
                        table_id=row[0],
                        week_no=row[1],
                        seat_count=row[2],
                        pot=row[3],
                        buy_in=row[4],
                        table_number=row[5]
                    )
                    tables.append(table)  # Add the Table instance to the list

            return tables  # Return the list of Table instances
        except Exception as e:
            print(f"Error fetching tables by type: {e}")
            return []  # Return an empty

