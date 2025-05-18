
#!/usr/bin/python3
import mysql.connector
from mysql.connector import Error
import csv
import uuid

DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = ""  # Replace with your password if any
DB_NAME = "ALX_prodev"


def connect_db():
    """Connect to the MySQL server (no specific DB)"""
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
    return None


def create_database(connection):
    """Create the ALX_prodev database if it doesn't exist"""
    try:
        cursor = connection.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME};")
        connection.commit()
        print(f"Database {DB_NAME} created successfully or already exists.")
    except Error as e:
        print(f"Error creating database: {e}")
    finally:
        cursor.close()


def connect_to_prodev():
    """Connect to the ALX_prodev database"""
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error connecting to {DB_NAME} database: {e}")
    return None


def create_table(connection):
    """Create the user_data table if it doesn't exist"""
    try:
        cursor = connection.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS user_data (
            user_id CHAR(36) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            age DECIMAL NOT NULL,
            INDEX (user_id)
        );
        """
        cursor.execute(create_table_query)
        connection.commit()
        print("Table user_data created successfully")
    except Error as e:
        print(f"Error creating table: {e}")
    finally:
        cursor.close()


def insert_data(connection, csv_file):
    """Insert data from a CSV file into the user_data table"""
    try:
        cursor = connection.cursor()

        # Read CSV data
        with open(csv_file, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                user_id = row['user_id']
                name = row['name']
                email = row['email']
                age = row['age']

                # Check if record already exists
                cursor.execute("SELECT user_id FROM user_data WHERE user_id = %s", (user_id,))
                if cursor.fetchone():
                    continue

                # Insert new record
                cursor.execute("""
                    INSERT INTO user_data (user_id, name, email, age)
                    VALUES (%s, %s, %s, %s);
                """, (user_id, name, email, age))

        connection.commit()
        print("Data inserted successfully")
    except Error as e:
        print(f"Error inserting data: {e}")
    except FileNotFoundError:
        print(f"CSV file '{csv_file}' not found.")
    finally:
        cursor.close()
