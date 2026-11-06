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
<strong lang="es" dir="ltr">Español</strong> ·
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

### Conecta tu agente de IA con los servicios de Biointron.

Desde las solicitudes de pedido hasta los resultados de los informes, incorpora los flujos de Biointron a las herramientas que ya utilizas.<br />
MCP establece la conexión. Los Skills guían el proceso. Tú mantienes el control.

[![Catálogo de herramientas MCP](https://img.shields.io/badge/MCP-tool_catalog-087F8C?style=flat-square)](../../docs/tool-catalog.md)
[![Skills](https://img.shields.io/badge/Agent-Skills-234E70?style=flat-square)](../../skills/README.md)
[![Licencia no comercial](https://img.shields.io/badge/License-Noncommercial-6B7280?style=flat-square)](../../LICENSE)
[![Beta Playground](https://img.shields.io/badge/Release-Beta_Playground-D7A345?style=flat-square)](#beta)

<br />

<!-- HERO: Keep the artwork path in sync across all language versions. -->
<img src="../../assets/biointron-os-hero.png" alt="Biointron OS" width="1000" />

<br />

**[Primeros pasos](#get-started) · [Herramientas MCP](../../docs/tool-catalog.md) · [Skills](../../skills/README.md) · [API y ejemplos](../../docs/api.md) · [Plataforma en línea](#online-platform) · [Preguntas frecuentes](#faq)**

</div>

---

## Una plataforma. Tres formas de conectarse.

Biointron OS es una interfaz de acceso a los servicios de Biointron para agentes de IA, modelos y personas. Reúne el acceso a los servicios y las instrucciones para los flujos de trabajo, con una hoja de ruta que abarca pedidos, diseños enviados, seguimiento y resultados.

| Para agentes | Para modelos | Para personas |
| :--- | :--- | :--- |
| Descubre e invoca servicios mediante **MCP**. | Trabaja con **datos estructurados** e interfaces documentadas. | Accede a los flujos mediante una **interfaz interactiva**. |
| Combina las llamadas a herramientas con Skills específicos de cada tarea. | Las convenciones de datos se están armonizando durante la fase Beta. | La experiencia web se ofrece por separado de este repositorio. |

Este repositorio es el punto de acceso público a los Skills, las guías de conexión, el catálogo de herramientas y los ejemplos. Los servicios empresariales de Biointron funcionan por separado.

<a id="get-started"></a>

## Primeros pasos

### 1 · Conecta MCP

Solicita el token de acceso al servicio y los permisos de uso a tu contacto de Biointron. En un cliente MCP compatible con **Streamable HTTP** y **autenticación Bearer**, añade:

| Parámetro | Valor |
| :--- | :--- |
| Nombre | `BiointronOS_MCP` |
| Transporte | Streamable HTTP |
| URL | `https://mcp-rusta-order-blgdfvompw.cn-shanghai.fcapp.run/mcp` |
| Autenticación | `Authorization: Bearer <MCP_ACCESS_TOKEN>` |

En los clientes compatibles con el formato `mcpServers`, puedes combinar la siguiente configuración con los ajustes existentes y sustituir el marcador del token por tu propio token.

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

Las dos cabeceras de tiempo de espera son campos personalizados de la configuración de referencia: 60000 milisegundos equivalen a 60 segundos y 660000 milisegundos a 11 minutos. Solo tendrán el efecto correspondiente si el cliente o el servicio admite estas cabeceras. Añadirlas a `headers` no garantiza por sí solo que cambie el tiempo de espera del cliente; consulta su documentación para configurar los ajustes concretos.

Consulta la [guía de instalación](../../docs/installation.md#mcp) para obtener más detalles de configuración.

### 2 · Añade Skills

Elige un Skill publicado en el [catálogo de Skills](../../skills/README.md). Descarga su carpeta completa, incluidos `references/`, los scripts suministrados y los demás archivos a los que hace referencia, y colócala en el directorio de Skills de tu agente. Consulta la [instalación de Skills](../../docs/installation.md#skills) para Codex y Claude Code.

Los dos paquetes de Skills están incluidos y se pueden descargar. `auto-html-report` genera informes localmente a partir de resultados JSON ya proporcionados, sin credenciales ni conexión MCP. Si falta el JSON, puede obtener primero los resultados mediante `get_report_results`, dentro del alcance autorizado, usando el número de pedido confirmado y el JWT válido del cliente actual, y después generar el informe. Un número de pedido por sí solo no basta. Biointron Account y App Key solo se utilizan cuando falta un JWT válido; se reutilizan los datos disponibles y solo se solicitan los que faltan. Las instrucciones del Skill están en inglés, pero los informes siguen disponibles en varios idiomas.

### 3 · Prueba una introducción de solo lectura

```text
Enumera las herramientas MCP de Biointron disponibles en esta sesión y explica para qué sirve cada una.
Indica qué funciones están listas y cuáles siguen en fase Beta.
No crees ni envíes ningún pedido.
```

El descubrimiento de herramientas es la primera comprobación de la conexión. Para que una operación empresarial se complete correctamente, su conexión con el backend también debe estar validada.

## Catálogo de herramientas MCP

| Herramienta | Finalidad | Efecto |
| :--- | :--- | :--- |
| `get_order_input_requirements` | Recopila por defecto preguntas independientes por lotes; antes de escribir, valida todos los datos de la etapa con `mode="validate"`. No necesita JWT de negocio. | Solo lectura |
| `search_order_antigens` | Busca por palabra clave en el catálogo y devuelve productos y variantes reales, junto con información para continuar por las páginas siguientes. | Solo lectura |
| `order_design_preflight` | Comprobar la elegibilidad de la empresa y las pruebas disponibles. | Solo lectura |
| `start_order_design` | Enviar el XLSX proporcionado y esperar la confirmación de guardado del diseño. | Escribe datos empresariales |
| `get_order_design_result` | Cuando el cliente elige verlo, recupera y entrega en modo de solo lectura el HTML real del diseño guardado. | Solo lectura |
| `add_order_to_cart` | Añadir un diseño cuyo guardado está confirmado al carrito. | Escribe datos empresariales |
| `end_order_workflow` | Indicar al cliente que descarte el contexto local, sin revocar la firma ni cancelar el pedido. | Solo instrucción al cliente |
| `get_order_cart` | Consultar el carrito de pedidos. | Solo lectura |
| `calculate_order_price` | Obtener un presupuesto para los pedidos seleccionados. | Solo lectura |
| `submit_verified_order` | Vuelve a comprobar la cotización y envía los pedidos seleccionados para confirmación humana. | Escribe datos empresariales |
| `get_report_results` | Recuperar resultados de informes existentes en formato JSON. | Solo lectura |

La implementación MCP actual registra 11 herramientas: 10 necesitan el JWT de negocio del cliente actual; `get_order_input_requirements` funciona localmente sin ese JWT. El despliegue y el funcionamiento de los procesos de principio a fin todavía deben verificarse. Consulta las [firmas, el estado y las limitaciones](../../docs/tool-catalog.md).

## Skills

| Skill | Finalidad | Estado de publicación |
| :--- | :--- | :--- |
| [Diseño de pedidos · `order-design`](../../skills/order_design/SKILL.md) | Explica paquetes, recopila datos por lotes, guía la selección del catálogo, permite ver el HTML del diseño guardado y gestiona carrito, cotización y envío para confirmación humana. | Incluido · Disponible para descargar |
| [Informe de resultados · `auto-html-report`](../../skills/auto_html_report/SKILL.md) | Genera informes HTML independientes y multilingües con tabla resumen, gráficos e imágenes disponibles a partir de resultados JSON proporcionados u obtenidos mediante una consulta autorizada. | Incluido · Disponible para descargar |

Enviar un pedido no significa que la producción haya comenzado ni que el experimento haya terminado. La producción empieza únicamente tras la confirmación de Biointron.

MCP expone operaciones; los Skills describen cómo las utiliza un agente dentro de una tarea. Instalar un Skill no concede acceso al servicio ni registra MCP automáticamente. [Explora el catálogo →](../../skills/README.md)

<a id="beta"></a>

## Beta Playground

Biointron OS se presenta como un entorno de pruebas Beta. Es posible que algunas conexiones aún no estén disponibles. Comunica el resultado real de cada paso; una respuesta HTTP satisfactoria o un nombre de herramienta visible no demuestran que una operación empresarial se haya completado.

La creación y el envío de pedidos requieren la autorización del usuario. Si una operación de escritura agota el tiempo de espera, consulta el estado del pedido existente antes de reintentar. Para obtener acceso o consultar una función no disponible, contacta con el representante de Biointron que te proporcionó la cuenta.

<a id="online-platform"></a>

## Plataforma en línea de Biointron

La plataforma en línea de Biointron lleva los flujos de trabajo de los proyectos RushDATA al navegador, con acceso a borradores de proyectos, el carrito, pedidos y un asistente de IA. Abre la plataforma para explorar los servicios disponibles y consultar la información de los proyectos.

[Visita la plataforma en línea de Biointron →](https://ai.biointron.com/#/landing)

<a href="https://ai.biointron.com/#/landing"><img src="../../assets/Biointron_Rushdata.png" alt="Interfaz de proyectos RushDATA en la plataforma en línea de Biointron" width="1000" /></a>

<a id="faq"></a>

## Preguntas frecuentes

<details>
<summary><strong>¿Necesito tanto MCP como Skills?</strong></summary>

MCP proporciona herramientas invocables. Los Skills añaden instrucciones para los flujos de trabajo y pueden tener sus propias dependencias. Sigue los requisitos de cada Skill publicado; descargar un Skill no basta para conectar un servicio.

</details>

<details>
<summary><strong>¿Que una herramienta aparezca en la lista significa que está lista para su uso empresarial?</strong></summary>

No. El descubrimiento confirma que la herramienta está registrada. También deben validarse la configuración del backend, el acceso a la cuenta y la operación solicitada. El catálogo deja constancia de esta distinción.

</details>

<details>
<summary><strong>¿Dónde están el servidor y la implementación de la lógica empresarial?</strong></summary>

Este repositorio distribuye materiales de integración públicos y Skills. El servicio alojado y la implementación empresarial privada se mantienen por separado.

</details>

## Documentación

| Empieza aquí | Referencia |
| :--- | :--- |
| [Instalar MCP y Skills](../../docs/installation.md) | [Catálogo de herramientas MCP](../../docs/tool-catalog.md) |
| [Catálogo de Skills](../../skills/README.md) | [API y ejemplos JSON](../../docs/api.md) |
| [Contribuir](../../CONTRIBUTING.md) | [Estado de la licencia](../../docs/license.md) |

Las guías detalladas están disponibles en chino e inglés.

## Licencia

Publicado bajo la licencia [PolyForm Noncommercial 1.0.0](../../LICENSE). **Esta licencia no permite el uso comercial.** El código fuente de este repositorio está disponible para uso no comercial. Consulta el [alcance y las condiciones](../../docs/license.md).

---

<div align="center">
<sub>Biointron OS · Para agentes. Para modelos. Para personas.</sub>
</div>
