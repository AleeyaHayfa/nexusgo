import sqlite3
import hashlib
import datetime

DATABASE_PATH = "database/database.db"

#Initialize Database

def init_database():
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
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

# User operations

def get_hashed_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def create_user(username, email, phone, password, profile_pic=None, dietary_preferences=None, allergies=None):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    hashed_password = get_hashed_password(password)
    try:
       cursor.execute("INSERT INTO users (username, email, phone, password, profile_pic, dietary_preferences, allergies) VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (username, email, phone, hashed_password, profile_pic, dietary_preferences, allergies))
       conn.commit()
       conn.close()
       return True
    except sqlite3.IntegrityError:
        conn.close()
        return False

def get_user_by_username(username):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()
    return user

def get_user_by_email(email):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
    user = cursor.fetchone()
    conn.close()
    return user


def verify_password(password, hashed_password):
    return get_hashed_password(password) == hashed_password

def update_user(user_id, username=None, email=None, phone=None, profile_pic=None, dietary_preferences=None, allergies=None):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    update_fields = {}
    if username:
        update_fields['username'] = username
    if email:
        update_fields['email'] = email
    if phone:
        update_fields['phone'] = phone
    if profile_pic:
        update_fields['profile_pic'] = profile_pic
    if dietary_preferences:
        update_fields['dietary_preferences'] = dietary_preferences
    if allergies:
        update_fields['allergies'] = allergies

    
    set_clause = ', '.join([f"{key} = ?" for key in update_fields])
    values = list(update_fields.values())
    
    sql = f"UPDATE users SET {set_clause} WHERE id = ?"
    
    cursor.execute(sql,values + [user_id])
    conn.commit()
    conn.close()
    return True

def get_user_by_id(user_id):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    return user

def get_all_users():
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, email, phone FROM users")
    users = cursor.fetchall()
    conn.close()
    return users

def delete_user(user_id):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()
    return True

# food_items operations

def add_food_item(user_id, name, quantity, expiration_date, category):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO food_items (user_id, name, quantity, expiration_date, category) VALUES (?, ?, ?, ?, ?)",
                  (user_id, name, quantity, expiration_date, category))
    conn.commit()
    conn.close()
    return True

def get_food_items(user_id):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM food_items WHERE user_id = ?", (user_id,))
    items = cursor.fetchall()
    conn.close()
    return items

def get_all_food_items():
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM food_items")
    items = cursor.fetchall()
    conn.close()
    return items

def update_food_item(item_id, name=None, quantity=None, expiration_date=None, category=None):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    update_fields = {}
    if name:
        update_fields['name'] = name
    if quantity:
        update_fields['quantity'] = quantity
    if expiration_date:
        update_fields['expiration_date'] = expiration_date
    if category:
        update_fields['category'] = category
    set_clause = ', '.join([f"{key} = ?" for key in update_fields])
    values = list(update_fields.values())
    sql = f"UPDATE food_items SET {set_clause} WHERE id = ?"
    cursor.execute(sql,values + [item_id])
    conn.commit()
    conn.close()
    return True


def delete_food_item(item_id):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM food_items WHERE id = ?", (item_id,))
    conn.commit()
    conn.close()
    return True

# Recipe operations

def add_recipe(user_id, name, ingredients, instructions, category):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO recipes (user_id, name, ingredients, instructions, category) VALUES (?, ?, ?, ?, ?)",
                  (user_id, name, ingredients, instructions, category))
    conn.commit()
    conn.close()
    return True

def get_recipes(user_id):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM recipes WHERE user_id = ?", (user_id,))
    recipes = cursor.fetchall()
    conn.close()
    return recipes

def get_all_recipes():
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM recipes")
    recipes = cursor.fetchall()
    conn.close()
    return recipes

def update_recipe(recipe_id, name=None, ingredients=None, instructions=None, category=None):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    update_fields = {}
    if name:
        update_fields['name'] = name
    if ingredients:
        update_fields['ingredients'] = ingredients
    if instructions:
        update_fields['instructions'] = instructions
    if category:
        update_fields['category'] = category
    
    set_clause = ', '.join([f"{key} = ?" for key in update_fields])
    values = list(update_fields.values())
    sql = f"UPDATE recipes SET {set_clause} WHERE id = ?"
    cursor.execute(sql,values + [recipe_id])
    conn.commit()
    conn.close()
    return True
    

def delete_recipe(recipe_id):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM recipes WHERE id = ?", (recipe_id,))
    conn.commit()
    conn.close()
    return True

# Community Post operations
def add_post(user_id, content):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO community_posts (user_id, content) VALUES (?, ?)", (user_id, content))
    conn.commit()
    conn.close()
    return True

def get_posts():
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT community_posts.id, content, created_at, username  FROM community_posts JOIN users ON community_posts.user_id = users.id ORDER BY created_at DESC")
    posts = cursor.fetchall()
    conn.close()
    return posts

def delete_post(post_id):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM community_posts WHERE id = ?", (post_id,))
    conn.commit()
    conn.close()
    return True
