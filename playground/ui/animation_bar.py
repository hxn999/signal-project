"""Transport controls driving the step-by-step animation."""

from __future__ import annotations

from PySide6.QtCore import QSize, Qt, QTimer
from PySide6.QtWidgets import QComboBox, QHBoxLayout, QSlider, QToolButton, QWidget

from ..state import PlaygroundState
from . import theme
from .widgets import label, transport_icon

MULTIPLIERS = (1, 10, 100, 1000)


class AnimationBar(QWidget):
    def __init__(self, state: PlaygroundState, parent=None):
        super().__init__(parent)
        self.state = state
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._tick)

        lay = QHBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(6)

        def button(kind: str, tip: str, slot, name: str = "transport") -> QToolButton:
            b = QToolButton()
            b.setObjectName(name)
            b.setIcon(transport_icon(kind, "#0b0d12" if name == "play" else theme.TEXT))
            b.setIconSize(QSize(20, 20))
            b.setToolTip(tip)
            b.clicked.connect(slot)
            lay.addWidget(b)
            return b

        button("first", "Reset (Home)", self.reset)
        button("prev", "Step back (←)", self.step_back)
        self.play_btn = button("play", "Play / pause (Space)", self.toggle, "play")
        button("next", "Step forward (→)", self.step_forward)
        button("last", "Finish (End)", self.finish)
        self._icons = {"play": transport_icon("play", "#0b0d12"), "pause": transport_icon("pause", "#0b0d12")}

        self.scrubber = QSlider(Qt.Horizontal)
        self.scrubber.setMinimum(-1)
        self.scrubber.valueChanged.connect(self._on_scrub)
        lay.addSpacing(8)
        lay.addWidget(self.scrubber, 1)
        self.step_label = label("", "stepBadge")
        self.step_label.setMinimumWidth(120)
        self.step_label.setAlignment(Qt.AlignCenter)
        lay.addWidget(self.step_label)

        lay.addSpacing(12)
        lay.addWidget(label("Speed", "dim"))
        self.speed = QSlider(Qt.Horizontal, minimum=1, maximum=60, value=6)
        self.speed.setFixedWidth(110)
        self.speed.valueChanged.connect(self._on_speed)
        lay.addWidget(self.speed)
        self.speed_label = label("", "dim")
        self.speed_label.setMinimumWidth(44)
        lay.addWidget(self.speed_label)
        self.multiplier = QComboBox()
        for m in MULTIPLIERS:
            self.multiplier.addItem(f"×{m}", m)
        self.multiplier.setToolTip("Steps advanced per tick — use for large images")
        lay.addWidget(self.multiplier)

        self._input_changed = True
        state.inputChanged.connect(lambda: setattr(self, "_input_changed", True))
        state.resultChanged.connect(self._on_result)
        state.stepChanged.connect(self._on_step)
        self._on_speed()
        self._on_result()

    # ---- transport ------------------------------------------------------------
    @property
    def playing(self) -> bool:
        return self.timer.isActive()

    def toggle(self) -> None:
        self.pause() if self.playing else self.play()

    def play(self) -> None:
        n = self.state.num_steps
        if n == 0:
            return
        if self.state.step < 0 or self.state.step >= n:
            self.state.set_step(0)
        self.timer.start(int(1000 / self.speed.value()))
        self.play_btn.setIcon(self._icons["pause"])

    def pause(self) -> None:
        self.timer.stop()
        self.play_btn.setIcon(self._icons["play"])

    def reset(self) -> None:
        self.pause()
        self.state.set_step(-1)

    def finish(self) -> None:
        self.pause()
        self.state.set_step(self.state.num_steps)

    def step_forward(self) -> None:
        self.pause()
        n, step = self.state.num_steps, self.state.step
        self.state.set_step(0 if step >= n else step + 1)

    def step_back(self) -> None:
        self.pause()
        n, step = self.state.num_steps, self.state.step
        self.state.set_step(n - 1 if step >= n else step - 1)

    def _tick(self) -> None:
        nxt = self.state.step + self.multiplier.currentData()
        if nxt >= self.state.num_steps:
            self.finish()
        else:
            self.state.set_step(nxt)

    # ---- sync ----------------------------------------------------------------
    def _on_speed(self) -> None:
        self.speed_label.setText(f"{self.speed.value()}/s")
        if self.playing:
            self.timer.setInterval(int(1000 / self.speed.value()))

    def _auto_multiplier(self) -> None:
        n = self.state.num_steps
        m = 1 if n <= 400 else 10 if n <= 4000 else 100
        self.multiplier.setCurrentIndex(MULTIPLIERS.index(m))

    def _on_result(self) -> None:
        self.pause()
        if self._input_changed:  # pick a sensible speed-up once per new input
            self._input_changed = False
            self._auto_multiplier()
        self.scrubber.blockSignals(True)
        self.scrubber.setMaximum(max(self.state.num_steps, 0))
        self.scrubber.blockSignals(False)
        self.setEnabled(self.state.num_steps > 0)
        self._on_step(self.state.step)

    def _on_step(self, step: int) -> None:
        self.scrubber.blockSignals(True)
        self.scrubber.setValue(step)
        self.scrubber.blockSignals(False)
        n = self.state.num_steps
        if n == 0:
            text = "No output"
        elif step < 0:
            text = f"Ready · {n:,} steps"
        elif step >= n:
            text = "Done"
        else:
            text = f"Step {step + 1:,} / {n:,}"
        self.step_label.setText(text)

    def _on_scrub(self, value: int) -> None:
        self.pause()
        self.state.set_step(value)
