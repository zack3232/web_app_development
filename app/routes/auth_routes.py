from flask import Blueprint

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    處理註冊頁面顯示與表單送出。
    輸入: POST 此路由時會夾帶表單上的 username, email, password
    處理邏輯:
      - GET: 顯示註冊表單
      - POST: 檢查欄位，判斷 email 是否已存在。沒有則 hash password 並呼叫 Model 建立 User。
    輸出: GET -> auth/register.html, POST 成功 -> 重導向 /auth/login
    """
    pass

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    處理登入頁面顯示與表單送出。
    輸入: POST 帶有 email 與 password
    處理邏輯: 
      - 比對密碼是否正確，如果正確將 User 的 ID 寫入 session 記錄登入狀態。
      - 密碼錯誤則給予 flash message 提示。
    輸出: GET -> auth/login.html, POST 成功 -> 重導向 /recipes
    """
    pass

@auth_bp.route('/logout', methods=['GET'])
def logout():
    """
    處理登出邏輯。
    處理邏輯: 自 session 清除登入的記錄 (user_id) 
    輸出: 重導向至首頁 '/'
    """
    pass
