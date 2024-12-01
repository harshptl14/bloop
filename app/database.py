import sqlite3
from datetime import datetime
from config import DB_PATH


def initialize_database():
    """Initializes the database and creates all required tables."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create app usage table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS app_usage (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            app_name TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            duration REAL DEFAULT 0
        )
    """)
    
    # Create workspaces table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS workspaces (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            apps TEXT NOT NULL
        )
    """)
    
    conn.commit()
    conn.close()


def add_record(app_name, timestamp=None):
    """Add a record to the database."""
    if timestamp is None:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    conn = None
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO app_usage (app_name, timestamp) VALUES (?, ?)", 
            (app_name, timestamp)
        )
        conn.commit()
    except sqlite3.Error as e:
        if conn:
            conn.rollback()
        raise e
    finally:
        if conn:
            conn.close()


def fetch_records(query, params=()):
    """Fetch records from the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(query, params)
    records = cursor.fetchall()
    conn.close()
    return records
