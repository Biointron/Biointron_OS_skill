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
<strong lang="fr" dir="ltr">Français</strong> ·
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

### Connectez votre agent IA aux services de Biointron.

Des demandes de commande aux résultats des rapports, retrouvez les processus Biointron dans les outils que vous utilisez déjà.<br />
MCP assure la connexion. Les Skills guident le processus. Vous gardez le contrôle.

[![Catalogue des outils MCP](https://img.shields.io/badge/MCP-tool_catalog-087F8C?style=flat-square)](../../docs/tool-catalog.md)
[![Skills](https://img.shields.io/badge/Agent-Skills-234E70?style=flat-square)](../../skills/README.md)
[![Licence non commerciale](https://img.shields.io/badge/License-Noncommercial-6B7280?style=flat-square)](../../LICENSE)
[![Beta Playground](https://img.shields.io/badge/Release-Beta_Playground-D7A345?style=flat-square)](#beta)

<br />

<!-- HERO: Keep the artwork path in sync across all language versions. -->
<img src="../../assets/biointron-os-hero.png" alt="Biointron OS" width="1000" />

<br />

**[Premiers pas](#get-started) · [Outils MCP](../../docs/tool-catalog.md) · [Skills](../../skills/README.md) · [API et exemples](../../docs/api.md) · [Plateforme en ligne](#online-platform) · [Questions fréquentes](#faq)**

</div>

---

## Une plateforme. Trois façons de se connecter.

Biointron OS est une interface donnant accès aux services de Biointron pour les agents IA, les modèles et les personnes. Elle réunit l'accès aux services et les instructions qui guident les processus, avec une feuille de route couvrant les commandes, les conceptions soumises, le suivi et les résultats.

| Pour les agents | Pour les modèles | Pour les personnes |
| :--- | :--- | :--- |
| Découvrez et appelez les services via **MCP**. | Travaillez avec des **données structurées** et des interfaces documentées. | Accédez aux processus via une **interface interactive**. |
| Associez les appels d'outils à des Skills propres à chaque tâche. | Les conventions de données sont en cours d'harmonisation pendant la phase Beta. | L'interface web est fournie séparément de ce dépôt. |

Ce dépôt est le point d'accès public aux Skills, aux guides de connexion, au catalogue des outils et aux exemples. Les services métier de Biointron fonctionnent séparément.

<a id="get-started"></a>

## Premiers pas

### 1 · Connecter MCP

Obtenez le jeton d'accès au service et les autorisations d'utilisation auprès de votre contact Biointron. Dans un client MCP prenant en charge **Streamable HTTP** et l'**authentification Bearer**, ajoutez les paramètres suivants :

| Paramètre | Valeur |
| :--- | :--- |
| Nom | `BiointronOS_MCP` |
| Transport | Streamable HTTP |
| URL | `https://mcp-rusta-order-blgdfvompw.cn-shanghai.fcapp.run/mcp` |
| Authentification | `Authorization: Bearer <MCP_ACCESS_TOKEN>` |

Dans les clients compatibles avec le format `mcpServers`, vous pouvez fusionner la configuration suivante avec vos paramètres existants et remplacer le jeton fictif par votre propre jeton.

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

Les deux en-têtes de délai d'attente sont des paramètres personnalisés de cette configuration de référence : 60000 millisecondes correspondent à 60 secondes et 660000 millisecondes à 11 minutes. Ils n'ont l'effet attendu que si le client ou le service prend en charge ces en-têtes. Les ajouter à `headers` ne garantit pas, à lui seul, la modification du délai d'attente du client ; consultez sa documentation pour effectuer les réglages appropriés.

Pour plus de détails, consultez le [guide d'installation](../../docs/installation.md#mcp).

### 2 · Ajouter des Skills

Choisissez un Skill publié dans le [catalogue des Skills](../../skills/README.md). Téléchargez son dossier complet, y compris `references/`, les scripts fournis et les autres fichiers référencés, puis placez-le dans le répertoire de Skills de votre agent. Consultez l'[installation des Skills](../../docs/installation.md#skills) pour Codex et Claude Code.

Les deux paquets de Skills sont désormais inclus dans ce dépôt et disponibles au téléchargement. `auto_html_report` utilise les résultats JSON existants fournis par l'utilisateur. Il ne récupère pas les données auprès d'un service ; un numéro de commande seul ne suffit pas à produire un rapport.

### 3 · Commencer par une découverte en lecture seule

```text
Liste les outils MCP de Biointron disponibles dans cette session et explique le rôle de chacun.
Indique les fonctionnalités prêtes à l'emploi et celles qui sont encore en phase Beta.
Ne crée et ne soumets aucune commande.
```

La découverte des outils constitue la première vérification de la connexion. La réussite d'une opération métier nécessite également une connexion validée avec le système qui la traite.

## Catalogue des outils MCP

| Outil | Fonction | Effet |
| :--- | :--- | :--- |
| `order_design_preflight` | Vérifier l'éligibilité de l'entreprise et les analyses disponibles. | Lecture seule |
| `start_order_design` | Envoyer le fichier XLSX fourni et attendre la confirmation de l'enregistrement de la conception. | Écrit des données métier |
| `add_order_to_cart` | Ajouter au panier une conception dont l'enregistrement est confirmé. | Écrit des données métier |
| `get_order_cart` | Consulter le panier de commandes. | Lecture seule |
| `calculate_order_price` | Obtenir un devis pour les commandes sélectionnées. | Lecture seule |
| `submit_verified_order` | Vérifier le devis et soumettre les commandes sélectionnées. | Écrit des données métier |
| `get_report_results` | Récupérer les résultats de rapports existants au format JSON. | Lecture seule |

Ces sept outils sont enregistrés dans l'implémentation MCP actuelle. Le bon fonctionnement des processus métier de bout en bout reste à vérifier. Consultez les [signatures, l'état et les limites](../../docs/tool-catalog.md).

## Skills

| Skill | Fonction | État de publication |
| :--- | :--- | :--- |
| [Conception de commandes · `order-design`](../../skills/order_design/SKILL.md) | Guider les demandes de commande, la soumission des conceptions et la soumission des commandes. | Inclus · Disponible au téléchargement |
| [Rapport de résultats · `auto_html_report`](../../skills/auto_html_report/SKILL.md) | Génère des rapports HTML autonomes et multilingues à partir des résultats JSON existants fournis par l'utilisateur, avec tableau récapitulatif, graphiques et images disponibles. | Inclus · Disponible au téléchargement |

MCP expose des opérations ; les Skills décrivent comment un agent les utilise dans le cadre d'une tâche. L'installation d'un Skill n'accorde pas l'accès au service et n'enregistre pas automatiquement MCP. [Parcourir le catalogue →](../../skills/README.md)

<a id="beta"></a>

## Beta Playground

Biointron OS est lancé sous la forme d'un environnement d'essai Beta. Certaines connexions peuvent encore être indisponibles. Indiquez le résultat réel de chaque étape ; une réponse HTTP réussie ou un nom d'outil visible ne prouve pas qu'une opération métier a été menée à terme.

La création et la soumission de commandes nécessitent l'autorisation de l'utilisateur. Si une opération d'écriture dépasse le délai d'attente, vérifiez l'état de la commande existante avant de réessayer. Pour obtenir un accès ou vous renseigner sur une fonctionnalité indisponible, contactez le représentant Biointron qui vous a fourni votre compte.

<a id="online-platform"></a>

## Plateforme en ligne Biointron

La plateforme en ligne de Biointron propose les flux de travail des projets RushDATA dans le navigateur, avec un accès aux brouillons de projets, au panier, aux commandes et à un assistant IA. Ouvrez la plateforme pour découvrir les services disponibles et consulter les informations des projets.

[Accéder à la plateforme en ligne Biointron →](https://ai.biointron.com/#/landing)

<a href="https://ai.biointron.com/#/landing"><img src="../../assets/Biointron_Rushdata.png" alt="Interface des projets RushDATA sur la plateforme en ligne Biointron" width="1000" /></a>

<a id="faq"></a>

## Questions fréquentes

<details>
<summary><strong>Ai-je besoin à la fois de MCP et des Skills ?</strong></summary>

MCP fournit des outils que l'agent peut appeler. Les Skills ajoutent des instructions pour les processus et peuvent avoir leurs propres dépendances. Respectez les prérequis de chaque Skill publié ; télécharger un Skill ne suffit pas à connecter un service.

</details>

<details>
<summary><strong>Un outil présent dans la liste est-il prêt à être utilisé pour des opérations métier ?</strong></summary>

Non. La découverte confirme que l'outil est enregistré. La configuration du système en arrière-plan, l'accès au compte et l'opération demandée doivent également être validés. Le catalogue rend compte de cette distinction.

</details>

<details>
<summary><strong>Où se trouvent le serveur et l'implémentation métier ?</strong></summary>

Ce dépôt distribue les documents d'intégration publics et les Skills. Le service hébergé et l'implémentation métier privée sont maintenus séparément.

</details>

## Documentation

| Pour commencer | Références |
| :--- | :--- |
| [Installer MCP et les Skills](../../docs/installation.md) | [Catalogue des outils MCP](../../docs/tool-catalog.md) |
| [Catalogue des Skills](../../skills/README.md) | [API et exemples JSON](../../docs/api.md) |
| [Contribuer](../../CONTRIBUTING.md) | [État de la licence](../../docs/license.md) |

Les guides détaillés sont disponibles en chinois et en anglais.

## Licence

Distribué sous licence [PolyForm Noncommercial 1.0.0](../../LICENSE). **Cette licence n'autorise pas l'usage commercial.** Le code source de ce dépôt est accessible pour un usage non commercial. Consultez le [périmètre et les conditions](../../docs/license.md).

---

<div align="center">
<sub>Biointron OS · Pour les agents. Pour les modèles. Pour les personnes.</sub>
</div>
