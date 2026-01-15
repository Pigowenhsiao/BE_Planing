# SPEC

## 目標
建立可追溯、可重算、可稽核的計算流程，確保「每一個數字都知道從哪裡來」。

## 技術棧
- 流程: Excel → SQLite → 重算 → Streamlit
- 語言: Python

## 範圍
- In: Excel 匯入、資料庫分層設計、計算引擎、手動輸入介面、結果對照與驗證、多語系支援。
- Out: 雲端部署、多使用者權限系統、排程/監控、企業級報表平台整合。

## 關鍵原則（本次確認）
1) 除 Sheet1 與 0時以降の完成数 外，其餘表格皆視為由這兩表計算所得；需重新檢查所有表格關係以驗證此假設。
2) 唯一鍵使用 serialnumber。
3) 計算邏輯以 Excel 現有公式邏輯為準。
4) 同時保留 Excel 邏輯結果與 Priority/門檻模型結果。
5) 手動輸入內容需提供 UI，且保留從 Excel 匯入的功能。
6) 版本先不保留，但需預留可版本化的彈性。
7) UI 以多分頁逐一呈現，涵蓋所有內容。
8) 欄位與輸出先維持 Excel 對應。

---

## 資料來源（Excel）
- Sheet1 (Raw 訂單資料)
- Sheet4 (彙總/派生)
- 仕掛 (WIP 相關彙總)
- 仕掛りリスト (WIP 明細)
- 完成数
- Build Plan
- ShippingPlan
- 0時以降の完成数 (Manual)
- 使い方
- vs ship (彙總/派生)

---

## 表格關係（需重新檢查）
### 目標假設
- 基礎來源僅: Sheet1、0時以降の完成数。
- 其餘表格皆可由上述兩表推導。

### 目前 Excel 公式關係（需驗證）
- Sheet4 <- 仕掛りリスト, 完成数, 仕掛
- 仕掛 <- 仕掛りリスト, Sheet4, ShippingPlan
- vs ship <- 仕掛
- Build Plan = 週輸入 + 加總/Gap 派生
- ShippingPlan 為輸入彙總（未見公式）

### 處理原則
- 先維持 Excel 對應與現況依賴，並在 Phase 1 完成關係重新檢查。
- 若確認兩表即可導出，將調整來源分層；若不成立，則擴充來源清單。

---

## Phase 1: 資料來源與計算鏈拆解
### 目標
- 釐清每一個輸出欄位的來源與計算邏輯，形成可實作的邏輯說明。

### 工作內容
- 對 Excel 做欄位級 mapping。
- 重新檢查所有表格關係，驗證「兩表來源」假設。
- 為每一個關鍵輸出定義:
  - Input 欄位清單
  - 計算公式（文字化，不使用 Excel 公式）

### 唯一鍵規則（serialnumber）
- 原則: 以 Excel 現有欄位對應，不改欄名。
- 若原表無 serialnumber 欄位，則以既有欄位組合生成並寫入 mapping。
- serialnumber 需在所有衍生表中可回溯到原始欄位來源。

### 產出
- Data Lineage Spec（計算血緣表）
- Python 可實作的「邏輯說明書」

### Data Lineage Spec 欄位範本
| Output 欄位 | 粒度 | 來源表 | 來源欄位 | 篩選/條件 | Join Key | 計算邏輯 | 時間窗 | 空值規則 | 責任人 |
|---|---|---|---|---|---|---|---|---|---|

### Data Lineage 雛型（根據現有 Excel）
#### Raw（輸入）
- Sheet1
  - 欄位: ORGANIZATION_CODE, ORDER_TYPE, CUSTOMER_NAME, END_CUSTOMER_NAME, ORDER_NUMBER, LINE,
    ORDERED_ITEM, UNIT_SELLING_PRICE, REQUEST_DATE, SCHEDULE_SHIP_DATE, ORDERED_QUANTITY,
    TRANSACTIONAL_CURR_CODE, UNIT_COST, ORGANIZATION_NAME, PROMISE_DATE, OPEN_FLAG, FLOW_STATUS_CODE
- 仕掛りリスト
  - 欄位: 工場, ファミリ, 品名, Waferロット, 製造オーダ, ロット番号,
    前工程実行日, 最終更新日時, 数量, 数量2, 工程, 開始, Seq, 原価工程,
    保留理由, 先行結果, 先行結果更新日, コメント, 出荷可能時期, Wafer完了日
- 完成数
  - 欄位: 工場, ファミリ名, 品名, 数量, 数量2
- ShippingPlan
  - 欄位結構: Item, Shipping Qty(1-3wk), OnHand Qty, OHQ, Shortage(OHQ/含WIP),
    WIP(多工序欄位), EOH(OHQ), EOH(OHQ+WIP)

#### Manual（人工輸入）
- 0時以降の完成数
  - 欄位: 工場, ファミリ名, 品名, 数量, 数量2
- Build Plan
  - 週別欄位 (WK01~WK13) 為人工輸入，加總/Gap 為派生

#### Derived（可重算）
- Sheet4（週需求/合計/完成實績/入庫前檢查等彙總）
- 仕掛（WIP 各工程與良品推定）
- vs ship（出荷要望 vs 不足數量）

### 代表性輸出定義（文字化邏輯）
1) Sheet4 合計
- Input: 週別需求欄位 (WK01~WK13)
- Logic: 合計為週別需求加總

2) Sheet4 完成實績
- Input: 完成数.品名、完成数.数量
- Logic: 以品名對應完成數；若存在 Prime/子品名則加總

3) Sheet4 入庫前檢查
- Input: 仕掛りリスト.数量
- Filter: 工程 = 入庫前検査，先行結果為合格
- Logic: 對符合條件的數量加總

4) 仕掛 包裝相關 WIP
- Input: 仕掛りリスト.数量
- Filter: 工程包含「ラベル印刷・包装 / 先行評価合否確認 / X線検査」，且結果為合格
- Logic: 依品名加總

5) 仕掛 良品推定
- Input: 上一站 WIP 與係數 (CF..CL)
- Logic: 逐站乘上係數並取整數

6) vs ship 不足數量
- Input: 仕掛 對應品名的不足數量
- Logic: 依品名對應不足數量

---

## Phase 2: 資料庫設計（Raw / Manual / Derived 分層）
### 原則
- Raw Data: 只讀、不可覆寫（目前不保留版本）
- Manual Data: 可寫、需稽核
- Extend Data: 可重算、可全部重建
- 版本彈性: 預留 snapshot/version 欄位以便未來啟用

### Raw Data tables
- 先維持 Excel 對應結構，並提供 serialnumber 欄位
- 預留 snapshot_id（目前不啟用）

### Manual Data tables
- 對應 0時以降の完成数 與其他人工補正
- 必須保留稽核資訊:
  - created_by, created_at, reason

### Extend Data tables
- 所有計算結果
- 支援 drop & rebuild

### 建議欄位（示例）
- raw_snapshot(id, source_file, imported_at, checksum)  # 預留，不啟用
- raw_sheet1(..., serialnumber)
- manual_input(id, serialnumber, input_date, site, type, quantity, note, created_by, created_at, reason)
- derived_wip(..., serialnumber, computed_at)
- derived_summary(..., serialnumber, computed_at)

---

## Phase 3: Python 計算引擎
### 設計原則
- 不模擬 UI，但計算邏輯需 1:1 對齊 Excel 公式
- 同時產出兩套結果:
  - Excel 邏輯結果（主輸出）
  - Priority/門檻模型結果（輔助輸出）

### 模組化建議
calc/
- load_raw.py
- apply_manual.py
- wip_calc.py
- summary_calc.py
- vs_ship_calc.py
- validators.py

### 特點
- 任一 Excel 版本 → 同一份結果
- 可單日重算、回溯歷史週、模擬假設情境

---

## Phase 4: 手動輸入介面（Streamlit）
### 功能
- 手動輸入:
  - 日期
  - 站點 / 類型
  - 數量
  - 備註
- Excel 匯入:
  - 上傳或指定路徑匯入
  - 匯入後可再手動補充
- 查詢:
  - 今日手動輸入紀錄
  - 修改歷史與異動人

### UI 分頁規劃（包含所有內容）
1) 總覽（期間選擇、指標、警示）
2) Raw Data: Sheet1
3) Raw Data: 仕掛りリスト
4) Raw Data: 完成数
5) Raw Data: ShippingPlan
6) Manual Data: 0時以降の完成数 + 其他人工補正
7) Extend Data: Sheet4
8) Extend Data: 仕掛
9) Extend Data: vs ship
10) Build Plan（輸入與加總/Gap）
11) 設定/字典（serialnumber 規則、閾值、對照表）
12) 匯入紀錄/操作紀錄

### UI 原則
- 先求可控與可稽核，不追求視覺複雜度
- 預設以 Excel 呈現格式對齊

---

## 多語系規範
### 語言
- 繁體中文 / 英文 / 日文

### 切換方式
- 下拉式選單（使用者手動選擇）

### 實作建議
- i18n 資源檔（例如: i18n/zh-TW.json, i18n/en.json, i18n/ja.json）
- UI 文案與欄位標籤一律走翻譯層

---

## 驗證與稽核
- 與 Excel 既有結果做週期對照
- 針對空值、日期缺失、合併表頭等情境建立檢核
- 所有 Manual 更新需保留稽核紀錄
- 以 Excel 對應為準，不先重構欄位或命名

---

## 交付物
- Data Lineage Spec
- 邏輯說明書
- DB schema 與資料字典
- Streamlit UI（含多語系）
- 匯入與重算流程（可重跑）
