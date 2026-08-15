# Guia de Desenvolvimento e Testes

Este documento orienta desenvolvedores que desejam contribuir, testar ou estender as funcionalidades do **Anki Discord Toolkit**.

---

## 1. Requisitos de Ambiente

- **Python 3.9+** (recomendado Python 3.10, 3.11, 3.12, 3.13 ou 3.14).
- **Anki 2.1.45+** (ou ambiente standalone para desenvolvimento/testes automatizados).
- Nenhuma dependência externa obrigatória em tempo de execução (100% biblioteca padrão Python + APIs oficiais do Anki/Qt).

---

## 2. Estrutura do Repositório

```text
anki-clone/
├── anki-addon/              # Código fonte do Addon para Anki
│   ├── __init__.py          # Ponto de entrada do bootstrap
│   ├── config.json          # Configuração padrão com schema completo
│   ├── manifest.json        # Metadados do addon para o Anki
│   ├── core/                # ConfigManager, Logger, EventBus, Exceptions, Constants
│   ├── theme/               # Pure Black Palette, Engine e Stylesheet Generators
│   ├── anki/                # NoteAdapter, DeckAdapter e Operations
│   ├── discord/             # Parser, Models, Security, Bridge, Client e Commands
│   ├── sync/                # JobQueue, SyncJob, SyncWorker e AntiDuplication
│   ├── routing/             # DeckRouter (Smart Deck Routing)
│   ├── templates/           # TemplateManager
│   ├── ui/                  # Dashboard, Settings Dialogs, Menu Manager
│   └── tests/               # Suíte completa de testes unitários
├── docs/                    # Documentação técnica detalhada
├── release/                 # Diretório de saída dos pacotes .ankiaddon
├── package_addon.py         # Script empacotador de release
├── test_addon.bat           # Executor automatizado e interativo para Windows
├── run_http_bridge.bat      # Executor do servidor HTTP Bridge de testes
├── README.md                # Guia do usuário e documentação geral
└── LICENSE                  # Licença MIT
```

---

## 3. Executando os Testes Automatizados

O projeto possui uma suíte de testes unitários com cobertura abrangente e zero dependências de GUI ou conexões externas ativas (testes rodam em modo headless perfeitamente).

### Via Terminal / PowerShell:
```bash
python -m unittest discover -s anki-addon/tests -p "test_*.py" -v
```

### Via Script Batch no Windows:
Basta clicar duas vezes em `test_addon.bat` ou rodar no terminal:
```cmd
test_addon.bat
```

---

## 4. Testando o Servidor HTTP Bridge Local

Você pode iniciar o servidor local de testes para disparar requisições HTTP REST diretamente sem precisar abrir o Discord:

### Iniciar Bridge:
```cmd
run_http_bridge.bat
```

### Disparar um Cartão de Teste via cURL / PowerShell:
```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:8765/api/card" -Method Post -ContentType "application/json" -Body '{"front": "O que é Redis?", "back": "Banco de dados em memória chave-valor.", "deck": "Database::Redis", "tags": ["db", "cache"]}'
```

---

## 5. Gerando o Pacote de Distribuição (.ankiaddon)

Para gerar o arquivo `.ankiaddon` instalável no Anki:

```bash
python package_addon.py
```

O arquivo final será salvo em `release/anki-discord-toolkit.ankiaddon`.
