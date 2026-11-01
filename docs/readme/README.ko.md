<div align="center">

<p dir="ltr">
<a href="../../README.md" lang="en" dir="ltr">English</a> ·
<a href="README.zh-CN.md" lang="zh-CN" dir="ltr">简体中文</a> ·
<a href="README.zh-TW.md" lang="zh-TW" dir="ltr">繁體中文</a> ·
<a href="README.ja.md" lang="ja" dir="ltr">日本語</a> ·
<strong lang="ko" dir="ltr">한국어</strong> ·
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

### AI 에이전트를 Biointron 서비스에 연결하세요.

주문 요청부터 결과 확인까지, 평소 사용하는 도구에서 Biointron 워크플로를 이용하세요.<br />
MCP가 연결을 제공하고, Skills가 작업 절차를 안내합니다. 모든 결정은 사용자가 내립니다.

[![MCP 도구 목록](https://img.shields.io/badge/MCP-tool_catalog-087F8C?style=flat-square)](../../docs/tool-catalog.md)
[![Skills](https://img.shields.io/badge/Agent-Skills-234E70?style=flat-square)](../../skills/README.md)
[![비상업적 이용 라이선스](https://img.shields.io/badge/License-Noncommercial-6B7280?style=flat-square)](../../LICENSE)
[![Beta Playground](https://img.shields.io/badge/Release-Beta_Playground-D7A345?style=flat-square)](#beta)

<br />

<!-- HERO: Keep the artwork path in sync across all language versions. -->
<img src="../../assets/biointron-os-hero.png" alt="Biointron OS" width="1000" />

<br />

**[시작하기](#get-started) · [MCP 도구](../../docs/tool-catalog.md) · [Skills](../../skills/README.md) · [API 및 예제](../../docs/api.md) · [온라인 플랫폼](#online-platform) · [자주 묻는 질문](#faq)**

</div>

---

## 하나의 플랫폼, 세 가지 연결 방식.

Biointron OS는 AI 에이전트, 모델, 사용자를 위한 Biointron 서비스 인터페이스입니다. 서비스 접근과 워크플로 안내를 한곳에 모으며, 주문, 설계 제출, 진행 상황, 결과를 아우르는 로드맵을 갖고 있습니다.

| 에이전트를 위해 | 모델을 위해 | 사용자를 위해 |
| :--- | :--- | :--- |
| **MCP**로 서비스를 검색하고 호출합니다. | **구조화된 데이터**와 문서화된 인터페이스를 사용합니다. | **대화형 인터페이스**에서 워크플로를 이용합니다. |
| 도구 호출에 작업별 Skills를 함께 사용합니다. | Beta 기간 동안 데이터 규약을 조율하고 있습니다. | 웹 서비스는 이 저장소와 별도로 제공됩니다. |

이 저장소는 Skills, 연결 가이드, 도구 목록, 예제를 공개하는 공간입니다. Biointron의 업무 서비스는 별도로 운영됩니다.

<a id="get-started"></a>

## 시작하기

### 1 · MCP 연결

Biointron 담당자에게 서비스 액세스 토큰과 사용 권한을 요청하세요. **Streamable HTTP**와 **Bearer 인증**을 지원하는 MCP 클라이언트에 다음 정보를 추가합니다.

| 설정 | 값 |
| :--- | :--- |
| 이름 | `BiointronOS_MCP` |
| 전송 방식 | Streamable HTTP |
| URL | `https://mcp-rusta-order-blgdfvompw.cn-shanghai.fcapp.run/mcp` |
| 인증 | `Authorization: Bearer <MCP_ACCESS_TOKEN>` |

`mcpServers` 형식을 지원하는 클라이언트에서는 아래 구성을 기존 설정에 병합하고 토큰 자리표시자를 자신의 토큰으로 바꿀 수 있습니다.

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

두 타임아웃 헤더는 참고 구성의 사용자 정의 항목입니다. 60000밀리초는 60초이고, 660000밀리초는 11분입니다. 클라이언트 또는 서비스가 이 헤더를 지원할 때만 해당 효과가 적용됩니다. `headers`에 추가하는 것만으로 클라이언트의 대기 시간이 변경된다고 보장할 수 없으므로, 구체적인 설정은 클라이언트 문서를 따르세요.

자세한 설정 방법은 [설치 가이드](../../docs/installation.md#mcp)를 참조하세요.

### 2 · Skills 추가

[Skills 목록](../../skills/README.md)에서 배포된 Skill을 선택하세요. `references/`와 제공된 스크립트 등 참조 파일을 포함한 전체 폴더를 다운로드하고 에이전트의 Skill 디렉터리에 넣으세요. Codex와 Claude Code의 설정 방법은 [Skill 설치](../../docs/installation.md#skills)를 참고하세요.

두 Skill 패키지가 이 저장소에 포함되어 있으며 다운로드할 수 있습니다. `auto_html_report`는 사용자가 제공한 기존 결과 JSON을 입력으로 사용합니다. 서비스에서 데이터를 가져오는 기능은 담당하지 않으므로 주문 번호만으로는 보고서를 만들 수 없습니다.

### 3 · 읽기 전용으로 먼저 살펴보기

```text
이 세션에서 사용할 수 있는 Biointron MCP 도구를 나열하고 각 도구의 용도를 설명해 주세요.
어떤 기능이 준비되어 있고 어떤 기능이 아직 Beta 단계인지 알려 주세요.
주문을 생성하거나 제출하지 마세요.
```

도구 검색은 연결을 확인하는 첫 단계입니다. 실제 업무 작업이 성공하려면 해당 백엔드 연결도 검증되어야 합니다.

## MCP 도구 목록

| 도구 | 용도 | 영향 |
| :--- | :--- | :--- |
| `order_design_preflight` | 회사 자격과 이용 가능한 검사 항목을 확인합니다. | 읽기 전용 |
| `start_order_design` | 제공된 XLSX를 제출하고 설계 저장 확인을 기다립니다. | 업무 데이터 쓰기 |
| `add_order_to_cart` | 저장이 확인된 설계를 장바구니에 추가합니다. | 업무 데이터 쓰기 |
| `get_order_cart` | 주문 장바구니를 조회합니다. | 읽기 전용 |
| `calculate_order_price` | 선택한 주문의 견적을 조회합니다. | 읽기 전용 |
| `submit_verified_order` | 견적을 확인한 뒤 선택한 주문을 제출합니다. | 업무 데이터 쓰기 |
| `get_report_results` | 기존 보고서 결과를 JSON으로 가져옵니다. | 읽기 전용 |

현재 MCP 구현에는 이 일곱 가지 도구가 등록되어 있습니다. 전체 업무 흐름을 실제로 사용할 수 있는지는 아직 검증이 필요합니다. [함수 시그니처, 상태, 제한 사항](../../docs/tool-catalog.md)을 확인하세요.

## Skills

| Skill | 용도 | 배포 상태 |
| :--- | :--- | :--- |
| [주문 설계 · `order-design`](../../skills/order_design/SKILL.md) | 주문 요청, 설계 제출, 주문 제출을 안내합니다. | 포함됨 · 다운로드 가능 |
| [결과 보고서 · `auto_html_report`](../../skills/auto_html_report/SKILL.md) | 사용자가 제공한 기존 결과 JSON으로 요약표, 차트, 사용 가능한 이미지를 포함하는 독립형 다국어 HTML 보고서를 생성합니다. | 포함됨 · 다운로드 가능 |

MCP는 호출 가능한 작업을 제공하고, Skills는 에이전트가 작업 중 이를 사용하는 방법을 설명합니다. Skill을 설치해도 서비스 접근 권한이 부여되거나 MCP가 자동으로 등록되지는 않습니다. [목록 보기 →](../../skills/README.md)

<a id="beta"></a>

## Beta Playground

Biointron OS는 Beta Playground 형태로 도입되고 있습니다. 일부 연결은 아직 사용할 수 없을 수 있습니다. 각 단계의 실제 결과를 보고해야 합니다. HTTP 성공 응답이나 도구 이름의 표시만으로 업무 작업이 완료되었다고 판단할 수 없습니다.

주문 생성과 제출에는 사용자 승인이 필요합니다. 쓰기 작업이 시간 초과되면 재시도 전에 기존 주문 상태를 확인하세요. 접근 권한이나 사용할 수 없는 기능에 대해서는 계정을 제공한 Biointron 담당자에게 문의하세요.

<a id="online-platform"></a>

## Biointron 온라인 플랫폼

Biointron 온라인 플랫폼은 RushDATA 프로젝트 워크플로를 브라우저에서 제공하며, 프로젝트 초안, 장바구니, 주문 및 AI 어시스턴트에 접근할 수 있습니다. 플랫폼을 열어 제공되는 서비스를 살펴보고 프로젝트 정보를 확인하세요.

[Biointron 온라인 플랫폼 방문하기 →](https://ai.biointron.com/#/landing)

<a href="https://ai.biointron.com/#/landing"><img src="../../assets/Biointron_Rushdata.png" alt="Biointron 온라인 플랫폼의 RushDATA 프로젝트 인터페이스" width="1000" /></a>

<a id="faq"></a>

## 자주 묻는 질문

<details>
<summary><strong>MCP와 Skills가 모두 필요한가요?</strong></summary>

MCP는 호출 가능한 도구를 제공합니다. Skills는 워크플로 지침을 추가하며 자체 의존성이 있을 수 있습니다. 배포된 각 Skill의 요구 사항을 따르세요. Skill을 다운로드하는 것만으로 서비스가 연결되지는 않습니다.

</details>

<details>
<summary><strong>도구가 목록에 있으면 실제 업무에 사용할 준비가 된 것인가요?</strong></summary>

아닙니다. 도구 검색은 등록 여부만 확인합니다. 백엔드 설정, 계정 접근 권한, 요청한 작업도 검증해야 합니다. 도구 목록은 이러한 차이를 구분해 안내합니다.

</details>

<details>
<summary><strong>서버와 업무 구현 코드는 어디에 있나요?</strong></summary>

이 저장소는 공개 통합 자료와 Skills를 배포합니다. 호스팅 서비스와 비공개 업무 구현은 별도로 유지 관리됩니다.

</details>

## 문서

| 시작 안내 | 참고 자료 |
| :--- | :--- |
| [MCP 및 Skills 설치](../../docs/installation.md) | [MCP 도구 목록](../../docs/tool-catalog.md) |
| [Skills 목록](../../skills/README.md) | [API 및 JSON 예제](../../docs/api.md) |
| [기여하기](../../CONTRIBUTING.md) | [라이선스 상태](../../docs/license.md) |

상세 가이드는 중국어와 영어로 제공됩니다.

## 라이선스

[PolyForm Noncommercial 1.0.0](../../LICENSE)에 따라 배포됩니다. **이 라이선스는 상업적 이용을 허용하지 않습니다.** 이 저장소는 비상업적 이용을 위해 소스를 공개합니다. [적용 범위 및 조건](../../docs/license.md)을 확인하세요.

---

<div align="center">
<sub>Biointron OS · 에이전트를 위해. 모델을 위해. 사용자를 위해.</sub>
</div>
