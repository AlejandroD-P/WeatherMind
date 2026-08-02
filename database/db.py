import sqlite3

DATABASE_NAME = "weathermind.db"


def get_connection():
    return sqlite3.connect(DATABASE_NAME)


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