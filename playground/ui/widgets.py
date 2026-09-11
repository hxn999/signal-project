"""Small shared widgets: cards, labels and painted transport icons."""

from __future__ import annotations

from PySide6.QtCore import QPointF, QRectF, Qt
from PySide6.QtGui import QColor, QIcon, QPainter, QPixmap, QPolygonF
from PySide6.QtWidgets import QFrame, QLabel, QVBoxLayout, QWidget


class Card(QFrame):
    """Rounded surface with a title; add content to ``self.body``."""

    def __init__(self, title: str = "", subtitle: str = "", parent: QWidget | None = None):
        super().__init__(parent)
        self.setObjectName("card")
        self.body = QVBoxLayout(self)
        self.body.setContentsMargins(14, 12, 14, 14)
        self.body.setSpacing(10)
        if title:
            t = QLabel(title)
            t.setObjectName("cardTitle")
            self.body.addWidget(t)
        if subtitle:
            s = label(subtitle, "hint")
            s.setWordWrap(True)
            self.body.addWidget(s)


def label(text: str = "", name: str = "", parent: QWidget | None = None) -> QLabel:
    lab = QLabel(text, parent)
    if name:
        lab.setObjectName(name)
    return lab


def _triangle(p: QPainter, x: float, y: float, w: float, h: float, right: bool) -> None:
    if right:
        pts = [QPointF(x, y), QPointF(x + w, y + h / 2), QPointF(x, y + h)]
    else:
        pts = [QPointF(x + w, y), QPointF(x, y + h / 2), QPointF(x + w, y + h)]
    p.drawPolygon(QPolygonF(pts))


def transport_icon(kind: str, color: str = "#e6e8ee", size: int = 48) -> QIcon:
    """Painted media icons (avoids emoji-font fallbacks for ⏮ ▶ ⏸ …)."""
    pm = QPixmap(size, size)
    pm.fill(Qt.transparent)
    p = QPainter(pm)
    p.setRenderHint(QPainter.Antialiasing)
    p.setPen(Qt.NoPen)
    p.setBrush(QColor(color))
    s = size
    bar = s * 0.11
    if kind == "play":
        _triangle(p, s * 0.3, s * 0.2, s * 0.5, s * 0.6, True)
    elif kind == "pause":
        p.drawRoundedRect(QRectF(s * 0.28, s * 0.22, s * 0.15, s * 0.56), 2, 2)
        p.drawRoundedRect(QRectF(s * 0.57, s * 0.22, s * 0.15, s * 0.56), 2, 2)
    elif kind == "next":
        _triangle(p, s * 0.32, s * 0.25, s * 0.38, s * 0.5, True)
    elif kind == "prev":
        _triangle(p, s * 0.3, s * 0.25, s * 0.38, s * 0.5, False)
    elif kind == "first":
        p.drawRect(QRectF(s * 0.18, s * 0.25, bar, s * 0.5))
        _triangle(p, s * 0.31, s * 0.25, s * 0.26, s * 0.5, False)
        _triangle(p, s * 0.55, s * 0.25, s * 0.26, s * 0.5, False)
    elif kind == "last":
        _triangle(p, s * 0.19, s * 0.25, s * 0.26, s * 0.5, True)
        _triangle(p, s * 0.43, s * 0.25, s * 0.26, s * 0.5, True)
        p.drawRect(QRectF(s * 0.71, s * 0.25, bar, s * 0.5))
    p.end()
    return QIcon(pm)
