import sqlite3
import os

def init_database():
    db_path = "database/database.db"
    if not os.path.exists(db_path):
        # Create database and tables if it doesnt exist
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Table for users
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                email TEXT NOT NULL UNIQUE,
                phone TEXT,
                password TEXT NOT NULL,
                profile_pic BLOB,
                dietary_preferences TEXT,
                allergies TEXT
            )
        """)

        # Table for food items
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS food_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                name TEXT NOT NULL,
                quantity REAL NOT NULL,
                expiration_date TEXT NOT NULL,
                category TEXT,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)

        # Table for recipes
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS recipes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                ingredients TEXT NOT NULL,
                instructions TEXT NOT NULL,
                category TEXT,
                user_id INTEGER,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)

        # Table for community posts
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS community_posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                content TEXT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)
    
        conn.commit()
        conn.close()
