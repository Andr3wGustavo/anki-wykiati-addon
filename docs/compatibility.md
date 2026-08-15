# Matriz de Compatibilidade e Requisitos

Este documento especifica o suporte de plataformas, versões do Anki e frameworks gráficos do **Anki Discord Toolkit**.

---

## 1. Versões do Anki Suportadas

| Versão do Anki | Status | Observações |
|---|---|---|
| **Anki 24.x+** | ✅ Suportado | Qt6 / PyQt6 nativo |
| **Anki 23.x+** | ✅ Suportado | Qt6 / PyQt6 |
| **Anki 2.1.50 — 2.1.66** | ✅ Suportado | Builds Qt5 e Qt6 |
| **Anki 2.1.45 — 2.1.49** | ✅ Suportado | Suporte legado via `aqt.qt` |
| **Anki < 2.1.45** | ⚠️ Não recomendado | Recomenda-se atualizar o Anki para garantir compatibilidade com `gui_hooks` modernos |

---

## 2. Sistemas Operacionais

- **Windows**: Windows 10 e Windows 11 (64-bit).
- **macOS**: macOS 11+ (Intel e Apple Silicon / M1 / M2 / M3 / M4).
- **Linux**: Ubuntu, Debian, Fedora, Arch Linux (qualquer distro com Python 3.9+).

---

## 3. Requisitos de Dependências

O **Anki Discord Toolkit** foi desenhado com arquitetura *Zero-External-Dependencies*:
- **Sem dependências C/Rust**: Nenhum compilador necessário.
- **Sem conflitos de pacotes**: Utiliza a biblioteca padrão do Python (`http.server`, `urllib`, `json`, `threading`, `hashlib`, `re`) e a camada nativa `aqt`/`PyQt` já embutida na instalação do Anki.
