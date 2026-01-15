WIP Analysis & Priority Control System  
技術交付文件（Technical Handover）
1. 系統目的（Purpose）
本系統用於：

將後段工程 Excel 計算邏輯系統化
將 Excel 降級為「資料來源（Input Snapshot）」
以 Python 重新計算 WIP / 完成數 / 狀態
支援 站點差異化 WIP 判斷
引入 Serial Number 等級的人工 Priority 紀律
以可視化方式即時呈現系統判定與人工決策
2. 系統架構（Architecture Overview）
Excel (Snapshot, Read-only)
↓
Pandas
↓
SQLite (Local)
↓
Streamlit UI

yaml
Copy code

### 架構設計原則
- 單人使用、低維運
- 每次 Excel 更新 → 全量重算
- 不保留歷史版本（可未來擴充）

---

## 3. 技術選型（Technology Stack）

| 層級 | 技術 | 說明 |
|---|---|---|
| 語言 | Python 3.10+ | 主開發語言 |
| 資料處理 | Pandas | 取代 Excel 公式 |
| 資料庫 | SQLite | Local、無併發 |
| UI | Streamlit | 快速視覺化 |
| 視覺 | Pandas Styler | 條件上色 |

---

## 4. 專案結構（Project Structure）

```text
wip_analysis/
├─ data/
│  ├─ input/              # Excel 原始資料
│  └─ local.db            # SQLite（自動產生）
│
├─ config/
│  └─ settings.py         # 全域設定（門檻、路徑）
│
├─ etl/
│  ├─ read_excel.py       # Excel 讀取
│  ├─ load_sqlite.py      # SQLite 寫入
│  └─ priority_repo.py    # Priority 存取
│
├─ calc/
│  ├─ wip_calc.py         # WIP 計算核心
│  └─ final_status.py     # Priority Override
│
├─ ui/
│  ├─ app.py              # Streamlit 主程式
│  ├─ priority_input.py   # Priority 輸入頁
│  └─ styles.py           # 顏色規則
│
├─ main.py                # 一鍵重算
└─ README.md
5. 資料來源規格（Data Source）
5.1 Excel 規則
Excel 為唯一外部資料來源

僅讀取，不寫回

每次執行時：

全量讀取

覆寫 SQLite

5.2 Sheet 定義
Text

Markdown
Sheet 名稱	角色
Sheet1	Raw 生產資料
0時以降の完成数	人工補完成數
CSV
Excel

6. 資料庫設計（SQLite Schema）
6.1 Raw Data（只讀）
sql
Copy code
raw_data (
  serial_number TEXT,
  site TEXT,
  process TEXT,
  input_qty INTEGER,
  complete_qty INTEGER
)
6.2 Manual Priority（人工紀律）
sql
Copy code
manual_priority (
  serial_number TEXT PRIMARY KEY,
  priority INTEGER NOT NULL,   -- 1 = 最高
  reason TEXT NOT NULL,
  owner TEXT NOT NULL,
  created_at DATETIME
)
設計原則

一個 Serial Number 僅允許一筆 Priority

Priority 為決策層，不修改 Raw Data

6.3 WIP Result（計算結果）
sql
Copy code
wip_result (
  serial_number TEXT,
  site TEXT,
  process TEXT,
  wip INTEGER,
  wip_status TEXT,
  priority INTEGER,
  final_status TEXT
)
7. 計算邏輯（Calculation Logic）
7.1 WIP 定義
ini
Copy code
WIP = Input − Complete − Manual_Adjust
7.2 站點差異化門檻
定義於 config/settings.py

python
Copy code
WIP_THRESHOLDS = {
  "SITE_A": {"urgent": 120, "next_week": 60},
  "SITE_B": {"urgent": 80,  "next_week": 40},
  "DEFAULT": {"urgent": 100, "next_week": 50}
}
7.3 系統 WIP 狀態
Text

Markdown
條件	狀態
wip ≥ urgent	URGENT
wip ≥ next_week	NEXT_WEEK
else	NORMAL
CSV
Excel

7.4 Priority Override 規則（最高優先）
Copy code
若 priority == 1 → final_status = URGENT_MANUAL
否則 → final_status = wip_status
8. 視覺化規格（UI）
8.1 顏色定義
Text

Markdown
final_status	顯示
URGENT_MANUAL	深紅 + 粗體
URGENT	紅
NEXT_WEEK	橘
NORMAL	無
CSV
Excel

8.2 Streamlit 功能頁
WIP Dashboard

表格顯示 WIP

狀態顏色即時呈現

Manual Priority

Serial Number 輸入

Priority / Reason / Owner

即時生效

9. 系統執行流程（Runtime Flow）
執行 main.py

讀取 Excel

覆寫 raw_data

套用人工補數

計算 WIP

套用站點門檻

套用 Priority Override

輸出 wip_result

Streamlit 顯示

🔧 開發守則（Coding Guideline）
1. 架構守則
ETL / Calculation / UI 必須分離

不可在 UI 內寫計算邏輯

不可在計算邏輯中寫 UI code

2. 資料守則
Raw Data 永遠只讀

Manual Data 只能存在於對應表

所有結果必須可重算

3. Priority 守則
Priority 是「決策紀律」，不是 workaround

必須填寫 Reason

Priority 只能 override，不可影響 Raw

4. 計算守則
不模擬 Excel 公式

以「業務意義」重寫邏輯

所有門檻必須設定檔化

5. 命名守則
表名：snake_case

欄位名：snake_case

狀態值：全大寫（URGENT）

6. 擴充守則
新規則 → 設定檔或資料表

不允許硬編碼 magic number

新狀態需同步更新 UI 樣式

10. 未來擴充（非本版範圍）
Priority 有效期限

客戶 / SLA 權重

歷史版本保存

自動寄送緊急清單

11. 結語
本系統不是報表工具
而是一套 可追蹤、可複製、可交接的工程決策系統

yaml
Copy code

