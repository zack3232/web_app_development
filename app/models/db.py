import sqlite3
import os

# 自動推導 instance 資料夾與資料庫絕對路徑
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'instance', 'database.db')

def get_db_connection():
    # 確保資料夾存在
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    # 將回傳結果轉為類似 dict 的形式，方便用 Key 存取
    conn.row_factory = sqlite3.Row
    # 開啟 Foreign Key 支援
    conn.execute('PRAGMA foreign_keys = ON;')
    return conn

def init_db():
    """初始化資料庫與資料表"""
    schema_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'database', 'schema.sql')
    if os.path.exists(schema_path):
        with open(schema_path, 'r', encoding='utf-8') as f:
            script = f.read()
        conn = get_db_connection()
        try:
            conn.executescript(script)
            conn.commit()
        finally:
            conn.close()
