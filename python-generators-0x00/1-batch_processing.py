import mysql.connector
from mysql.connector import Error


def stream_users_in_batches(batch_size):
    """
    Generator function that yields batches of user_data rows from the database.
    """
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='your_mysql_password',  # Replace this with your actual password
            database='ALX_prodev'
        )

        if connection.is_connected():
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT COUNT(*) AS total FROM user_data")
            total_rows = cursor.fetchone()['total']

            offset = 0
            while offset < total_rows:
                cursor.execute(
                    "SELECT user_id, name, email, age FROM user_data LIMIT %s OFFSET %s",
                    (batch_size, offset)
                )
                rows = cursor.fetchall()
                if not rows:
                    return  # Use of 'return' to stop early if something goes wrong
                yield rows
                offset += batch_size

    except Error as e:
        print(f"Error: {e}")
        return  # Return early in case of a DB error
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


def batch_processing(batch_size):
    """
    Generator function that yields users over age 25 from streamed batches.
    """
    for batch in stream_users_in_batches(batch_size):  # 1 loop
        for user in batch:  # 2nd loop
            if user['age'] > 25:
                yield user  # yield matching user
