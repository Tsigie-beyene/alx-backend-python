# Python Generators - Streaming SQL Data

## Objective

This project demonstrates how to use Python generators to efficiently stream data from a SQL database one row at a time. It includes a script that sets up a MySQL database and populates it with user data from a CSV file. This is foundational work for building memory-efficient data pipelines using Python.

## Files

- `seed.py`: Sets up the database `ALX_prodev`, creates the `user_data` table if it doesn't exist, and populates it with data from a CSV file (`user_data.csv`).
- `0-main.py`: Driver script used to execute and verify the functionality of `seed.py`.
- `user_data.csv`: Sample data file containing user information (UUID, name, email, age).

## Features

- Connects to MySQL server.
- Creates a database `ALX_prodev` if it doesn't exist.
- Creates a `user_data` table with appropriate schema and indexing.
- Reads and inserts data from `user_data.csv` into the table.
- Skips inserting duplicate records based on `user_id`.

## Table Schema

```sql
CREATE TABLE user_data (
    user_id CHAR(36) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    age DECIMAL NOT NULL,
    INDEX (user_id)
);
