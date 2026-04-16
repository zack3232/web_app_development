# 路由設計 - 食譜收藏夾系統

## 1. 路由總覽表格

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
|---|---|---|---|---|
| 網站首頁 | GET | `/` | `templates/main/index.html` | 呈現網站介紹，引導未登入者註冊 |
| 註冊頁面 | GET | `/auth/register` | `templates/auth/register.html` | 顯示註冊表單 |
| 處理註冊 | POST | `/auth/register` | — | 接收並驗證註冊資訊，建立新帳號 |
| 登入頁面 | GET | `/auth/login` | `templates/auth/login.html` | 顯示登入表單 |
| 處理登入 | POST | `/auth/login` | — | 比對密碼並儲存 Session 登入狀態 |
| 處理登出 | GET | `/auth/logout` | — | 清除 Session 並導向首頁 |
| 食譜列表 | GET | `/recipes` | `templates/recipe/list.html` | 顯示登入者的食譜清單，可附帶搜尋查詢字串 |
| 新增食譜頁面 | GET | `/recipes/new` | `templates/recipe/form.html` | 顯示空白填寫表單 |
| 建立食譜 | POST | `/recipes` | — | 接收表單欄位，存入資料庫 |
| 食譜詳情 | GET | `/recipes/<id>` | `templates/recipe/detail.html` | 顯示單筆食譜的食材與步驟等內容 |
| 編輯食譜頁面 | GET | `/recipes/<id>/edit` | `templates/recipe/form.html` | 顯示帶有原資料的表單 |
| 更新食譜 | POST | `/recipes/<id>/update` | — | 以新資料覆蓋舊記錄 |
| 刪除食譜 | POST | `/recipes/<id>/delete` | — | 刪除對應記錄並重導向 |
| 最愛列表 | GET | `/favorites` | `templates/favorite/list.html` | 顯示有加入最愛的食譜清單 |
| 切換最愛 | POST | `/recipes/<id>/favorite`| — | 點擊愛心切換加入 / 移除最愛 |

## 2. 每個路由的詳細說明

### 2.1 網站首頁 (`/`)
- 輸入: 無。
- 邏輯: 檢查系統中目前是否有登入的 Session，若有則可以直接提供「查看我的食譜」之跳轉按鈕。
- 輸出: 渲染 `templates/main/index.html`。

### 2.2 Auth (會員認證)
- **/auth/register**：收到 GET 時渲染 `register.html`。收到 POST 時提取 `username`, `email`, `password`，將密碼使用 Werkzeug hash 之後呼叫 `User.create()`，若 email 衝突則閃現 (flash) 錯誤訊息，成功則轉向 `/auth/login`。
- **/auth/login**：收到 GET 渲染 `login.html`。收到 POST 提取 `email`, `password` 進行比對，成功後將 `user_id` 寫入 Flask Session，並轉向 `/recipes`。

### 2.3 Recipe (食譜 CRUD)
- **/recipes**：GET 方法，從 `request.args.get('q')` 讀取搜尋條件，並呼叫 `Recipe.get_all()` 或個人的 API 取回食譜清單，傳給 `list.html`。POST 方法則是從 `request.form` 拿資料建立實體後，redirect 至 `/recipes`。
- **/recipes/<id>/update**：收到 POST 後重新更新對應的食譜。為防止越權，須比對 `recipe.user_id == session['user_id']`。
- **/recipes/<id>/delete**：收到 POST，驗證身份後執行刪除，轉向 `/recipes`。

### 2.4 Favorite (我的最愛)
- **/favorites**：從 session 取出 user_id 呼叫 `Favorite.get_user_favorites()`，並將清單給 `favorite/list.html` 渲染。
- **/recipes/<id>/favorite**：收到 POST，呼叫 `Favorite.toggle()`。為了增強體驗，可以重新導向回使用者剛剛所在的同一個 `recipes/<id>` 詳情頁面。

## 3. Jinja2 模板清單

將來前端版面我們使用基礎的網頁結構。由 `base.html` 統一包含 `<head>`、Navbar 及 Bootstrap 樣式：
- `templates/base.html` (被所有模板繼承)
- `templates/main/index.html` (首頁 Landing Page)
- `templates/auth/register.html` 
- `templates/auth/login.html`
- `templates/recipe/list.html` 
- `templates/recipe/form.html` (新增與編輯共用相同的表單介面以避免重複程式碼)
- `templates/recipe/detail.html`
- `templates/favorite/list.html` 

## 4. 路由骨架程式碼
對應的 Python 文件已經準備好在以下路徑，並透過 Flask Blueprint 切分與註冊：
- `app/routes/main_routes.py`
- `app/routes/auth_routes.py`
- `app/routes/recipe_routes.py`
- `app/routes/favorite_routes.py`
