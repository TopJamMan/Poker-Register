class PlayerTable:
    def __init__(self, player_id, table_id, placement=None, seat=None, total_buy_in=0.00):
        """
        Initialize a PlayerTable object with required parameters.

        :param player_id: The player's ID (Primary Key, Foreign Key).
        :param table_id: The table's ID (Primary Key, Foreign Key).
        :param placement: The player's placement in the table.
        :param seat: The seat number occupied by the player.
        :param total_buy_in: The total buy-in amount for the player at this table.
        """
        self.player_id = player_id
        self.table_id = table_id
        self.placement = placement
        self.seat = seat
        self.total_buy_in = total_buy_in

    def save_to_db(self, connection):
        """
        Save the PlayerTable instance to the database.

        :param connection: The active database connection.
        """
        try:
            with connection.cursor() as cursor:
                # Insert or update record based on player_id and table_id
                cursor.execute(
                    """
                    INSERT INTO PlayerTable (playerId, tableId, placement, seat, totalBuyIn)
                    VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT (playerId, tableId) DO UPDATE
                    SET placement = EXCLUDED.placement, seat = EXCLUDED.seat, totalBuyIn = EXCLUDED.totalBuyIn
                    """,
                    (self.player_id, self.table_id, self.placement, self.seat, self.total_buy_in)
                )
            connection.commit()
        except Exception as e:
            connection.rollback()
            raise e

    def delete_from_db(self, connection):
        """
        Delete the PlayerTable instance from the database.

        :param connection: The active database connection.
        """
        try:
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM PlayerTable WHERE playerId = %s AND tableId = %s", (self.player_id, self.table_id))
            connection.commit()
        except Exception as e:
            connection.rollback()
            raise e

    @classmethod
    def load_from_db(cls, connection, player_id, table_id):
        """
        Load a PlayerTable instance from the database.

        :param connection: The active database connection.
        :param player_id: The ID of the player.
        :param table_id: The ID of the table.
        :return: A PlayerTable object if found, otherwise None.
        """
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT playerId, tableId, placement, seat, totalBuyIn
                    FROM PlayerTable
                    WHERE playerId = %s AND tableId = %s
                    """,
                    (player_id, table_id)
                )
                row = cursor.fetchone()
                if row:
                    return cls(player_id=row[0], table_id=row[1], placement=row[2], seat=row[3], total_buy_in=row[4])
                else:
                    return None
        except Exception as e:
            raise e
