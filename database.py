import sqlite3

def create_connection():
    conn = sqlite3.connect('user_data.db')
    return conn

def create_table():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            name TEXT,
            email TEXT,
            gewicht REAL,
            groesse REAL,
            geschlecht TEXT,
            alter INTEGER,
            aktivitaetslevel TEXT,
            bmi REAL,
            kalorienbedarf REAL
        )
    ''')
    conn.commit()
    conn.close()

def insert_user(username, name, email):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO users (username, name, email)
        VALUES (?, ?, ?)
    ''', (username, name, email))
    conn.commit()
    conn.close()

def update_user_data(username, gewicht, groesse, geschlecht, alter, aktivitaetslevel, bmi, kalorienbedarf):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE users
        SET gewicht = ?, groesse = ?, geschlecht = ?, alter = ?, aktivitaetslevel = ?, bmi = ?, kalorienbedarf = ?
        WHERE username = ?
    ''', (gewicht, groesse, geschlecht, alter, aktivitaetslevel, bmi, kalorienbedarf, username))
    conn.commit()
    conn.close()

def get_user_data(username):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM users WHERE username = ?
    ''', (username,))
    user_data = cursor.fetchone()
    conn.close()
    return user_data
