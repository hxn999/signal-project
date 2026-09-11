"""Dark theme: colour tokens, QPalette and stylesheet."""

from __future__ import annotations

from PySide6.QtGui import QColor, QFont, QPalette
from PySide6.QtWidgets import QApplication

BG = "#0f1115"
SURFACE = "#171a21"
SURFACE_2 = "#1f232c"
SURFACE_3 = "#282d38"
BORDER = "#2a2f3a"
TEXT = "#e6e8ee"
TEXT_DIM = "#9aa3b2"
TEXT_FAINT = "#6b7385"
ACCENT = "#6c8cff"
ACCENT_HOVER = "#8aa3ff"
HIGHLIGHT = "#ffb454"   # current output cell / step
NEGATIVE = "#4f8dff"    # diverging map, negative end
POSITIVE = "#ff7a59"    # diverging map, positive end
ERROR = "#ff6b6b"

MONO_FAMILY = "Cascadia Mono, Consolas, monospace"

STYLESHEET = f"""
* {{
    color: {TEXT};
    font-size: 10pt;
}}
QMainWindow, QWidget#central {{
    background: {BG};
}}
QToolTip {{
    background: {SURFACE_3};
    color: {TEXT};
    border: 1px solid {BORDER};
    padding: 4px 6px;
    border-radius: 4px;
}}
QScrollArea, QScrollArea > QWidget > QWidget#sidebar {{
    background: {BG};
    border: none;
}}
QFrame#card {{
    background: {SURFACE};
    border: 1px solid {BORDER};
    border-radius: 10px;
}}
QLabel#cardTitle {{
    font-size: 11pt;
    font-weight: 600;
}}
QLabel#appTitle {{
    font-size: 15pt;
    font-weight: 700;
}}
QLabel#appSubtitle, QLabel#dim, QLabel#caption {{
    color: {TEXT_DIM};
}}
QLabel#caption {{
    font-size: 9pt;
}}
QLabel#hint {{
    color: {TEXT_FAINT};
    font-size: 9pt;
}}
QLabel#error {{
    color: {ERROR};
}}
QLabel#glyph {{
    color: {TEXT_FAINT};
    font-size: 22pt;
}}
QLabel#paneTitle {{
    font-weight: 600;
}}
QLabel#equation {{
    font-family: {MONO_FAMILY};
    font-size: 10pt;
    color: {TEXT};
}}
QLabel#stepBadge {{
    background: {SURFACE_3};
    color: {HIGHLIGHT};
    border-radius: 9px;
    padding: 2px 10px;
    font-weight: 600;
}}

QPushButton, QToolButton {{
    background: {SURFACE_2};
    border: 1px solid {BORDER};
    border-radius: 7px;
    padding: 6px 12px;
}}
QPushButton:hover, QToolButton:hover {{
    background: {SURFACE_3};
    border-color: #3a4150;
}}
QPushButton:pressed, QToolButton:pressed {{
    background: {BORDER};
}}
QPushButton:disabled, QToolButton:disabled {{
    color: {TEXT_FAINT};
}}
QPushButton#primary {{
    background: {ACCENT};
    border-color: {ACCENT};
    color: #0b0d12;
    font-weight: 600;
}}
QPushButton#primary:hover {{
    background: {ACCENT_HOVER};
}}
QPushButton#segLeft, QPushButton#segRight {{
    background: {SURFACE_2};
    color: {TEXT_DIM};
    padding: 6px 10px;
}}
QPushButton#segLeft {{
    border-top-right-radius: 0;
    border-bottom-right-radius: 0;
}}
QPushButton#segRight {{
    border-left: none;
    border-top-left-radius: 0;
    border-bottom-left-radius: 0;
}}
QPushButton#segLeft:checked, QPushButton#segRight:checked {{
    background: {SURFACE_3};
    color: {TEXT};
    border-color: #3a4150;
    font-weight: 600;
}}
QToolButton#transport {{
    font-size: 12pt;
    min-width: 34px;
    min-height: 30px;
    padding: 2px 6px;
}}
QToolButton#play {{
    font-size: 12pt;
    min-width: 44px;
    min-height: 30px;
    padding: 2px 6px;
    background: {ACCENT};
    border-color: {ACCENT};
    color: #0b0d12;
}}
QToolButton#play:hover {{
    background: {ACCENT_HOVER};
}}
QToolButton::menu-indicator {{
    image: none;
    width: 0;
}}

QSpinBox, QDoubleSpinBox, QComboBox, QLineEdit {{
    background: {SURFACE_2};
    border: 1px solid {BORDER};
    border-radius: 6px;
    padding: 4px 6px;
    min-height: 20px;
    selection-background-color: {ACCENT};
    selection-color: #0b0d12;
}}
QSpinBox:focus, QDoubleSpinBox:focus, QComboBox:focus, QLineEdit:focus {{
    border-color: {ACCENT};
}}
QSpinBox::up-button, QSpinBox::down-button,
QDoubleSpinBox::up-button, QDoubleSpinBox::down-button {{
    width: 16px;
    border: none;
    background: transparent;
}}
QComboBox::drop-down {{
    border: none;
    width: 20px;
}}
QComboBox QAbstractItemView {{
    background: {SURFACE_2};
    border: 1px solid {BORDER};
    selection-background-color: {SURFACE_3};
    selection-color: {TEXT};
    outline: none;
    padding: 4px;
}}
QMenu {{
    background: {SURFACE_2};
    border: 1px solid {BORDER};
    padding: 4px;
}}
QMenu::item {{
    padding: 6px 18px;
    border-radius: 4px;
}}
QMenu::item:selected {{
    background: {SURFACE_3};
}}

QTabWidget::pane {{
    border: none;
}}
QTabBar::tab {{
    background: transparent;
    color: {TEXT_DIM};
    padding: 7px 14px;
    margin-right: 4px;
    border-bottom: 2px solid transparent;
}}
QTabBar::tab:selected {{
    color: {TEXT};
    border-bottom: 2px solid {ACCENT};
}}
QTabBar::tab:hover:!selected {{
    color: {TEXT};
}}
QTabWidget#mainTabs QTabBar::tab {{
    font-size: 10.5pt;
    font-weight: 600;
    padding: 9px 18px;
}}

QSlider::groove:horizontal {{
    height: 4px;
    background: {SURFACE_3};
    border-radius: 2px;
}}
QSlider::sub-page:horizontal {{
    background: {ACCENT};
    border-radius: 2px;
}}
QSlider::handle:horizontal {{
    background: {TEXT};
    width: 14px;
    height: 14px;
    margin: -5px 0;
    border-radius: 7px;
}}
QSlider::handle:horizontal:hover {{
    background: {ACCENT_HOVER};
}}

QScrollBar:vertical {{
    background: transparent;
    width: 10px;
    margin: 2px;
}}
QScrollBar::handle:vertical {{
    background: {SURFACE_3};
    border-radius: 4px;
    min-height: 30px;
}}
QScrollBar::add-line, QScrollBar::sub-line {{
    height: 0;
    width: 0;
}}
QScrollBar::add-page, QScrollBar::sub-page {{
    background: transparent;
}}

QStatusBar {{
    background: {SURFACE};
    border-top: 1px solid {BORDER};
    color: {TEXT_DIM};
}}
QStatusBar QLabel {{
    color: {TEXT_DIM};
    padding: 0 8px;
}}
QCheckBox::indicator {{
    width: 16px;
    height: 16px;
    border-radius: 4px;
    border: 1px solid {BORDER};
    background: {SURFACE_2};
}}
QCheckBox::indicator:checked {{
    background: {ACCENT};
    border-color: {ACCENT};
}}
"""


def apply_theme(app: QApplication) -> None:
    app.setStyle("Fusion")
    font = QFont("Segoe UI Variable Text")
    if not font.exactMatch():
        font = QFont("Segoe UI")
    font.setPointSizeF(10)
    app.setFont(font)

    pal = QPalette()
    roles = {
        QPalette.Window: BG,
        QPalette.WindowText: TEXT,
        QPalette.Base: SURFACE_2,
        QPalette.AlternateBase: SURFACE,
        QPalette.Text: TEXT,
        QPalette.Button: SURFACE_2,
        QPalette.ButtonText: TEXT,
        QPalette.Highlight: ACCENT,
        QPalette.HighlightedText: "#0b0d12",
        QPalette.ToolTipBase: SURFACE_3,
        QPalette.ToolTipText: TEXT,
        QPalette.PlaceholderText: TEXT_FAINT,
    }
    for role, color in roles.items():
        pal.setColor(role, QColor(color))
    pal.setColor(QPalette.Disabled, QPalette.Text, QColor(TEXT_FAINT))
    pal.setColor(QPalette.Disabled, QPalette.ButtonText, QColor(TEXT_FAINT))
    app.setPalette(pal)
    app.setStyleSheet(STYLESHEET)
