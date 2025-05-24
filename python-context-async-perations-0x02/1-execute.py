
#!/usr/bin/env python3
import sqlite3

class ExecuteQuery:
    """
    Context manager that handles connecting to the database, executing a parameterized query,
    fetching results, and closing the connection.
    """
    def __init__(self, db_name, query, params=()):
        self.db_name = db_name
        self.query = query
        self.params = params
        self.conn = None
        self.cursor = None
        self.results = None

    def __enter__(self):
        """
        Establish the connection, execute the query, and fetch results.
        """
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self.cursor.execute(self.query, self.params)
        self.results = self.cursor.fetchall()
        return self.results

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Commit if no error, rollback if an exception occurred, and close connection.
        """
        if self.conn:
            if exc_type is not None:
                self.conn.rollback()
                print(f"[ERROR] Exception occurred: {exc_value}. Rolling back.")
            else:
                self.conn.commit()
            self.conn.close()
            print("[INFO] Connection closed.")

# Usage of ExecuteQuery context manager
if __name__ == "__main__":
    query = "SELECT * FROM users WHERE age > ?"
    params = (25,)
    with ExecuteQuery("users.db", query, params) as results:
        for row in results:
            print(row)
