import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'academic_digitize.db')

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def initialize_database():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS DigitizedNotes (
        note_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        word_count REAL,
        formula_density REAL,
        has_diagrams REAL,
        image_brightness REAL,
        subject_tag INTEGER,
        is_approved INTEGER,
        uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(user_id) REFERENCES Users(id)
    )
    ''')
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    initialize_database()
    print("Database metrics tables successfully initialized.")