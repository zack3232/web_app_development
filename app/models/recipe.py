from .db import get_db_connection

class Recipe:
    @staticmethod
    def create(user_id, title, description, ingredients, instructions, category, tags, image_url):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                """INSERT INTO recipes (user_id, title, description, ingredients, instructions, category, tags, image_url) 
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                (user_id, title, description, ingredients, instructions, category, tags, image_url)
            )
            conn.commit()
            return cursor.lastrowid
        finally:
            conn.close()

    @staticmethod
    def get_all(search_query=None):
        conn = get_db_connection()
        cursor = conn.cursor()
        if search_query:
            wildcard = f"%{search_query}%"
            cursor.execute("""
                SELECT * FROM recipes 
                WHERE title LIKE ? OR tags LIKE ? 
                ORDER BY created_at DESC
            """, (wildcard, wildcard))
        else:
            cursor.execute("SELECT * FROM recipes ORDER BY created_at DESC")
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    @staticmethod
    def get_by_id(recipe_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM recipes WHERE id = ?", (recipe_id,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None
        
    @staticmethod
    def get_by_user(user_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM recipes WHERE user_id = ? ORDER BY created_at DESC", (user_id,))
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    @staticmethod
    def update(recipe_id, title, description, ingredients, instructions, category, tags, image_url):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                """UPDATE recipes SET 
                   title = ?, description = ?, ingredients = ?, instructions = ?, 
                   category = ?, tags = ?, image_url = ?, updated_at = CURRENT_TIMESTAMP
                   WHERE id = ?""",
                (title, description, ingredients, instructions, category, tags, image_url, recipe_id)
            )
            conn.commit()
            return cursor.rowcount > 0
        finally:
            conn.close()

    @staticmethod
    def delete(recipe_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM recipes WHERE id = ?", (recipe_id,))
            conn.commit()
            return cursor.rowcount > 0
        finally:
            conn.close()
