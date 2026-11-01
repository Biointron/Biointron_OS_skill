<div align="center">

<p dir="ltr">
<a href="../../README.md" lang="en" dir="ltr">English</a> ·
<a href="README.zh-CN.md" lang="zh-CN" dir="ltr">简体中文</a> ·
<strong lang="zh-TW" dir="ltr">繁體中文</strong> ·
<a href="README.ja.md" lang="ja" dir="ltr">日本語</a> ·
<a href="README.ko.md" lang="ko" dir="ltr">한국어</a> ·
<a href="README.tr.md" lang="tr" dir="ltr">Türkçe</a> ·
<a href="README.ru.md" lang="ru" dir="ltr">Русский</a> ·
<a href="README.vi.md" lang="vi" dir="ltr">Tiếng Việt</a> ·
<a href="README.th.md" lang="th" dir="ltr">ไทย</a> ·
<a href="README.de.md" lang="de" dir="ltr">Deutsch</a> ·
<a href="README.es.md" lang="es" dir="ltr">Español</a> ·
<a href="README.fr.md" lang="fr" dir="ltr">Français</a> ·
<a href="README.uk.md" lang="uk" dir="ltr">Українська</a> ·
<a href="README.pl.md" lang="pl" dir="ltr">Polski</a> ·
<a href="README.pt-BR.md" lang="pt-BR" dir="ltr">Português (Brasil)</a> ·
<a href="README.fa.md" lang="fa" dir="rtl">فارسی</a> ·
<a href="README.ar.md" lang="ar" dir="rtl">العربية</a> ·
<a href="README.id.md" lang="id" dir="ltr">Bahasa Indonesia</a> ·
<a href="README.it.md" lang="it" dir="ltr">Italiano</a> ·
<a href="README.el.md" lang="el" dir="ltr">Ελληνικά</a> ·
<a href="README.ml.md" lang="ml" dir="ltr">മലയാളം</a> ·
<a href="README.ur-Latn.md" lang="ur-Latn" dir="ltr">Roman Urdu</a> ·
<a href="README.ro.md" lang="ro" dir="ltr">Română</a>
</p>

# Biointron OS

### 讓你的 AI Agent 連接百英服務。

從訂單需求到結果取得，將百英工作流程融入你熟悉的工具。<br />
MCP 負責連接，Skills 引導流程，每一步都由你掌握。

[![MCP 工具目錄](https://img.shields.io/badge/MCP-tool_catalog-087F8C?style=flat-square)](../../docs/tool-catalog.md)
[![Skills](https://img.shields.io/badge/Agent-Skills-234E70?style=flat-square)](../../skills/README.md)
[![非商業授權](https://img.shields.io/badge/License-Noncommercial-6B7280?style=flat-square)](../../LICENSE)
[![Beta Playground](https://img.shields.io/badge/Release-Beta_Playground-D7A345?style=flat-square)](#beta)

<br />

<!-- HERO: Keep the artwork path in sync across all language versions. -->
<img src="../../assets/biointron-os-hero.png" alt="Biointron OS" width="1000" />

<br />

**[開始使用](#get-started) · [MCP 工具](../../docs/tool-catalog.md) · [Skills](../../skills/README.md) · [API 與範例](../../docs/api.md) · [線上平台](#online-platform) · [常見問題](#faq)**

</div>

---

## 一個平台，三種連接方式。

Biointron OS 為 AI Agent、模型及使用者提供百英服務的接入介面。它整合服務存取與工作流程指引，規劃逐步涵蓋訂單、設計提交、進度及結果。

| 面向 Agent | 面向模型 | 面向使用者 |
| :--- | :--- | :--- |
| 透過 **MCP** 探索並呼叫服務。 | 使用**結構化資料**及有文件說明的介面。 | 透過**互動式介面**使用工作流程。 |
| 搭配適用於特定任務的 Skills 呼叫工具。 | Beta 階段持續對齊資料規範。 | 網頁服務獨立於本儲存庫提供。 |

本儲存庫是 Skills、連接指南、工具目錄及範例的公開入口。百英業務服務獨立運作。

<a id="get-started"></a>

## 開始使用

### 1 · 連接 MCP

向你的百英聯絡窗口取得服務存取權杖與使用權限。在支援 **Streamable HTTP** 和 **Bearer 驗證**的 MCP 用戶端中新增：

| 設定項目 | 值 |
| :--- | :--- |
| 名稱 | `BiointronOS_MCP` |
| 傳輸方式 | Streamable HTTP |
| 網址 | `https://mcp-rusta-order-blgdfvompw.cn-shanghai.fcapp.run/mcp` |
| 驗證 | `Authorization: Bearer <MCP_ACCESS_TOKEN>` |

若用戶端支援 `mcpServers` 格式，可將以下設定合併至現有設定，並用自己的權杖取代占位符。

```json
{
  "mcpServers": {
    "BiointronOS_MCP": {
      "url": "https://mcp-rusta-order-blgdfvompw.cn-shanghai.fcapp.run/mcp",
      "headers": {
        "Authorization": "Bearer <MCP_ACCESS_TOKEN>",
        "START_MCP_TIMEOUT_MS": "60000",
        "RUN_MCP_TIMEOUT_MS": "660000"
      }
    }
  }
}
```

兩個逾時標頭是參考設定中的自訂項目：60000 毫秒為 60 秒，660000 毫秒為 11 分鐘。只有用戶端或服務支援這些標頭時，才會有相應效果；僅將它們放入 `headers` 不能保證改變用戶端的等待時間，具體設定請依照用戶端文件。

更多設定方式請參閱[安裝指南](../../docs/installation.md#mcp)。

### 2 · 新增 Skills

從 [Skills 目錄](../../skills/README.md)選擇本倉庫已包含的 Skill。下載完整資料夾，保留 `references/` 與隨附腳本，放入 Agent 的 Skill 目錄。Codex 與 Claude Code 的設定方式見 [Skill 安裝說明](../../docs/installation.md#skills)。

兩個套件現已包含在本倉庫：`order-design` 位於 `skills/order_design/`，`auto_html_report` 位於 `skills/auto_html_report/`，均可下載。套件已提供不代表完整業務流程已通過驗證。

### 3 · 先進行唯讀體驗

```text
列出本次工作階段可用的 Biointron MCP 工具，並說明各工具的用途。
告訴我哪些功能已就緒，哪些仍處於 Beta 階段。
不要建立或提交訂單。
```

探索工具是確認連接的第一步。業務操作要成功，仍須驗證其對應的後端連接。

## MCP 工具目錄

| 工具 | 用途 | 操作性質 |
| :--- | :--- | :--- |
| `order_design_preflight` | 檢查公司資格和可用檢測項目。 | 唯讀 |
| `start_order_design` | 提交客戶 XLSX 並等待設計儲存確認。 | 寫入業務資料 |
| `add_order_to_cart` | 將已確認儲存的設計加入購物車。 | 寫入業務資料 |
| `get_order_cart` | 查詢訂單購物車。 | 唯讀 |
| `calculate_order_price` | 取得指定訂單的報價。 | 唯讀 |
| `submit_verified_order` | 核驗報價後提交選定訂單。 | 寫入業務資料 |
| `get_report_results` | 以 JSON 取得既有報告結果。 | 唯讀 |

目前的 MCP 實作已註冊這七個工具。端到端業務流程是否就緒仍待驗證。請參閱[工具簽章、狀態與限制](../../docs/tool-catalog.md)。

## Skills

| Skill | 用途 | 發布狀態 |
| :--- | :--- | :--- |
| [訂單設計 · `order-design`](../../skills/order_design/SKILL.md) | 引導設計提交、加入購物車、報價核查及授權範圍內的訂單提交。 | 已包含，可下載 |
| [結果報告 · `auto_html_report`](../../skills/auto_html_report/SKILL.md) | 將使用者提供的既有結果 JSON 製作為獨立的多語言 HTML 報告，包含彙總表、圖表及可用圖片。 | 已包含，可下載 |

MCP 提供可呼叫的操作；Skills 說明 Agent 如何在任務中使用這些操作。安裝 Skill 不會授予服務存取權限，也不會自動註冊 MCP。[瀏覽目錄 →](../../skills/README.md)

`auto_html_report` Skill 需要使用者提供既有結果 JSON，不負責從服務取得資料；只有訂單編號不足以產生報告。

<a id="beta"></a>

## Beta Playground

Biointron OS 正以 Beta Playground 形式逐步推出，部分連接可能仍無法使用。請如實回報每一步的結果；HTTP 成功或工具名稱可見，並不代表業務操作已完成。

建立及提交訂單需要使用者授權。若寫入逾時，請先核查既有訂單狀態再重試。如需存取權限或遇到尚未開放的功能，請聯絡提供帳號的百英窗口。

<a id="online-platform"></a>

## Biointron 線上平台

Biointron 線上平台將 RushDATA 專案流程帶入瀏覽器，提供專案草稿、購物車、訂單與 AI 助理的入口。開啟平台即可探索可用服務並查看專案資訊。

[前往 Biointron 線上平台 →](https://ai.biointron.com/#/landing)

<a href="https://ai.biointron.com/#/landing"><img src="../../assets/Biointron_Rushdata.png" alt="Biointron 線上平台介面，提供 RushDATA 專案入口" width="1000" /></a>

<a id="faq"></a>

## 常見問題

<details>
<summary><strong>MCP 和 Skills 都需要嗎？</strong></summary>

MCP 提供可呼叫的工具。Skills 補充工作流程指引，也可能有各自的相依項目。請遵循每個已發布 Skill 的要求；僅下載 Skill 不會連接服務。

</details>

<details>
<summary><strong>工具出現在清單中，是否表示可以用於業務？</strong></summary>

不是。探索到工具只確認它已註冊。後端設定、帳號存取權限及要求執行的操作也必須經過驗證。工具目錄會區分這些狀態。

</details>

<details>
<summary><strong>伺服器端與業務實作在哪裡？</strong></summary>

本儲存庫提供公開接入資料與 Skills。託管服務及內部業務實作另行維護。

</details>

## 文件

| 從這裡開始 | 參考資料 |
| :--- | :--- |
| [安裝 MCP 與 Skills](../../docs/installation.md) | [MCP 工具目錄](../../docs/tool-catalog.md) |
| [Skills 目錄](../../skills/README.md) | [API 與 JSON 範例](../../docs/api.md) |
| [參與貢獻](../../CONTRIBUTING.md) | [授權狀態](../../docs/license.md) |

詳細指南提供中文及英文版本。

## 授權

採用 [PolyForm Noncommercial 1.0.0](../../LICENSE)。**本授權不允許商業使用。** 本儲存庫的原始碼可供非商業用途使用。請參閱[適用範圍與條款](../../docs/license.md)。

---

<div align="center">
<sub>Biointron OS · 面向 Agent。面向模型。面向使用者。</sub>
</div>
