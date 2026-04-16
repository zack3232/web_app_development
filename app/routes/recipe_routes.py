from flask import Blueprint

recipe_bp = Blueprint('recipe', __name__, url_prefix='/recipes')

@recipe_bp.route('/', methods=['GET'])
def list_recipes():
    """
    顯示食譜清單。
    輸入: Query params 'q'（選填）提供搜尋關鍵字。
    處理邏輯: 必須是登入狀態，根據 user_id 或 q 呼叫 Recipe.get_all。
    輸出: 渲染 recipe/list.html，並將清單資料傳遞進去
    """
    pass

@recipe_bp.route('/new', methods=['GET'])
def new_recipe():
    """
    顯示新增食譜表單。
    處理邏輯: 確認登入狀態。
    輸出: 渲染 recipe/form.html
    """
    pass

@recipe_bp.route('/', methods=['POST'])
def create_recipe():
    """
    接收表單並存入資料庫形成新食譜。
    輸入: title, description, ingredients 等表單資料。
    邏輯: User 必須登入（取得其 user_id），呼叫 Recipe.create() 新增紀錄。
    輸出: 成功後導向 /recipes
    """
    pass

@recipe_bp.route('/<int:recipe_id>', methods=['GET'])
def detail_recipe(recipe_id):
    """
    顯示某食譜的全貌內容。
    處理邏輯: 取出指定 ID，渲染頁面，並順便得知是否被當前用戶加入最愛。
    輸出: recipe/detail.html
    """
    pass

@recipe_bp.route('/<int:recipe_id>/edit', methods=['GET'])
def edit_recipe(recipe_id):
    """
    顯示編輯食譜表單，並載入既定資料。
    處理邏輯: 驗證當前欲修改的是否屬於登入者，成功後提供既有紀錄。
    輸出: recipe/form.html (帶入初始變數)
    """
    pass

@recipe_bp.route('/<int:recipe_id>/update', methods=['POST'])
def update_recipe(recipe_id):
    """
    接收編輯過的食譜內容並寫入資料表。
    輸入: 表單所有變更的欄位。
    邏輯: 確保操作者與擁有者一致，進行 Update。
    輸出: 重導向回 /recipes/<recipe_id>
    """
    pass

@recipe_bp.route('/<int:recipe_id>/delete', methods=['POST'])
def delete_recipe(recipe_id):
    """
    刪除食譜。
    邏輯: 權限檢查後呼叫 delete。刪除後即離開此畫面。
    輸出: 重導向回 /recipes
    """
    pass
