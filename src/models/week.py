class Week:
    def __init__(self, week_id=None, table_count=0, week_no=0):
        """
        Initialize a Week object with optional parameters.

        :param week_id: The unique identifier for the week (Primary Key).
        :param table_count: The number of tables associated with this week.
        :param week_no: The number of the week.
        """
        self.week_id = week_id
        self.table_count = table_count
        self.week_no = week_no

    def save_to_db(self, connection):
        """
        Save the Week instance to the database.

        :param connection: The active database connection.
        """
        try:
            with connection.cursor() as cursor:
                if self.week_id is None:
                    # Insert new week if week_id is not set
                    cursor.execute(
                        """
                        INSERT INTO Week (tableCount, weekNo)
                        VALUES (%s, %s) RETURNING weekId
                        """,
                        (self.table_count, self.week_no)
                    )
                    self.week_id = cursor.fetchone()[0]  # Get the generated week ID
                else:
                    # Update existing week if week_id is set
                    cursor.execute(
                        """
                        UPDATE Week
                        SET tableCount = %s, weekNo = %s
                        WHERE weekId = %s
                        """,
                        (self.table_count, self.week_no, self.week_id)
                    )
            connection.commit()
        except Exception as e:
            connection.rollback()
            raise e

    def delete_from_db(self, connection):
        """
        Delete the Week instance from the database.

        :param connection: The active database connection.
        """
        try:
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM Week WHERE weekId = %s", (self.week_id,))
            connection.commit()
        except Exception as e:
            connection.rollback()
            raise e

    @classmethod
    def load_from_db(cls, connection, week_id):
        """
        Load a Week instance from the database.

        :param connection: The active database connection.
        :param week_id: The ID of the week to load.
        :return: A Week object if found, otherwise None.
        """
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT weekId, tableCount, weekNo FROM Week WHERE weekId = %s", (week_id,))
                row = cursor.fetchone()
                if row:
                    return cls(week_id=row[0], table_count=row[1], week_no=row[2])
                else:
                    return None
        except Exception as e:
            raise e
