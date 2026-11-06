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
<strong lang="de" dir="ltr">Deutsch</strong> ·
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

### Verbinden Sie Ihren KI-Agenten mit den Diensten von Biointron.

Von der Bestellanfrage bis zu den Berichtsergebnissen: Nutzen Sie Biointron-Abläufe in den Werkzeugen, mit denen Sie bereits arbeiten.<br />
MCP stellt die Verbindung her. Skills leiten den Ablauf. Sie behalten die Kontrolle.

[![MCP-Werkzeugkatalog](https://img.shields.io/badge/MCP-tool_catalog-087F8C?style=flat-square)](../../docs/tool-catalog.md)
[![Skills](https://img.shields.io/badge/Agent-Skills-234E70?style=flat-square)](../../skills/README.md)
[![Lizenz für nichtkommerzielle Nutzung](https://img.shields.io/badge/License-Noncommercial-6B7280?style=flat-square)](../../LICENSE)
[![Beta Playground](https://img.shields.io/badge/Release-Beta_Playground-D7A345?style=flat-square)](#beta)

<br />

<!-- HERO: Keep the artwork path in sync across all language versions. -->
<img src="../../assets/biointron-os-hero.png" alt="Biointron OS" width="1000" />

<br />

**[Erste Schritte](#get-started) · [MCP-Werkzeuge](../../docs/tool-catalog.md) · [Skills](../../skills/README.md) · [API und Beispiele](../../docs/api.md) · [Online-Plattform](#online-platform) · [Häufige Fragen](#faq)**

</div>

---

## Eine Plattform. Drei Wege zur Verbindung.

Biointron OS bietet KI-Agenten, Modellen und Menschen eine Schnittstelle zu den Diensten von Biointron. Es verbindet den Dienstzugang mit Anleitungen für Arbeitsabläufe. Die geplante Entwicklung umfasst Bestellungen, eingereichte Entwurfsdaten, den Fortschritt und die Ergebnisse.

| Für Agenten | Für Modelle | Für Menschen |
| :--- | :--- | :--- |
| Dienste über **MCP** ermitteln und aufrufen. | Mit **strukturierten Daten** und dokumentierten Schnittstellen arbeiten. | Über eine **interaktive Oberfläche** auf Arbeitsabläufe zugreifen. |
| Werkzeugaufrufe mit aufgabenspezifischen Skills kombinieren. | Die Datenkonventionen werden während der Beta-Phase abgestimmt. | Die Weboberfläche wird getrennt von diesem Repository bereitgestellt. |

Dieses Repository ist die öffentliche Anlaufstelle für Skills, Verbindungsanleitungen, den Werkzeugkatalog und Beispiele. Die Geschäftsdienste von Biointron werden separat betrieben.

<a id="get-started"></a>

## Erste Schritte

### 1 · MCP verbinden

Das Zugriffstoken für den Dienst und die Nutzungsberechtigung erhalten Sie von Ihrer Kontaktperson bei Biointron. Fügen Sie in einem MCP-Client, der **Streamable HTTP** und **Bearer-Authentifizierung** unterstützt, folgende Angaben hinzu:

| Einstellung | Wert |
| :--- | :--- |
| Name | `BiointronOS_MCP` |
| Transport | Streamable HTTP |
| URL | `https://mcp-rusta-order-blgdfvompw.cn-shanghai.fcapp.run/mcp` |
| Authentifizierung | `Authorization: Bearer <MCP_ACCESS_TOKEN>` |

In Clients, die das Format `mcpServers` unterstützen, können Sie die folgende Konfiguration mit Ihren vorhandenen Einstellungen zusammenführen. Ersetzen Sie den Token-Platzhalter durch Ihr eigenes Token.

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

Die beiden Timeout-Header sind benutzerdefinierte Angaben dieser Beispielkonfiguration: 60000 Millisekunden entsprechen 60 Sekunden, 660000 Millisekunden entsprechen 11 Minuten. Sie wirken nur, wenn der Client oder Dienst diese Header unterstützt. Das bloße Eintragen unter `headers` garantiert keine Änderung der Wartezeit des Clients; richten Sie die konkreten Einstellungen nach dessen Dokumentation ein.

Weitere Hinweise finden Sie in der [Installationsanleitung](../../docs/installation.md#mcp).

### 2 · Skills hinzufügen

Wählen Sie einen veröffentlichten Skill aus dem [Skill-Katalog](../../skills/README.md). Laden Sie den vollständigen Ordner einschließlich `references/`, mitgelieferter Skripte und weiterer referenzierter Dateien herunter und legen Sie ihn im Skill-Verzeichnis Ihres Agenten ab. Die Schritte für Codex und Claude Code finden Sie unter [Skills installieren](../../docs/installation.md#skills).

Beide Skill-Pakete sind enthalten und können heruntergeladen werden. `auto-html-report` erstellt Berichte lokal aus bereits bereitgestellten Ergebnis-JSONs; dafür sind weder Zugangsdaten noch eine MCP-Verbindung erforderlich. Fehlt das JSON, können mit entsprechender Autorisierung zuerst die bestätigte Auftragsnummer und das gültige JWT des aktuellen Kunden an `get_report_results` übergeben und anschließend die Ergebnisse als Bericht aufbereitet werden. Eine Auftragsnummer allein genügt nicht. Biointron Account und App Key werden nur benötigt, wenn kein gültiges JWT vorliegt; vorhandene Angaben werden wiederverwendet und nur fehlende erfragt. Die Skill-Anweisungen sind auf Englisch, die Berichte können weiterhin mehrsprachig erstellt werden.

### 3 · Mit einer schreibgeschützten Einführung beginnen

```text
Liste die in dieser Sitzung verfügbaren Biointron-MCP-Werkzeuge auf und erkläre ihre jeweilige Funktion.
Sage mir, welche Funktionen einsatzbereit sind und welche sich noch in der Beta-Phase befinden.
Erstelle keine Bestellung und reiche keine Bestellung ein.
```

Die Werkzeugerkennung ist die erste Verbindungsprüfung. Eine erfolgreiche Geschäftsoperation setzt zusätzlich eine geprüfte Verbindung zum jeweiligen Backend voraus.

## MCP-Werkzeugkatalog

| Werkzeug | Zweck | Auswirkung |
| :--- | :--- | :--- |
| `get_order_input_requirements` | Standardmäßig unabhängige Fragen in Gruppen sammeln; vor einem Schreibvorgang alle Eingaben der Phase gemeinsam mit `mode="validate"` prüfen. Kein Geschäfts-JWT erforderlich. | Nur lesend |
| `search_order_antigens` | Den Produktkatalog nach Stichwort durchsuchen; tatsächliche Produkte und Varianten sowie Angaben für weitere Ergebnisseiten liefern. | Nur lesend |
| `order_design_preflight` | Unternehmensberechtigung und verfügbare Testpositionen prüfen. | Nur lesend |
| `start_order_design` | Die bereitgestellte XLSX-Datei senden und die bestätigte Speicherung des Entwurfs abwarten. | Schreibt Geschäftsdaten |
| `get_order_design_result` | Nach Auswahl durch den Kunden das tatsächliche HTML des gespeicherten Entwurfs schreibgeschützt abrufen und bereitstellen. | Nur lesend |
| `add_order_to_cart` | Einen bestätigt gespeicherten Entwurf zum Warenkorb hinzufügen. | Schreibt Geschäftsdaten |
| `end_order_workflow` | Client zum Verwerfen des lokalen Kontexts auffordern; keine Signatur widerrufen oder Bestellung stornieren. | Nur Client-Anweisung |
| `get_order_cart` | Den Bestellwarenkorb lesen. | Nur lesend |
| `calculate_order_price` | Ein Angebot für ausgewählte Bestellungen abrufen. | Nur lesend |
| `submit_verified_order` | Angebot erneut prüfen und ausgewählte Bestellungen zur Bestätigung durch einen Menschen einreichen. | Schreibt Geschäftsdaten |
| `get_report_results` | Vorhandene Berichtsergebnisse als JSON abrufen. | Nur lesend |

Die aktuelle MCP-Implementierung registriert 11 Werkzeuge: 10 benötigen das Geschäfts-JWT des aktuellen Kunden; `get_order_input_requirements` arbeitet lokal ohne dieses JWT. Die Bereitstellung und die durchgängige Funktionsfähigkeit der Geschäftsabläufe müssen weiterhin geprüft werden. Siehe [Signaturen, Status und Einschränkungen](../../docs/tool-catalog.md).

## Skills

| Skill | Zweck | Veröffentlichungsstatus |
| :--- | :--- | :--- |
| [Auftragsdesign · `order-design`](../../skills/order_design/SKILL.md) | Pakete erläutern, Angaben in Gruppen sammeln, die Produktauswahl begleiten, nach dem Speichern optional das Entwurfs-HTML anzeigen sowie Warenkorb, Angebot und Einreichung zur menschlichen Bestätigung bearbeiten. | Enthalten · Zum Download verfügbar |
| [Ergebnisbericht · `auto-html-report`](../../skills/auto_html_report/SKILL.md) | Aus vorhandenen oder autorisiert abgerufenen Ergebnis-JSONs eigenständige mehrsprachige HTML-Berichte mit Übersichtstabelle, Diagrammen und verfügbaren Bildern erstellen. | Enthalten · Zum Download verfügbar |

Das Einreichen einer Bestellung bedeutet weder den Beginn der Produktion noch den Abschluss eines Experiments. Die Produktion beginnt erst nach der Bestätigung durch Biointron.

MCP stellt Operationen bereit; Skills beschreiben, wie ein Agent diese innerhalb einer Aufgabe verwendet. Die Installation eines Skills gewährt keinen Dienstzugang und registriert MCP nicht automatisch. [Katalog ansehen →](../../skills/README.md)

<a id="beta"></a>

## Beta Playground

Biointron OS wird als Beta-Testumgebung eingeführt. Einige Verbindungen sind möglicherweise noch nicht verfügbar. Geben Sie das tatsächliche Ergebnis jedes Schritts an; eine erfolgreiche HTTP-Antwort oder ein sichtbarer Werkzeugname belegt nicht, dass eine Geschäftsoperation abgeschlossen wurde.

Das Erstellen und Einreichen von Bestellungen erfordert die Autorisierung durch den Nutzer. Wird bei einem Schreibvorgang das Zeitlimit überschritten, prüfen Sie den bestehenden Bestellstatus, bevor Sie es erneut versuchen. Bei Fragen zum Zugang oder zu einer nicht verfügbaren Funktion wenden Sie sich an die Biointron-Kontaktperson, die Ihr Konto bereitgestellt hat.

<a id="online-platform"></a>

## Biointron Online-Plattform

Die Online-Plattform von Biointron bringt RushDATA-Projektabläufe in den Browser und bietet Zugang zu Projektentwürfen, Warenkorb, Bestellungen und einem KI-Assistenten. Öffnen Sie die Plattform, um verfügbare Dienste zu entdecken und Projektinformationen einzusehen.

[Biointron Online-Plattform besuchen →](https://ai.biointron.com/#/landing)

<a href="https://ai.biointron.com/#/landing"><img src="../../assets/Biointron_Rushdata.png" alt="RushDATA-Projektoberfläche auf der Biointron Online-Plattform" width="1000" /></a>

<a id="faq"></a>

## Häufige Fragen

<details>
<summary><strong>Brauche ich sowohl MCP als auch Skills?</strong></summary>

MCP stellt aufrufbare Werkzeuge bereit. Skills ergänzen Anweisungen für Arbeitsabläufe und können eigene Abhängigkeiten haben. Beachten Sie die Anforderungen des jeweiligen veröffentlichten Skills; der Download eines Skills allein verbindet noch keinen Dienst.

</details>

<details>
<summary><strong>Ist ein aufgelistetes Werkzeug bereits für den Geschäftsbetrieb einsatzbereit?</strong></summary>

Nein. Die Erkennung bestätigt, dass das Werkzeug registriert ist. Die Backend-Konfiguration, der Kontozugriff und die angeforderte Operation müssen ebenfalls geprüft werden. Der Katalog hält diese Unterscheidung fest.

</details>

<details>
<summary><strong>Wo befinden sich der Server und die Implementierung der Geschäftslogik?</strong></summary>

Dieses Repository stellt öffentliche Integrationsunterlagen und Skills bereit. Der gehostete Dienst und die private Implementierung der Geschäftslogik werden separat gepflegt.

</details>

## Dokumentation

| Einstieg | Referenz |
| :--- | :--- |
| [MCP und Skills installieren](../../docs/installation.md) | [MCP-Werkzeugkatalog](../../docs/tool-catalog.md) |
| [Skill-Katalog](../../skills/README.md) | [API und JSON-Beispiele](../../docs/api.md) |
| [Mitwirken](../../CONTRIBUTING.md) | [Lizenzstatus](../../docs/license.md) |

Ausführliche Anleitungen stehen auf Chinesisch und Englisch zur Verfügung.

## Lizenz

Lizenziert unter [PolyForm Noncommercial 1.0.0](../../LICENSE). **Diese Lizenz erlaubt keine kommerzielle Nutzung.** Der Quellcode dieses Repositorys ist für die nichtkommerzielle Nutzung zugänglich. Siehe [Geltungsbereich und Bedingungen](../../docs/license.md).

---

<div align="center">
<sub>Biointron OS · Für Agenten. Für Modelle. Für Menschen.</sub>
</div>
