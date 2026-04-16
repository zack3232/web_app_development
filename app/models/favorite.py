from .db import get_db_connection

class Favorite:
    @staticmethod
    def toggle(user_id, recipe_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            # 檢查是否已經在最愛中
            cursor.execute("SELECT id FROM favorites WHERE user_id = ? AND recipe_id = ?", (user_id, recipe_id))
            row = cursor.fetchone()
            if row:
                # 若已存在則移除
                cursor.execute("DELETE FROM favorites WHERE id = ?", (row['id'],))
                action = 'removed'
            else:
                # 否則新增至最愛
                cursor.execute("INSERT INTO favorites (user_id, recipe_id) VALUES (?, ?)", (user_id, recipe_id))
                action = 'added'
            conn.commit()
            return action
        finally:
            conn.close()

    @staticmethod
    def get_user_favorites(user_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        # 關聯查詢：抓取使用者最愛的食譜詳細資料
        cursor.execute("""
            SELECT r.* FROM recipes r
            JOIN favorites f ON r.id = f.recipe_id
            WHERE f.user_id = ?
            ORDER BY f.created_at DESC
        """, (user_id,))
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]
        
    @staticmethod
    def is_favorited(user_id, recipe_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM favorites WHERE user_id = ? AND recipe_id = ?", (user_id, recipe_id))
        row = cursor.fetchone()
        conn.close()
        return bool(row)
