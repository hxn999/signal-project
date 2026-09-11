"""Side-by-side input ⊛ kernel = output view with the multiply-add breakdown."""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout, QWidget

from ..core.convolution import PADDING_LABELS, ConvResult, Step
from ..state import PlaygroundState
from . import theme
from .animation_bar import AnimationBar
from .matrix_grid import MatrixGrid, format_value
from .widgets import Card, label

MAX_TERMS = 12


def _term(v: float) -> str:
    s = format_value(v)
    return f"({s})" if s.startswith("−") else s


def equation_html(res: ConvResult, st: Step) -> str:
    m, n = st.out_pos
    r0, c0 = st.window_origin
    kh, kw = st.patch.shape
    top, left = res.pad[0], res.pad[2]
    terms = [f"{_term(x)}·{_term(k)}" for x, k in zip(st.patch.ravel(), res.applied_kernel.ravel())]
    shown = " + ".join(terms[:MAX_TERMS])
    if len(terms) > MAX_TERMS:
        shown += f" + … <span style='color:{theme.TEXT_FAINT}'>({len(terms) - MAX_TERMS} more terms)</span>"
    rows = f"{r0 - top}…{r0 - top + kh - 1}"
    cols = f"{c0 - left}…{c0 - left + kw - 1}"
    head = (f"<span style='color:{theme.HIGHLIGHT}; font-weight:600'>y[{m}, {n}]</span>"
            f"<span style='color:{theme.TEXT_DIM}'> = Σ<sub>i,j</sub> x<sub>pad</sub>[{m * res.stride[0]}+i, "
            f"{n * res.stride[1]}+j] · h̃[i, j] &nbsp;(h̃ = flipped h) &nbsp;·&nbsp; "
            f"window over x rows {rows}, cols {cols}</span>")
    body = (f"= {shown}<br>= <span style='color:{theme.HIGHLIGHT}; font-weight:600'>"
            f"{format_value(st.value)}</span>")
    return f"{head}<br>{body}"


class Pane(QWidget):
    def __init__(self, title: str, grid: MatrixGrid, parent=None):
        super().__init__(parent)
        v = QVBoxLayout(self)
        v.setContentsMargins(0, 0, 0, 0)
        v.setSpacing(2)
        self.title = label(title, "paneTitle")
        self.caption = label("", "caption")
        v.addWidget(self.title, 0, Qt.AlignHCenter)
        v.addWidget(self.caption, 0, Qt.AlignHCenter)
        v.addWidget(grid, 1)


class StepView(QWidget):
    def __init__(self, state: PlaygroundState, parent=None):
        super().__init__(parent)
        self.state = state
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 12, 0, 0)
        root.setSpacing(12)

        canvas = Card()
        row = QHBoxLayout()
        row.setSpacing(6)
        self.input_grid = MatrixGrid(sketchable=True, symbol="x")
        self.input_grid.cellEdited.connect(self._on_input_edit)
        self.kernel_grid = MatrixGrid(max_cell=44, symbol="h̃")
        self.kernel_grid.cmap = "diverging"
        self.output_grid = MatrixGrid(symbol="y")
        self.input_pane = Pane("Input  x[m, n]", self.input_grid)
        self.kernel_pane = Pane("Kernel (flipped)  h[−i, −j]", self.kernel_grid)
        self.output_pane = Pane("Output  y[m, n]", self.output_grid)
        row.addWidget(self.input_pane, 5)
        row.addWidget(label("⊛", "glyph"), 0, Qt.AlignVCenter)
        row.addWidget(self.kernel_pane, 2)
        row.addWidget(label("=", "glyph"), 0, Qt.AlignVCenter)
        row.addWidget(self.output_pane, 4)
        canvas.body.addLayout(row, 1)
        root.addWidget(canvas, 1)

        breakdown = Card()
        self.equation = label("", "equation")
        self.equation.setTextFormat(Qt.RichText)
        self.equation.setWordWrap(True)
        self.equation.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.equation.setMinimumHeight(48)
        breakdown.body.addWidget(self.equation)
        self.animation = AnimationBar(state)
        breakdown.body.addWidget(self.animation)
        root.addWidget(breakdown)

        state.resultChanged.connect(self._on_result)
        state.stepChanged.connect(self._on_step)
        self._on_result()

    def _on_input_edit(self, r: int, c: int, value: float) -> None:
        if self.state.source == "sketch":
            self.state.set_sketch_cell(r, c, value)

    def _on_result(self) -> None:
        s, res = self.state, self.state.result
        sketch = s.source == "sketch"
        self.input_grid.sketchable = self.input_grid.editable = sketch
        x = s.input
        in_range = (0.0, 255.0) if not sketch else (min(float(x.min()), 0.0), max(float(x.max()), 1e-12))
        h, w = x.shape
        kh, kw = s.kernel.shape
        self.kernel_pane.caption.setText(f"{kh}×{kw} · {s.kernel_name} · reflected for convolution")
        if res is None:
            self.input_grid.set_matrix(x, vrange=in_range)
            self.kernel_grid.set_matrix(s.kernel[::-1, ::-1])
            self.output_grid.set_matrix([[0.0]])
            self.output_grid.set_visible_count(0)
            self.input_pane.caption.setText(f"{h}×{w}")
            self.output_pane.caption.setText("—")
            self._on_step(s.step)
            return
        self.input_grid.set_matrix(res.padded, pad=res.pad, vrange=in_range)
        self.kernel_grid.set_matrix(res.applied_kernel)
        out = res.output
        self.output_grid.set_matrix(out, vrange=(float(out.min()), float(out.max())))

        hp, wp = res.padded.shape
        pad = "no padding" if res.padding == "valid" else f"{PADDING_LABELS[res.padding].lower()} pad → {hp}×{wp}"
        self.input_pane.caption.setText(f"{h}×{w} · {pad}")
        sr, sc = res.stride
        self.output_pane.caption.setText(f"{out.shape[0]}×{out.shape[1]} · stride {sr}×{sc}")
        self._on_step(s.step)

    def _on_step(self, step: int) -> None:
        res = self.state.result
        if res is None:
            self.equation.setText(f"<span style='color:{theme.ERROR}'>{self.state.error}</span>")
            self.input_grid.set_window(None)
            self.output_grid.set_highlight(None)
            return
        n = res.num_steps
        if 0 <= step < n:
            st = res.step(step)
            kh, kw = res.applied_kernel.shape
            self.input_grid.set_window((*st.window_origin, kh, kw))
            self.output_grid.set_visible_count(step + 1)
            self.output_grid.set_highlight(st.out_pos)
            self.equation.setText(equation_html(res, st))
            return
        self.input_grid.set_window(None)
        self.output_grid.set_highlight(None)
        dim = theme.TEXT_DIM
        if step < 0:
            self.output_grid.set_visible_count(0)
            self.equation.setText(
                f"<span style='color:{dim}'>Ready. Press <b>Play</b> (Space) or step with → to slide the "
                f"flipped kernel across the input one output sample at a time.</span>")
        else:
            out = res.output
            self.output_grid.set_visible_count(None)
            self.equation.setText(
                f"<span style='color:{dim}'>Output complete: {out.shape[0]}×{out.shape[1]} samples · "
                f"min {format_value(float(out.min()))} · max {format_value(float(out.max()))} · "
                f"mean {format_value(float(out.mean()))}.</span><br>"
                f"<span style='color:{theme.TEXT_FAINT}'>Press Play to animate the computation, "
                f"or hover any cell to inspect its value.</span>")
