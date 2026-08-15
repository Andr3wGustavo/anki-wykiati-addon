# Changelog

Todas as alterações notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere ao [Versionamento Semântico](https://semver.org/lang/pt-BR/).

---

## [1.0.0] - 2026-08-15

### Adicionado
- **Pure Black OLED / AMOLED Theme**:
  - Paleta centralizada com fundo preto absoluto `#000000`.
  - Estilização completa de componentes nativos Qt (Menus, Botões, Tabelas, Caixas de Entrada, Scrollbars finas).
  - Injeção de CSS em WebViews (Deck Browser, Reviewer de Cartões e Telas de Estatísticas).
  - Suporte a personalização de cor de destaque (Accent) em tempo real.
  - Atalho global `Ctrl+Shift+B` para alternar o tema instantaneamente.
- **Discord → Anki Integration Engine**:
  - Parser robusto com suporte ao comando `!anki`, blocos de código markdown, multilinhas e tags.
  - Detecção automática e suporte ao modelo de notas **Cloze Deletion** (`{{c1::...}}`).
  - Suporte a comandos operacionais do Discord: `!anki-help`, `!anki-status`, `!anki-decks` e `!anki-ping`.
  - Servidor REST Webhook HTTP local integrado (`http://127.0.0.1:8765/api/card`) para envio direto de cartões via scripts e bots.
  - Trabalhador em background (Poller) do Discord usando a API REST oficial com token de bot.
- **Fila, Anti-Duplicação e Background Worker**:
  - Fila persistente FIFO (`JobQueue`) com suporte a re-tentativas automáticas.
  - Registro criptográfico de anti-duplicação (`AntiDuplicationRegistry`) baseado em SHA-256 e ID de mensagem.
  - Thread trabalhadora assíncrona (`SyncWorker`) que nunca congela a interface gráfica do Anki.
- **Roteamento Inteligente de Decks (Smart Deck Routing)**:
  - Regras configuráveis por tags e palavras-chave para envio automático de cartões para baralhos temáticos (ex: `python` → `Programming::Python`).
- **Interface Gráfica Completa (UI)**:
  - Dashboard de Métricas com contadores de cartões criados, mensagens processadas e histórico de jobs.
  - Criador rápido de cartões de teste integrado ao Dashboard.
  - Diálogos dedicados para Configurações do Tema, Configurações do Discord, Regras de Decks e Templates.
  - Integração no menu `Ferramentas` (Tools) do Anki.
- **Suíte de Testes Automatizados**:
  - 35 testes unitários cobrindo todos os módulos do sistema em modo headless.
- **Scripts de Automação para Windows**:
  - `test_addon.bat`: Menu interativo e testes automatizados em um clique.
  - `run_http_bridge.bat`: Inicializador rápido do servidor Webhook local.
  - `package_addon.py`: Gerador automático de pacote `.ankiaddon`.
