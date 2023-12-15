def database_error_handler(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"Database error occurred: {e}")
            # Handle the database error, e.g., log to a file, send a notification, etc.
            return None
    return wrapper