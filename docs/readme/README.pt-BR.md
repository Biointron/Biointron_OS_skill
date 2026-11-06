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
<strong lang="pt-BR" dir="ltr">Português (Brasil)</strong> ·
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

### Conecte seu agente de IA aos serviços da Biointron.

Das solicitações de pedidos aos resultados dos relatórios, use os fluxos da Biointron nas ferramentas que você já conhece.<br />
O MCP estabelece a conexão. Os Skills orientam o fluxo de trabalho. Você mantém o controle.

[![Catálogo de ferramentas MCP](https://img.shields.io/badge/MCP-tool_catalog-087F8C?style=flat-square)](../../docs/tool-catalog.md)
[![Skills](https://img.shields.io/badge/Agent-Skills-234E70?style=flat-square)](../../skills/README.md)
[![Licença não comercial](https://img.shields.io/badge/License-Noncommercial-6B7280?style=flat-square)](../../LICENSE)
[![Beta Playground](https://img.shields.io/badge/Release-Beta_Playground-D7A345?style=flat-square)](#beta)

<br />

<!-- HERO: Keep the artwork path in sync across all language versions. -->
<img src="../../assets/biointron-os-hero.png" alt="Biointron OS" width="1000" />

<br />

**[Primeiros passos](#get-started) · [Ferramentas MCP](../../docs/tool-catalog.md) · [Skills](../../skills/README.md) · [API e exemplos](../../docs/api.md) · [Plataforma online](#online-platform) · [Perguntas frequentes](#faq)**

</div>

---

## Uma plataforma. Três formas de se conectar.

O Biointron OS é uma interface de acesso aos serviços da Biointron para agentes de IA, modelos e pessoas. Ele reúne o acesso aos serviços e as orientações para os fluxos de trabalho, com um plano de desenvolvimento que abrange pedidos, projetos enviados, andamento e resultados.

| Para agentes | Para modelos | Para pessoas |
| :--- | :--- | :--- |
| Descubra e invoque serviços por meio do **MCP**. | Trabalhe com **dados estruturados** e interfaces documentadas. | Acesse os fluxos por meio de uma **interface interativa**. |
| Combine chamadas de ferramentas com Skills específicos para cada tarefa. | As convenções de dados estão sendo alinhadas durante a fase Beta. | A experiência web é disponibilizada separadamente deste repositório. |

Este repositório é o ponto de acesso público aos Skills, aos guias de conexão, ao catálogo de ferramentas e aos exemplos. Os serviços de negócio da Biointron funcionam separadamente.

<a id="get-started"></a>

## Primeiros passos

### 1 · Conecte o MCP

Obtenha o token de acesso ao serviço e as permissões necessárias com seu contato na Biointron. Em um cliente MCP compatível com **Streamable HTTP** e **autenticação Bearer**, adicione:

| Configuração | Valor |
| :--- | :--- |
| Nome | `BiointronOS_MCP` |
| Transporte | Streamable HTTP |
| URL | `https://mcp-rusta-order-blgdfvompw.cn-shanghai.fcapp.run/mcp` |
| Autenticação | `Authorization: Bearer <MCP_ACCESS_TOKEN>` |

Em clientes compatíveis com o formato `mcpServers`, mescle esta configuração com as configurações existentes e substitua o marcador pelo seu próprio token:

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

Os dois cabeçalhos de timeout são itens personalizados da configuração de referência: 60000 ms = 60 segundos e 660000 ms = 11 minutos. Eles só têm efeito se o cliente ou o serviço oferecer suporte a esses cabeçalhos; incluí-los em `headers` não garante, por si só, uma alteração no tempo de espera do cliente. Configure os limites de tempo conforme a documentação do seu cliente.

Veja mais detalhes no [guia de instalação](../../docs/installation.md#mcp).

### 2 · Adicione Skills

Escolha um dos Skills incluídos no [catálogo de Skills](../../skills/README.md). Baixe a pasta completa, incluindo `references/` e quaisquer scripts fornecidos, e coloque-a no diretório de Skills do seu agente. Consulte a [instalação de Skills](../../docs/installation.md#skills) para Codex e Claude Code.

Os dois pacotes já estão incluídos neste repositório: `skills/order_design/` para `order-design` e `skills/auto_html_report/` para `auto-html-report`. Eles estão disponíveis para download; isso não comprova a validação completa dos fluxos de negócio.

### 3 · Comece com uma introdução somente de leitura

```text
Liste as ferramentas MCP da Biointron disponíveis nesta sessão e explique a função de cada uma.
Informe quais recursos estão prontos e quais ainda estão em fase Beta.
Não crie nem envie nenhum pedido.
```

A descoberta de ferramentas é a primeira verificação da conexão. Para que uma operação de negócio seja concluída com sucesso, a conexão com o respectivo sistema de backend também precisa ser validada.

## Catálogo de ferramentas MCP

| Ferramenta | Finalidade | Efeito |
| :--- | :--- | :--- |
| `get_order_input_requirements` | Coleta perguntas independentes em lotes por padrão; valida todos os dados da etapa antes da gravação. Não exige JWT de negócio. | Somente leitura |
| `search_order_antigens` | Pesquisa produtos e especificações reais por palavra-chave, com informações para carregar as próximas páginas. | Somente leitura |
| `order_design_preflight` | Verificar a elegibilidade da empresa e os testes disponíveis. | Somente leitura |
| `start_order_design` | Enviar o XLSX fornecido e aguardar a confirmação de salvamento do projeto. | Grava dados de negócio |
| `get_order_design_result` | Após a escolha do cliente, lê o HTML real do projeto salvo para entrega, sem modificar o pedido. | Somente leitura |
| `add_order_to_cart` | Adicionar ao carrinho um projeto com salvamento confirmado. | Grava dados de negócio |
| `end_order_workflow` | Orientar o cliente a descartar o contexto local, sem revogar a assinatura nem cancelar o pedido. | Somente instrução ao cliente |
| `get_order_cart` | Consultar o carrinho de pedidos. | Somente leitura |
| `calculate_order_price` | Obter uma cotação para os pedidos selecionados. | Somente leitura |
| `submit_verified_order` | Confere a cotação e envia os pedidos selecionados para confirmação humana. | Grava dados de negócio |
| `get_report_results` | Recuperar resultados de relatórios existentes em formato JSON. | Somente leitura |

A implementação local lista **11 ferramentas**: 10 exigem o JWT do cliente atual em `business_token`; `get_order_input_requirements` funciona localmente sem JWT. Esta atualização ainda não foi implantada, e o funcionamento dos processos de ponta a ponta continua sem validação em ambiente real. Consulte as [assinaturas, o status e as limitações](../../docs/tool-catalog.md).

## Skills

| Skill | Finalidade | Status de publicação |
| :--- | :--- | :--- |
| [Projeto de pedidos · `order-design`](../../skills/order_design/SKILL.md) | Explicar pacotes, coletar dados em lotes, selecionar produtos do catálogo, oferecer a visualização do HTML após salvar o projeto, conferir carrinho e cotações e enviar pedidos para confirmação humana. | Incluído; disponível para download |
| [Relatório HTML · `auto-html-report`](../../skills/auto_html_report/SKILL.md) | Gerar relatórios HTML independentes, em vários idiomas, a partir de resultados JSON fornecidos pelo usuário, com tabelas de resumo, gráficos e imagens disponíveis. | Incluído; disponível para download |

O MCP disponibiliza operações; os Skills descrevem como um agente as utiliza em uma tarefa. Instalar um Skill não concede acesso ao serviço nem registra o MCP automaticamente. [Explore o catálogo →](../../skills/README.md)

O envio de pedidos aguarda a confirmação da Biointron; não comprova o início da produção nem a conclusão de experimentos.

Com resultados JSON já fornecidos, o Skill `auto-html-report` gera o relatório localmente, sem credenciais nem conexão MCP. Sem JSON, uma consulta autorizada pode usar o número do pedido e o JWT do cliente atual em `get_report_results`, antes de gerar o relatório. Apenas o número do pedido não basta. Reutilize um JWT válido; solicite somente os dados que faltarem de Biointron Account e App Key quando for necessário obter o JWT.

As instruções do pacote de relatórios estão em inglês, mas o relatório segue o idioma solicitado pelo cliente.

<a id="beta"></a>

## Beta Playground

O Biointron OS está sendo apresentado como um ambiente de testes Beta. Algumas conexões ainda podem estar indisponíveis. Informe o resultado real de cada etapa; uma resposta HTTP bem-sucedida ou um nome de ferramenta visível não comprova que uma operação de negócio foi concluída.

A criação e o envio de pedidos exigem autorização do usuário. Se uma operação de gravação exceder o tempo limite, verifique o status do pedido existente antes de tentar novamente. Para obter acesso ou consultar um recurso indisponível, entre em contato com o representante da Biointron que forneceu sua conta.

<a id="online-platform"></a>

## Plataforma online Biointron

A plataforma online da Biointron reúne os fluxos de projetos RushDATA no navegador, com acesso a rascunhos de projetos, carrinho, pedidos e um assistente de IA. Abra a plataforma para explorar os serviços disponíveis e consultar as informações dos projetos.

[Acesse a plataforma online da Biointron →](https://ai.biointron.com/#/landing)

<a href="https://ai.biointron.com/#/landing"><img src="../../assets/Biointron_Rushdata.png" alt="Interface da plataforma online Biointron com acesso aos projetos RushDATA" width="1000" /></a>

<a id="faq"></a>

## Perguntas frequentes

<details>
<summary><strong>Preciso tanto do MCP quanto dos Skills?</strong></summary>

O MCP fornece ferramentas que podem ser invocadas. Os Skills acrescentam instruções para os fluxos de trabalho e podem ter suas próprias dependências. Siga os requisitos de cada Skill publicado; apenas baixar um Skill não conecta um serviço.

</details>

<details>
<summary><strong>Uma ferramenta aparecer na lista significa que está pronta para uso em operações de negócio?</strong></summary>

Não. A descoberta confirma que a ferramenta está registrada. A configuração do backend, o acesso à conta e a operação solicitada também precisam ser validados. O catálogo registra essa distinção.

</details>

<details>
<summary><strong>Onde estão o servidor e a implementação da lógica de negócio?</strong></summary>

Este repositório distribui os materiais públicos de integração e os Skills. O serviço hospedado e a implementação privada da lógica de negócio são mantidos separadamente.

</details>

## Documentação

| Comece aqui | Referência |
| :--- | :--- |
| [Instalar MCP e Skills](../../docs/installation.md) | [Catálogo de ferramentas MCP](../../docs/tool-catalog.md) |
| [Catálogo de Skills](../../skills/README.md) | [API e exemplos JSON](../../docs/api.md) |
| [Contribuir](../../CONTRIBUTING.md) | [Status da licença](../../docs/license.md) |

Os guias detalhados estão disponíveis em chinês e inglês.

## Licença

Licenciado sob a [PolyForm Noncommercial 1.0.0](../../LICENSE). **Esta licença não permite o uso comercial.** O código-fonte deste repositório está disponível para uso não comercial. Consulte o [escopo e os termos](../../docs/license.md).

---

<div align="center">
<sub>Biointron OS · Para agentes. Para modelos. Para pessoas.</sub>
</div>
