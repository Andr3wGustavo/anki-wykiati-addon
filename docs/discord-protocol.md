# Protocolo de Mensagens Discord → Anki

O **Anki Discord Toolkit** aceita mensagens com o prefixo de comando `!anki` ou comandos operacionais no canal do Discord ou através do Webhook HTTP.

---

## 1. Estrutura do Comando `!anki`

O comando `!anki` utiliza pares chave-valor por linhas. Cada campo começa com o nome do campo seguido de dois pontos (`:`).

### Campos Suportados:

| Campo | Obrigatório | Descrição | Exemplo |
|---|---|---|---|
| `front:` | **Sim** | Texto da frente (pergunta ou omissão cloze). Suporta Markdown e multilinhas. | `front: O que é Docker?` |
| `back:` | Não | Texto do verso (resposta ou detalhes). Suporta Markdown e código. | `back: Docker é uma plataforma de containers.` |
| `deck:` | Não | Nome do baralho de destino (pode ser hierárquico com `::`). Se omitido, usa as Regras de Roteamento ou o Deck Padrão. | `deck: Dev::Docker` |
| `tags:` | Não | Tags separadas por vírgula, espaço, ponto e vírgula ou `#hashtags`. | `tags: docker, devops, infra` |
| `type:` | Não | Tipo de Nota (`Basic`, `Cloze`, `Basic (and reversed card)`). Auto-detectado se houver `{{c1::...}}`. | `type: Cloze` |
| `extra:` | Não | Campo de notas adicionais (usado em modelos Cloze ou cartões avançados). | `extra: Revisar documentação oficial` |

---

## 2. Exemplos Práticos de Mensagens

### Exemplo 1: Cartão Básico Simples
```text
!anki
front: O que significa a sigla ACID em bancos de dados?
back: Atomicidade, Consistência, Isolamento e Durabilidade.
deck: Database::Relacional
tags: database, sql, acid
```

---

### Exemplo 2: Cartão com Bloco de Código Multilinha
```text
!anki
front: Como filtrar elementos pares em uma lista em Python?
back:
```python
numeros = [1, 2, 3, 4, 5, 6]
pares = [n for n in numeros if n % 2 == 0]
print(pares) # [2, 4, 6]
```
deck: Programming::Python
tags: #python #listcomprehension
```

---

### Exemplo 3: Cartão de Omissão de Palavras (Cloze Deletion)
> *Nota: O addon detecta automaticamente a presença de `{{c1::...}}` e seleciona o modelo **Cloze** sem você precisar especificar `type: Cloze`!*

```text
!anki
front: O {{c1::HTTPS}} utiliza a porta padrão {{c2::443}} e é protegido por criptografia {{c3::TLS/SSL}}.
deck: Networking::Security
tags: redes, seguranca, web
```

---

## 3. Comandos Operacionais

Você também pode enviar comandos de consulta rápidos no Discord:

- `!anki-help`: Exibe um guia interativo de uso com exemplos formatados.
- `!anki-status`: Exibe a versão do addon, status do Pure Black Theme, total de cartões criados e métricas.
- `!anki-decks`: Lista todos os baralhos disponíveis na sua coleção do Anki.
- `!anki-ping`: Testa a conectividade com o Anki ("Pong!").
