class Week:
    def __init__(self, week_no, fiver_table_count, free_table_count):
        """
        Initialize a Week object with optional parameters.

        :param table_count: The number of tables associated with this week.
        :param week_no: The number of the week.
        """

        self.week_no = week_no
        self.fiver_table_count = fiver_table_count
        self.free_table_count = free_table_count

    def save_to_db(self, connection):
        """
        Save the Week instance to the database.

        :param connection: The active database connection.
        """
        try:
            with connection.cursor() as cursor:
                    # Insert new week if week_id is not set
                    cursor.execute(
                        """
                        INSERT INTO Week (weekNo,freetablecount, fivertablecount)
                        VALUES (%s, %s, %s) 
                        """,
                        (self.week_no,self.free_table_count, self.fiver_table_count, )
                    )
            connection.commit()
        except Exception as e:
            connection.rollback()
            raise e

    @staticmethod
    def get_current_week_number(connection):
        """
        Fetch the current week number from the Week table.

        :param connection: The active database connection.
        :return: Current week number or None if not found.
        """
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                        SELECT weekNo FROM "week" ORDER BY weekNo DESC LIMIT 1
                    """)
                result = cursor.fetchone()
                if result:
                    return result[0]  # Return the current week number
                else:
                    return None  # Return None if no week found
        except Exception as e:
            print(f"Error fetching current week number: {e}")
            return None  # Return None on error
