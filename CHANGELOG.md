# Changelog

Todas as alterações notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere ao [Versionamento Semântico](https://semver.org/lang/pt-BR/).

---

## [1.1.0] - 2026-08-16

### Adicionado
- **Diálogos de Configuração 100% Responsivos com Barra de Rolagem**:
  - `BaseToolkitDialog` agora envolve o conteúdo em um `QScrollArea` transparente e fluido com scrollbars escuras de alta performance.
  - Ajuste de tamanho dinâmico sem quebra de layout ou cortes em telas menores e monitores de qualquer resolução.
- **Estúdio de Tema com Círculo RGB Interativo (`RGBWheelWidget`)**:
  - Seletor circular de cores RGB em gradiente cônico com detecção precisa de clique e arrasto para escolher qualquer cor de fundo.
  - Suporte completo a cores de fundo customizadas (`theme.background`), com atualização dinâmica de variáveis CSS `--canvas` e folhas de estilo Qt em tempo real.
  - Presets rápidos para modos OLED: *🖤 Full Black AMOLED (#000000)*, *🌌 Deep Midnight (#0B0E14)*, *🌲 Forest Night (#08120C)*, *🪐 Obsidian Dark (#121214)*, *🔮 Cosmic Violet (#0E0B14)* e *⚓ Cyberpunk Dark (#0D1117)*.
  - Card de pré-visualização ao vivo atualizado em tempo real dentro do diálogo.
- **Modo Somente Imagem na Frente (Front-Only Image Cards)**:
  - Opção no layout de imagem `image_only_front` para criação de flashcards puramente visuais, onde a imagem recebida do Discord fica exclusivamente na frente e o verso permanece limpo.
  - Roteamento configurável de deck de destino (ex: `Medicina::Anatomia`) com criação automática do deck.
- **Guia Didático e Documentação Interna Integrada (`HelpDialog`)**:
  - Novo diálogo didático e ação no menu *Help & Setup Guide...* com instruções detalhadas passo a passo para configuração de canais do Discord, Bot Token, modo desenvolvedor, círculo RGB e REST Webhook.
  - Caixas de dicas didáticas embutidas no próprio diálogo de configurações do Discord.
- **Galeria Visual no README.md com 6 Espaços Formatados**:
  - 3 espaços dedicados para exemplos do Dashboard (Métricas em Tempo Real, Criador Rápido de Cards e Fila FIFO de Jobs).
  - 3 espaços dedicados para exemplos das Configurações (Canais de Imagem do Discord, Estúdio de Tema com Círculo RGB e Regras de Roteamento de Decks).

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
