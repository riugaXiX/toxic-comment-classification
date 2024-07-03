import bcrypt
import db  # Assuming db.py contains get_db_connection

def register_user(username, password):
    conn = db.get_db_connection()
    cursor = conn.cursor()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_password))
        conn.commit()
    except db.mysql.connector.IntegrityError:
        return False, "Username already exists"
    finally:
        cursor.close()
        conn.close()
    return True, "Registration successful"

def login_user(username, password):
    conn = db.get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    if user and bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
        return True, user
    return False, "Invalid username or password"
