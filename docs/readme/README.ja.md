<div align="center">

<p dir="ltr">
<a href="../../README.md" lang="en" dir="ltr">English</a> ·
<a href="README.zh-CN.md" lang="zh-CN" dir="ltr">简体中文</a> ·
<a href="README.zh-TW.md" lang="zh-TW" dir="ltr">繁體中文</a> ·
<strong lang="ja" dir="ltr">日本語</strong> ·
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

### AI エージェントから、Biointron のサービスへ。

注文の依頼から結果の取得まで、いつもの AI ツールで Biointron のワークフローへ。<br />
MCP がサービスをつなぎ、Skills が手順をガイドします。操作の判断はユーザーが行います。

[![MCP tool catalog](https://img.shields.io/badge/MCP-tool_catalog-087F8C?style=flat-square)](../tool-catalog.md)
[![Skills](https://img.shields.io/badge/Agent-Skills-234E70?style=flat-square)](../../skills/README.md)
[![Noncommercial license](https://img.shields.io/badge/License-Noncommercial-6B7280?style=flat-square)](../../LICENSE)
[![Beta Playground](https://img.shields.io/badge/Release-Beta_Playground-D7A345?style=flat-square)](#beta)

<br />

<!-- HERO: Keep the artwork path in sync across all language versions. -->
<img src="../../assets/biointron-os-hero.png" alt="Biointron OS" width="1000" />

<br />

**[はじめに](#get-started) · [MCP ツール](../tool-catalog.md) · [Skills](../../skills/README.md) · [API とサンプル](../api.md) · [オンラインプラットフォーム](#online-platform) · [FAQ](#faq)**

</div>

---

## ひとつのプラットフォーム、3 つの接点。

Biointron OS は、AI エージェント、モデル、ユーザーのための Biointron サービスへの窓口です。サービスへの接続とワークフローの手順をまとめ、注文、設計データの提出、進捗の確認、結果の取得を段階的につなぎます。

| エージェント向け | モデル向け | ユーザー向け |
| :--- | :--- | :--- |
| **MCP** でサービスを検出・呼び出し。 | **構造化データ**とインターフェース仕様を利用。 | **対話型の画面**から業務サービスを利用。 |
| Skills がタスクの手順をガイド。 | データ仕様は Beta 期間中に整備。 | Web 画面は本リポジトリとは別に提供。 |

このリポジトリでは Skills、接続ガイド、ツール一覧、サンプルを公開します。業務サービスは別途運用されます。

<a id="get-started"></a>

## はじめに

### 1 · MCP を接続

Biointron の担当者からサービス用アクセストークンを取得し、アカウントの権限を確認します。**Streamable HTTP** と **Bearer 認証**に対応する MCP クライアントへ、次の情報を設定してください。

| 設定 | 値 |
| :--- | :--- |
| 名前 | `BiointronOS_MCP` |
| 接続方式 | Streamable HTTP |
| URL | `https://mcp-rusta-order-blgdfvompw.cn-shanghai.fcapp.run/mcp` |
| 認証 | `Authorization: Bearer <MCP_ACCESS_TOKEN>` |

`mcpServers` 形式に対応するクライアントでは、次の設定例を既存の設定に追加し、`<MCP_ACCESS_TOKEN>` を発行されたサービス用アクセストークンに置き換えてください。

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

`START_MCP_TIMEOUT_MS` と `RUN_MCP_TIMEOUT_MS` は参考設定の独自リクエストヘッダーで、それぞれ **60 秒**と **11 分**に相当します。MCP 標準のタイムアウト設定ではなく、クライアントまたはサービス側の明示的な対応が必要です。`headers` に追加するだけではクライアントの待機時間が変更されるとは限りません。利用するクライアントの仕様に従って設定してください。詳しくは[インストールガイド](../installation.md#mcp)をご覧ください。

### 2 · Skills を追加

[Skills 一覧](../../skills/README.md)から Skill を選び、参照ファイルと付属スクリプトを含むフォルダー全体をダウンロードして、エージェントの Skill ディレクトリに配置します。Codex と Claude Code の設定先は [Skill のインストール](../installation.md#skills)に記載しています。

`skills/order_design`（`order-design`）と `skills/auto_html_report`（`auto_html_report`）の両フォルダーを同梱しています。注文設計は MCP サービスを利用します。レポート Skill は提供済みの結果 JSON からレポートを作成し、結果の取得は行いません。

### 3 · 読み取り専用の確認から始める

```text
このセッションで利用できる Biointron MCP ツールと、その用途を説明してください。
利用可能な機能と、まだ Beta 段階の機能を教えてください。
注文の作成や送信は行わないでください。
```

ツールの検出は接続確認の最初のステップです。業務操作には、対応するバックエンド接続の検証が必要です。

## MCP ツール一覧

| ツール | 用途 | 操作 |
| :--- | :--- | :--- |
| `order_design_preflight` | 会社の利用資格と検査項目を確認。 | 読み取り専用 |
| `start_order_design` | 提供された XLSX を送信し、設計の保存確認を待つ。 | 書き込み |
| `add_order_to_cart` | 保存確認済みの設計をカートに追加。 | 書き込み |
| `get_order_cart` | 注文カートを照会。 | 読み取り専用 |
| `calculate_order_price` | 選択した注文の見積もりを取得。 | 読み取り専用 |
| `submit_verified_order` | 見積もりを確認して選択した注文を提出。 | 書き込み |
| `get_report_results` | 既存のレポート結果を JSON で取得。 | 読み取り専用 |

現行 MCP 実装には、この 7 つのツールが登録されています。業務フロー全体の検証は未完了です。[引数・状態・制限を確認](../tool-catalog.md)。

## Skills

| Skill | 用途 | 公開状況 |
| :--- | :--- | :--- |
| [注文設計 · `order-design`](../../skills/order_design/SKILL.md) | 設計データの提出、カートと見積もりの確認、許可された注文の送信をガイド。 | 同梱済み |
| [HTML レポート · `auto_html_report`](../../skills/auto_html_report/SKILL.md) | 提供された結果 JSON から、集計表・グラフ・利用可能な画像を含む単独ファイルの多言語 HTML レポートを作成。 | 同梱済み |

MCP は呼び出せる操作を提供し、Skills はタスクでの使い方を説明します。Skill のインストールだけでは、サービスの権限取得や MCP 登録は行われません。[一覧を見る →](../../skills/README.md)

<a id="beta"></a>

## Beta Playground

Biointron OS は Beta Playground として順次公開されています。一部の接続は利用できない場合があります。各ステップの実際の結果を確認してください。HTTP の成功やツール名の表示だけでは、業務操作の完了を意味しません。

注文の作成・送信にはユーザーの許可が必要です。書き込みがタイムアウトした場合は、再試行の前に既存の注文状態を確認してください。アクセスや未提供の機能については、アカウントを案内した Biointron の担当者へお問い合わせください。

<a id="online-platform"></a>

## Biointron オンラインプラットフォーム

ブラウザーから Biointron のサービスにアクセスできます。オンラインプラットフォームは RushDATA のプロジェクト作業をまとめ、下書き、カート、注文、AI アシスタントへの入口を提供します。利用可能なサービスやプロジェクト情報を一か所で確認できます。

**[Biointron オンラインプラットフォームへ →](https://ai.biointron.com/#/landing)**

<a href="https://ai.biointron.com/#/landing"><img src="../../assets/Biointron_Rushdata.png" alt="Biointron オンラインプラットフォーム：RushDATA 作業画面、プロジェクトナビゲーション、AI アシスタント" width="1000" /></a>

<a id="faq"></a>

## FAQ

<details>
<summary><strong>MCP と Skills の両方が必要ですか？</strong></summary>

MCP はツールへの接続、Skills はタスクの手順を提供します。Skill 独自の依存関係がある場合もあるため、公開パッケージの要件を確認してください。Skill のダウンロードだけではサービスに接続されません。

</details>

<details>
<summary><strong>ツールが表示されれば、業務で利用できますか？</strong></summary>

表示は登録済みであることを示します。バックエンド設定、アカウント権限、個別操作の検証も必要です。ツール一覧ではこれらを区別しています。

</details>

<details>
<summary><strong>サーバーや業務の実装はどこにありますか？</strong></summary>

このリポジトリは公開接続資料と Skills を配布します。ホストされたサービスと内部の業務実装は別途管理されています。

</details>

## ドキュメント

| 使い始める | リファレンス |
| :--- | :--- |
| [MCP と Skills のインストール](../installation.md) | [MCP ツール一覧](../tool-catalog.md) |
| [Skills 一覧](../../skills/README.md) | [API と JSON サンプル](../api.md) |
| [貢献方法](../../CONTRIBUTING.md) | [ライセンスの状況](../license.md) |

詳細ガイドは中国語と英語で提供しています。

## License

[PolyForm Noncommercial 1.0.0](../../LICENSE) を採用しています。**本ライセンスは商用利用を許可しません**。ソースを公開し、非商用目的での利用を認めています。詳細は[適用範囲と条項](../license.md)をご確認ください。

---

<div align="center">
<sub>Biointron OS · For Agents. For Models. For People.</sub>
</div>
