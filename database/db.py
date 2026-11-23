import os
import sys
import sqlite3

if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DB_PATH = os.path.join(BASE_DIR, "weathermind.db")
DATABASE_NAME = DB_PATH


def get_connection():
    return sqlite3.connect(DB_PATH)


def initialize_database():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS history(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        city TEXT,
        activity TEXT,
        temperature REAL,
        humidity REAL,
        wind REAL,
        uv REAL,
        precipitation REAL,
        risk TEXT,
        recommendation TEXT
    )
    """)

    conn.commit()
    conn.close()