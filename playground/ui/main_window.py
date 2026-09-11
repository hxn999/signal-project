"""Main window: sidebar of controls + step-by-step / result tabs."""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtGui import QKeySequence, QShortcut
from PySide6.QtWidgets import (
    QHBoxLayout,
    QMainWindow,
    QScrollArea,
    QStatusBar,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from ..state import PlaygroundState
from .compute_panel import ComputePanel
from .input_panel import InputPanel
from .kernel_panel import KernelPanel
from .result_view import ResultView
from .step_view import StepView
from .widgets import Card, label

SIDEBAR_WIDTH = 360


class MainWindow(QMainWindow):
    def __init__(self, state: PlaygroundState | None = None):
        super().__init__()
        self.state = state or PlaygroundState(self)
        self.setWindowTitle("2D Convolution Playground")
        self.resize(1440, 900)

        central = QWidget(objectName="central")
        self.setCentralWidget(central)
        root = QHBoxLayout(central)
        root.setContentsMargins(16, 12, 16, 12)
        root.setSpacing(16)

        root.addWidget(self._build_sidebar())

        self.tabs = QTabWidget(objectName="mainTabs")
        self.step_view = StepView(self.state)
        self.result_view = ResultView(self.state)
        self.tabs.addTab(self.step_view, "Step-by-step")
        self.tabs.addTab(self.result_view, "Result map")
        root.addWidget(self.tabs, 1)

        status = QStatusBar()
        self.status_label = label()
        status.addWidget(self.status_label)
        self.setStatusBar(status)

        self.input_panel.brushChanged.connect(lambda v: setattr(self.step_view.input_grid, "brush_value", v))
        self.input_panel.imageLoaded.connect(lambda: self.tabs.setCurrentWidget(self.result_view))
        self.state.resultChanged.connect(self._update_status)
        self._update_status()
        self._install_shortcuts()

    def _build_sidebar(self) -> QScrollArea:
        sidebar = QWidget(objectName="sidebar")
        v = QVBoxLayout(sidebar)
        v.setContentsMargins(0, 0, 6, 0)
        v.setSpacing(12)

        v.addWidget(label("2D Convolution Playground", "appTitle"))
        sub = label("CSE 219 · Signals and Linear Systems — the kernel as the impulse response "
                    "of a 2D LTI system", "appSubtitle")
        sub.setWordWrap(True)
        v.addWidget(sub)

        self.input_panel = InputPanel(self.state)
        self.kernel_panel = KernelPanel(self.state)
        self.compute_panel = ComputePanel(self.state)
        for title, panel in (("Input", self.input_panel), ("Kernel", self.kernel_panel),
                             ("Computation", self.compute_panel)):
            card = Card(title)
            card.body.addWidget(panel)
            v.addWidget(card)
        v.addStretch(1)

        scroll = QScrollArea()
        scroll.setWidget(sidebar)
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setFixedWidth(SIDEBAR_WIDTH)
        return scroll

    def _install_shortcuts(self) -> None:
        bar = self.step_view.animation
        for key, slot in ((Qt.Key_Space, bar.toggle), (Qt.Key_Right, bar.step_forward),
                          (Qt.Key_Left, bar.step_back), (Qt.Key_Home, bar.reset), (Qt.Key_End, bar.finish)):
            QShortcut(QKeySequence(key), self, slot)

    def _update_status(self) -> None:
        s, res = self.state, self.state.result
        h, w = s.input.shape
        kh, kw = s.kernel.shape
        parts = [f"Input {h}×{w} ({s.source})", f"Kernel {kh}×{kw} ({s.kernel_name})",
                 f"Stride {s.stride[0]}×{s.stride[1]}", f"Padding {s.padding}"]
        if res is not None:
            parts.append(f"Output {res.output.shape[0]}×{res.output.shape[1]}")
        else:
            parts.append(f"⚠ {s.error}")
        self.status_label.setText("   ·   ".join(parts))
