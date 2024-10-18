class Player:
    def __init__(self, player_id=None, first_name='', last_name='', membership_status='Active', times_played=0, points=0, total_spent=0.00):
        """
        Initialize a Player object with optional parameters.

        :param player_id: The unique identifier for the player (Primary Key).
        :param first_name: The first name of the player.
        :param last_name: The last name of the player.
        :param membership_status: The membership status of the player (default is 'Active').
        :param times_played: The number of times the player has played.
        :param points: The total points accumulated by the player.
        :param total_spent: The total amount spent by the player.
        """
        self.player_id = player_id
        self.first_name = first_name
        self.last_name = last_name
        self.membership_status = membership_status
        self.times_played = times_played
        self.points = points
        self.total_spent = total_spent

    def save_to_db(self, connection):
        """
        Save the Player instance to the database.

        :param connection: The active database connection.
        """
        try:
            with connection.cursor() as cursor:
                if self.player_id is None:
                    # Insert new player if player_id is not set
                    cursor.execute(
                        """
                        INSERT INTO Player (firstName, lastName, membershipStatus, timesPlayed, points, totalSpent)
                        VALUES (%s, %s, %s, %s, %s, %s) RETURNING playerId
                        """,
                        (self.first_name, self.last_name, self.membership_status, self.times_played, self.points, self.total_spent)
                    )
                    self.player_id = cursor.fetchone()[0]  # Get the generated player ID
                else:
                    # Update existing player if player_id is set
                    cursor.execute(
                        """
                        UPDATE Player
                        SET firstName = %s, lastName = %s, membershipStatus = %s, timesPlayed = %s, points = %s, totalSpent = %s
                        WHERE playerId = %s
                        """,
                        (self.first_name, self.last_name, self.membership_status, self.times_played, self.points, self.total_spent, self.player_id)
                    )
            connection.commit()
        except Exception as e:
            connection.rollback()
            raise e

    def delete_from_db(self, connection):
        """
        Delete the Player instance from the database.

        :param connection: The active database connection.
        """
        try:
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM Player WHERE playerId = %s", (self.player_id,))
            connection.commit()
        except Exception as e:
            connection.rollback()
            raise e

    @classmethod
    def load_from_db(cls, connection, player_id):
        """
        Load a Player instance from the database.

        :param connection: The active database connection.
        :param player_id: The ID of the player to load.
        :return: A Player object if found, otherwise None.
        """
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT playerId, firstName, lastName, membershipStatus, timesPlayed, points, totalSpent FROM Player WHERE playerId = %s", (player_id,))
                row = cursor.fetchone()
                if row:
                    return cls(player_id=row[0], first_name=row[1], last_name=row[2], membership_status=row[3], times_played=row[4], points=row[5], total_spent=row[6])
                else:
                    return None
        except Exception as e:
            raise e
