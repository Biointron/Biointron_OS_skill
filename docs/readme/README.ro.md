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
<a href="README.it.md" lang="it" dir="ltr">Italiano</a> ·
<a href="README.el.md" lang="el" dir="ltr">Ελληνικά</a> ·
<a href="README.ml.md" lang="ml" dir="ltr">മലയാളം</a> ·
<a href="README.ur-Latn.md" lang="ur-Latn" dir="ltr">Roman Urdu</a> ·
<strong lang="ro" dir="ltr">Română</strong>
</p>

# Biointron OS

### Conectează-ți agentul AI la serviciile Biointron.

De la solicitarea unei comenzi până la obținerea rezultatelor, integrează fluxurile Biointron în instrumentele pe care le folosești deja.<br />
MCP asigură conexiunea. Skills ghidează fluxul de lucru. Tu păstrezi controlul.

[![Catalog de instrumente MCP](https://img.shields.io/badge/MCP-tool_catalog-087F8C?style=flat-square)](../../docs/tool-catalog.md)
[![Skills](https://img.shields.io/badge/Agent-Skills-234E70?style=flat-square)](../../skills/README.md)
[![Licență necomercială](https://img.shields.io/badge/License-Noncommercial-6B7280?style=flat-square)](../../LICENSE)
[![Beta Playground](https://img.shields.io/badge/Release-Beta_Playground-D7A345?style=flat-square)](#beta)

<br />

<!-- HERO: Keep the artwork path in sync across all language versions. -->
<img src="../../assets/biointron-os-hero.png" alt="Biointron OS" width="1000" />

<br />

**[Primii pași](#get-started) · [Instrumente MCP](../../docs/tool-catalog.md) · [Skills](../../skills/README.md) · [API și exemple](../../docs/api.md) · [Platforma online](#online-platform) · [Întrebări frecvente](#faq)**

</div>

---

## O platformă. Trei moduri de conectare.

Biointron OS este o interfață către serviciile Biointron pentru agenți AI, modele și oameni. Reunește accesul la servicii și îndrumarea pentru fluxurile de lucru, cu un plan de dezvoltare care acoperă comenzile, proiectele trimise, progresul și rezultatele.

| Pentru agenți | Pentru modele | Pentru oameni |
| :--- | :--- | :--- |
| Descoperă și apelează servicii prin **MCP**. | Lucrează cu **date structurate** și interfețe documentate. | Accesează fluxurile printr-o **interfață interactivă**. |
| Combină apelurile de instrumente cu Skills specifice fiecărei sarcini. | Convențiile privind datele sunt în curs de armonizare în etapa Beta. | Experiența web este oferită separat de acest depozit. |

Acest depozit este punctul public de acces la Skills, ghiduri de conectare, catalogul de instrumente și exemple. Serviciile operaționale Biointron rulează separat.

<a id="get-started"></a>

## Primii pași

### 1 · Conectează MCP

Obține tokenul de acces la serviciu și permisiunea de utilizare de la persoana ta de contact Biointron. Într-un client MCP care acceptă **Streamable HTTP** și **autentificare Bearer**, adaugă:

| Setare | Valoare |
| :--- | :--- |
| Nume | `BiointronOS_MCP` |
| Transport | Streamable HTTP |
| URL | `https://mcp-rusta-order-blgdfvompw.cn-shanghai.fcapp.run/mcp` |
| Autentificare | `Authorization: Bearer <MCP_ACCESS_TOKEN>` |

În clienții care acceptă formatul `mcpServers`, poți îmbina configurația de mai jos cu setările existente și înlocui textul substituent al tokenului cu propriul token.

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

Cele două antete pentru timpul de așteptare sunt câmpuri personalizate ale configurației de referință: 60000 de milisecunde înseamnă 60 de secunde, iar 660000 de milisecunde înseamnă 11 minute. Ele au efectul corespunzător numai dacă sunt acceptate de client sau de serviciu. Simpla includere în `headers` nu garantează modificarea timpului de așteptare al clientului; urmează documentația clientului pentru setările concrete.

Pentru detalii despre configurare, consultă [ghidul de instalare](../../docs/installation.md#mcp).

### 2 · Adaugă Skills

Alege unul dintre pachetele Skill incluse în [catalogul Skills](../../skills/README.md). Descarcă întregul folder, inclusiv `references/` și orice scripturi furnizate, și plasează-l în directorul Skills al agentului tău. Consultă [instalarea Skills](../../docs/installation.md#skills) pentru Codex și Claude Code.

Ambele pachete sunt acum incluse în acest depozit: `skills/order_design/` pentru `order-design` și `skills/auto_html_report/` pentru `auto_html_report`. Sunt disponibile pentru descărcare; prezența lor nu confirmă validarea completă a fluxurilor operaționale.

### 3 · Începe cu o verificare fără modificări

```text
Enumeră instrumentele MCP Biointron disponibile în această sesiune și explică rolul fiecăruia.
Spune-mi ce funcții sunt pregătite și care sunt încă în etapa Beta.
Nu crea și nu trimite nicio comandă.
```

Descoperirea instrumentelor este primul pas de verificare a conexiunii. Reușita unei operațiuni necesită validarea conexiunii la serviciul backend corespunzător.

## Catalog de instrumente MCP

| Instrument | Scop | Efect |
| :--- | :--- | :--- |
| `order_design_preflight` | Verifică eligibilitatea companiei și testele disponibile. | Doar citire |
| `start_order_design` | Trimite fișierul XLSX furnizat și așteaptă confirmarea salvării proiectului. | Scrie date operaționale |
| `add_order_to_cart` | Adaugă în coș un proiect a cărui salvare este confirmată. | Scrie date operaționale |
| `get_order_cart` | Citește coșul de comenzi. | Doar citire |
| `calculate_order_price` | Obține oferta de preț pentru comenzile selectate. | Doar citire |
| `submit_verified_order` | Verifică oferta și trimite comenzile selectate. | Scrie date operaționale |
| `get_report_results` | Obține rezultatele rapoartelor existente în format JSON. | Doar citire |

Aceste șapte instrumente sunt înregistrate în implementarea MCP actuală. Funcționarea completă a fluxurilor operaționale rămâne de verificat. Consultă [semnăturile, starea și limitele](../../docs/tool-catalog.md).

## Skills

| Skill | Scop | Starea publicării |
| :--- | :--- | :--- |
| [Proiectarea comenzilor · `order-design`](../../skills/order_design/SKILL.md) | Ghidează trimiterea proiectelor, adăugarea în coș, verificarea ofertelor de preț și plasarea comenzilor autorizate. | Inclus; disponibil pentru descărcare |
| [Raportarea rezultatelor · `auto_html_report`](../../skills/auto_html_report/SKILL.md) | Generează rapoarte HTML autonome în mai multe limbi din rezultatele JSON furnizate de utilizator, cu tabele de sinteză, grafice și imaginile disponibile. | Inclus; disponibil pentru descărcare |

MCP expune operațiuni; Skills descriu cum le folosește un agent în cadrul unei sarcini. Instalarea unui Skill nu acordă acces la servicii și nu înregistrează automat MCP. [Deschide catalogul →](../../skills/README.md)

Skill-ul `auto_html_report` necesită rezultate JSON existente, furnizate de utilizator. Nu preia date de la serviciu; doar identificatorul comenzii nu este suficient.

<a id="beta"></a>

## Beta Playground

Biointron OS este lansat treptat ca Beta Playground. Unele conexiuni pot fi încă indisponibile. Raportează rezultatul real al fiecărui pas; un răspuns HTTP de succes sau afișarea numelui unui instrument nu confirmă finalizarea unei operațiuni.

Crearea și trimiterea comenzilor necesită autorizarea utilizatorului. Dacă o operațiune de scriere depășește timpul de așteptare, verifică starea comenzii existente înainte de a încerca din nou. Pentru acces sau o funcție indisponibilă, contactează reprezentantul Biointron care ți-a furnizat contul.

<a id="online-platform"></a>

## Platforma online Biointron

Platforma online Biointron aduce fluxurile proiectelor RushDATA în browser, cu acces la ciornele proiectelor, coșul de cumpărături, comenzi și un asistent AI. Deschide platforma pentru a explora serviciile disponibile și a consulta informațiile despre proiecte.

[Accesează platforma online Biointron →](https://ai.biointron.com/#/landing)

<a href="https://ai.biointron.com/#/landing"><img src="../../assets/Biointron_Rushdata.png" alt="Interfața platformei online Biointron cu acces la proiectele RushDATA" width="1000" /></a>

<a id="faq"></a>

## Întrebări frecvente

<details>
<summary><strong>Am nevoie atât de MCP, cât și de Skills?</strong></summary>

MCP furnizează instrumente apelabile. Skills adaugă instrucțiuni pentru fluxuri de lucru și pot avea propriile dependențe. Respectă cerințele fiecărui Skill publicat; simpla descărcare a unui Skill nu conectează un serviciu.

</details>

<details>
<summary><strong>Dacă un instrument apare în listă, este pregătit pentru utilizare operațională?</strong></summary>

Nu. Descoperirea confirmă înregistrarea instrumentului. Configurarea backendului, accesul contului și operațiunea solicitată trebuie, de asemenea, validate. Catalogul face această distincție.

</details>

<details>
<summary><strong>Unde se află serverul și implementarea operațională?</strong></summary>

Acest depozit distribuie materiale publice de integrare și Skills. Serviciul găzduit și implementarea operațională privată sunt întreținute separat.

</details>

## Documentație

| Începe aici | Referințe |
| :--- | :--- |
| [Instalează MCP și Skills](../../docs/installation.md) | [Catalog de instrumente MCP](../../docs/tool-catalog.md) |
| [Catalog Skills](../../skills/README.md) | [API și exemple JSON](../../docs/api.md) |
| [Contribuie](../../CONTRIBUTING.md) | [Informații despre licență](../../docs/license.md) |

Ghidurile detaliate sunt disponibile în chineză și engleză.

## Licență

Licențiat conform [PolyForm Noncommercial 1.0.0](../../LICENSE). **Utilizarea comercială nu este permisă în baza acestei licențe.** Codul sursă al acestui depozit este disponibil pentru utilizare necomercială. Consultă [domeniul de aplicare și condițiile](../../docs/license.md).

---

<div align="center">
<sub>Biointron OS · Pentru agenți. Pentru modele. Pentru oameni.</sub>
</div>
