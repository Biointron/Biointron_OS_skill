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
<a href="README.pl.md" lang="pl" dir="ltr">Polski</a> ·
<a href="README.pt-BR.md" lang="pt-BR" dir="ltr">Português (Brasil)</a> ·
<a href="README.fa.md" lang="fa" dir="rtl">فارسی</a> ·
<a href="README.ar.md" lang="ar" dir="rtl">العربية</a> ·
<a href="README.id.md" lang="id" dir="ltr">Bahasa Indonesia</a> ·
<strong lang="it" dir="ltr">Italiano</strong> ·
<a href="README.el.md" lang="el" dir="ltr">Ελληνικά</a> ·
<a href="README.ml.md" lang="ml" dir="ltr">മലയാളം</a> ·
<a href="README.ur-Latn.md" lang="ur-Latn" dir="ltr">Roman Urdu</a> ·
<a href="README.ro.md" lang="ro" dir="ltr">Română</a>
</p>

# Biointron OS

### Collega il tuo agente AI ai servizi Biointron.

Dalle richieste d'ordine ai risultati dei report, porta i flussi di lavoro Biointron negli strumenti che già usi.<br />
MCP fornisce la connessione. Le Skills guidano il flusso di lavoro. Il controllo resta a te.

[![Catalogo degli strumenti MCP](https://img.shields.io/badge/MCP-tool_catalog-087F8C?style=flat-square)](../../docs/tool-catalog.md)
[![Skills](https://img.shields.io/badge/Agent-Skills-234E70?style=flat-square)](../../skills/README.md)
[![Licenza non commerciale](https://img.shields.io/badge/License-Noncommercial-6B7280?style=flat-square)](../../LICENSE)
[![Beta Playground](https://img.shields.io/badge/Release-Beta_Playground-D7A345?style=flat-square)](#beta)

<br />

<!-- HERO: Keep the artwork path in sync across all language versions. -->
<img src="../../assets/biointron-os-hero.png" alt="Biointron OS" width="1000" />

<br />

**[Inizia](#get-started) · [Strumenti MCP](../../docs/tool-catalog.md) · [Skills](../../skills/README.md) · [API ed esempi](../../docs/api.md) · [Piattaforma online](#online-platform) · [FAQ](#faq)**

</div>

---

## Una piattaforma. Tre modi per connettersi.

Biointron OS è un'interfaccia ai servizi Biointron per agenti AI, modelli e persone. Riunisce l'accesso ai servizi e le istruzioni sui flussi di lavoro, con una roadmap che comprende ordini, invio di progetti, avanzamento e risultati.

| Per gli agenti | Per i modelli | Per le persone |
| :--- | :--- | :--- |
| Individua e richiama servizi tramite **MCP**. | Lavora con **dati strutturati** e interfacce documentate. | Accedi ai flussi di lavoro tramite un'**interfaccia interattiva**. |
| Abbina le chiamate agli strumenti a Skills specifiche per il compito. | Le convenzioni sui dati vengono allineate durante la Beta. | L'esperienza web viene fornita separatamente da questo repository. |

Questo repository è il punto di riferimento pubblico per Skills, guide alla connessione, catalogo degli strumenti ed esempi. I servizi operativi Biointron vengono eseguiti separatamente.

<a id="get-started"></a>

## Inizia

### 1 · Connetti MCP

Ottieni il token di accesso al servizio e le autorizzazioni necessarie dal tuo referente Biointron. In un client MCP che supporta **Streamable HTTP** e **autenticazione Bearer**, aggiungi:

| Impostazione | Valore |
| :--- | :--- |
| Nome | `BiointronOS_MCP` |
| Trasporto | Streamable HTTP |
| URL | `https://mcp-rusta-order-blgdfvompw.cn-shanghai.fcapp.run/mcp` |
| Autenticazione | `Authorization: Bearer <MCP_ACCESS_TOKEN>` |

Nei client che supportano il formato `mcpServers`, integra questa configurazione nelle impostazioni esistenti e sostituisci il segnaposto con il tuo token:

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

I due header di timeout sono elementi personalizzati della configurazione di riferimento: 60000 ms = 60 secondi e 660000 ms = 11 minuti. Hanno effetto solo se il client o il servizio li supporta; inserirli in `headers` non garantisce, da solo, una modifica del tempo di attesa del client. Imposta i timeout secondo la documentazione del client che utilizzi.

Per maggiori dettagli, consulta la [guida all'installazione](../../docs/installation.md#mcp).

### 2 · Aggiungi le Skills

Scegli una delle Skills incluse nel [catalogo delle Skills](../../skills/README.md). Scarica la cartella completa, compresi `references/` e gli eventuali script forniti, e inseriscila nella directory delle Skills del tuo agente. Per Codex e Claude Code, consulta [Installazione delle Skills](../../docs/installation.md#skills).

Entrambi i pacchetti sono ora inclusi nel repository: `skills/order_design/` per `order-design` e `skills/auto_html_report/` per `auto_html_report`. Sono disponibili per il download; la loro presenza non dimostra la validazione completa dei processi operativi.

### 3 · Prova un'introduzione in sola lettura

```text
Elenca gli strumenti MCP Biointron disponibili in questa sessione e spiega cosa fa ciascuno.
Dimmi quali funzionalità sono pronte e quali sono ancora in Beta.
Non creare né inviare ordini.
```

L'individuazione degli strumenti è il primo controllo della connessione. Per completare un'operazione è necessaria la validazione della relativa connessione al backend.

## Catalogo degli strumenti MCP

| Strumento | Scopo | Effetto |
| :--- | :--- | :--- |
| `order_design_preflight` | Verifica l'idoneità dell'azienda e i test disponibili. | Sola lettura |
| `start_order_design` | Invia il file XLSX fornito e attende la conferma del salvataggio del progetto. | Scrive dati operativi |
| `add_order_to_cart` | Aggiunge al carrello un progetto il cui salvataggio è confermato. | Scrive dati operativi |
| `get_order_cart` | Consulta il carrello degli ordini. | Sola lettura |
| `calculate_order_price` | Ottiene un preventivo per gli ordini selezionati. | Sola lettura |
| `submit_verified_order` | Verifica il preventivo e inoltra gli ordini selezionati. | Scrive dati operativi |
| `get_report_results` | Recupera risultati di report esistenti in formato JSON. | Sola lettura |

Questi sette strumenti sono registrati nell'attuale implementazione MCP. La disponibilità operativa dell'intero flusso resta da verificare. Consulta [firme, stato e limiti](../../docs/tool-catalog.md).

## Skills

| Skill | Scopo | Stato del rilascio |
| :--- | :--- | :--- |
| [Progettazione degli ordini · `order-design`](../../skills/order_design/SKILL.md) | Guida l'invio dei progetti, l'aggiunta al carrello, la verifica dei preventivi e l'inoltro degli ordini autorizzati. | Incluso; disponibile per il download |
| [Report dei risultati · `auto_html_report`](../../skills/auto_html_report/SKILL.md) | Genera report HTML autonomi in più lingue dai risultati JSON forniti dall'utente, con tabelle riepilogative, grafici e immagini disponibili. | Incluso; disponibile per il download |

MCP espone le operazioni; le Skills descrivono come un agente le usa per un compito. Installare una Skill non concede l'accesso al servizio né registra automaticamente MCP. [Esplora il catalogo →](../../skills/README.md)

La Skill `auto_html_report` richiede risultati JSON già forniti dall'utente. Non recupera dati dal servizio; il solo identificativo dell'ordine non è sufficiente.

<a id="beta"></a>

## Beta Playground

Biointron OS viene presentato come Beta Playground. Alcune connessioni potrebbero non essere ancora disponibili. Riporta l'esito effettivo di ogni passaggio: una risposta HTTP positiva o il nome di uno strumento visibile non dimostrano che un'operazione sia stata completata.

La creazione e l'invio di ordini richiedono l'autorizzazione dell'utente. Se una scrittura va in timeout, verifica lo stato dell'ordine esistente prima di riprovare. Per l'accesso o una funzionalità non disponibile, contatta il referente Biointron che ti ha fornito l'account.

<a id="online-platform"></a>

## Piattaforma online Biointron

La piattaforma online di Biointron porta i flussi di lavoro dei progetti RushDATA nel browser, con accesso alle bozze dei progetti, al carrello, agli ordini e a un assistente AI. Apri la piattaforma per esplorare i servizi disponibili e consultare le informazioni sui progetti.

[Visita la piattaforma online Biointron →](https://ai.biointron.com/#/landing)

<a href="https://ai.biointron.com/#/landing"><img src="../../assets/Biointron_Rushdata.png" alt="Interfaccia della piattaforma online Biointron con accesso ai progetti RushDATA" width="1000" /></a>

<a id="faq"></a>

## FAQ

<details>
<summary><strong>Mi servono sia MCP sia le Skills?</strong></summary>

MCP fornisce strumenti richiamabili. Le Skills aggiungono istruzioni sui flussi di lavoro e possono avere dipendenze proprie. Segui i requisiti di ogni Skill pubblicata: il solo download di una Skill non collega un servizio.

</details>

<details>
<summary><strong>Se uno strumento è elencato, è pronto per l'uso operativo?</strong></summary>

No. L'individuazione conferma che lo strumento è registrato. Occorre anche validare la configurazione del backend, l'accesso dell'account e l'operazione richiesta. Il catalogo distingue questi stati.

</details>

<details>
<summary><strong>Dove si trovano il server e l'implementazione dei processi operativi?</strong></summary>

Questo repository distribuisce materiali di integrazione pubblici e Skills. Il servizio ospitato e l'implementazione privata dei processi operativi vengono mantenuti separatamente.

</details>

## Documentazione

| Da dove iniziare | Riferimenti |
| :--- | :--- |
| [Installa MCP e Skills](../../docs/installation.md) | [Catalogo degli strumenti MCP](../../docs/tool-catalog.md) |
| [Catalogo delle Skills](../../skills/README.md) | [API ed esempi JSON](../../docs/api.md) |
| [Contribuisci](../../CONTRIBUTING.md) | [Stato della licenza](../../docs/license.md) |

Le guide dettagliate sono disponibili in cinese e in inglese.

## Licenza

Distribuito con licenza [PolyForm Noncommercial 1.0.0](../../LICENSE). **Questa licenza non consente l'uso commerciale.** Il codice sorgente di questo repository è disponibile per uso non commerciale. Consulta [ambito e condizioni](../../docs/license.md).

---

<div align="center">
<sub>Biointron OS · Per gli agenti. Per i modelli. Per le persone.</sub>
</div>

