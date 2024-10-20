import csv
import os

class Player:
    def __init__(self, first_name='', last_name='', student_no=None,points=0, total_won=0, total_spent=0):
        self.first_name = first_name
        self.last_name = last_name
        self.student_no = student_no
        self.membership_status = False
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
                    SELECT studentnumber, firstName, lastName, points, timesPlayed, totalWon, totalSpent
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
