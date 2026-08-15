"""
About and Diagnostics Dialog for Anki Discord Toolkit.
"""

from typing import Any, Optional

try:
    from ..core.constants import ADDON_AUTHOR, ADDON_NAME, ADDON_SHORT_NAME, ADDON_VERSION
    from ..theme.palette import PALETTE
    from .components.base_dialog import BaseToolkitDialog, QT_AVAILABLE
except (ImportError, ValueError):
    from core.constants import ADDON_AUTHOR, ADDON_NAME, ADDON_SHORT_NAME, ADDON_VERSION
    from theme.palette import PALETTE
    from ui.components.base_dialog import BaseToolkitDialog, QT_AVAILABLE

if QT_AVAILABLE:
    try:
        from aqt.qt import QLabel, QPushButton, QTextBrowser, QVBoxLayout
    except ImportError:
        try:
            from PyQt6.QtWidgets import QLabel, QPushButton, QTextBrowser, QVBoxLayout
        except ImportError:
            from PyQt5.QtWidgets import QLabel, QPushButton, QTextBrowser, QVBoxLayout
else:
    QLabel = QPushButton = QTextBrowser = QVBoxLayout = object


class AboutDialog(BaseToolkitDialog):
    """
    Displays add-on branding, release details, and documentation info.
    """
    def __init__(self, parent: Optional[Any] = None) -> None:
        super().__init__(
            parent,
            title=f"Sobre o {ADDON_NAME}",
            subtitle=f"Versão v{ADDON_VERSION} — Automação de Conhecimento e Tema Pure Black OLED",
        )
        if not QT_AVAILABLE:
            return

        self._build_ui()

    def _build_ui(self) -> None:
        layout = QVBoxLayout()
        layout.setSpacing(12)

        info_browser = QTextBrowser(self)
        info_browser.setOpenExternalLinks(True)
        info_browser.setStyleSheet(f"background-color: {PALETTE.BACKGROUND_SURFACE}; border: 1px solid {PALETTE.BORDER_DEFAULT}; border-radius: 6px; padding: 10px;")

        html_content = f"""
        <h3 style="color: {PALETTE.ACCENT_PRIMARY}; margin-top: 0;">{ADDON_NAME} v{ADDON_VERSION}</h3>
        <p><b>Desenvolvido por:</b> {ADDON_AUTHOR}</p>
        <p><b>Licença:</b> MIT License (Software Livre)</p>
        <hr style="border: 0; border-top: 1px solid {PALETTE.BORDER_SUBTLE};">
        <p><b>Principais Recursos:</b></p>
        <ul>
            <li><b>🖤 Pure Black Theme:</b> Interface de alto contraste em preto absoluto (#000000) otimizada para telas OLED/AMOLED.</li>
            <li><b>💬 Discord & Webhooks:</b> Transforme mensagens do Discord e requisições HTTP em flashcards estruturados instantaneamente.</li>
            <li><b>⚡ Fila & Anti-Duplicação:</b> Processamento seguro em background que nunca congela a interface do Anki.</li>
            <li><b>🎯 Roteamento Inteligente:</b> Regras automáticas de direcionamento para baralhos por tags e palavras-chave.</li>
            <li><b>🧩 Suporte a Templates:</b> Compatível com cartões Básicos, Invertidos e Cloze Deletion.</li>
        </ul>
        <hr style="border: 0; border-top: 1px solid {PALETTE.BORDER_SUBTLE};">
        <p style="font-size: 11px; color: {PALETTE.TEXT_MUTED};">
            Para dúvidas, suporte ou novidades, consulte a documentação inclusa no projeto.
        </p>
        """
        info_browser.setHtml(html_content)
        layout.addWidget(info_browser)

        # Hide save button since this is purely informational
        self.btn_save.setVisible(False)
        self.btn_cancel.setText("Fechar")

        self.body_layout.addLayout(layout)
