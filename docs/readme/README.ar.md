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
<strong lang="ar" dir="rtl">العربية</strong> ·
<a href="README.id.md" lang="id" dir="ltr">Bahasa Indonesia</a> ·
<a href="README.it.md" lang="it" dir="ltr">Italiano</a> ·
<a href="README.el.md" lang="el" dir="ltr">Ελληνικά</a> ·
<a href="README.ml.md" lang="ml" dir="ltr">മലയാളം</a> ·
<a href="README.ur-Latn.md" lang="ur-Latn" dir="ltr">Roman Urdu</a> ·
<a href="README.ro.md" lang="ro" dir="ltr">Română</a>
</p>

# Biointron OS

### صِل وكيل الذكاء الاصطناعي لديك بخدمات Biointron.

من طلبات الشراء إلى نتائج التقارير، أضف سير عمل Biointron إلى الأدوات التي تستخدمها بالفعل.<br />
يوفّر MCP الاتصال، وتوجّه Skills سير العمل، وتبقى أنت صاحب القرار.

[![فهرس أدوات MCP](https://img.shields.io/badge/MCP-tool_catalog-087F8C?style=flat-square)](../../docs/tool-catalog.md)
[![Skills](https://img.shields.io/badge/Agent-Skills-234E70?style=flat-square)](../../skills/README.md)
[![ترخيص غير تجاري](https://img.shields.io/badge/License-Noncommercial-6B7280?style=flat-square)](../../LICENSE)
[![Beta Playground](https://img.shields.io/badge/Release-Beta_Playground-D7A345?style=flat-square)](#beta)

<br />

<!-- HERO: Keep the artwork path in sync across all language versions. -->
<img src="../../assets/biointron-os-hero.png" alt="Biointron OS" width="1000" />

<br />

**[ابدأ](#get-started) · [أدوات MCP](../../docs/tool-catalog.md) · [Skills](../../skills/README.md) · [API والأمثلة](../../docs/api.md) · [المنصة عبر الإنترنت](#online-platform) · [الأسئلة الشائعة](#faq)**

</div>

<div dir="rtl">

---

## منصة واحدة. ثلاث طرق للتواصل.

Biointron OS هو واجهة لخدمات Biointron موجّهة لوكلاء الذكاء الاصطناعي والنماذج والأشخاص. يجمع الوصول إلى الخدمات مع إرشادات سير العمل، ضمن خطة تطوير تشمل الطلبات وتقديم التصاميم ومتابعة التقدم والنتائج.

| للوكلاء | للنماذج | للأشخاص |
| ---: | ---: | ---: |
| اكتشف الخدمات واستدعها عبر **MCP**. | اعمل باستخدام **بيانات منظّمة** وواجهات موثّقة. | استخدم مسارات العمل من خلال **واجهة تفاعلية**. |
| اجمع استدعاءات الأدوات مع Skills مخصّصة للمهمة. | يجري توحيد مواصفات البيانات خلال مرحلة Beta. | تُقدَّم تجربة الويب بصورة منفصلة عن هذا المستودع. |

هذا المستودع هو المكان العام لنشر Skills وأدلة الاتصال وفهرس الأدوات والأمثلة. تعمل خدمات Biointron التشغيلية بصورة مستقلة.

<a id="get-started"></a>

## ابدأ

### 1 · اتصل عبر MCP

احصل على رمز الوصول إلى الخدمة والصلاحيات المطلوبة من جهة اتصالك في Biointron. أضف الإعدادات التالية في عميل MCP يدعم **Streamable HTTP** و**مصادقة Bearer**:

| الإعداد | القيمة |
| ---: | ---: |
| الاسم | `BiointronOS_MCP` |
| النقل | Streamable HTTP |
| العنوان | `https://mcp-rusta-order-blgdfvompw.cn-shanghai.fcapp.run/mcp` |
| المصادقة | `Authorization: Bearer <MCP_ACCESS_TOKEN>` |

في العملاء الذين يدعمون تنسيق `mcpServers`، ادمج هذا التكوين مع إعداداتك الحالية واستبدل القيمة النائبة برمز الوصول الخاص بك:

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

رأسا المهلة الزمنية عنصران مخصّصان في التكوين المرجعي: 60000 مللي ثانية = 60 ثانية، و660000 مللي ثانية = 11 دقيقة. لا يكون لهما أثر إلا إذا كان العميل أو الخدمة يدعم هذين الرأسين؛ فإضافتهما إلى `headers` وحدها لا تضمن تغيير مدة انتظار العميل. اضبط المهل الزمنية وفقًا لوثائق العميل الذي تستخدمه.

راجع [دليل التثبيت](../../docs/installation.md#mcp) لمزيد من التفاصيل.

### 2 · أضف Skills

اختر إحدى Skills المتوفرة في [فهرس Skills](../../skills/README.md). نزّل مجلدها كاملًا، بما فيه `references/` وأي نصوص برمجية مرفقة، وضعه في دليل Skills الخاص بوكيلك. راجع [تثبيت Skills](../../docs/installation.md#skills) لمعرفة خطوات Codex وClaude Code.

الحزمتان مضمنتان الآن في هذا المستودع: `skills/order_design/` لـ `order-design` و`skills/auto_html_report/` لـ `auto-html-report`. يمكن تنزيلهما؛ وجودهما لا يثبت التحقق من سير العمليات بالكامل.

### 3 · جرّب مقدمة للقراءة فقط

```text
اعرض أدوات Biointron MCP المتاحة في هذه الجلسة، واشرح وظيفة كل أداة.
أخبرني بالقدرات الجاهزة والقدرات التي لا تزال في مرحلة Beta.
لا تُنشئ طلبًا ولا ترسله.
```

اكتشاف الأدوات هو أول اختبار للاتصال. ويتطلب نجاح أي عملية تشغيلية التحقق من اتصالها المقابل بالخدمة الخلفية.

## فهرس أدوات MCP

| الأداة | الغرض | الأثر |
| ---: | ---: | ---: |
| `get_order_input_requirements` | يجمع الأسئلة المستقلة في دفعات افتراضيًا، ويتحقق من جميع بيانات المرحلة قبل الكتابة. لا يتطلب JWT للأعمال. | قراءة فقط |
| `search_order_antigens` | يبحث بالكلمات المفتاحية عن المنتجات والمواصفات الفعلية ويعيد معلومات متابعة الصفحات. | قراءة فقط |
| `order_design_preflight` | التحقق من أهلية الشركة وعناصر الاختبار المتاحة. | قراءة فقط |
| `start_order_design` | إرسال ملف XLSX المقدَّم وانتظار تأكيد حفظ التصميم. | كتابة بيانات تشغيلية |
| `get_order_design_result` | بعد اختيار العميل، يقرأ HTML الفعلي للتصميم المحفوظ لتسليمه دون تعديل الطلب. | قراءة فقط |
| `add_order_to_cart` | إضافة التصميم المؤكد حفظه إلى سلة الطلبات. | كتابة بيانات تشغيلية |
| `end_order_workflow` | توجيه العميل للتخلص من السياق المحلي دون إبطال التوقيع أو إلغاء الطلب. | تعليمات للعميل فقط |
| `get_order_cart` | عرض سلة الطلبات. | قراءة فقط |
| `calculate_order_price` | الحصول على عرض سعر للطلبات المحددة. | قراءة فقط |
| `submit_verified_order` | يراجع عرض السعر ويرسل الطلبات المحددة للتأكيد البشري. | كتابة بيانات تشغيلية |
| `get_report_results` | جلب نتائج تقارير موجودة بصيغة JSON. | قراءة فقط |

يتضمن التنفيذ المحلي **11 أداة**: تتطلب 10 منها JWT للعميل الحالي في `business_token`، بينما تعمل `get_order_input_requirements` محليًا دون JWT. لم يُنشر هذا التحديث بعد، ولم تُتحقق جاهزية سير العمل بالكامل في بيئة فعلية. راجع [تواقيع الأدوات وحالتها وحدودها](../../docs/tool-catalog.md).

## Skills

| Skill | الغرض | حالة الإصدار |
| ---: | ---: | ---: |
| [تصميم الطلبات · `order-design`](../../skills/order_design/SKILL.md) | شرح الباقات وجمع المعلومات على دفعات واختيار المنتجات من الفهرس وإتاحة عرض HTML للتصميم بعد حفظه ومراجعة السلة وعروض الأسعار وإرسال الطلبات للتأكيد البشري. | مضمنة؛ متاحة للتنزيل |
| [تقرير النتائج · `auto-html-report`](../../skills/auto_html_report/SKILL.md) | إنشاء تقارير HTML مستقلة بلغات متعددة من نتائج JSON يقدّمها المستخدم، مع جداول تلخيصية ورسوم بيانية والصور المتاحة. | مضمنة؛ متاحة للتنزيل |

يتيح MCP العمليات، وتصف Skills كيفية استخدام الوكيل لها ضمن مهمة. تثبيت Skill لا يمنح صلاحية الوصول إلى الخدمة ولا يسجّل MCP تلقائيًا. [تصفّح الفهرس ←](../../skills/README.md)

ينتظر الطلب المرسل تأكيد Biointron؛ ولا يعني إرساله بدء الإنتاج أو اكتمال التجربة.

عند توفر نتائج JSON المقدمة مسبقًا، تنشئ Skill المسماة `auto-html-report` التقرير محليًا دون بيانات اعتماد أو اتصال MCP. إذا لم يتوفر JSON، يمكن ضمن نطاق التفويض استخدام رقم الطلب وJWT للعميل الحالي مع `get_report_results` لجلب النتائج ثم إنشاء التقرير. رقم الطلب وحده غير كافٍ. أعد استخدام JWT الصالح؛ وعند الحاجة إلى الحصول عليه، أعد استخدام Biointron Account وApp Key المتوفرين واطلب القيم الناقصة فقط.

تعليمات حزمة التقارير مكتوبة بالإنجليزية، لكن التقرير يُنشأ باللغة التي يطلبها العميل.

<a id="beta"></a>

## Beta Playground

يُقدَّم Biointron OS بوصفه Beta Playground. قد تبقى بعض الاتصالات غير متاحة. أبلغ عن النتيجة الفعلية لكل خطوة؛ فنجاح استجابة HTTP أو ظهور اسم أداة لا يثبت اكتمال عملية تشغيلية.

يتطلب إنشاء الطلبات وإرسالها تفويضًا من المستخدم. إذا انتهت مهلة عملية كتابة، فتحقّق من حالة الطلب الموجود قبل إعادة المحاولة. لطلب الوصول أو الاستفسار عن قدرة غير متاحة، تواصل مع ممثل Biointron الذي زوّدك بالحساب.

<a id="online-platform"></a>

## منصة Biointron عبر الإنترنت

تجمع منصة Biointron عبر الإنترنت سير عمل مشاريع RushDATA داخل المتصفح، مع إمكانية الوصول إلى مسودات المشاريع وسلة التسوق والطلبات ومساعد ذكاء اصطناعي. افتح المنصة لاستكشاف الخدمات المتاحة وعرض معلومات المشاريع.

[زيارة منصة Biointron عبر الإنترنت ←](https://ai.biointron.com/#/landing)

<a href="https://ai.biointron.com/#/landing"><img src="../../assets/Biointron_Rushdata.png" alt="واجهة منصة Biointron عبر الإنترنت للوصول إلى مشاريع RushDATA" width="1000" /></a>

<a id="faq"></a>

## الأسئلة الشائعة

<details>
<summary><strong>هل أحتاج إلى MCP وSkills معًا؟</strong></summary>

يوفّر MCP أدوات قابلة للاستدعاء. تضيف Skills تعليمات لسير العمل، وقد تكون لها متطلبات خاصة بها. اتبع متطلبات كل Skill منشورة؛ فتنزيل Skill وحده لا ينشئ اتصالًا بالخدمة.

</details>

<details>
<summary><strong>هل ظهور أداة في القائمة يعني أنها جاهزة للاستخدام التشغيلي؟</strong></summary>

لا. يؤكد اكتشاف الأداة أنها مسجّلة فقط. يجب أيضًا التحقق من إعدادات الخدمة الخلفية وصلاحية الحساب والعملية المطلوبة. يوضّح الفهرس هذا الفرق.

</details>

<details>
<summary><strong>أين الخادم وتنفيذ منطق الأعمال؟</strong></summary>

يوزّع هذا المستودع مواد التكامل العامة وSkills. وتُدار الخدمة المستضافة والتنفيذ الخاص لمنطق الأعمال بصورة منفصلة.

</details>

## الوثائق

| ابدأ هنا | المراجع |
| ---: | ---: |
| [تثبيت MCP وSkills](../../docs/installation.md) | [فهرس أدوات MCP](../../docs/tool-catalog.md) |
| [فهرس Skills](../../skills/README.md) | [API وأمثلة JSON](../../docs/api.md) |
| [المساهمة](../../CONTRIBUTING.md) | [حالة الترخيص](../../docs/license.md) |

تتوفر الأدلة التفصيلية باللغتين الصينية والإنجليزية.

## الترخيص

متاح بموجب ترخيص [PolyForm Noncommercial 1.0.0](../../LICENSE). **لا يسمح هذا الترخيص بالاستخدام التجاري.** تتوفر الشفرة المصدرية لهذا المستودع للاستخدام غير التجاري. راجع [النطاق والشروط](../../docs/license.md).

</div>

---

<div align="center">
<sub>Biointron OS · للوكلاء. للنماذج. للأشخاص.</sub>
</div>

