
#!/usr/bin/env python3
import time
import sqlite3
import functools

# Simple in-memory cache
query_cache = {}

def with_db_connection(func):
    """
    Decorator that opens a SQLite database connection,
    passes it to the decorated function, and ensures the connection is closed afterward.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            return func(conn, *args, **kwargs)
        finally:
            conn.close()
    return wrapper

def cache_query(func):
    """
    Decorator to cache the results of a SQL query based on the query string.
    Avoids redundant calls to the database for repeated queries.
    """
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        # Assume the query is passed either as the first argument or in kwargs
        query = args[0] if args else kwargs.get('query')
        if query in query_cache:
            print(f"[CACHE] Returning cached result for query: {query}")
            return query_cache[query]
        print(f"[CACHE] Executing and caching query: {query}")
        result = func(conn, *args, **kwargs)
        query_cache[query] = result
        return result
    return wrapper

@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    """
    Execute a SQL query and fetch all results.
    Results are cached to avoid repeated database access.
    """
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

# First call will cache the result
users = fetch_users_with_cache(query="SELECT * FROM users")
print(users)

# Second call will use the cached result
users_again = fetch_users_with_cache(query="SELECT * FROM users")
print(users_again)
