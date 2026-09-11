"""Launch the Interactive 2D Convolution Playground."""

import sys

from PySide6.QtWidgets import QApplication

from playground.ui.main_window import MainWindow
from playground.ui.theme import apply_theme


def main() -> int:
    app = QApplication(sys.argv)
    app.setApplicationName("2D Convolution Playground")
    apply_theme(app)
    window = MainWindow()
    window.show()
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
