# database.py
import sqlite3

def init_db():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()

    # Check if the tables exist and drop them
    c.execute('DROP TABLE IF EXISTS meals')
    c.execute('DROP TABLE IF EXISTS workouts')

    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT,
            email TEXT,
            name TEXT
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS meals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            date TEXT,
            type TEXT,
            meal TEXT,
            calories REAL,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS workouts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            date TEXT,
            workout TEXT,
            duration INTEGER,
            calories_burned REAL,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS weights (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            date TEXT,
            weight REAL,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS bmi (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            date TEXT,
            bmi REAL,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    ''')

    conn.commit()
    conn.close()

def register_user(username, password, email, name):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO users (username, password, email, name)
        VALUES (?, ?, ?, ?)
    ''', (username, password, email, name))
    conn.commit()
    conn.close()

def get_user(username):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('''
        SELECT * FROM users WHERE username = ?
    ''', (username,))
    user = c.fetchone()
    conn.close()
    return user

def add_meal(user_id, date, meal_type, meal, calories):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO meals (user_id, date, type, meal, calories)
        VALUES (?, ?, ?, ?, ?)
    ''', (user_id, date, meal_type, meal, calories))
    conn.commit()
    conn.close()

def get_meals(user_id, date):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('''
        SELECT date, type, meal, calories FROM meals WHERE user_id = ? AND date = ?
    ''', (user_id, date))
    meals = c.fetchall()
    conn.close()
    return meals

def add_workout(user_id, date, workout, duration, calories_burned):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO workouts (user_id, date, workout, duration, calories_burned)
        VALUES (?, ?, ?, ?, ?)
    ''', (user_id, date, workout, duration, calories_burned))
    conn.commit()
    conn.close()

def get_workouts(user_id, date):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('''
        SELECT date, workout, duration, calories_burned FROM workouts WHERE user_id = ? AND date = ?
    ''', (user_id, date))
    workouts = c.fetchall()
    conn.close()
    return workouts

def add_weight(user_id, date, weight):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO weights (user_id, date, weight)
        VALUES (?, ?, ?)
    ''', (user_id, date, weight))
    conn.commit()
    conn.close()

def add_bmi(user_id, date, bmi):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO bmi (user_id, date, bmi)
        VALUES (?, ?, ?)
    ''', (user_id, date, bmi))
    conn.commit()
    conn.close()

def get_weights(user_id):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('''
        SELECT date, weight FROM weights WHERE user_id = ?
    ''', (user_id,))
    weights = c.fetchall()
    conn.close()
    return weights

def get_bmi(user_id):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('''
        SELECT date, bmi FROM bmi WHERE user_id = ?
    ''', (user_id,))
    bmis = c.fetchall()
    conn.close()
    return bmis

def get_all_users():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('SELECT * FROM users')
    users = c.fetchall()
    conn.close()
    return users

def get_all_meals():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('SELECT * FROM meals')
    meals = c.fetchall()
    conn.close()
    return meals

def get_all_weights():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('SELECT * FROM weights')
    weights = c.fetchall()
    conn.close()
    return weights

def get_all_bmi():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('SELECT * FROM bmi')
    bmis = c.fetchall()
    conn.close()
    return bmis
