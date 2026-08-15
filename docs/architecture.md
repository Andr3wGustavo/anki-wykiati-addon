# Anki Discord Toolkit — Arquitetura de Sistema

Este documento descreve a arquitetura técnica do **Anki Discord Toolkit**, seus módulos, camadas de abstração, fluxos de dados e decisões de engenharia.

---

## 1. Visão Geral da Arquitetura

O sistema segue rigorosamente o princípio de responsabilidade única (SRP), inversão de dependência (DIP) e desacoplamento de camadas. O núcleo do Anki nunca é manipulado diretamente por conexões de rede ou parsers brutos.

```text
┌────────────────────────────────────────────────────────┐
│                      INPUT LAYER                       │
│  - Discord REST Bot Poller                             │
│  - Local HTTP Webhook Bridge (127.0.0.1:8765)           │
│  - Manual Test Creator (Dashboard GUI)                 │
└───────────────────────────┬────────────────────────────┘
                            │ Raw Text / JSON
                            ▼
┌────────────────────────────────────────────────────────┐
│                    SECURITY & PARSER                   │
│  - AuthorizationPolicy (Users, Channels, Rate Limit)   │
│  - DiscordParser (Key-Value blocks, Markdown, Cloze)   │
└───────────────────────────┬────────────────────────────┘
                            │ CardPayload (Domain Model)
                            ▼
┌────────────────────────────────────────────────────────┐
│                   QUEUE & DEDUPLICATION                │
│  - AntiDuplicationRegistry (Content Hash & Msg IDs)    │
│  - JobQueue (Thread-Safe FIFO, Persistent Storage)     │
└───────────────────────────┬────────────────────────────┘
                            │ SyncJob (Status: PENDING)
                            ▼
┌────────────────────────────────────────────────────────┐
│                     ROUTING ENGINE                     │
│  - DeckRouter (Tag Rules -> Keyword Rules -> Default)  │
└───────────────────────────┬────────────────────────────┘
                            │ Target Deck Resolved
                            ▼
┌────────────────────────────────────────────────────────┐
│                    ANKI ADAPTER LAYER                  │
│  - TemplateManager (Basic, Cloze, Reversed Field Map)  │
│  - NoteAdapter & DeckAdapter (Safe Anki Collection API)│
│  - Operations Dispatcher (Main GUI Thread Safe)        │
└───────────────────────────┬────────────────────────────┘
                            │
                            ▼
                   Collection / Notes
```

---

## 2. Descrição dos Módulos

### 2.1 Core (`core/`)
- `constants.py`: Centraliza todas as constantes do sistema (versões, comandos Discord, chaves de campos, limites).
- `config.py`: Gerenciador de configurações reativo. Suporta notação ponto (`config.get("theme.accent")`), autocura de arquivos corrompidos, mescla recursiva com schema padrão e persistência transparente no `AddonManager` do Anki ou em fallback local.
- `logger.py`: Logger estruturado com níveis dinâmicos (`DEBUG`, `INFO`, `WARNING`, `ERROR`), rotação de arquivos e prefixo `[ADT]`.
- `event_bus.py`: Barramento pub/sub desacoplado para comunicação síncrona entre módulos.
- `exceptions.py`: Hierarquia de exceções de domínio (`ParserError`, `SecurityError`, `DuplicateCardError`, etc.).

### 2.2 Tema Pure Black AMOLED (`theme/`)
- `palette.py`: Tokens de cores imutáveis focados em contraste real `#000000` para telas OLED.
- `styles.py`: Gerador de QSS para widgets nativos Qt e CSS para injeção no DeckBrowser e Reviewer do Anki.
- `engine.py`: Gerencia ciclo de vida do tema, alternância rápida e injeção em WebViews sem dependências externas.

### 2.3 Integração Discord (`discord/`)
- `models.py`: Modelos puros desacoplados do Anki (`CardPayload`, `DiscordMessageEvent`, `DiscordUser`, `JobStatus`).
- `parser.py`: Parser robusto de mensagens `!anki`, com suporte a blocos multilinhas, blocos de código markdown, detecção automática de Cloze `{{c1::...}}` e tags.
- `security.py`: `AuthorizationPolicy` para whitelist de usuários, whitelist de canais/servidores, limitação de taxa (sliding window) e proteção contra injeção.
- `commands.py`: Roteador de comandos informativos (`!anki-help`, `!anki-status`, `!anki-decks`, `!anki-ping`).
- `client.py`: Cliente dual: servidor HTTP local para webhooks (`/api/card`) e trabalhador poller do Discord via API REST pura da biblioteca padrão (`urllib`).

### 2.4 Fila e Anti-Duplicação (`sync/`)
- `jobs.py`: Modelo `SyncJob` com ciclo de estados (`PENDING`, `PROCESSING`, `SUCCESS`, `FAILED`, `RETRY`, `DUPLICATE`).
- `queue.py`: Fila FIFO persistida em disco com suporte a re-tentativas automáticas até o limite configurado.
- `dedup.py`: Registro de anti-duplicação baseado em hash criptográfico de conteúdo (`SHA256`) e ID de mensagem.
- `worker.py`: Thread trabalhadora em background que consome a fila e despacha as criações de cartão para a thread principal do Anki.

### 2.5 Roteamento Inteligente (`routing/`)
- `router.py`: Motor de regras hierárquicas:
  1. Deck explícito no cartão.
  2. Regra por tag (ex: `python` -> `Programming::Python`).
  3. Regra por palavra-chave no texto (ex: `docker` -> `DevOps::Docker`).
  4. Deck padrão de fallback.

### 2.6 Interface do Usuário (`ui/`)
- `dashboard.py`: Painel de controle visual com métricas em tempo real, criador rápido de testes e tabela de jobs.
- `theme_settings.py`: Diálogo de configuração de cores de destaque e overrides de WebView.
- `discord_settings.py`: Gerenciamento de credenciais do Discord e servidor HTTP.
- `deck_rules_dialog.py`: Tabela interativa para adicionar/remover regras de roteamento.
- `templates_dialog.py`: Inspetor de tipos de notas disponíveis no Anki.
- `about_dialog.py`: Informações do addon e diagnóstico do sistema.
- `menu.py`: Injeção de menus e atalhos globais (`Ctrl+Shift+D` para Dashboard, `Ctrl+Shift+B` para Pure Black).
