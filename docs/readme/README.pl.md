<div align="center">

<p dir="ltr">
<a href="../../README.md" lang="en" dir="ltr">English</a> ·
<a href="README.zh-CN.md" lang="zh-CN" dir="ltr">简体中文</a> ·
<a href="README.zh-TW.md" lang="zh-TW" dir="ltr">繁體中文</a> ·
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
<strong lang="pl" dir="ltr">Polski</strong> ·
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

### Połącz swojego agenta AI z usługami Biointron.

Od zapytań o zamówienia po wyniki w raportach — korzystaj z procesów Biointron w narzędziach, których już używasz.<br />
MCP zapewnia połączenie. Skills prowadzą przez proces. Ty zachowujesz kontrolę.

[![Katalog narzędzi MCP](https://img.shields.io/badge/MCP-tool_catalog-087F8C?style=flat-square)](../../docs/tool-catalog.md)
[![Skills](https://img.shields.io/badge/Agent-Skills-234E70?style=flat-square)](../../skills/README.md)
[![Licencja niekomercyjna](https://img.shields.io/badge/License-Noncommercial-6B7280?style=flat-square)](../../LICENSE)
[![Beta Playground](https://img.shields.io/badge/Release-Beta_Playground-D7A345?style=flat-square)](#beta)

<br />

<!-- HERO: Keep the artwork path in sync across all language versions. -->
<img src="../../assets/biointron-os-hero.png" alt="Biointron OS" width="1000" />

<br />

**[Pierwsze kroki](#get-started) · [Narzędzia MCP](../../docs/tool-catalog.md) · [Skills](../../skills/README.md) · [API i przykłady](../../docs/api.md) · [Platforma internetowa](#online-platform) · [Najczęstsze pytania](#faq)**

</div>

---

## Jedna platforma. Trzy sposoby połączenia.

Biointron OS to interfejs dostępu do usług Biointron dla agentów AI, modeli i ludzi. Łączy dostęp do usług z instrukcjami prowadzącymi przez procesy. Plan rozwoju obejmuje zamówienia, przesłane projekty, postępy realizacji i wyniki.

| Dla agentów | Dla modeli | Dla ludzi |
| :--- | :--- | :--- |
| Wykrywaj i wywołuj usługi przez **MCP**. | Pracuj z **danymi strukturalnymi** i udokumentowanymi interfejsami. | Korzystaj z procesów przez **interaktywny interfejs**. |
| Łącz wywołania narzędzi ze Skills przeznaczonymi do konkretnych zadań. | Konwencje danych są uzgadniane w fazie Beta. | Interfejs internetowy jest udostępniany niezależnie od tego repozytorium. |

To repozytorium jest publicznym źródłem Skills, instrukcji połączenia, katalogu narzędzi i przykładów. Usługi biznesowe Biointron działają oddzielnie.

<a id="get-started"></a>

## Pierwsze kroki

### 1 · Połącz MCP

Uzyskaj token dostępu do usługi oraz wymagane uprawnienia od swojego przedstawiciela Biointron. W kliencie MCP obsługującym **Streamable HTTP** i **uwierzytelnianie Bearer** dodaj:

| Ustawienie | Wartość |
| :--- | :--- |
| Nazwa | `BiointronOS_MCP` |
| Transport | Streamable HTTP |
| URL | `https://mcp-rusta-order-blgdfvompw.cn-shanghai.fcapp.run/mcp` |
| Uwierzytelnianie | `Authorization: Bearer <MCP_ACCESS_TOKEN>` |

W klientach obsługujących format `mcpServers` połącz poniższą konfigurację z istniejącymi ustawieniami i zastąp symbol zastępczy własnym tokenem:

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

Dwa nagłówki limitu czasu są niestandardowymi elementami przykładowej konfiguracji: 60000 ms = 60 sekund, a 660000 ms = 11 minut. Działają tylko wtedy, gdy klient lub usługa je obsługuje; samo dodanie ich do `headers` nie gwarantuje zmiany czasu oczekiwania klienta. Limity czasu ustaw zgodnie z dokumentacją używanego klienta.

Szczegóły znajdziesz w [instrukcji instalacji](../../docs/installation.md#mcp).

### 2 · Dodaj Skills

Wybierz opublikowany Skill z [katalogu Skills](../../skills/README.md). Pobierz cały jego folder, łącznie z `references/`, dostarczonymi skryptami i pozostałymi plikami, do których się odwołuje, i umieść go w katalogu Skills swojego agenta. Instrukcje dla Codex i Claude Code znajdziesz w części [instalacja Skills](../../docs/installation.md#skills).

Oba pakiety Skills są dołączone i dostępne do pobrania. `auto-html-report` tworzy raporty lokalnie z już dostarczonych wyników JSON, bez danych uwierzytelniających ani połączenia MCP. Jeśli brakuje JSON, w ramach udzielonej zgody można najpierw pobrać wyniki przez `get_report_results`, używając potwierdzonego numeru zamówienia i ważnego JWT bieżącego klienta, a następnie utworzyć raport. Sam numer zamówienia nie wystarcza. Biointron Account i App Key są używane tylko wtedy, gdy brakuje ważnego JWT; podane już wartości są wykorzystywane ponownie, a pytania dotyczą wyłącznie brakujących. Instrukcje Skill są po angielsku, ale raporty nadal mogą być wielojęzyczne.

### 3 · Zacznij od przeglądu w trybie tylko do odczytu

```text
Wymień narzędzia Biointron MCP dostępne w tej sesji i wyjaśnij, do czego służy każde z nich.
Wskaż, które funkcje są gotowe, a które nadal pozostają w fazie Beta.
Nie twórz ani nie składaj żadnego zamówienia.
```

Wykrywanie narzędzi to pierwszy etap sprawdzania połączenia. Pomyślne wykonanie operacji biznesowej wymaga także zweryfikowanego połączenia z odpowiednim systemem zaplecza.

## Katalog narzędzi MCP

| Narzędzie | Przeznaczenie | Skutek |
| :--- | :--- | :--- |
| `get_order_input_requirements` | Domyślnie zbiera niezależne pytania w partiach; przed zapisem sprawdza wszystkie dane etapu razem za pomocą `mode="validate"`. Nie wymaga biznesowego JWT. | Tylko odczyt |
| `search_order_antigens` | Wyszukuje w katalogu według słowa kluczowego i zwraca rzeczywiste produkty i warianty oraz informacje potrzebne do wczytania dalszych stron. | Tylko odczyt |
| `order_design_preflight` | Sprawdzenie uprawnień firmy i dostępnych badań. | Tylko odczyt |
| `start_order_design` | Przesłanie dostarczonego pliku XLSX i oczekiwanie na potwierdzenie zapisu projektu. | Zapisuje dane biznesowe |
| `get_order_design_result` | Po wyborze klienta pobiera w trybie tylko do odczytu i udostępnia rzeczywisty HTML zapisanego projektu. | Tylko odczyt |
| `add_order_to_cart` | Dodanie projektu z potwierdzonym zapisem do koszyka. | Zapisuje dane biznesowe |
| `end_order_workflow` | Polecić klientowi odrzucenie lokalnego kontekstu bez unieważniania podpisu ani anulowania zamówienia. | Tylko instrukcja dla klienta |
| `get_order_cart` | Odczyt koszyka zamówień. | Tylko odczyt |
| `calculate_order_price` | Pobranie wyceny wybranych zamówień. | Tylko odczyt |
| `submit_verified_order` | Ponownie weryfikuje wycenę i przesyła wybrane zamówienia do zatwierdzenia przez człowieka. | Zapisuje dane biznesowe |
| `get_report_results` | Pobranie wyników istniejących raportów w formacie JSON. | Tylko odczyt |

W obecnej implementacji MCP zarejestrowano 11 narzędzi: 10 wymaga biznesowego JWT bieżącego klienta; `get_order_input_requirements` działa lokalnie bez tego JWT. Wdrożenie oraz działanie procesów biznesowych od początku do końca nadal wymagają weryfikacji. Zobacz [sygnatury, stan i ograniczenia](../../docs/tool-catalog.md).

## Skills

| Skill | Przeznaczenie | Stan publikacji |
| :--- | :--- | :--- |
| [Projektowanie zamówień · `order-design`](../../skills/order_design/SKILL.md) | Wyjaśnia pakiety, zbiera dane partiami, pomaga wybrać produkty z katalogu, oferuje podgląd HTML po zapisaniu projektu oraz prowadzi przez koszyk, wycenę i przesłanie do zatwierdzenia przez człowieka. | Dołączono · Dostępny do pobrania |
| [Raport wyników · `auto-html-report`](../../skills/auto_html_report/SKILL.md) | Tworzy samodzielne, wielojęzyczne raporty HTML z tabelą podsumowującą, wykresami i dostępnymi obrazami na podstawie dostarczonych wyników JSON lub wyników pobranych w autoryzowanym zapytaniu. | Dołączono · Dostępny do pobrania |

Przesłanie zamówienia nie oznacza rozpoczęcia produkcji ani zakończenia eksperymentu. Produkcja rozpoczyna się dopiero po potwierdzeniu przez Biointron.

MCP udostępnia operacje, a Skills opisują, jak agent korzysta z nich w ramach zadania. Instalacja Skill nie przyznaje dostępu do usługi i nie rejestruje automatycznie MCP. [Przeglądaj katalog →](../../skills/README.md)

<a id="beta"></a>

## Beta Playground

Biointron OS jest wprowadzany jako środowisko testowe Beta. Niektóre połączenia mogą być jeszcze niedostępne. Podawaj rzeczywisty wynik każdego kroku; poprawna odpowiedź HTTP ani widoczna nazwa narzędzia nie dowodzą zakończenia operacji biznesowej.

Tworzenie i składanie zamówień wymaga upoważnienia użytkownika. Jeśli operacja zapisu przekroczy limit czasu, sprawdź stan istniejącego zamówienia przed ponowieniem próby. W sprawie dostępu lub niedostępnej funkcji skontaktuj się z przedstawicielem Biointron, który udostępnił Ci konto.

<a id="online-platform"></a>

## Platforma internetowa Biointron

Platforma internetowa Biointron przenosi procesy projektów RushDATA do przeglądarki, zapewniając dostęp do szkiców projektów, koszyka, zamówień i asystenta AI. Otwórz platformę, aby poznać dostępne usługi i przeglądać informacje o projektach.

[Odwiedź platformę internetową Biointron →](https://ai.biointron.com/#/landing)

<a href="https://ai.biointron.com/#/landing"><img src="../../assets/Biointron_Rushdata.png" alt="Interfejs projektów RushDATA na platformie internetowej Biointron" width="1000" /></a>

<a id="faq"></a>

## Najczęstsze pytania

<details>
<summary><strong>Czy potrzebuję zarówno MCP, jak i Skills?</strong></summary>

MCP dostarcza narzędzia, które można wywoływać. Skills dodają instrukcje procesów i mogą mieć własne zależności. Kieruj się wymaganiami każdego opublikowanego Skill; samo pobranie Skill nie łączy z usługą.

</details>

<details>
<summary><strong>Czy obecność narzędzia na liście oznacza gotowość do użytku biznesowego?</strong></summary>

Nie. Wykrycie potwierdza rejestrację narzędzia. Należy też zweryfikować konfigurację systemu zaplecza, dostęp do konta i żądaną operację. Katalog uwzględnia to rozróżnienie.

</details>

<details>
<summary><strong>Gdzie znajdują się serwer i implementacja logiki biznesowej?</strong></summary>

To repozytorium udostępnia publiczne materiały integracyjne i Skills. Usługa hostowana i prywatna implementacja logiki biznesowej są utrzymywane oddzielnie.

</details>

## Dokumentacja

| Zacznij tutaj | Materiały referencyjne |
| :--- | :--- |
| [Instalacja MCP i Skills](../../docs/installation.md) | [Katalog narzędzi MCP](../../docs/tool-catalog.md) |
| [Katalog Skills](../../skills/README.md) | [API i przykłady JSON](../../docs/api.md) |
| [Współpraca](../../CONTRIBUTING.md) | [Stan licencji](../../docs/license.md) |

Szczegółowe instrukcje są dostępne po chińsku i angielsku.

## Licencja

Udostępniono na licencji [PolyForm Noncommercial 1.0.0](../../LICENSE). **Ta licencja nie zezwala na wykorzystanie komercyjne.** Kod źródłowy tego repozytorium jest dostępny do użytku niekomercyjnego. Zobacz [zakres i warunki](../../docs/license.md).

---

<div align="center">
<sub>Biointron OS · Dla agentów. Dla modeli. Dla ludzi.</sub>
</div>
