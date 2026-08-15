# Guia de Instalação e Release do Add-on

---

## 1. Como Instalar no Anki Desktop

### Método A: Instalação por Arquivo (.ankiaddon)
1. Baixe ou gere o arquivo `release/anki-discord-toolkit.ankiaddon`.
2. Abra o **Anki**.
3. No menu superior, clique em: **Ferramentas (Tools)** → **Extensões (Add-ons)** (ou pressione `Ctrl+Shift+A`).
4. Clique no botão **"Instalar de arquivo..." (Install from file...)**.
5. Selecione o arquivo `anki-discord-toolkit.ankiaddon`.
6. Reinicie o Anki.
7. O menu **Anki Discord Toolkit** aparecerá sob o menu **Ferramentas**.

---

### Método B: Instalação Manual (Link Simbólico ou Cópia da Pasta)
1. Localize a pasta de complementos do Anki:
   - **Windows:** `%APPDATA%\Anki2\addons21\`
   - **macOS:** `~/Library/Application Support/Anki2/addons21/`
   - **Linux:** `~/.local/share/Anki2/addons21/`
2. Copie a pasta `anki-addon` para dentro de `addons21` e renomeie-a para `anki_discord_toolkit`.
3. Reinicie o Anki.

---

## 2. Como Gerar Novos Releases

Para gerar um novo pacote limpo de distribuição:

```bash
python package_addon.py
```

O script criará automaticamente:
- `release/anki-discord-toolkit.ankiaddon` (Formato oficial do Anki)
- `release/anki-discord-toolkit.zip` (Arquivo compactado padrão)
