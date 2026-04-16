from .db import get_db_connection

class User:
    def __init__(self, id, username, email, password_hash, created_at):
        self.id = id
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.created_at = created_at

    @staticmethod
    def create(username, email, password_hash):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",
                (username, email, password_hash)
            )
            conn.commit()
            return cursor.lastrowid
        finally:
            conn.close()

    @staticmethod
    def get_by_id(user_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return User(row['id'], row['username'], row['email'], row['password_hash'], row['created_at'])
        return None

    @staticmethod
    def get_by_email(email):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return User(row['id'], row['username'], row['email'], row['password_hash'], row['created_at'])
        return None
