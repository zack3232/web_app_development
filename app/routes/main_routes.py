from flask import Blueprint

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """
    處理首頁請求。
    輸入: 無
    處理邏輯: 判斷是否為登入狀態，若有 user_id 則可在畫面上引導至個人收藏清單。
    輸出: 渲染 templates/main/index.html
    """
    pass
