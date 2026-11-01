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
<strong lang="ur-Latn" dir="ltr">Roman Urdu</strong> ·
<a href="README.ro.md" lang="ro" dir="ltr">Română</a>
</p>

# Biointron OS

### Apne AI agent ko Biointron ki khidmaat se jorein.

Order ki darkhwast se report ke nataij tak, Biointron ke kaam ke marahil ko un tools mein laayein jo aap pehle se istemal karte hain.<br />
MCP rabta faraham karta hai. Skills kaam ke marahil mein rehnumai karti hain. Ikhtiyar aap ke paas rehta hai.

[![MCP tools ki fehrist](https://img.shields.io/badge/MCP-tool_catalog-087F8C?style=flat-square)](../../docs/tool-catalog.md)
[![Skills](https://img.shields.io/badge/Agent-Skills-234E70?style=flat-square)](../../skills/README.md)
[![Ghair-tijarati license](https://img.shields.io/badge/License-Noncommercial-6B7280?style=flat-square)](../../LICENSE)
[![Beta Playground](https://img.shields.io/badge/Release-Beta_Playground-D7A345?style=flat-square)](#beta)

<br />

<!-- HERO: Keep the artwork path in sync across all language versions. -->
<img src="../../assets/biointron-os-hero.png" alt="Biointron OS" width="1000" />

<br />

**[Shuru karein](#get-started) · [MCP tools](../../docs/tool-catalog.md) · [Skills](../../skills/README.md) · [API aur misaalein](../../docs/api.md) · [Online platform](#online-platform) · [Aam sawalat](#faq)**

</div>

---

## Ek platform. Rabte ke teen tareeqe.

Biointron OS, AI agents, models aur logon ke liye Biointron ki khidmaat tak rasai ka interface hai. Yeh khidmaat tak rasai aur kaam ke marahil ki rehnumai ko ek jagah lata hai. Is ki taraqqi ke mansube mein orders, design jama karwana, peshraft aur nataij shamil hain.

| Agents ke liye | Models ke liye | Logon ke liye |
| :--- | :--- | :--- |
| **MCP** ke zariye khidmaat talash karein aur call karein. | **Munazzam data** aur wazahat shuda interfaces ke saath kaam karein. | **Interactive interface** ke zariye kaam ke marahil tak rasai hasil karein. |
| Tools ki calls ke saath har kaam ke liye makhsoos Skills istemal karein. | Beta ke dauran data ke usool hum-ahang kiye ja rahe hain. | Web interface is repository se alag faraham kiya jata hai. |

Yeh repository Skills, rabte ki rehnumai, tools ki fehrist aur misaalon ka awaami markaz hai. Biointron ki karobari khidmaat alag chalti hain.

<a id="get-started"></a>

## Shuru karein

### 1 · MCP ko connect karein

Apne Biointron numainde se service access token aur zaroori ijazatein hasil karein. Aise MCP client mein jo **Streamable HTTP** aur **Bearer authentication** ko support karta ho, yeh maloomat shamil karein:

| Setting | Qeemat |
| :--- | :--- |
| Naam | `BiointronOS_MCP` |
| Transport | Streamable HTTP |
| URL | `https://mcp-rusta-order-blgdfvompw.cn-shanghai.fcapp.run/mcp` |
| Tasdeeq | `Authorization: Bearer <MCP_ACCESS_TOKEN>` |

`mcpServers` format ko support karne wale clients mein is configuration ko maujooda settings ke saath mila dein aur placeholder ki jagah apna token daalein:

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

Dono timeout headers is misaali configuration ke custom items hain: 60000 milliseconds = 60 seconds aur 660000 milliseconds = 11 minutes. In ka asar sirf tab hota hai jab client ya service in headers ko support kare; sirf inhein `headers` mein daalne se client ka intezar ka waqt badalne ki zamanat nahin milti. Timeout apne client ki documentation ke mutabiq set karein.

Mazeed tafseel ke liye [installation guide](../../docs/installation.md#mcp) dekhein.

### 2 · Skills shamil karein

[Skills ki fehrist](../../skills/README.md) se shamil shuda Skill chunein. Us ka poora folder, `references/` aur saath diye gaye scripts samet, download karke apne agent ki Skill directory mein rakhein. Codex aur Claude Code ke liye [Skill ki installation](../../docs/installation.md#skills) dekhein.

Dono packages ab is repository mein shamil hain: `order-design` ke liye `skills/order_design/` aur `auto_html_report` ke liye `skills/auto_html_report/`. Dono download kiye ja sakte hain; packages ki mojoodgi poore karobari amal ki tasdeeq nahin karti.

### 3 · Sirf parhne wala taaruf aazmaayein

```text
Is session mein dastiyab Biointron MCP tools ki fehrist dein aur har tool ka kaam samjhaayein.
Bataayein kaun si salahiyatein tayyar hain aur kaun si abhi Beta mein hain.
Koi order na banaayein aur na jama karein.
```

Tools ki dastiyabi maloom karna rabte ki pehli jaanch hai. Kisi karobari amal ki kamyabi ke liye us ke mutaliqa backend connection ki tasdeeq zaroori hai.

## MCP tools ki fehrist

| Tool | Maqsad | Asar |
| :--- | :--- | :--- |
| `order_design_preflight` | Company ki ahliyat aur dastiyab tests check karta hai. | Sirf parhna |
| `start_order_design` | Di hui XLSX file bhej kar design save hone ki tasdeeq ka intezar karta hai. | Karobari data likhta hai |
| `add_order_to_cart` | Save hone ki tasdeeq wale design ko cart mein dalta hai. | Karobari data likhta hai |
| `get_order_cart` | Order cart parhta hai. | Sirf parhna |
| `calculate_order_price` | Chune gaye orders ki qeemat hasil karta hai. | Sirf parhna |
| `submit_verified_order` | Qeemat ki tasdeeq ke baad chune gaye orders jama karta hai. | Karobari data likhta hai |
| `get_report_results` | Maujood reports ke nataij JSON mein hasil karta hai. | Sirf parhna |

Yeh saat tools maujooda MCP implementation mein registered hain. Poore karobari silsile ki tayyari ki tasdeeq abhi baqi hai. [Parameters, halat aur hudood](../../docs/tool-catalog.md) dekhein.

## Skills

| Skill | Maqsad | Release ki halat |
| :--- | :--- | :--- |
| [Order Design · `order-design`](../../skills/order_design/SKILL.md) | Design jama karwane, cart mein shamil karne, qeemat ki peshkash jaanchne aur ijazat shuda orders jama karwane mein rehnumai. | Shamil hai; download ke liye dastiyab |
| [Nataij ki Report · `auto_html_report`](../../skills/auto_html_report/SKILL.md) | User ke diye hue maujood nataij ke JSON se mukhtalif zabanon mein mustaqil HTML reports banata hai, jin mein khulase ki tables, charts aur dastiyab tasaveer hoti hain. | Shamil hai; download ke liye dastiyab |

MCP operations faraham karta hai; Skills batati hain ke agent kisi kaam mein unhein kaise istemal kare. Skill install karne se service ki rasai nahin milti aur MCP khud-ba-khud register nahin hota. [Fehrist dekhein →](../../skills/README.md)

`auto_html_report` Skill ko user ke diye hue maujood nataij ka JSON chahiye. Yeh service se data hasil nahin karta; sirf order number kaafi nahin hai.

<a id="beta"></a>

## Beta Playground

Biointron OS ko Beta Playground ke taur par pesh kiya ja raha hai. Kuch connections abhi dastiyab nahin ho sakte. Har qadam ka asal nateeja bataayein; HTTP ki kamyab response ya tool ka naam nazar aana is baat ka saboot nahin ke karobari amal mukammal ho gaya.

Order banane aur jama karne ke liye user ki ijazat zaroori hai. Agar data likhne ke amal ka waqt khatam ho jaye, dobara koshish se pehle maujood order ki halat jaanchein. Rasai ya kisi ghair-dastiyab salahiyat ke liye us Biointron numainde se rabta karein jis ne aap ka account faraham kiya.

<a id="online-platform"></a>

## Biointron ka online platform

Biointron ka online platform RushDATA projects ke kaam ke marahil browser mein faraham karta hai, jahan project drafts, shopping cart, orders aur AI assistant tak rasai milti hai. Dastiyab services dekhne aur projects ki maloomat parhne ke liye platform kholein.

[Biointron ka online platform kholein →](https://ai.biointron.com/#/landing)

<a href="https://ai.biointron.com/#/landing"><img src="../../assets/Biointron_Rushdata.png" alt="Biointron ke online platform ka interface, jahan RushDATA projects tak rasai milti hai" width="1000" /></a>

<a id="faq"></a>

## Aam sawalat

<details>
<summary><strong>Kya mujhe MCP aur Skills dono ki zaroorat hai?</strong></summary>

MCP call kiye ja sakne wale tools faraham karta hai. Skills kaam ke marahil ki hidayat deti hain aur un ki apni dependencies bhi ho sakti hain. Har jari shuda Skill ki zarooriyat par amal karein; sirf Skill download karna service se rabta nahin banata.

</details>

<details>
<summary><strong>Kya tool ka fehrist mein hona us ke karobari istemal ke liye tayyar hone ka matlab hai?</strong></summary>

Nahin. Tool ka milna sirf us ke register hone ki tasdeeq hai. Backend configuration, account ki rasai aur darkhwast kiye gaye amal ki bhi tasdeeq honi chahiye. Fehrist in halaton ka farq wazeh karti hai.

</details>

<details>
<summary><strong>Server aur karobari implementation kahan hain?</strong></summary>

Yeh repository awaami integration ka mawaad aur Skills faraham karti hai. Hosted service aur niji karobari implementation alag maintain ki jati hain.

</details>

## Dastavezat

| Yahan se shuru karein | Hawale |
| :--- | :--- |
| [MCP aur Skills install karein](../../docs/installation.md) | [MCP tools ki fehrist](../../docs/tool-catalog.md) |
| [Skills ki fehrist](../../skills/README.md) | [API aur JSON ki misaalein](../../docs/api.md) |
| [Hissa daalein](../../CONTRIBUTING.md) | [License ki halat](../../docs/license.md) |

Tafseeli rehnumai Cheeni aur Angrezi mein faraham ki gayi hai.

## License

[PolyForm Noncommercial 1.0.0](../../LICENSE) ke tehat licensed hai. **Is license ke tehat tijarati istemal ki ijazat nahin hai.** Is repository ka source code ghair-tijarati istemal ke liye dastiyab hai. [Daaira aur sharaait](../../docs/license.md) dekhein.

---

<div align="center">
<sub>Biointron OS · Agents ke liye. Models ke liye. Logon ke liye.</sub>
</div>

