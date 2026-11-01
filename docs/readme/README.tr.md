<div align="center">

<p dir="ltr">
<a href="../../README.md" lang="en" dir="ltr">English</a> ·
<a href="README.zh-CN.md" lang="zh-CN" dir="ltr">简体中文</a> ·
<a href="README.zh-TW.md" lang="zh-TW" dir="ltr">繁體中文</a> ·
<a href="README.ja.md" lang="ja" dir="ltr">日本語</a> ·
<a href="README.ko.md" lang="ko" dir="ltr">한국어</a> ·
<strong lang="tr" dir="ltr">Türkçe</strong> ·
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

### Yapay zekâ ajanınızı Biointron hizmetlerine bağlayın.

Sipariş taleplerinden raporlanan sonuçlara kadar Biointron iş akışlarını zaten kullandığınız araçlara taşıyın.<br />
MCP bağlantıyı sağlar. Skills iş akışına rehberlik eder. Kontrol sizde kalır.

[![MCP araç kataloğu](https://img.shields.io/badge/MCP-tool_catalog-087F8C?style=flat-square)](../../docs/tool-catalog.md)
[![Skills](https://img.shields.io/badge/Agent-Skills-234E70?style=flat-square)](../../skills/README.md)
[![Ticari olmayan kullanım lisansı](https://img.shields.io/badge/License-Noncommercial-6B7280?style=flat-square)](../../LICENSE)
[![Beta Playground](https://img.shields.io/badge/Release-Beta_Playground-D7A345?style=flat-square)](#beta)

<br />

<!-- HERO: Keep the artwork path in sync across all language versions. -->
<img src="../../assets/biointron-os-hero.png" alt="Biointron OS" width="1000" />

<br />

**[Başlangıç](#get-started) · [MCP araçları](../../docs/tool-catalog.md) · [Skills](../../skills/README.md) · [API ve örnekler](../../docs/api.md) · [Çevrimiçi platform](#online-platform) · [SSS](#faq)**

</div>

---

## Tek platform. Üç bağlantı yolu.

Biointron OS; yapay zekâ ajanları, modeller ve insanlar için Biointron hizmetlerine erişim arayüzüdür. Hizmet erişimini ve iş akışı rehberliğini bir araya getirir; yol haritası siparişleri, tasarım gönderimlerini, ilerlemeyi ve sonuçları kapsar.

| Ajanlar için | Modeller için | İnsanlar için |
| :--- | :--- | :--- |
| **MCP** üzerinden hizmetleri keşfedin ve çağırın. | **Yapılandırılmış verilerle** ve belgelenmiş arayüzlerle çalışın. | **Etkileşimli bir arayüz** üzerinden iş akışlarına erişin. |
| Araç çağrılarını göreve özel Skills ile birlikte kullanın. | Veri kuralları Beta sürecinde uyumlu hâle getiriliyor. | Web deneyimi bu depodan ayrı olarak sunulur. |

Bu depo; Skills, bağlantı kılavuzları, araç kataloğu ve örnekler için herkese açık kaynak noktasıdır. Biointron iş hizmetleri ayrı olarak çalışır.

<a id="get-started"></a>

## Başlangıç

### 1 · MCP bağlantısını kurun

Biointron yetkilinizden hizmet erişim belirtecini ve kullanım iznini alın. **Streamable HTTP** ve **Bearer kimlik doğrulamasını** destekleyen bir MCP istemcisine şunları ekleyin:

| Ayar | Değer |
| :--- | :--- |
| Ad | `BiointronOS_MCP` |
| Aktarım | Streamable HTTP |
| URL | `https://mcp-rusta-order-blgdfvompw.cn-shanghai.fcapp.run/mcp` |
| Kimlik doğrulama | `Authorization: Bearer <MCP_ACCESS_TOKEN>` |

`mcpServers` biçimini destekleyen istemcilerde aşağıdaki yapılandırmayı mevcut ayarlarla birleştirebilir ve belirteç yer tutucusunu kendi belirtecinizle değiştirebilirsiniz.

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

İki zaman aşımı başlığı, referans yapılandırmadaki özel alanlardır: 60000 milisaniye 60 saniyeye, 660000 milisaniye ise 11 dakikaya eşittir. Yalnızca istemci veya hizmet bu başlıkları destekliyorsa ilgili etkiler oluşur. Bunları yalnızca `headers` içine eklemek, istemcinin bekleme süresinin değişmesini garanti etmez; ayrıntılı ayarlar için istemcinin belgelerini izleyin.

Ayrıntılı ayarlar için [kurulum kılavuzuna](../../docs/installation.md#mcp) bakın.

### 2 · Skills ekleyin

[Skills kataloğundan](../../skills/README.md) yayımlanmış bir Skill seçin. `references/`, sağlanan betikler ve başvurulan diğer dosyalar dâhil klasörün tamamını indirin ve ajanınızın Skill dizinine yerleştirin. Codex ve Claude Code için [Skill kurulumu](../../docs/installation.md#skills) bölümüne bakın.

Her iki Skill paketi de bu depoda bulunur ve indirilebilir. `auto_html_report`, kullanıcının sağladığı mevcut sonuç JSON'unu girdi olarak kullanır. Hizmetten veri getirmez; yalnızca sipariş numarası rapor oluşturmak için yeterli değildir.

### 3 · Önce salt okunur bir tanıtım deneyin

```text
Bu oturumda kullanılabilen Biointron MCP araçlarını listele ve her birinin ne yaptığını açıkla.
Hangi yeteneklerin hazır olduğunu, hangilerinin hâlâ Beta aşamasında kaldığını söyle.
Sipariş oluşturma veya gönderme.
```

Araç keşfi ilk bağlantı kontrolüdür. Bir iş işleminin başarıyla tamamlanması için ilgili arka uç bağlantısının ayrıca doğrulanması gerekir.

## MCP araç kataloğu

| Araç | Amaç | Etki |
| :--- | :--- | :--- |
| `order_design_preflight` | Şirket uygunluğunu ve kullanılabilir testleri kontrol eder. | Salt okunur |
| `start_order_design` | Sağlanan XLSX dosyasını gönderir ve tasarımın kaydedildiğinin onayını bekler. | İş verilerine yazar |
| `add_order_to_cart` | Kaydı onaylanmış tasarımı sepete ekler. | İş verilerine yazar |
| `get_order_cart` | Sipariş sepetini okur. | Salt okunur |
| `calculate_order_price` | Seçilen siparişler için fiyat teklifi alır. | Salt okunur |
| `submit_verified_order` | Fiyat teklifini doğrular ve seçilen siparişleri gönderir. | İş verilerine yazar |
| `get_report_results` | Mevcut rapor sonuçlarını JSON olarak alır. | Salt okunur |

Bu yedi araç mevcut MCP uygulamasında kayıtlıdır. İş akışının uçtan uca kullanıma hazır olup olmadığı henüz doğrulanmalıdır. [İmzalar, durum ve sınırlar](../../docs/tool-catalog.md) bölümüne bakın.

## Skills

| Skill | Amaç | Yayın durumu |
| :--- | :--- | :--- |
| [Sipariş Tasarımı · `order-design`](../../skills/order_design/SKILL.md) | Sipariş taleplerine, tasarım gönderimine ve sipariş gönderimine rehberlik eder. | Depoda mevcut · İndirilebilir |
| [Sonuç Raporu · `auto_html_report`](../../skills/auto_html_report/SKILL.md) | Kullanıcının sağladığı mevcut sonuç JSON'undan özet tablo, grafikler ve mevcut görseller içeren bağımsız, çok dilli HTML raporları oluşturur. | Depoda mevcut · İndirilebilir |

MCP işlemleri kullanıma sunar; Skills, ajanın bunları bir görev içinde nasıl kullanacağını açıklar. Bir Skill kurmak hizmet erişimi sağlamaz ve MCP'yi otomatik olarak kaydetmez. [Kataloğa göz atın →](../../skills/README.md)

<a id="beta"></a>

## Beta Playground

Biointron OS, Beta Playground olarak kullanıma sunuluyor. Bazı bağlantılar hâlâ kullanılamıyor olabilir. Her adımın gerçek sonucunu bildirin; başarılı bir HTTP yanıtı veya görünür bir araç adı, iş işleminin tamamlandığını kanıtlamaz.

Sipariş oluşturma ve gönderme, kullanıcı yetkilendirmesi gerektirir. Bir yazma işlemi zaman aşımına uğrarsa yeniden denemeden önce mevcut sipariş durumunu kontrol edin. Erişim veya kullanılamayan bir yetenek için hesabınızı sağlayan Biointron temsilcisiyle iletişime geçin.

<a id="online-platform"></a>

## Biointron Çevrimiçi Platformu

Biointron'un çevrimiçi platformu, RushDATA proje iş akışlarını tarayıcıya taşır; proje taslaklarına, alışveriş sepetine, siparişlere ve bir AI asistanına erişim sunar. Kullanılabilir hizmetleri keşfetmek ve proje bilgilerini görüntülemek için platformu açın.

[Biointron çevrimiçi platformunu ziyaret edin →](https://ai.biointron.com/#/landing)

<a href="https://ai.biointron.com/#/landing"><img src="../../assets/Biointron_Rushdata.png" alt="Biointron çevrimiçi platformunun RushDATA proje arayüzü" width="1000" /></a>

<a id="faq"></a>

## Sık sorulan sorular

<details>
<summary><strong>Hem MCP'ye hem de Skills'e ihtiyacım var mı?</strong></summary>

MCP çağrılabilir araçlar sağlar. Skills iş akışı talimatları ekler ve kendilerine ait bağımlılıkları olabilir. Yayımlanmış her Skill'in gereksinimlerini izleyin; yalnızca bir Skill indirmek hizmet bağlantısı kurmaz.

</details>

<details>
<summary><strong>Bir aracın listelenmesi, iş kullanımına hazır olduğu anlamına mı gelir?</strong></summary>

Hayır. Keşif, aracın kayıtlı olduğunu doğrular. Arka uç yapılandırması, hesap erişimi ve talep edilen işlem de doğrulanmalıdır. Katalog bu ayrımı belirtir.

</details>

<details>
<summary><strong>Sunucu ve iş mantığının uygulaması nerede?</strong></summary>

Bu depo, herkese açık entegrasyon materyallerini ve Skills'i dağıtır. Barındırılan hizmet ve özel iş mantığı uygulaması ayrı olarak yönetilir.

</details>

## Belgeler

| Buradan başlayın | Başvuru kaynakları |
| :--- | :--- |
| [MCP ve Skills kurulumu](../../docs/installation.md) | [MCP araç kataloğu](../../docs/tool-catalog.md) |
| [Skills kataloğu](../../skills/README.md) | [API ve JSON örnekleri](../../docs/api.md) |
| [Katkıda bulunun](../../CONTRIBUTING.md) | [Lisans durumu](../../docs/license.md) |

Ayrıntılı kılavuzlar Çince ve İngilizce olarak sunulur.

## Lisans

[PolyForm Noncommercial 1.0.0](../../LICENSE) kapsamında lisanslanmıştır. **Bu lisans kapsamında ticari kullanıma izin verilmez.** Bu deponun kaynakları ticari olmayan kullanım için erişime açıktır. [Kapsam ve koşullara](../../docs/license.md) bakın.

---

<div align="center">
<sub>Biointron OS · Ajanlar için. Modeller için. İnsanlar için.</sub>
</div>
