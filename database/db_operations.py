import sqlite3
from database.connection import get_db_connection

def register_user(username, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO Users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        success = True
    except sqlite3.IntegrityError:
        success = False
    conn.close()
    return success

def verify_user(username, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Users WHERE username=? AND password=?", (username, password))
    user = cursor.fetchone()
    conn.close()
    return user

def log_digitized_note(user_id, word_count, formula_density, has_diagrams, image_brightness, subject_tag, is_approved):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO DigitizedNotes 
        (user_id, word_count, formula_density, has_diagrams, image_brightness, subject_tag, is_approved)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (user_id, word_count, formula_density, has_diagrams, image_brightness, subject_tag, is_approved))
    conn.commit()
    conn.close()

def get_user_analytics(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT COUNT(note_id) as total_notes, 
               AVG(word_count) as avg_words,
               SUM(is_approved) as approved_count
        FROM DigitizedNotes WHERE user_id=?
    """, (user_id,))
    analytics = cursor.fetchone()
    conn.close()
    return analytics