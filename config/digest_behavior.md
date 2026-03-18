# Digest behavior (edit this file to change summarization behavior)

這份文件定義「怎麼抓」「怎麼整理」「輸出格式」——讓所有 cron（05:10 / 09:00 / 13:50 / 21:30 及其 fallback）共用同一套規則。

## 1) 抓取策略（預設規則 + 來源特例）

### 預設規則（多數來源）
1. **優先用 `web_fetch`** 抓可讀內容。
2. 若遇到以下情況，改用 **`browser`**：
   - `web_fetch` 抓不到重點（只有導覽、空白、或內容過少）
   - 403 / 反爬限制
   - 需要動態渲染才有內容
3. 抓取時請保留「來源連結」供 digest 末尾列出。

### 來源特例：PTT 股市版（強制用 browser + selector 抽取）
- PTT 不要用「快照文字抽取」的方式（很容易抽不到推文數/標題對應）。
- 直接用 `browser` 開 `https://www.ptt.cc/bbs/Stock/index.html`，用 DOM selector 抽取：
  - 列表：`.r-ent`（取前 10）
  - 推文數：`.nrec`
  - 標題：`.title a`
  - 連結：`.title a[href]`
- 若遇 18+ 驗證頁：先點「我同意 / 進入」後再抓列表。

## 2) 摘要輸出規則（HTML 內容層）

- 全文以**繁體中文**。
- 每個來源（source）獨立成一個 section，標題使用 `config/digest_sources.yaml` 的 `label`。
- 每個 section 先給 3–5 個 bullet 的「本來源重點」。
- 末尾固定有一段：
  - **Cross-market takeaways（跨市場觀察）**
  - **Risk watch（風險/變數）**
  - **Source links（來源連結清單）**

## 3) 來源別格式要求（額外規格）

### CNA 中央社｜股市
- 以「今日市場重點」方式整理，偏新聞摘要。

### 鉅亨網
- 在 section 內列出 **5 則最值得看的重點**：
  - 格式：`標題 + 1 句重點`（避免長段落）。

### PTT 股市版
- 先整理首頁前 **30 篇文章**：
  - 格式：`推/噓或回應量（若可取得）+ 標題`。
- 再挑出其中 **3 個最熱門主題**，每個主題寫 **2–3 句摘要**。

## 4) 檔案與發布（沿用 RUNBOOK）

- 產出：`digests/YYYY-MM-DD-HHMM.html`（Asia/Taipei）
- 更新：`index.html`（最新卡片 + 歷史列表）
- **必須**：commit + push 到 `origin main`

## 5) 如何新增/移除來源

- 只需要改 `config/digest_sources.yaml`：
  - 新增一個 `sources:` entry，填 `id/label/urls/notes`。
- 如需新增「特殊格式要求」，再補到本檔（本檔第 3 節）。
