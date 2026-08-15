# Referência Completa de Configuração (`config.json`)

O arquivo `config.json` gerencia todas as preferências, conexões e regras de roteamento do **Anki Discord Toolkit**.

---

## 1. Estrutura Padrão

```json
{
  "addon_enabled": true,
  "debug_mode": false,
  "log_level": "INFO",
  "theme": {
    "enabled": true,
    "background": "#000000",
    "surface": "#0C0D0E",
    "surface_secondary": "#16181A",
    "accent": "#3B82F6",
    "text_primary": "#FFFFFF",
    "text_secondary": "#A0AAB4",
    "border": "#22272B",
    "apply_to_webviews": true,
    "pure_black_reviewer": true
  },
  "discord": {
    "enabled": false,
    "mode": "http",
    "bot_token": "",
    "channel_ids": [],
    "authorized_users": [],
    "guild_ids": [],
    "polling_interval_seconds": 5,
    "http_bridge_enabled": true,
    "http_bridge_host": "127.0.0.1",
    "http_bridge_port": 8765,
    "secret_token": "",
    "rate_limit_per_minute": 60,
    "max_message_length": 4000
  },
  "anki": {
    "default_deck": "Default",
    "default_template": "Basic",
    "tags_prefix": "",
    "auto_create_decks": true,
    "duplicate_policy": "skip"
  },
  "routing": {
    "enabled": true,
    "rules": [
      {
        "type": "tag",
        "pattern": "python",
        "deck": "Programming::Python"
      },
      {
        "type": "tag",
        "pattern": "docker",
        "deck": "DevOps::Docker"
      }
    ]
  },
  "stats": {
    "cards_created": 0,
    "messages_processed": 0,
    "failed_jobs": 0,
    "last_sync_timestamp": 0
  }
}
```

---

## 2. Detalhamento dos Campos

### `theme`
- `enabled`: Ativa/desativa o tema Pure Black #000000.
- `accent`: Código hexadecimal da cor de destaque da interface (ex: `#3B82F6` para azul, `#10B981` para verde).
- `apply_to_webviews`: Se `true`, injeta o fundo preto e estilo de alto contraste no Deck Browser e telas web do Anki.
- `pure_black_reviewer`: Aplica o fundo preto absoluto no visualizador de cartões durante o estudo.

### `discord`
- `enabled`: Habilita o trabalhador poller automático do Discord Bot.
- `bot_token`: Token secreto do bot do Discord.
- `channel_ids`: Lista de IDs de canais do Discord autorizados a criar cartões. Se vazio, aceita qualquer canal onde o bot esteja presente.
- `authorized_users`: Lista de IDs de usuários do Discord autorizados. Se vazio, aceita todos.
- `polling_interval_seconds`: Frequência de consulta da API do Discord (padrão: 5 segundos).
- `http_bridge_enabled`: Ativa o servidor REST webhook local em `http://127.0.0.1:8765/api/card`.
- `http_bridge_port`: Porta de rede do servidor local (padrão: 8765).
- `rate_limit_per_minute`: Número máximo de cartões aceitos por minuto por usuário (padrão: 60).

### `anki`
- `default_deck`: Baralho padrão para cartões que não especificarem baralho nem casarem com regras de roteamento.
- `default_template`: Modelo padrão (`Basic`, `Cloze`, etc.).
- `tags_prefix`: Prefixo automático a ser anexado em todas as tags geradas pelo Discord (opcional).

### `routing`
- `rules`: Lista de regras ordenadas por prioridade.
  - `type`: `"tag"` para casar com tags informadas ou `"keyword"` para buscar termos no texto.
  - `pattern`: Palavra-chave ou nome da tag.
  - `deck`: Nome do baralho de destino no Anki.
