"""Computation parameters: stride and padding mode, plus live shape readout."""

from __future__ import annotations

from PySide6.QtWidgets import QComboBox, QGridLayout, QHBoxLayout, QSpinBox, QVBoxLayout, QWidget

from ..core.convolution import PADDING_LABELS
from ..state import PlaygroundState
from .widgets import label


class ComputePanel(QWidget):
    def __init__(self, state: PlaygroundState, parent=None):
        super().__init__(parent)
        self.state = state
        v = QVBoxLayout(self)
        v.setContentsMargins(0, 0, 0, 0)
        v.setSpacing(8)

        g = QGridLayout()
        g.setHorizontalSpacing(8)
        g.setVerticalSpacing(8)
        self.stride_r = QSpinBox(minimum=1, maximum=8, value=state.stride[0])
        self.stride_c = QSpinBox(minimum=1, maximum=8, value=state.stride[1])
        for spin in (self.stride_r, self.stride_c):
            spin.valueChanged.connect(self._on_stride)
        stride_row = QHBoxLayout()
        stride_row.addWidget(self.stride_r, 1)
        stride_row.addWidget(label("×", "dim"))
        stride_row.addWidget(self.stride_c, 1)
        g.addWidget(label("Stride (rows × cols)", "dim"), 0, 0)
        g.addLayout(stride_row, 0, 1)

        self.padding = QComboBox()
        for key, text in PADDING_LABELS.items():
            self.padding.addItem(text, key)
        self.padding.setCurrentIndex(self.padding.findData(state.padding))
        self.padding.currentIndexChanged.connect(lambda: state.set_padding(self.padding.currentData()))
        g.addWidget(label("Padding", "dim"), 1, 0)
        g.addWidget(self.padding, 1, 1)
        g.setColumnStretch(1, 1)
        v.addLayout(g)

        self.readout = label("", "dim")
        self.readout.setWordWrap(True)
        v.addWidget(self.readout)
        self.error = label("", "error")
        self.error.setWordWrap(True)
        v.addWidget(self.error)

        state.resultChanged.connect(self._sync)
        self._sync()

    def _on_stride(self) -> None:
        self.state.set_stride(self.stride_r.value(), self.stride_c.value())

    def _sync(self) -> None:
        s, res = self.state, self.state.result
        h, w = s.input.shape
        lines = [f"Input  {h}×{w}"]
        if res is not None:
            hp, wp = res.padded.shape
            m, n = res.output.shape
            lines += [f"Padded input  {hp}×{wp}", f"Output  {m}×{n}  ·  {res.num_steps:,} steps"]
        self.readout.setText("<br>".join(lines))
        self.error.setText(s.error)
        self.error.setVisible(bool(s.error))
