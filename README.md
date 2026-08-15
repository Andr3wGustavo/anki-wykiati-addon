# 🖤 Anki Discord Toolkit (ADT) 💬

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python: 3.9+](https://img.shields.io/badge/python-3.9+-brightgreen.svg)](https://python.org)
[![Anki: 2.1.45+](https://img.shields.io/badge/Anki-2.1.45%2B%20%7C%2024.x%2B-blueviolet.svg)](https://apps.ankiweb.net/)
[![Tests: 35 Passing](https://img.shields.io/badge/tests-35%20passing-success.svg)](test_addon.bat)
[![Theme: Pure Black #000000](https://img.shields.io/badge/Theme-Pure%20Black%20AMOLED-black.svg)](#-pure-black-theme-oled--amoled)

Um add-on profissional, modular e de alta performance para o **Anki**, integrando automação de criação de flashcards via **Discord / Webhooks HTTP** e um tema **Pure Black (#000000 AMOLED)** de alto contraste projetado para telas modernas.

---

## 📑 Sumário

- [Visão Geral e Diferenciais](#-visão-geral-e-diferenciais)
- [Arquitetura e Fluxo de Dados](#-arquitetura-e-fluxo-de-dados)
- [Como Rodar os Testes (.bat no Windows)](#-como-rodar-os-testes-bat-no-windows)
- [Instalação no Anki](#-instalação-no-anki)
- [Protocolo Discord (!anki)](#-protocolo-discord-anki)
- [Servidor HTTP Bridge (Webhooks)](#-servidor-http-bridge-webhooks)
- [Configuração de Bot no Discord](#-configuração-de-bot-no-discord)
- [Pure Black Theme (OLED / AMOLED)](#-pure-black-theme-oled--amoled)
- [Roteamento Inteligente de Decks](#-roteamento-inteligente-de-decks)
- [Estrutura do Código-Fonte](#-estrutura-do-código-fonte)
- [Perguntas Frequentes (FAQ) & Soluções](#-perguntas-frequentes-faq--soluções)

---

## 🌟 Visão Geral e Diferenciais

O **Anki Discord Toolkit** resolve dois dos maiores desafios de estudantes e desenvolvedores:
1. **Fricção ao criar cartões**: Você está discutindo um tópico técnico no Discord ou lendo código e quer transformar uma dúvida/conceito em flashcard imediatamente sem sair da conversa ou abrir a janela do Anki.
2. **Cansaço visual do tema padrão**: O dark mode nativo do Anki utiliza tons acinzentados. O ADT implementa preto absoluto `#000000`, economizando bateria em painéis OLED e garantindo legibilidade nítida.

### ✨ Principais Recursos:
- **🖤 Pure Black Real**: Fundo preto sólido `#000000` em toda a interface Qt e nas páginas WebViews (Deck Browser, Card Reviewer e Estatísticas).
- **💬 Criação Instantânea via Discord**: Basta digitar `!anki` no seu canal do Discord com a frente e verso.
- **⚡ Fila Assíncrona Não-Bloqueante**: Utiliza thread trabalhadora em background; a interface do Anki nunca congela esperando requisições de rede.
- **🛡️ Anti-Duplicação Criptográfica**: Gera hash SHA-256 de cada cartão e rastreia IDs de mensagens para evitar cartões repetidos.
- **🎯 Roteamento Inteligente (Smart Deck Routing)**: Direciona cartões automaticamente para baralhos específicos baseado em tags (ex: tag `python` vai para `Programming::Python`).
- **🧩 Suporte a Cloze Deletion**: Detecta automaticamente a sintaxe `{{c1::...}}` e formata para o modelo de lacunas do Anki.
- **🌐 Servidor Webhook HTTP Local**: Permite integrar bots externos, scripts Python, extensões de navegador ou automações via REST API em `http://127.0.0.1:8765/api/card`.

---

## 🏗️ Arquitetura e Fluxo de Dados

O projeto segue os princípios **SOLID** e arquitetura limpa:

```text
       ┌──────────────────┐               ┌──────────────────┐
       │   Discord Bot    │               │  Local Webhook   │
       │ (REST Poller API)│               │ (HTTP 127.0.0.1) │
       └────────┬─────────┘               └────────┬─────────┘
                │                                  │
                └─────────────────┬────────────────┘
                                  │ Mensagem Bruta
                                  ▼
                     ┌───────────────────────────┐
                     │    AuthorizationPolicy    │ (Segurança / Whitelist / Rate Limit)
                     └────────────┬──────────────┘
                                  │
                                  ▼
                     ┌───────────────────────────┐
                     │       DiscordParser       │ (Extrai Front, Back, Tags, Cloze)
                     └────────────┬──────────────┘
                                  │ CardPayload
                                  ▼
                     ┌───────────────────────────┐
                     │  AntiDuplicationRegistry  │ (Verifica Hash SHA-256)
                     └────────────┬──────────────┘
                                  │
                                  ▼
                     ┌───────────────────────────┐
                     │         JobQueue          │ (Fila Persistente em Disco)
                     └────────────┬──────────────┘
                                  │
                                  ▼
                     ┌───────────────────────────┐
                     │        SyncWorker         │ (Thread em Background)
                     └────────────┬──────────────┘
                                  │ DeckRouter (Tag/Keyword Rules)
                                  ▼
                     ┌───────────────────────────┐
                     │   NoteAdapter (Anki API)  │ (Thread Principal do Anki)
                     └────────────┬──────────────┘
                                  │
                                  ▼
                     ┌───────────────────────────┐
                     │    Anki Collection DB     │ 🎴 Card Salvo com Sucesso!
                     └───────────────────────────┘
```

---

## 🚀 Como Rodar os Testes (.bat no Windows)

Para facilitar os testes, foi criado um script interativo `test_addon.bat` na raiz do projeto.

### Passo a Passo:
1. Abra o arquivo **`test_addon.bat`** (clicando duas vezes ou executando pelo Prompt de Comando / PowerShell).
2. O menu interativo exibirá as seguintes opções:

```text
===============================================================================
               ANKI DISCORD TOOLKIT - PAINEL DE CONTROLE E TESTES
===============================================================================

  [1] Executar Todos os Testes Unitarios Automatizados (35 Testes)
  [2] Gerar Pacote Distribuivel .ankiaddon (Pasta release/)
  [3] Iniciar Servidor HTTP Bridge Local (Modo Teste Standalone)
  [4] Enviar Cartao de Teste via Webhook Local (cURL / PowerShell)
  [5] Instalar Add-on Diretamente no Anki Local (%APPDATA%\Anki2)
  [6] Sair
===============================================================================
```

- **Opção 1**: Executa todos os 35 testes unitários cobrindo todos os módulos com 100% de sucesso.
- **Opção 2**: Gera o pacote `.ankiaddon` e `.zip` na pasta `release/`.
- **Opção 3**: Inicia o servidor HTTP Webhook para testes offline sem abrir o Anki.
- **Opção 4**: Envia um cartão de exemplo em JSON via PowerShell para testar a comunicação.
- **Opção 5**: Copia os arquivos do add-on diretamente para a pasta de extensões do seu Anki.

---

## 📦 Instalação no Anki

### Método 1: Gerar e Instalar o arquivo `.ankiaddon`
1. Execute `test_addon.bat` e escolha a opção `[2]` (ou rode `python package_addon.py`).
2. Abra o Anki e vá em: **Ferramentas (Tools)** → **Complementos (Add-ons)** (ou tecle `Ctrl+Shift+A`).
3. Clique em **"Instalar de arquivo..."** e selecione `release/anki-discord-toolkit.ankiaddon`.
4. Reinicie o Anki.

### Método 2: Instalação Rápida no Windows
1. Execute `test_addon.bat` e escolha a opção `[5]`.
2. O script copiará o código diretamente para `%APPDATA%\Anki2\addons21\anki_discord_toolkit`.
3. Reinicie o Anki.

---

## 💬 Protocolo Discord (!anki)

Para criar cartões pelo Discord, envie mensagens no canal autorizado seguindo a sintaxe chave-valor:

### Cartão Básico:
```text
!anki
front: O que é o Virtual DOM no React?
back: É uma representação leve em memória da árvore do DOM real, usada para otimizar re-renderizações através do algoritmo de reconciliação (Diffing).
deck: Frontend::React
tags: react, javascript, web
```

### Cartão com Código / Markdown:
```text
!anki
front: Como instanciar uma thread em Python?
back:
```python
import threading

def worker():
    print("Executando em background!")

t = threading.Thread(target=worker, daemon=True)
t.start()
```
deck: Programming::Python
tags: python, threading, concurrency
```

### Cartão Cloze (Omissão de Palavras):
```text
!anki
front: O protocolo {{c1::DNS}} converte nomes de domínio em endereços {{c2::IP}} na porta {{c3::53}}.
deck: Networking
tags: redes, dns, protocolos
```

---

## 🌐 Servidor HTTP Bridge (Webhooks)

O add-on inclui um servidor REST HTTP embutido (`http://127.0.0.1:8765`).

### Exemplo de Envio em JSON (cURL):
```bash
curl -X POST http://127.0.0.1:8765/api/card \
  -H "Content-Type: application/json" \
  -d '{
    "front": "O que é Redis?",
    "back": "Um banco de dados em memória chave-valor de altíssima velocidade.",
    "deck": "Database::Redis",
    "tags": ["redis", "nosql", "cache"]
  }'
```

### Exemplo de Envio via Python:
```python
import urllib.request
import json

payload = {
    "front": "Qual é a complexidade de busca em uma Hash Table balanceada?",
    "back": "O(1) no caso médio.",
    "deck": "Computer Science::Algorithms",
    "tags": ["dsa", "complexity"]
}

req = urllib.request.Request(
    "http://127.0.0.1:8765/api/card",
    data=json.dumps(payload).encode("utf-8"),
    headers={"Content-Type": "application/json"}
)

with urllib.request.urlopen(req) as resp:
    print(resp.read().decode("utf-8"))
```

---

## 🤖 Configuração de Bot no Discord

Caso deseje que o Anki leia mensagens diretamente de canais do Discord:
1. Acesse o [Discord Developer Portal](https://discord.com/developers/applications).
2. Crie uma nova Aplicação (ex: `Anki Bot`).
3. Vá na aba **Bot** → **Reset Token** e copie o seu Token secreto.
4. Em **Privileged Gateway Intents**, ative **Message Content Intent**.
5. No Anki, acesse **Ferramentas** → **Anki Discord Toolkit** → **Configurações do Discord**.
6. Cole o seu Bot Token, informe os IDs dos canais permitidos e marque **"Habilitar Leitor Automático de Mensagens"**.
7. Clique em **Salvar**.

---

## 🖤 Pure Black Theme (OLED / AMOLED)

O tema do **Anki Discord Toolkit** foi desenhado com precisão pixel a pixel:
- **Fundo `#000000` absoluto**: Reduz o cansaço visual e economiza bateria em telas OLED.
- **Tipografia Nítida**: Texto primário `#FFFFFF` de alto contraste e secundário `#A0AAB4`.
- **Cores de Destaque Personalizáveis**: Escolha entre Azul Vivid (`#3B82F6`), Verde Esmeralda (`#10B981`), Roxo Índigo (`#6366F1`), Vermelho Carmesim (`#EF4444`) ou Âmbar Dourado (`#F59E0B`).
- **Atalho Rápido**: Pressione `Ctrl+Shift+B` no Anki a qualquer momento para ligar/desligar o tema.

---

## 🎯 Roteamento Inteligente de Decks

Você não precisa especificar o `deck:` em todas as mensagens! O motor de regras direciona automaticamente:

1. **Regras de Tag**: Se o cartão tiver a tag `python`, ele vai automaticamente para `Programming::Python`.
2. **Regras de Palavra-chave**: Se o texto contiver o termo `docker`, ele vai para `DevOps::Docker`.
3. **Deck Padrão**: Se nenhuma regra casar e você não informou o deck, ele vai para o baralho padrão configurado (`Default`).

Gerencie essas regras visualmente em **Ferramentas** → **Anki Discord Toolkit** → **Regras de Roteamento de Decks**.

---

## 📂 Estrutura do Código-Fonte

```text
anki-addon/
├── __init__.py               # Ponto de entrada e bootstrap do addon
├── config.json               # Schema padrão de configuração
├── manifest.json             # Metadados do pacote Anki
│
├── core/                     # Módulos fundamentais
│   ├── config.py             # ConfigManager reativo com autocura
│   ├── logger.py             # Logger estruturado com rotação e prefixo [ADT]
│   ├── constants.py          # Constantes, limites e protocolos
│   ├── event_bus.py          # Barramento de eventos Pub/Sub thread-safe
│   └── exceptions.py         # Hierarquia de exceções de domínio
│
├── theme/                    # Motor de Estilo Pure Black
│   ├── palette.py            # Tokens de cores OLED/AMOLED
│   ├── styles.py             # Geradores de QSS nativo e CSS de WebViews
│   └── engine.py             # Ciclo de vida e injeção de estilo
│
├── anki/                     # Camada de Adaptação com APIs do Anki
│   ├── notes.py              # NoteAdapter: criação, formatação e tags
│   ├── decks.py              # DeckAdapter: localização e criação hierárquica
│   └── operations.py         # Despachante seguro para a thread principal da GUI
│
├── discord/                  # Integração com Discord e Webhooks
│   ├── models.py             # Modelos de domínio (CardPayload, DiscordEvent)
│   ├── parser.py             # Parser do protocolo !anki
│   ├── security.py           # AuthorizationPolicy (whitelist e rate limiting)
│   ├── commands.py           # Handlers de !anki-help, !anki-status, etc.
│   ├── bridge.py             # Orquestrador do Discord Bridge
│   └── client.py             # Servidor HTTP Webhook e Poller REST
│
├── sync/                     # Fila de Processamento em Background
│   ├── jobs.py               # Modelo SyncJob e ciclo de estados
│   ├── queue.py              # Fila FIFO thread-safe com persistência em disco
│   ├── dedup.py              # Registro anti-duplicação por SHA-256 e ID
│   └── worker.py             # Background Sync Worker
│
├── routing/                  # Motor de Roteamento Inteligente
│   └── router.py             # DeckRouter por tags e palavras-chave
│
├── templates/                # Gerenciamento de Modelos de Cartões
│   └── manager.py            # Mapeamento para Basic, Reversed e Cloze
│
├── ui/                       # Interface Gráfica (Qt / PyQt)
│   ├── menu.py               # Injeção no menu "Ferramentas" e atalhos
│   ├── dashboard.py          # Painel de controle e monitoramento de jobs
│   ├── theme_settings.py     # Diálogo de configurações do tema
│   ├── discord_settings.py   # Diálogo de configurações do Discord
│   ├── deck_rules_dialog.py  # Gerenciador de regras de baralhos
│   ├── templates_dialog.py   # Inspetor de tipos de notas
│   ├── about_dialog.py       # Diálogo sobre o addon e diagnóstico
│   └── components/           # Componentes base reutilizáveis (BaseToolkitDialog)
│
└── tests/                    # Suíte de Testes Automatizados (35 Testes)
    ├── test_config.py
    ├── test_parser.py
    ├── test_security.py
    ├── test_routing.py
    ├── test_queue_and_dedup.py
    ├── test_theme.py
    ├── test_bridge_and_commands.py
    └── test_templates_and_adapter.py
```

---

## ❓ Perguntas Frequentes (FAQ) & Soluções

#### 1. Preciso instalar alguma biblioteca externa via `pip`?
**Não.** O Anki Discord Toolkit foi projetado com arquitetura de zero dependências externas. Tudo roda na biblioteca padrão do Python e nas bibliotecas Qt/PyQt embutidas no próprio Anki.

#### 2. Como posso testar sem precisar conectar ao Discord agora?
Você pode:
- Usar o **Criador Rápido de Cartão** dentro do **Dashboard** (`Ferramentas` → `Anki Discord Toolkit` → `Dashboard e Métricas`).
- Ou executar a opção `[4]` no `test_addon.bat` para disparar uma requisição HTTP de teste.

#### 3. Como o add-on lida com duplicatas?
Cada mensagem gera um hash criptográfico baseado no conteúdo normalizado da pergunta, resposta e baralho. Se você reenviar a mesma mensagem, o add-on identifica a repetição e ignora a criação sem gerar erros na coleção.

#### 4. O add-on funciona em Mac e Linux?
**Sim!** O código é 100% multiplataforma e suporta Windows, macOS (Intel e Apple Silicon) e distribuições Linux.

---

## 📄 Licença

Este projeto está licenciado sob a **MIT License** — consulte o arquivo [LICENSE](LICENSE) para mais detalhes.
