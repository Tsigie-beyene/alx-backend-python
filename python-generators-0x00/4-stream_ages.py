import seed


def stream_user_ages():
    """
    Generator that yields user ages one at a time from the database.
    """
    connection = seed.connect_to_prodev()
    cursor = connection.cursor()
    cursor.execute("SELECT age FROM user_data")
    for row in cursor:
        yield row[0]  # row is a tuple (age,)
    cursor.close()
    connection.close()


def calculate_average_age():
    """
    Calculates and prints the average age using the stream_user_ages generator.
    """
    total_age = 0
    count = 0
    for age in stream_user_ages():  # Loop 1
        total_age += age
        count += 1

    if count > 0:
        average_age = total_age / count
        print(f"Average age of users: {average_age:.2f}")
    else:
        print("No users found.")


if __name__ == "__main__":
    calculate_average_age()
