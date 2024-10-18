# db_connection.py
import os
import psycopg2
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Database:
    def __init__(self):
        self.connection = None
        try:
            # Fetch database credentials from environment variables
            dbname = os.getenv("DB_NAME")
            user = os.getenv("DB_USER")
            password = os.getenv("DB_PASSWORD")
            host = os.getenv("DB_HOST")
            port = os.getenv("DB_PORT")

            # Establish the connection
            self.connection = psycopg2.connect(
                dbname=dbname,
                user=user,
                password=password,
                host=host,
                port=port
            )
            print("Database connection successful.")
        except Exception as e:
            print(f"Error connecting to database: {e}")

    def close_connection(self):
        if self.connection:
            self.connection.close()
            print("Database connection closed.")

    def get_connection(self):
        return self.connection
