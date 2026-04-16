# Architecture - 食譜收藏夾系統

## 1. 技術架構說明

本專案採用經典的 Web 應用程式架構，不進行前後端分離，直接由後端渲染頁面提供給使用者。以下為主要技術選型與架構說明：

- **選用技術與原因**：
  - **後端（Python + Flask）**：Flask 是輕量且具備高度彈性的 Python 網頁框架，非常適合快速構建中小型應用程式與驗證 MVP。
  - **模板引擎（Jinja2）**：與 Flask 緊密結合的模板引擎。可以在 HTML 中嵌入 Python 語法，由後端負責將資料塞入模板（Server-Side Rendering），幫助我們加速前端開發。
  - **資料庫（SQLite）**：輕量級的關聯式資料庫。將資料庫存放在單一檔案中，無需額外安裝伺服器，適合小型本地專案及測試環境。

- **Flask MVC 模式說明**：
  - **Model（模型）**：負責與 SQLite 進行互動。將對應到與食譜、使用者相關的資料表。
  - **View（視圖）**：在此系統中，View 為 Jinja2 模板引擎處理過後的 HTML。負責將接收到的資料呈現為使用者可見的 UI。
  - **Controller（控制器）**：也就是 Flask 中的 Route（路由）。負責對應使用者的 URL 請求，進行業務邏輯處理、呼叫 Model 取得資料，最後把資料傳遞給 Jinja2 渲染畫面。

## 2. 專案資料夾結構

為了保持專案整潔及後續維護的彈性，我們會使用模組化的方式拆分資料夾，而不是把所有程式碼塞在同一個檔案內：

```text
web_app_development/
├── app/                  # 應用程式主要資料夾
│   ├── models/           # 存放資料庫模型定義 (例如 user.py, recipe.py)
│   ├── routes/           # 存放 Flask 模組化路由 (例如 auth_routes.py, recipe_routes.py)
│   ├── templates/        # 存放 Jinja2 HTML 模板
│   │   ├── base.html     # 共用的頁面版型 (Header, Footer, Navbar)
│   │   ├── auth/         # 登入與註冊頁面
│   │   └── recipe/       # 食譜列表、新增與詳細頁面
│   └── static/           # 存放靜態資源 (CSS 樣式表, JS 腳本, 圖片)
├── docs/                 # 系統文件存放區
│   ├── PRD.md            # 產品需求文件
│   └── ARCHITECTURE.md   # 架構設計文件 (本檔)
├── instance/             # Flask instance 資料夾
│   └── database.db       # SQLite 資料庫檔案
├── .agents/              # AI Prompt 與技能資源 (已存在)
├── app.py                # 整個應用程式的主程式及入口點
└── requirements.txt      # 記錄專案 Python 模組相依性套件
```

## 3. 元件關係圖

以下圖示呈現使用者、Flask、Jinja2 及 SQLite 之間如何互動與處理請求：

```mermaid
flowchart TD
    Client[使用者的瀏覽器 Browser]
    
    subgraph Controller
        Route[Flask Route<br/>(負責 URL 映射與邏輯)]
    end
    
    subgraph Model
        DB_Models[Models<br/>(負責處理資料存取)]
    end
    
    subgraph View
        Jinja2[Jinja2 Templates<br/>(負責畫面排版)]
    end
    
    Database[(SQLite Database)]
    
    %% 請求流程
    Client -->|1. 發送 HTTP 請求 (GET/POST)| Route
    Route -->|2. 處理商業邏輯並請求資料| DB_Models
    DB_Models -->|3. 執行 SQL 查詢或更新| Database
    Database -->|4. 返回查詢結果| DB_Models
    DB_Models -->|5. 將資料回傳給處理函數| Route
    Route -->|6. 將資料注入模板進行渲染| Jinja2
    Jinja2 -->|7. 產出最終的 HTML| Route
    Route -->|8. 回傳 HTTP Response| Client
```

## 4. 關鍵設計決策

1. **不採用前後端分離（保持 SSR 渲染）**
   - **原因**：為了在初次開發時最大化速度，使用模板渲染能減少前端 API 串接與狀態管理的成本。此方式也能大幅降低一開始學習或開發的複雜度。
2. **使用藍圖（Blueprints）分離路由（Routes）**
   - **原因**：即使是輕量級專案，將所有路由塞在 `app.py` 會使得檔案難以閱讀。我們會把「使用者認證處理（Auth）」與「食譜管理（Recipe）」切分到不同檔案中掛載，讓邏輯更清晰。
3. **無強制使用 ORM，或者選擇 SQLAlchemy**
   - **原因**：為了資料庫管理的穩定性，我們可以考慮直接使用 Python 的 `sqlite3` 自行編寫 SQL。或者如果後續需要比較乾淨的模型宣告，再考慮導入 `Flask-SQLAlchemy`。
4. **雜湊儲存密碼以策安全**
   - **原因**：將使用 Werkzeug 的內建安全性工具對使用者密碼進行 Hash 處理。避免在 SQLite 檔案中看見明文密碼，滿足 PRD 中要求的資安考量。
