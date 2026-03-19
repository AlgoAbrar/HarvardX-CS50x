from flask import redirect, session
from functools import wraps
import sqlite3

def login_required(f):
    """
    Decorate routes to require login.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def get_db():
    """
    Get a database connection.
    """
    conn = sqlite3.connect("habits.db")
    conn.row_factory = dict_factory
    return conn

def dict_factory(cursor, row):
    """
    Convert database row objects to dictionaries.
    This makes them mutable (can be modified).
    """
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def init_db():
    """
    Initialize the database with required tables.
    """
    db = get_db()

    # Create users table
    db.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            hash TEXT NOT NULL
        )
    """)

    # Create habits table
    db.execute("""
        CREATE TABLE IF NOT EXISTS habits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            color TEXT DEFAULT '#4CAF50',
            frequency TEXT DEFAULT 'daily',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
        )
    """)

    # Create completions table
    db.execute("""
        CREATE TABLE IF NOT EXISTS completions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            habit_id INTEGER NOT NULL,
            date DATE NOT NULL,
            completed BOOLEAN DEFAULT 0,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (habit_id) REFERENCES habits (id) ON DELETE CASCADE,
            UNIQUE(habit_id, date)
        )
    """)

    # Create indexes for better performance
    db.execute("CREATE INDEX IF NOT EXISTS idx_completions_habit_date ON completions(habit_id, date)")
    db.execute("CREATE INDEX IF NOT EXISTS idx_habits_user ON habits(user_id)")

    db.commit()
    print("Database initialized successfully!")

def validate_date(date_string):
    """
    Validate if a string is a valid date in YYYY-MM-DD format.
    """
    try:
        from datetime import datetime
        datetime.strptime(date_string, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def format_date(date_string, format="%b %d, %Y"):
    """
    Format a date string.
    """
    from datetime import datetime
    date_obj = datetime.strptime(date_string, "%Y-%m-%d")
    return date_obj.strftime(format)
