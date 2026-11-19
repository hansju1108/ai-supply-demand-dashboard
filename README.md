# AI 產業供需缺口觀測站

**網站預計網址：** https://hansju1108.github.io/ai-supply-demand-dashboard/

本儀表板整理 19 張 Excel 資料表的 2026-11-20 V3 靜態研究快照，包含終端 AI 推論需求、四大 CSP 資本支出、2027–2028 資料中心容量模型、硬體供應與驗證警示。第三方模型預估的 GW 不是確定已投運算力。

## GitHub Pages 啟用

請至 **Settings → Pages → Build and deployment → Source: GitHub Actions**。提交 `dashboard-data.json` 或網站範本後，`.github/workflows/pages.yml` 會自動建置與發佈；也支援 Actions 頁面的手動執行。

## 每週更新（台灣時間週五約 09:00）

已設每週五 01:00 UTC 的 GitHub Actions 定時工作。其流程為：驗證 `dashboard-data.json` 的必要分頁與資料日期、建立網站、部署 Pages。資料超過十天未更新會在 Actions 發出 **stale snapshot** 警告。

**重要：定時部署不等於自動收集新研究資料。** 現有 ChatGPT 每週研究任務不會自動將輸出寫入 GitHub。若每週沒有新數據提交至 GitHub，網頁仍顯示原資料日期，不能將重發佈視為最新市場驗證。

## V3 新增的變現與融資風險

- `14_變現與租金覆蓋`：財報收入/成本與第三方假設分開；Anthropic 2026 Q3／Q2可比費用含訓練與內部使用，不能當成推論租金。
- `15_2028情境模型`：2028 347/441 B USD 是 **SKY 情境營收充足比 78.7%**，不是實際租金支付率。
- `16_融資與信用鏈`：SEC披露、C級未核實擔保、資金與承諾不得混算。
- `17_專案租金風險標籤`：逐案用途、取消條款、融資依賴、歸屬證據。
- `18_四層跨層驗證`：按「使用→變現→信用→算力供給」逐項查核。
- 原始資料截至 **2026-11-19**，修訂／發佈日期 **2026-11-20**。GitHub Actions檢查網站嵌入的JS語法及資料一致性，但不代替人工稽核報告。

## 提交每週新數據

1. 優先 SEC、公司 IR（A 級），再使用法說與具方法的報告（B 級），第三方模型（C 級）獨立標註。
2. 更新 `dashboard-data.json`，沿用 19 個 V3 工作表的鍵名與二維陣列格式；將 `asOf` 設為實際查核日期、`version` 設為新版本。
3. 透過 Pull Request 審核來源、口徑與算術一致性，再合併至 `main`；GitHub Actions 會驗證、重建與部署。
4. 舊版資料可使用 Git commit history 追溯。不要在儲存庫提交私人帳密、付費研究資料或 token。

## 檔案
- `dashboard-data.json`：19 張工作表V3基準資料
- `index.template.html`：完整網站與資料插入點
- `scripts/validate_data.py`：結構、日期與資料過舊提示
- `scripts/build_site.py`：建立包含 JSON 的單檔 HTML 與部署目錄
- `scripts/check_site_js.py`：網站 JavaScript 語法檢查
- `.github/workflows/pages.yml`：建置、驗證、排程、部署

驗證程式只能保證結構與時效標註，無法獨立確認原始數據是否屬實。