
import mysql.connector
from mysql.connector import Error

def stream_users():
    """
    Generator function to stream user_data rows one by one from the ALX_prodev database.
    Yields:
        dict: A dictionary with user_id, name, email, and age.
    """
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='your_mysql_password',
            database='ALX_prodev'
        )

        if connection.is_connected():
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT user_id, name, email, age FROM user_data")

            for row in cursor:
                yield row

    except Error as e:
        print(f"Database error: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
