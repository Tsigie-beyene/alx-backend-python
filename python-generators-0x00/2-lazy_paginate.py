seed = __import__('seed')


def paginate_users(page_size, offset):
    """
    Fetch a single page of users from the database using LIMIT and OFFSET.
    """
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}")
    rows = cursor.fetchall()
    cursor.close()
    connection.close()
    return rows


def lazy_pagination(page_size):
    """
    Generator that lazily yields pages of users from the database.
    Uses a single loop to yield page-by-page.
    """
    offset = 0
    while True:  # 1 loop only
        page = paginate_users(page_size, offset)
        if not page:
            break
        yield page
        offset += page_size
