"""MatrixGrid: a QPainter widget that renders, highlights and edits a 2D matrix.

Used for the sketchable input, the kernel editor/viewer and the output. Small
matrices show values in tiles; large ones (images) fall back to pixel rendering.
"""

from __future__ import annotations

import numpy as np
from PySide6.QtCore import QPointF, QRectF, QSize, Qt, Signal
from PySide6.QtGui import (
    QBrush,
    QColor,
    QDoubleValidator,
    QFont,
    QFontMetricsF,
    QImage,
    QPainter,
    QPen,
)
from PySide6.QtWidgets import QLineEdit, QToolTip, QWidget

from . import theme


def _rgb(hex_color: str) -> np.ndarray:
    c = QColor(hex_color)
    return np.array([c.red(), c.green(), c.blue()], dtype=np.float64)


SEQ_LO = _rgb("#12151c")
SEQ_HI = _rgb("#f2f4f8")
DIV_ZERO = _rgb("#262b36")
DIV_NEG = _rgb(theme.NEGATIVE)
DIV_POS = _rgb(theme.POSITIVE)
EMPTY = _rgb("#1a1e26")


def format_value(v: float) -> str:
    if not np.isfinite(v):
        return "nan"
    if abs(v - round(v)) < 1e-9:
        s = str(int(round(v)))
    elif abs(v) >= 100:
        s = f"{v:.0f}"
    elif abs(v) >= 10:
        s = f"{v:.1f}"
    else:
        s = f"{v:.2f}".rstrip("0").rstrip(".")
        if s in ("0", "-0"):
            s = f"{v:.1e}"
    return s.replace("-", "−")


def colorize(data: np.ndarray, cmap: str, vrange: tuple[float, float] | None) -> np.ndarray:
    """Map values to uint8 RGB. cmap: 'sequential' | 'diverging' | 'auto'."""
    vmin, vmax = vrange if vrange is not None else (float(data.min()), float(data.max()))
    if cmap == "auto":
        cmap = "diverging" if vmin < 0 else "sequential"
    if cmap == "diverging":
        a = max(abs(vmin), abs(vmax)) or 1.0
        t = np.clip(data / a, -1, 1)[..., None]
        rgb = np.where(t < 0, DIV_ZERO + (DIV_NEG - DIV_ZERO) * -t, DIV_ZERO + (DIV_POS - DIV_ZERO) * t)
    else:
        if vmax - vmin < 1e-12:
            t = np.full(data.shape, 1.0 if vmax > 0 else 0.0)
        else:
            t = np.clip((data - vmin) / (vmax - vmin), 0, 1)
        rgb = SEQ_LO + (SEQ_HI - SEQ_LO) * t[..., None]
    return np.ascontiguousarray(rgb.round().astype(np.uint8))


class MatrixGrid(QWidget):
    cellEdited = Signal(int, int, float)   # interior (unpadded) coordinates

    def __init__(self, parent=None, *, sketchable: bool = False, editable: bool = False,
                 max_cell: float = 56, symbol: str = "x"):
        super().__init__(parent)
        self.setMouseTracking(True)
        self.setMinimumSize(80, 80)
        self.sketchable = sketchable
        self.editable = editable or sketchable
        self.max_cell = max_cell
        self.symbol = symbol
        self.brush_value = 1.0
        self.min_text_cell = 22.0
        self.cmap = "auto"

        self._data = np.zeros((1, 1))
        self._rgb = colorize(self._data, self.cmap, None)
        self._vrange: tuple[float, float] | None = None
        self._pad = (0, 0, 0, 0)
        self._visible: int | None = None     # raster-order count of revealed cells
        self._window: tuple[int, int, int, int] | None = None
        self._cell_hl: tuple[int, int] | None = None
        self._hover: tuple[int, int] | None = None
        self._painting: float | None = None
        self._last_paint: tuple[int, int] | None = None
        self._editor: QLineEdit | None = None
        self._edit_cell: tuple[int, int] | None = None

    # ---- public API ----------------------------------------------------------
    def set_matrix(self, data: np.ndarray, *, pad=(0, 0, 0, 0),
                   vrange: tuple[float, float] | None = None) -> None:
        self._data = np.asarray(data, dtype=np.float64)
        self._pad = tuple(pad)
        self._vrange = vrange
        self._rgb = colorize(self._data, self.cmap, vrange)
        if self._hover and not self._in_bounds(*self._hover):
            self._hover = None
        self.updateGeometry()
        self.update()

    def matrix(self) -> np.ndarray:
        return self._data

    def set_visible_count(self, count: int | None) -> None:
        if count != self._visible:
            self._visible = count
            self.update()

    def set_window(self, window: tuple[int, int, int, int] | None) -> None:
        if window != self._window:
            self._window = window
            self.update()

    def set_highlight(self, cell: tuple[int, int] | None) -> None:
        if cell != self._cell_hl:
            self._cell_hl = cell
            self.update()

    # ---- geometry ------------------------------------------------------------
    def _geometry(self) -> tuple[float, float, float]:
        rows, cols = self._data.shape
        margin = 6
        cell = min((self.width() - 2 * margin) / cols, (self.height() - 2 * margin) / rows, self.max_cell)
        cell = max(cell, 0.5)
        x0 = (self.width() - cell * cols) / 2
        y0 = (self.height() - cell * rows) / 2
        return x0, y0, cell

    def _cell_at(self, pos: QPointF) -> tuple[int, int] | None:
        x0, y0, cell = self._geometry()
        c = int((pos.x() - x0) // cell)
        r = int((pos.y() - y0) // cell)
        return (r, c) if self._in_bounds(r, c) else None

    def _in_bounds(self, r: int, c: int) -> bool:
        rows, cols = self._data.shape
        return 0 <= r < rows and 0 <= c < cols

    def _is_interior(self, r: int, c: int) -> bool:
        top, bottom, left, right = self._pad
        rows, cols = self._data.shape
        return top <= r < rows - bottom and left <= c < cols - right

    def _cell_rect(self, r: int, c: int, h: int = 1, w: int = 1) -> QRectF:
        x0, y0, cell = self._geometry()
        return QRectF(x0 + c * cell, y0 + r * cell, w * cell, h * cell)

    def sizeHint(self) -> QSize:
        rows, cols = self._data.shape
        cell = min(self.max_cell, 36)
        return QSize(int(min(cols * cell, 640)) + 12, int(min(rows * cell, 640)) + 12)

    def minimumSizeHint(self) -> QSize:
        return QSize(80, 80)

    # ---- painting -------------------------------------------------------------
    def paintEvent(self, _event) -> None:
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing, True)
        rows, cols = self._data.shape
        x0, y0, cell = self._geometry()
        grid_rect = QRectF(x0, y0, cell * cols, cell * rows)

        rgb = self._rgb
        if self._visible is not None and self._visible < rows * cols:
            rgb = rgb.copy()
            rgb.reshape(-1, 3)[max(self._visible, 0):] = EMPTY.astype(np.uint8)
        img = QImage(rgb.data, cols, rows, cols * 3, QImage.Format_RGB888)
        p.setRenderHint(QPainter.SmoothPixmapTransform, False)
        p.drawImage(grid_rect, img)

        tiles = cell >= 8
        if tiles:  # tile gaps in the background colour
            p.setPen(QPen(QColor(theme.BG), max(1.0, cell * 0.06)))
            for r in range(rows + 1):
                p.drawLine(QPointF(x0, y0 + r * cell), QPointF(x0 + cols * cell, y0 + r * cell))
            for c in range(cols + 1):
                p.drawLine(QPointF(x0 + c * cell, y0), QPointF(x0 + c * cell, y0 + rows * cell))

        if any(self._pad):
            self._paint_padding(p, x0, y0, cell)

        if cell >= self.min_text_cell:
            self._paint_values(p, x0, y0, cell)

        if self._window is not None:
            r, c, h, w = self._window
            rect = self._cell_rect(r, c, h, w).adjusted(-1, -1, 1, 1)
            accent = QColor(theme.ACCENT)
            fill = QColor(accent)
            fill.setAlpha(45)
            p.setBrush(fill)
            p.setPen(QPen(accent, 2.5 if cell >= 8 else 1.5))
            p.drawRoundedRect(rect, 4, 4)

        if self._cell_hl is not None:
            r, c = self._cell_hl
            rect = self._cell_rect(r, c).adjusted(-1, -1, 1, 1)
            p.setBrush(Qt.NoBrush)
            p.setPen(QPen(QColor(theme.HIGHLIGHT), 2.5 if cell >= 8 else 1.5))
            p.drawRoundedRect(rect, 3, 3)

        if self._hover is not None and self.editable and tiles:
            p.setBrush(Qt.NoBrush)
            p.setPen(QPen(QColor(255, 255, 255, 110), 1.5))
            p.drawRoundedRect(self._cell_rect(*self._hover).adjusted(1, 1, -1, -1), 3, 3)
        p.end()

    def _paint_padding(self, p: QPainter, x0: float, y0: float, cell: float) -> None:
        top, bottom, left, right = self._pad
        rows, cols = self._data.shape
        dim = QColor(theme.BG)
        dim.setAlpha(120)
        hatch = QColor(theme.TEXT_FAINT)
        hatch.setAlpha(70)
        bands = [
            QRectF(x0, y0, cols * cell, top * cell),
            QRectF(x0, y0 + (rows - bottom) * cell, cols * cell, bottom * cell),
            QRectF(x0, y0 + top * cell, left * cell, (rows - top - bottom) * cell),
            QRectF(x0 + (cols - right) * cell, y0 + top * cell, right * cell, (rows - top - bottom) * cell),
        ]
        p.setPen(Qt.NoPen)
        for band in bands:
            if band.width() > 0 and band.height() > 0:
                p.setBrush(dim)
                p.drawRect(band)
                p.setBrush(QBrush(hatch, Qt.BDiagPattern))
                p.drawRect(band)
        inner = QRectF(x0 + left * cell, y0 + top * cell,
                       (cols - left - right) * cell, (rows - top - bottom) * cell)
        pen = QPen(QColor(theme.TEXT_DIM), 1.2, Qt.DashLine)
        p.setPen(pen)
        p.setBrush(Qt.NoBrush)
        p.drawRect(inner)

    def _paint_values(self, p: QPainter, x0: float, y0: float, cell: float) -> None:
        rows, cols = self._data.shape
        base = QFont(self.font())
        base.setPixelSize(int(max(8, min(cell * 0.3, 15))))
        base.setWeight(QFont.Medium)
        p.setFont(base)
        fm = QFontMetricsF(base)
        limit = rows * cols if self._visible is None else max(self._visible, 0)
        lum = (self._rgb[..., 0] * 0.299 + self._rgb[..., 1] * 0.587 + self._rgb[..., 2] * 0.114)
        for r in range(rows):
            for c in range(cols):
                if r * cols + c >= limit:
                    return
                text = format_value(self._data[r, c])
                rect = QRectF(x0 + c * cell, y0 + r * cell, cell, cell)
                width = fm.horizontalAdvance(text)
                if width > cell * 0.88:
                    f = QFont(base)
                    f.setPixelSize(max(6, int(base.pixelSize() * cell * 0.88 / width)))
                    p.setFont(f)
                dark_text = lum[r, c] > 140
                color = QColor("#10131a") if dark_text else QColor(theme.TEXT)
                if not self._is_interior(r, c):
                    color.setAlpha(150)
                p.setPen(color)
                p.drawText(rect, Qt.AlignCenter, text)
                if width > cell * 0.88:
                    p.setFont(base)

    # ---- interaction ------------------------------------------------------------
    def _interior_coords(self, r: int, c: int) -> tuple[int, int]:
        return r - self._pad[0], c - self._pad[2]

    def _paint_cell(self, cell: tuple[int, int]) -> None:
        cells = [cell]
        if self._last_paint is not None:  # fill gaps during fast drags
            (r0, c0), (r1, c1) = self._last_paint, cell
            n = max(abs(r1 - r0), abs(c1 - c0))
            cells = [(round(r0 + (r1 - r0) * t / n), round(c0 + (c1 - c0) * t / n))
                     for t in range(1, n + 1)] if n else []
        self._last_paint = cell
        for r, c in cells:
            if self._is_interior(r, c):
                self.cellEdited.emit(*self._interior_coords(r, c), float(self._painting))

    def mousePressEvent(self, event) -> None:
        if not self.sketchable or self._editor is not None:
            return super().mousePressEvent(event)
        cell = self._cell_at(event.position())
        if cell is None:
            return
        if event.button() == Qt.LeftButton:
            self._painting = self.brush_value
        elif event.button() == Qt.RightButton:
            self._painting = 0.0
        else:
            return
        self._last_paint = None
        self._paint_cell(cell)

    def mouseMoveEvent(self, event) -> None:
        cell = self._cell_at(event.position())
        if cell != self._hover:
            self._hover = cell
            self.update()
        if self._painting is not None and cell is not None:
            if cell != self._last_paint:
                self._paint_cell(cell)
        elif cell is not None:
            r, c = cell
            ir, ic = self._interior_coords(r, c)
            note = "" if self._is_interior(r, c) else "  (padding)"
            text = f"{self.symbol}[{ir}, {ic}] = {format_value(self._data[r, c])}{note}"
            QToolTip.showText(event.globalPosition().toPoint(), text, self)
        else:
            QToolTip.hideText()

    def mouseReleaseEvent(self, event) -> None:
        self._painting = None
        self._last_paint = None
        super().mouseReleaseEvent(event)

    def leaveEvent(self, event) -> None:
        self._hover = None
        self.update()
        super().leaveEvent(event)

    def mouseDoubleClickEvent(self, event) -> None:
        if not self.editable:
            return
        cell = self._cell_at(event.position())
        if cell is not None and self._is_interior(*cell):
            self._painting = None
            self._open_editor(cell)

    def _open_editor(self, cell: tuple[int, int]) -> None:
        self._close_editor(commit=False)
        x0, y0, size = self._geometry()
        if size < 14:
            return
        r, c = cell
        editor = QLineEdit(self)
        editor.setValidator(QDoubleValidator(-1e9, 1e9, 6, editor))
        editor.setAlignment(Qt.AlignCenter)
        editor.setText(f"{self._data[r, c]:g}")
        w = max(size, 56)
        editor.setGeometry(int(x0 + c * size + size / 2 - w / 2), int(y0 + r * size + size / 2 - 15),
                           int(w), 30)
        editor.selectAll()
        # Only react while this editor is still the active one: after Enter the
        # next cell's editor may already be open when editingFinished arrives.
        editor.returnPressed.connect(lambda: self._editor is editor and self._commit_and_advance())
        editor.editingFinished.connect(lambda: self._editor is editor and self._close_editor(commit=True))
        editor.installEventFilter(self)
        self._editor, self._edit_cell = editor, cell
        editor.show()
        editor.setFocus()

    def eventFilter(self, obj, event) -> bool:
        if obj is self._editor and event.type() == event.Type.KeyPress and event.key() == Qt.Key_Escape:
            self._close_editor(commit=False)
            return True
        return super().eventFilter(obj, event)

    def _commit_and_advance(self) -> None:
        cell = self._edit_cell
        self._close_editor(commit=True)
        if cell is None:
            return
        rows, cols = self._data.shape
        top, bottom, left, right = self._pad
        r, c = cell
        c += 1
        if c >= cols - right:
            c, r = left, r + 1
        if r < rows - bottom:
            self._open_editor((r, c))

    def _close_editor(self, commit: bool) -> None:
        editor, cell = self._editor, self._edit_cell
        if editor is None:
            return
        self._editor = self._edit_cell = None
        text = editor.text().replace("−", "-").replace(",", ".")
        editor.removeEventFilter(self)
        editor.hide()
        editor.deleteLater()
        if commit and cell is not None:
            try:
                value = float(text)
            except ValueError:
                return
            if value != self._data[cell]:
                self.cellEdited.emit(*self._interior_coords(*cell), value)
        self.setFocus()
