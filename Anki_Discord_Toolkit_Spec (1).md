# Anki Discord Toolkit — Especificação Completa e Roadmap de Implementação

## 1. Objetivo

Construir um addon profissional para Anki chamado **Anki Discord Toolkit**.

O projeto começa com duas funcionalidades principais:

1. **Pure Black Theme**
   - Interface visual com fundo preto sólido `#000000`.
   - Personalização sem depender apenas do dark mode do sistema.
2. **Discord → Anki**
   - Receber conteúdo estruturado do Discord e transformá-lo em notas/cards do Anki.
   - Definir automaticamente Front, Back, Deck e Tags.

A arquitetura deve ser modular para permitir futuras integrações com IA, PDFs, OCR, Obsidian, Telegram, URLs e outros sistemas.

> Regra fundamental: não implementar tudo de uma vez. Primeiro criar uma base pequena, estável e testável; depois evoluir por versões.

---

# 2. Resultado final desejado

O usuário deverá conseguir:

```text
Anki
 └── Tools
      └── Anki Discord Toolkit
           ├── Dashboard
           ├── Theme
           ├── Discord
           ├── Deck Rules
           ├── Templates
           └── Settings
```

Fluxo Discord:

```text
Discord
   ↓
Discord Bridge
   ↓
Validação
   ↓
Parser
   ↓
Fila
   ↓
Anki Addon
   ↓
Collection
   ↓
Deck
   ↓
Note/Card
```

---

# 3. Princípios obrigatórios

A implementação deve seguir estas regras:

- Código modular.
- Baixo acoplamento.
- Configuração separada do código.
- Logs estruturados.
- Tratamento de exceções.
- Testes automatizados sempre que possível.
- Não bloquear a UI do Anki.
- Não escrever diretamente no arquivo `.anki2` por conta própria.
- Usar as APIs/classes do Anki para trabalhar com Collection, Notes e Cards.
- Toda operação demorada deve ser executada em background.
- Toda operação de UI deve voltar para a thread principal.
- Não assumir APIs internas sem verificar a versão atual do Anki.
- Evitar dependências externas desnecessárias.
- Manter compatibilidade com as versões suportadas explicitamente pelo projeto.
- Documentar decisões técnicas.

A documentação oficial do Anki recomenda usar `anki`/`aqt` em vez de manipular diretamente o arquivo `.anki2`, e recomenda operações em background para tarefas longas. 

---

# 4. Stack

## Core

- Python
- Anki API
- `aqt`
- Qt/PyQt através de `aqt.qt`

## Interface

- Qt
- Widgets nativos do Anki
- QSS apenas quando apropriado

## Discord

Criar uma camada de integração isolada.

Não acoplar o restante do addon diretamente ao cliente Discord.

## Persistência

- Configuração do addon em arquivo de configuração próprio.
- Collection manipulada pelas APIs do Anki.
- Nunca criar uma segunda base de dados para duplicar a Collection sem necessidade.

---

# 5. Arquitetura

Estrutura inicial recomendada:

```text
anki-discord-toolkit/
│
├── __init__.py
├── config.json
├── README.md
├── LICENSE
│
├── core/
│   ├── __init__.py
│   ├── config.py
│   ├── logger.py
│   ├── constants.py
│   └── exceptions.py
│
├── ui/
│   ├── __init__.py
│   ├── menu.py
│   ├── dashboard.py
│   ├── settings.py
│   └── theme_settings.py
│
├── theme/
│   ├── __init__.py
│   ├── engine.py
│   ├── palette.py
│   └── styles.py
│
├── anki/
│   ├── __init__.py
│   ├── notes.py
│   ├── cards.py
│   ├── decks.py
│   └── operations.py
│
├── discord/
│   ├── __init__.py
│   ├── bridge.py
│   ├── client.py
│   ├── parser.py
│   ├── commands.py
│   └── models.py
│
├── sync/
│   ├── __init__.py
│   ├── queue.py
│   ├── worker.py
│   └── jobs.py
│
├── templates/
│   ├── __init__.py
│   └── manager.py
│
├── tests/
│   ├── test_parser.py
│   ├── test_config.py
│   ├── test_routing.py
│   └── test_validation.py
│
└── docs/
    ├── architecture.md
    ├── development.md
    └── discord-protocol.md
```

A estrutura pode ser adaptada se a versão atual do Anki tiver convenções diferentes.

---

# 6. Fase 0 — Pesquisa técnica antes de programar

Antes de escrever código:

1. Verificar a documentação atual do Anki.
2. Verificar a versão atual do Anki.
3. Verificar a versão de Qt/PyQt usada pela versão-alvo.
4. Identificar APIs públicas/recomendadas.
5. Identificar APIs internas que podem mudar.
6. Definir versões suportadas.
7. Definir como o addon será empacotado.
8. Definir estratégia de instalação local.
9. Definir estratégia de publicação futura no AnkiWeb.
10. Criar um documento `docs/compatibility.md`.

Não assumir que exemplos antigos da internet continuam válidos.

A documentação atual informa que o Anki usa PyQt para grande parte da interface e recomenda importar classes Qt por `aqt.qt`, justamente para facilitar compatibilidade entre builds Qt. 

---

# 7. Fase 1 — Skeleton

Criar o addon mínimo.

Requisitos:

- `__init__.py` carregando sem erro.
- Menu aparecendo no Anki.
- Janela simples de teste.
- Logger funcionando.
- Configuração carregando.
- Nenhuma integração Discord ainda.

Primeiro teste:

```text
Abrir Anki
↓
Addon carrega
↓
Nenhum erro
↓
Tools
↓
Anki Discord Toolkit
```

---

# 8. Fase 2 — Sistema de configuração

Criar configuração central.

Exemplo conceitual:

```json
{
  "theme": {
    "enabled": true,
    "background": "#000000"
  },
  "discord": {
    "enabled": false
  },
  "anki": {
    "default_deck": "Default"
  }
}
```

Requisitos:

- Valores padrão.
- Validação.
- Recuperação de configuração corrompida.
- Não salvar dados secretos em texto puro quando isso puder ser evitado.
- API interna única para ler/escrever configurações.

Criar:

```python
ConfigManager
```

---

# 9. Fase 3 — Pure Black Theme

Objetivo:

```text
#000000
```

como fundo principal.

Criar:

```text
theme/
├── engine.py
├── palette.py
└── styles.py
```

## Engine

Responsável por:

- ativar;
- desativar;
- reaplicar;
- restaurar.

## Palette

Centralizar:

```text
BACKGROUND = #000000
TEXT = ...
BORDER = ...
SURFACE = ...
```

Não espalhar cores pelo projeto.

---

# 10. Requisitos visuais

Testar:

- Deck Browser.
- Main Window.
- Reviewer.
- Browser.
- Editor.
- Menus.
- Dialogs.
- Settings.
- Tooltips.
- Scrollbars.
- Campos de texto.

Importante:

O objetivo é fundo preto sólido, mas o texto e controles devem continuar legíveis.

Não aplicar simplesmente `background: #000000` em absolutamente todos os widgets sem testar contraste e comportamento.

Criar uma camada de estilo controlada.

---

# 11. Fase 4 — Menu e Settings

Criar:

```text
Tools
└── Anki Discord Toolkit
    ├── Dashboard
    ├── Theme Settings
    ├── Discord Settings
    └── About
```

Settings:

```text
Theme
[✓] Enable Pure Black

Background:
[#000000]

Discord
[ ] Enable Bridge

Default Deck:
[Default]

Logging:
[INFO]
```

---

# 12. Fase 5 — Modelo interno de Card

Criar um modelo independente da implementação do Anki.

Exemplo conceitual:

```python
CardPayload(
    front="...",
    back="...",
    deck="...",
    tags=["python", "study"],
    note_type="Basic"
)
```

Isso é importante porque o Discord não deve conhecer detalhes internos do Anki.

Fluxo:

```text
Discord Message
      ↓
Parser
      ↓
CardPayload
      ↓
Anki Adapter
      ↓
Note
```

---

# 13. Fase 6 — Discord Protocol

Definir um protocolo claro.

Formato recomendado:

```text
!anki

front:
O que é Docker?

back:
Docker é uma plataforma de containers.

deck:
Programming::Docker

tags:
docker,containers,devops
```

O parser deve:

- detectar campos;
- validar campos obrigatórios;
- normalizar espaços;
- normalizar tags;
- detectar deck inexistente;
- retornar erros amigáveis.

---

# 14. Fase 7 — Discord Commands

Criar comandos:

```text
!anki
!anki-help
!anki-status
```

Posteriormente:

```text
!anki-decks
!anki-template
!anki-sync
```

Não implementar todos na primeira versão.

---

# 15. Fase 8 — Discord Bridge

Separar:

```text
Discord Client
```

de:

```text
Anki Bridge
```

O Discord Bridge deve transformar mensagens em eventos internos.

Exemplo:

```text
Discord
 ↓
DiscordEvent
 ↓
Parser
 ↓
CardPayload
 ↓
Queue
```

---

# 16. Segurança do Discord

Obrigatório:

- Autenticação.
- Identificação de usuário autorizado.
- Lista de servidores/canais autorizados.
- Validação de comandos.
- Limitação de tamanho.
- Rate limiting.
- Não executar comandos arbitrários recebidos do Discord.
- Não executar código Python recebido por mensagem.
- Não permitir que mensagens controlem o sistema operacional.

Criar:

```text
AuthorizationPolicy
```

---

# 17. Fase 9 — Queue

Criar fila:

```text
PENDING
PROCESSING
SUCCESS
FAILED
```

Cada job:

```text
id
timestamp
payload
status
error
retry_count
```

Objetivos:

- Não perder mensagens.
- Evitar duplicação.
- Permitir retry.
- Não travar o Anki.

---

# 18. Fase 10 — Anki Adapter

Criar uma camada:

```text
anki/
```

Responsável por:

- localizar/criar deck;
- criar Note;
- criar Card;
- adicionar tags;
- salvar;
- atualizar UI.

O restante do addon nunca deve acessar a Collection diretamente sem passar pelo adapter quando isso puder ser evitado.

---

# 19. Threading / Background Operations

Regra crítica:

```text
UI
│
├── menus
├── dialogs
└── visual updates

Background
│
├── network
├── Discord
├── parsing pesado
├── processamento
└── operações longas
```

Nunca bloquear a UI esperando rede.

A documentação oficial do Anki explica que operações longas na thread principal congelam a interface e recomenda operações em background; alterações de UI devem ocorrer na thread principal. 

Usar as ferramentas de operações/background disponibilizadas pelo Anki quando apropriado.

---

# 20. Fase 11 — Anti-Duplicação

O mesmo card não deve ser criado várias vezes se a mensagem for processada novamente.

Criar identificador:

```text
source = discord
message_id = ...
```

Manter metadados suficientes para reconhecer mensagens já processadas.

Exemplo:

```text
discord:guild:channel:message
```

---

# 21. Fase 12 — Smart Deck Routing

Criar regras:

```text
python → Programming::Python
linux → Linux
docker → Programming::Docker
network → Networking
```

Interface:

```text
Tag/Keyword
     ↓
Deck
```

Permitir prioridade:

```text
Regra específica
↓
Regra de categoria
↓
Deck padrão
```

---

# 22. Fase 13 — Templates

Suportar inicialmente:

```text
Basic
Basic (and reversed)
Cloze
```

Arquitetura:

```text
TemplateManager
```

Não prender o parser Discord a um único tipo de note.

---

# 23. Fase 14 — Dashboard

Dashboard inicial:

```text
Cards Created: 0
Messages Processed: 0
Failed Jobs: 0
Last Sync: Never
Discord: Disabled
Theme: Enabled
```

Depois:

- cards por dia;
- cards por deck;
- erros;
- filas;
- histórico.

---

# 24. Fase 15 — Testes

Criar testes para:

### Parser

```text
front válido
back válido
deck válido
tags válidas
campo ausente
formato inválido
```

### Config

```text
config normal
config vazia
config corrompida
valores inválidos
```

### Routing

```text
tag → deck
keyword → deck
fallback
```

### Security

```text
usuário autorizado
usuário não autorizado
canal autorizado
canal não autorizado
payload inválido
```

---

# 25. Fase 16 — Teste manual

Criar uma matriz:

```text
Windows
Linux
macOS
```

Testar:

- instalação;
- inicialização;
- tema;
- criação de card;
- Discord;
- restart;
- atualização;
- remoção;
- recuperação de erro.

---

# 26. Debugging

Durante desenvolvimento:

- usar logs;
- testar via console do Anki;
- capturar exceptions;
- evitar prints excessivos;
- criar modo DEBUG.

A documentação oficial possui console/debugger próprios para addons e recomenda atenção a mensagens de depreciação. 

Criar:

```text
DEBUG = false
```

Quando ativado:

```text
[ADT] Discord connected
[ADT] Message received
[ADT] Card parsed
[ADT] Card queued
[ADT] Card created
```

---

# 27. Fase 17 — Empacotamento

O addon final deve possuir uma estrutura limpa.

Separar:

```text
source/
```

de:

```text
release/
```

Nunca incluir:

- `.git/`
- cache;
- ambiente virtual;
- arquivos temporários;
- secrets;
- tokens;
- logs pessoais;
- testes desnecessários no pacote final.

Se uma dependência externa for necessária, verificar cuidadosamente como ela deve ser empacotada para a versão/arquitetura do Anki. A documentação alerta que módulos externos podem exigir bundling específico, especialmente quando possuem extensões C. 

---

# 28. Instalação local

Preparar um ZIP de release.

Testar:

```text
ZIP
 ↓
Anki
 ↓
Tools
 ↓
Add-ons
 ↓
Install from file
 ↓
Restart
```

A instalação limpa deve funcionar sem depender do ambiente de desenvolvimento.

---

# 29. Teste de instalação limpa

Obrigatório:

1. Criar perfil de teste do Anki.
2. Instalar addon.
3. Abrir Anki.
4. Confirmar que não existem erros.
5. Ativar tema.
6. Configurar Discord.
7. Criar card.
8. Reiniciar Anki.
9. Confirmar persistência.
10. Desinstalar.
11. Confirmar remoção limpa.

---

# 30. Git

Criar repositório:

```text
anki-discord-toolkit
```

Branches:

```text
main
develop
feature/*
fix/*
release/*
```

Commits pequenos:

```text
feat: add addon bootstrap
feat: add configuration manager
feat: add pure black theme
feat: add theme settings
feat: add discord parser
feat: add card payload model
feat: add anki adapter
feat: add queue
test: add parser tests
fix: prevent duplicate cards
```

---

# 31. Versionamento

Usar:

```text
MAJOR.MINOR.PATCH
```

Exemplo:

```text
0.1.0
0.2.0
1.0.0
```

Sugestão:

```text
0.x = desenvolvimento
1.0 = primeira versão estável
```

---

# 32. Roadmap de versões

## v0.1.0

- Skeleton
- Menu
- Config
- Logger

## v0.2.0

- Pure Black Theme
- Theme Settings

## v0.3.0

- CardPayload
- Anki Adapter
- Basic card creation

## v0.4.0

- Discord parser
- Discord bridge
- Authorization

## v0.5.0

- Queue
- Retry
- Anti-duplicação

## v0.6.0

- Deck routing
- Tags
- Templates

## v0.7.0

- Dashboard
- Statistics
- Better error handling

## v0.8.0

- Hardening
- Testing
- Compatibility

## v0.9.0

- Release candidate
- Installation tests
- Documentation

## v1.0.0

- Stable release

---

# 33. Funcionalidades futuras

Somente depois da v1:

## AI

```text
Discord
 ↓
AI
 ↓
Question/Answer
 ↓
Anki
```

Possíveis providers:

- OpenAI
- Gemini
- modelos locais

## PDF

```text
PDF
 ↓
Text extraction
 ↓
Chunking
 ↓
AI
 ↓
Cards
```

## OCR

```text
Image
 ↓
OCR
 ↓
Text
 ↓
AI
 ↓
Anki
```

## Obsidian

```text
Obsidian
 ↓
Markdown
 ↓
Parser
 ↓
Anki
```

## Web Capture

```text
URL
 ↓
Reader
 ↓
Text
 ↓
AI
 ↓
Anki
```

---

# 34. Não implementar ainda

Evitar começar com:

- RAG;
- múltiplos provedores de IA;
- OCR;
- Telegram;
- WhatsApp;
- Obsidian;
- dashboard complexo;
- marketplace;
- sincronização em nuvem.

Primeiro fazer muito bem:

```text
Theme
+
Discord
+
Anki
```

---

# 35. Critério de sucesso da v1

A versão 1 será considerada pronta quando:

```text
[✓] Addon instala
[✓] Addon remove
[✓] Anki inicia sem erros
[✓] Pure Black funciona
[✓] Configurações persistem
[✓] Discord recebe mensagens
[✓] Mensagens são validadas
[✓] Cards são criados
[✓] Deck é selecionado
[✓] Tags funcionam
[✓] Duplicação é evitada
[✓] Erros são tratados
[✓] UI não congela
[✓] Logs funcionam
[✓] Testes passam
[✓] ZIP de release funciona
[✓] Documentação está completa
```

---

# 36. Regra para a IA que irá implementar

Você é o engenheiro responsável por construir este projeto.

Não pule diretamente para a implementação completa.

Execute em ciclos:

```text
ANALYZE
↓
PLAN
↓
IMPLEMENT
↓
TEST
↓
DEBUG
↓
REVIEW
↓
COMMIT
↓
NEXT FEATURE
```

Antes de alterar uma parte importante:

1. Entenda a arquitetura.
2. Verifique a documentação atual.
3. Verifique compatibilidade.
4. Implemente a menor solução correta.
5. Teste.
6. Corrija.
7. Documente.
8. Faça commit.

Nunca reescreva o projeto inteiro apenas para adicionar uma feature.

---

# 37. Regra de qualidade

Não aceitar:

```text
TODO
pass
mock permanente
hardcoded secrets
API keys no código
código duplicado
threads sem controle
operações bloqueantes na UI
```

Também não usar APIs antigas sem verificar se continuam recomendadas.

---

# 38. Secrets

Nunca colocar:

```text
DISCORD_TOKEN
OPENAI_API_KEY
GEMINI_API_KEY
```

no Git.

Usar configuração segura/local e `.gitignore`.

Criar:

```text
.env.example
```

somente como referência, sem valores reais.

---

# 39. Documentação

Criar:

```text
README.md
docs/architecture.md
docs/development.md
docs/discord-protocol.md
docs/configuration.md
docs/release.md
CHANGELOG.md
```

README deve explicar:

- O que é.
- Instalação.
- Configuração.
- Uso.
- Discord.
- Troubleshooting.
- Desenvolvimento.
- Compatibilidade.

---

# 40. Publicação

Quando estiver estável:

1. Criar release Git.
2. Gerar pacote.
3. Testar instalação limpa.
4. Revisar permissões.
5. Remover secrets.
6. Revisar documentação.
7. Publicar no canal oficial de distribuição do Anki.
8. Fornecer instruções de instalação.
9. Manter changelog.
10. Monitorar issues.

Não declarar compatibilidade com uma versão do Anki sem realmente testá-la.

---

# 41. UX final

O usuário deve sentir que está usando um produto único.

Não parecer:

```text
script + bot + gambiarra
```

Deve parecer:

```text
Anki Discord Toolkit
```

com:

```text
Theme
Discord
Cards
Decks
Templates
Settings
Dashboard
```

---

# 42. Arquitetura futura

A arquitetura deve permitir:

```text
                 ┌──────── Discord
                 │
                 ├──────── Obsidian
                 │
                 ├──────── PDF
                 │
Input Layer ─────┼──────── Web
                 │
                 ├──────── Telegram
                 │
                 └──────── AI
                         │
                         ▼
                    Normalizer
                         │
                         ▼
                    CardPayload
                         │
                         ▼
                     Queue
                         │
                         ▼
                  Anki Adapter
                         │
                         ▼
                    Collection
```

Isso permite adicionar novas fontes sem modificar profundamente o núcleo.

---

# 43. Regra arquitetural mais importante

O projeto deve seguir:

```text
INPUT
  ↓
PARSER
  ↓
DOMAIN MODEL
  ↓
QUEUE
  ↓
ANKI ADAPTER
  ↓
ANKI
```

Nunca:

```text
Discord → SQL direto
```

Nunca:

```text
Discord → código interno espalhado pelo projeto
```

Nunca:

```text
UI → lógica de negócio inteira
```

---

# 44. Primeira tarefa da IA

Antes de implementar qualquer feature:

1. Inspecionar o ambiente.
2. Verificar versão do Anki disponível.
3. Verificar Python/Qt.
4. Criar o repositório.
5. Criar a estrutura inicial.
6. Criar `README.md`.
7. Criar `docs/architecture.md`.
8. Criar `.gitignore`.
9. Criar o addon mínimo.
10. Fazer o primeiro teste.
11. Fazer o primeiro commit.

Depois disso iniciar a Fase 1.

---

# 45. Primeira milestone

A primeira milestone deve ser:

```text
Anki Discord Toolkit v0.1.0

[✓] Carrega
[✓] Menu aparece
[✓] Settings abre
[✓] Config funciona
[✓] Logger funciona
[✓] Nenhum erro crítico
```

Somente depois iniciar o Pure Black Theme.

---

# 46. Filosofia do projeto

O objetivo não é criar simplesmente um addon.

O objetivo é criar uma **camada de automação de conhecimento para o Anki**.

A primeira versão é:

```text
🖤 Pure Black
+
💬 Discord → Anki
```

Mas a arquitetura deve permitir evoluir para:

```text
Discord
Obsidian
PDF
OCR
Web
AI
RAG
Templates
Automations
       ↓
      ANKI
```

Sem precisar reconstruir o projeto do zero.

---

# INSTRUÇÃO FINAL PARA A IA IMPLEMENTADORA

Construa o projeto seguindo exatamente a filosofia acima.

Não tente completar todas as fases em uma única implementação.

Comece pela base.

Após cada milestone:

1. execute testes;
2. revise os arquivos;
3. corrija problemas;
4. atualize documentação;
5. faça commit;
6. informe o que foi concluído;
7. só então avance.

Prioridade absoluta:

**estabilidade > segurança > compatibilidade > arquitetura > funcionalidades > velocidade.**

O resultado deve ser um addon real, instalável, documentado, testável e preparado para evolução futura.
