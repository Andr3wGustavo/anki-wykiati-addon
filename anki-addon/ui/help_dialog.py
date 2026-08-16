"""
Interactive Help and Didactic Setup Guide for Anki Wykiati Toolkit.
Provides step-by-step instructions for Discord bot configuration, image channel ingestion,
front-only card setup, RGB background customization, and REST Webhook integration.
"""

from typing import Any, Optional

try:
    from ..core.constants import ADDON_NAME, ADDON_VERSION
    from ..theme.palette import PALETTE
    from .components.base_dialog import BaseToolkitDialog, QT_AVAILABLE
except (ImportError, ValueError):
    from core.constants import ADDON_NAME, ADDON_VERSION
    from theme.palette import PALETTE
    from ui.components.base_dialog import BaseToolkitDialog, QT_AVAILABLE

if QT_AVAILABLE:
    try:
        from aqt.qt import (
            QFrame,
            QHBoxLayout,
            QLabel,
            QPushButton,
            QTextBrowser,
            QVBoxLayout,
            QWidget,
        )
    except ImportError:
        try:
            from PyQt6.QtWidgets import (
                QFrame,
                QHBoxLayout,
                QLabel,
                QPushButton,
                QTextBrowser,
                QVBoxLayout,
                QWidget,
            )
        except ImportError:
            from PyQt5.QtWidgets import (
                QFrame,
                QHBoxLayout,
                QLabel,
                QPushButton,
                QTextBrowser,
                QVBoxLayout,
                QWidget,
            )
else:
    QFrame = QHBoxLayout = QLabel = QPushButton = QTextBrowser = QVBoxLayout = QWidget = object


HELP_HTML_CONTENT = """
<div style="font-family: 'Segoe UI', -apple-system, sans-serif; color: #FFFFFF; line-height: 1.6; padding: 4px;">
    
    <div style="background: rgba(255, 255, 255, 0.04); border: 1px solid rgba(255, 255, 255, 0.12); border-radius: 6px; padding: 14px; margin-bottom: 16px;">
        <h2 style="color: #38BDF8; margin: 0 0 8px 0; font-size: 16px;">🚀 Guia Rápido de Configuração / Quick Start Guide</h2>
        <p style="color: #A1A1AA; font-size: 13px; margin: 0;">
            Bem-vindo ao <b>Anki Wykiati Toolkit</b>. Este guia explica didaticamente como configurar cada funcionalidade do plugin para automatizar seus estudos com imagens e cards do Discord.
        </p>
    </div>

    <!-- SEÇÃO 1: IMAGENS DO DISCORD PARA O ANKI -->
    <div style="border-left: 3px solid #38BDF8; padding-left: 12px; margin-bottom: 20px;">
        <h3 style="color: #FFFFFF; margin: 0 0 6px 0; font-size: 14px;">1. Ingestão Automática de Imagens (Canal do Discord ➔ Deck do Anki)</h3>
        <p style="color: #A1A1AA; font-size: 12px; margin: 0 0 8px 0;">
            Você pode fazer com que todas as imagens postadas em um ou mais canais do Discord sejam automaticamente baixadas para o Anki e transformadas em flashcards.
        </p>
        <ol style="color: #D4D4D8; font-size: 12px; margin: 0; padding-left: 20px;">
            <li><b>Ativar Modo Desenvolvedor no Discord:</b> No seu Discord, clique na engrenagem <i>Configurações do Usuário > Avançado > Modo Desenvolvedor (Ativar)</i>.</li>
            <li><b>Copiar o ID do Canal:</b> Clique com o botão direito sobre o canal desejado no Discord e escolha <b>Copiar ID do Canal</b> (ex: <code>119283746509182736</code>).</li>
            <li><b>Inserir no Plugin:</b> No Anki, vá em <i>Ferramentas > Anki Wykiati Toolkit > Discord and Image Settings</i> e cole o ID no campo <b>Image Channels (IDs)</b>.</li>
            <li><b>Definir o Deck de Destino:</b> No campo <b>Target Image Deck</b>, digite o nome do deck onde deseja receber as imagens (ex: <code>Medicina::Anatomia</code> ou <code>Imagens::Discord</code>). Se o deck não existir, o plugin o cria automaticamente!</li>
            <li><b>Somente Imagem na Frente (Sem Verso):</b> No campo <b>Card Layout Mode</b>, selecione <b>Image on Front Only (Empty Back / Visual Card)</b>. Assim, a imagem fica sozinha na frente do card, sem texto no verso!</li>
        </ol>
    </div>

    <!-- SEÇÃO 2: BOT DO DISCORD -->
    <div style="border-left: 3px solid #4ADE80; padding-left: 12px; margin-bottom: 20px;">
        <h3 style="color: #FFFFFF; margin: 0 0 6px 0; font-size: 14px;">2. Configuração do Bot do Discord (Token & Permissões)</h3>
        <p style="color: #A1A1AA; font-size: 12px; margin: 0 0 8px 0;">
            Para que o Anki consiga monitorar os canais do Discord em segundo plano:
        </p>
        <ol style="color: #D4D4D8; font-size: 12px; margin: 0; padding-left: 20px;">
            <li>Acesse o <a href="https://discord.com/developers/applications" style="color: #38BDF8;">Discord Developer Portal</a> e clique em <b>New Application</b>.</li>
            <li>No menu lateral esquerdo, vá em <b>Bot</b> e clique em <b>Reset Token</b> para gerar e copiar seu <b>Bot Token</b>.</li>
            <li>Role a página do Bot para baixo e <b>ATIVE</b> a opção <b>Message Content Intent</b> (obrigatório para que o bot leia mensagens e imagens).</li>
            <li>No menu <b>OAuth2 > URL Generator</b>, selecione os escopos <code>bot</code> e as permissões <code>Read Messages/View Channels</code>, <code>Send Messages</code> e <code>Attach Files</code>, e use o link gerado para convidar o bot ao seu servidor Discord.</li>
            <li>Cole o Token no campo <b>Bot Token</b> do plugin e marque a caixa <b>Enable Discord Bot Background Poller</b>.</li>
        </ol>
    </div>

    <!-- SEÇÃO 3: TEMA FULL BLACK & CÍRCULO RGB -->
    <div style="border-left: 3px solid #FBBF24; padding-left: 12px; margin-bottom: 20px;">
        <h3 style="color: #FFFFFF; margin: 0 0 6px 0; font-size: 14px;">3. Estúdio de Tema: Full Black AMOLED & Círculo RGB</h3>
        <p style="color: #A1A1AA; font-size: 12px; margin: 0 0 8px 0;">
            Personalize as cores de fundo e de destaque de toda a interface do Anki:
        </p>
        <ul style="color: #D4D4D8; font-size: 12px; margin: 0; padding-left: 20px;">
            <li><b>Círculo RGB:</b> Vá em <i>Theme & Appearance Studio</i> e clique em qualquer ponto do círculo RGB para escolher a cor de fundo exata que preferir.</li>
            <li><b>Presets OLED:</b> Escolha entre <i>🖤 Full Black AMOLED (#000000)</i>, <i>🌌 Deep Midnight</i>, <i>🌲 Forest Night</i>, <i>🪐 Obsidian</i> ou <i>⚓ Cyberpunk Dark</i>.</li>
            <li><b>Cor de Destaque (Accent):</b> Escolha a cor dos botões e seleções (Azul Apple, Verde Esmeralda, Roxo, Vermelho, Laranja, etc.).</li>
            <li><b>Atalho Rápido:</b> Pressione <code>Ctrl+Shift+B</code> a qualquer momento para ativar ou desativar o tema instantaneamente.</li>
        </ul>
    </div>

    <!-- SEÇÃO 4: COMANDOS E PROTOCOLO !ANKI -->
    <div style="border-left: 3px solid #A78BFA; padding-left: 12px; margin-bottom: 20px;">
        <h3 style="color: #FFFFFF; margin: 0 0 6px 0; font-size: 14px;">4. Comandos e Criação de Cards via Texto no Discord</h3>
        <p style="color: #A1A1AA; font-size: 12px; margin: 0 0 8px 0;">
            Você também pode digitar no Discord mensagens com o prefixo <code>!anki</code>:
        </p>
        <pre style="background: rgba(0,0,0,0.6); border: 1px solid rgba(255,255,255,0.1); border-radius: 4px; padding: 8px; color: #E4E4E7; font-size: 11px;">
!anki
front: O que é o miocárdio?
back: É a camada média e mais espessa da parede cardíaca, formada por músculo estriado cardíaco.
deck: Medicina::Cardiologia
tags: anatomia, coracao
        </pre>
        <p style="color: #A1A1AA; font-size: 12px; margin: 6px 0 0 0;">
            Comandos de status úteis no chat: <code>!anki-help</code>, <code>!anki-status</code>, <code>!anki-decks</code>, <code>!anki-ping</code>.
        </p>
    </div>

    <!-- SEÇÃO 5: LOCAL HTTP WEBHOOK BRIDGE -->
    <div style="border-left: 3px solid #F472B6; padding-left: 12px; margin-bottom: 10px;">
        <h3 style="color: #FFFFFF; margin: 0 0 6px 0; font-size: 14px;">5. Integração Externa via REST Webhook Local</h3>
        <p style="color: #A1A1AA; font-size: 12px; margin: 0 0 8px 0;">
            O plugin possui um servidor HTTP embutido em <code>http://127.0.0.1:8765/api/card</code> para integração com extensões do Chrome, scripts Python ou automações locais:
        </p>
        <pre style="background: rgba(0,0,0,0.6); border: 1px solid rgba(255,255,255,0.1); border-radius: 4px; padding: 8px; color: #E4E4E7; font-size: 11px;">
curl -X POST http://127.0.0.1:8765/api/card \
  -H "Content-Type: application/json" \
  -d '{"image_url": "https://site.com/foto.png", "deck": "Medicina::Anatomia"}'
        </pre>
    </div>

</div>
"""


class HelpDialog(BaseToolkitDialog):
    """
    Didactic documentation and step-by-step setup guide modal dialog.
    """
    def __init__(self, parent: Optional[Any] = None) -> None:
        super().__init__(
            parent,
            title="Help & Interactive Setup Guide",
            subtitle=f"{ADDON_NAME} v{ADDON_VERSION} — Guia Didático e Referência Completa",
            width=720,
            height=600,
        )
        if not QT_AVAILABLE:
            return

        self._build_ui()

    def _build_ui(self) -> None:
        layout = QVBoxLayout()
        layout.setSpacing(10)

        browser = QTextBrowser(self)
        browser.setHtml(HELP_HTML_CONTENT)
        browser.setOpenExternalLinks(True)
        browser.setStyleSheet(
            "QTextBrowser { background-color: #050507; border: 1px solid rgba(255,255,255,0.10); border-radius: 6px; padding: 12px; }"
            "QScrollBar:vertical { background: transparent; width: 6px; }"
            "QScrollBar::handle:vertical { background: rgba(255,255,255,0.20); border-radius: 3px; min-height: 20px; }"
        )
        layout.addWidget(browser)

        # Footer button customize
        self.btn_save.setVisible(False)
        self.btn_cancel.setText("Close")

        self.body_layout.addLayout(layout)
