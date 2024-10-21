import csv
import os

from sympy import false


class Player:
    def __init__(self, first_name='', last_name='', student_no=None,points=0, total_won=0, total_spent=0, membership_status = False):
        self.first_name = first_name
        self.last_name = last_name
        self.student_no = student_no
        self.membership_status = membership_status
        self.total_won = total_won
        self.total_spent = total_spent
        self.points = points

    def check_membership_status(self):
        """Check the player's membership status against members.csv."""
        csv_file_path = os.path.join("src/resources", "members.csv")

        try:
            with open(csv_file_path, mode="r") as file:
                csv_reader = csv.reader(file)
                for row in csv_reader:
                    if self.student_no == row[-1].strip():
                        self.membership_status = True
                        break
        except FileNotFoundError:
            raise Exception("The members.csv file was not found.")
        except Exception as e:
            raise e

    def save_to_db(self, connection):
        """Save the player's information to the database."""
        self.check_membership_status()

        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO player (firstName, lastName, membershipStatus, timesPlayed, studentNumber, totalWon, totalSpent, points)
                    VALUES (%s, %s, %s, 1, %s, %s, %s,%s)  -- Start timesPlayed at 1 for a new member
                    ON CONFLICT (studentNumber)  -- Specify the column to check for conflicts
                    DO UPDATE SET 
                        timesPlayed = player.timesPlayed + 1  -- Increment timesPlayed only
                    """,
                    (self.first_name, self.last_name, self.membership_status, self.student_no, self.total_won,
                     self.total_spent, self.points)
                )
            # Commit the transaction
            connection.commit()
        except Exception as e:
            connection.rollback()  # Roll back the transaction in case of an error
            raise e

    def increment_total_spent(self, connection, amount):
        """Increment the player's total spent amount in the database."""
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE player
                    SET totalSpent = COALESCE(totalSpent, 0) + %s
                    WHERE studentNumber = %s
                    """,
                    (amount, self.student_no)  # Ensure both are integers or correct types
                )
            connection.commit()  # Commit the transaction
        except Exception as e:
            connection.rollback()  # Roll back the transaction in case of an error
            raise e

    def edit_member(self, connection, old_student_no):
        """Update the player's details in the database."""
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE player
                    SET studentnumber = %s,
                        firstName = %s,
                        lastName = %s,
                        points = %s,
                        totalWon = %s,
                        totalSpent = %s,
                        membershipStatus = %s
                    WHERE studentnumber = %s
                    """,
                    (
                        self.student_no,
                        self.first_name,
                        self.last_name,
                        self.points,
                        self.total_won,
                        self.total_spent,
                        self.membership_status,
                        old_student_no
                    )  # Ensure that the types of these fields match the database columns
                )
            connection.commit()  # Commit the transaction
        except Exception as e:
            connection.rollback()  # Roll back the transaction in case of an error
            raise e

    def delete_member(self, connection):
        """Delete the player from the database."""
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    DELETE FROM player
                    WHERE studentNumber = %s
                    """,
                    (self.student_no,)  # Use the player's student_no to identify the record
                )
            connection.commit()  # Commit the transaction
        except Exception as e:
            connection.rollback()  # Roll back the transaction in case of an error
            raise e

    @staticmethod
    def get_league_standing(connection):
        """Retrieve league standings for players."""
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT firstName, lastName, points, timesPlayed, totalWon, totalSpent
                    FROM player
                    WHERE membershipStatus = TRUE and totalSpent > 0
                    ORDER BY points DESC
                    """
                )

                standings = cursor.fetchall()  # Fetch all the results
                connection.commit()  # Commit the transaction
                return standings  # Return the fetched standings
        except Exception as e:
            connection.rollback()  # Roll back the transaction in case of an error
            raise e  # Optionally log the error or handle it as needed

    @staticmethod
    def get_all_members(connection):
        """Retrieve league standings for players."""
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT studentnumber, firstName, lastName, points, timesPlayed, totalWon, totalSpent, membershipstatus
                    FROM player
                    ORDER BY lastName DESC
                    """
                )

                standings = cursor.fetchall()  # Fetch all the results
                connection.commit()  # Commit the transaction
                return standings  # Return the fetched standings
        except Exception as e:
            connection.rollback()  # Roll back the transaction in case of an error
            raise e  # Optionally log the error or handle it as needed

    @staticmethod
    def get_player_info(connection, student_number):
        """Fetch player info for the specified student number and return a Player instance."""
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT firstname, lastname, studentNumber, points, totalWon, totalSpent, membershipStatus 
                    FROM Player 
                    WHERE studentNumber = %s
                """, (student_number,))
                result = cursor.fetchone()
                if result:
                    # Create a Player instance with the fetched data
                    player = Player(
                        first_name=result[0],
                        last_name=result[1],
                        student_no=result[2],
                        points=result[3],
                        total_won=result[4],
                        total_spent=result[5],
                        membership_status=result[6]
                    )
                    return player
                else:
                    print(f"No player found with student number: {student_number}")
                    return None
        except Exception as e:
            print(f"Error fetching player info: {e}")
            return None