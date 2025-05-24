#!/usr/bin/env python3
import sqlite3

class DatabaseConnection:
    """
    Custom class-based context manager for managing SQLite database connections.
    """
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None

    def __enter__(self):
        """
        Open the database connection and return the connection object.
        """
        self.conn = sqlite3.connect(self.db_name)
        return self.conn

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Ensure the connection is closed. Rollback if there was an exception.
        """
        if self.conn:
            if exc_type is not None:
                self.conn.rollback()
                print(f"[ERROR] Exception occurred: {exc_value}. Rolling back.")
            else:
                self.conn.commit()
            self.conn.close()
            print("[INFO] Database connection closed.")

# Using the context manager to perform a query
if __name__ == "__main__":
    with DatabaseConnection('users.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        results = cursor.fetchall()
        for row in results:
            print(row)
