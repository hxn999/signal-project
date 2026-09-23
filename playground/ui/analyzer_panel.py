"""Analyzer panel: causality, BIBO stability, DC gain and kernel classification.

Displayed as a Card in the sidebar. Updates automatically when the kernel or
result changes.
"""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QVBoxLayout, QWidget

from ..core.analyzer import (
    BIBOResult,
    CausalityResult,
    check_causality,
    compute_bibo,
    dc_gain,
    kernel_classification,
)
from ..state import PlaygroundState
from ..ui import theme
from .matrix_grid import format_value
from .widgets import label


class AnalyzerPanel(QWidget):
    """Sidebar widget showing causality, stability and DC-gain analysis."""

    def __init__(self, state: PlaygroundState, parent=None):
        super().__init__(parent)
        self.state = state
        v = QVBoxLayout(self)
        v.setContentsMargins(0, 0, 0, 0)
        v.setSpacing(10)

        # --- Causality ---
        self.causal_title = label("Causality (raster-scan)", "dim")
        self.causal_title.setStyleSheet(f"font-weight: 600; color: {theme.TEXT};")
        v.addWidget(self.causal_title)
        self.causal_body = label("", "dim")
        self.causal_body.setWordWrap(True)
        self.causal_body.setTextFormat(Qt.RichText)
        v.addWidget(self.causal_body)

        # --- BIBO stability ---
        self.bibo_title = label("BIBO stability", "dim")
        self.bibo_title.setStyleSheet(f"font-weight: 600; color: {theme.TEXT};")
        v.addWidget(self.bibo_title)
        self.bibo_body = label("", "dim")
        self.bibo_body.setWordWrap(True)
        self.bibo_body.setTextFormat(Qt.RichText)
        v.addWidget(self.bibo_body)

        # --- DC gain ---
        self.dc_title = label("DC gain & classification", "dim")
        self.dc_title.setStyleSheet(f"font-weight: 600; color: {theme.TEXT};")
        v.addWidget(self.dc_title)
        self.dc_body = label("", "dim")
        self.dc_body.setWordWrap(True)
        self.dc_body.setTextFormat(Qt.RichText)
        v.addWidget(self.dc_body)

        state.resultChanged.connect(self._refresh)
        state.kernelChanged.connect(self._refresh)
        self._refresh()

    # --------------------------------------------------------------------- #
    def _refresh(self) -> None:
        self._refresh_causality()
        self._refresh_bibo()
        self._refresh_dc()

    def _refresh_causality(self) -> None:
        cr: CausalityResult = check_causality(self.state.kernel)
        if cr.is_causal:
            html = (f"<span style='color:{theme.ACCENT}'>✓ Causal</span> under raster-scan ordering"
                    f"<br><span style='color:{theme.TEXT_DIM}'>Origin at ({cr.origin[0]}, {cr.origin[1]})"
                    f" — all non-zero elements are at or after the origin.</span>")
        else:
            a, b = cr.shift  # type: ignore[misc]
            html = (f"<span style='color:{theme.HIGHLIGHT}'>✗ Non-causal</span> with origin at "
                    f"({cr.origin[0]}, {cr.origin[1]})"
                    f"<br><span style='color:{theme.TEXT_DIM}'>Minimum origin shift to make causal: "
                    f"<b>(a, b) = ({a}, {b})</b></span>")
        self.causal_body.setText(html)

    def _refresh_bibo(self) -> None:
        s = self.state
        output = s.result.output if s.result else None
        br: BIBOResult = compute_bibo(s.kernel, s.input, output)

        s_str = format_value(br.s_abs)
        b_str = format_value(br.b_max)
        bound_str = format_value(br.y_bound)
        actual_str = format_value(br.y_actual_max)

        html = (f"<span style='color:{theme.ACCENT}'>✓ BIBO stable</span>"
                f" (finite kernel ⇒ S &lt; ∞)"
                f"<br><span style='color:{theme.TEXT_DIM}'>"
                f"S = ΣΣ|h| = {s_str}"
                f"<br>B = max|x| = {b_str}"
                f"<br>Bound: |y| ≤ B·S = {bound_str}")

        if output is not None:
            html += f"<br>Actual max|y| = {actual_str}"
            if br.y_actual_max <= br.y_bound + 1e-9:
                html += f"  <span style='color:{theme.ACCENT}'>≤ bound ✓</span>"
        html += "</span>"
        self.bibo_body.setText(html)

    def _refresh_dc(self) -> None:
        g = dc_gain(self.state.kernel)
        cls = kernel_classification(self.state.kernel)
        g_str = format_value(g)

        if cls == "Averaging":
            cls_color = theme.ACCENT
            cls_desc = "non-zero DC gain → averaging / low-pass"
        else:
            cls_color = theme.HIGHLIGHT
            cls_desc = "DC gain ≈ 0 → differencing / high-pass"

        html = (f"G = ΣΣh = <b>{g_str}</b>"
                f"<br><span style='color:{cls_color}'>{cls}</span>"
                f" — <span style='color:{theme.TEXT_DIM}'>{cls_desc}</span>")
        self.dc_body.setText(html)
