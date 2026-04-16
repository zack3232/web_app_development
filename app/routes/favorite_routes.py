from flask import Blueprint

favorite_bp = Blueprint('favorite', __name__)

@favorite_bp.route('/favorites', methods=['GET'])
def list_favorites():
    """
    顯示所有已被目前用戶加入最愛的食譜。
    處理邏輯: 確認登入與 Session 資訊，呼叫 models/favorite 取得關聯結果。
    輸出: 渲染 favorite/list.html
    """
    pass

@favorite_bp.route('/recipes/<int:recipe_id>/favorite', methods=['POST'])
def toggle_favorite(recipe_id):
    """
    加入或移除最愛切換功能。
    輸入: 目標的 recipe_id 參數。
    邏輯: 呼叫 Favorite.toggle 來進行加入與刪除判定。
    輸出: 回到請求發送前的來源頁面，或 /recipes/<recipe_id>
    """
    pass
