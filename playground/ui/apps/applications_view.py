"""The Applications tab: one page per image-processing application."""

from __future__ import annotations

from PySide6.QtWidgets import QTabWidget, QVBoxLayout, QWidget

from ...state import PlaygroundState
from .base import AppContext
from .canny_page import CannyPage
from .compression_page import CompressionPage
from .deconv_page import DeconvPage
from .detection_page import DetectionPage
from .portrait_page import PortraitPage
from .stereo_page import StereoPage
from .superres_page import SuperResPage

PAGES = (CompressionPage, DetectionPage, PortraitPage, DeconvPage, CannyPage, StereoPage,
         SuperResPage)


class ApplicationsView(QWidget):
    def __init__(self, state: PlaygroundState, parent=None):
        super().__init__(parent)
        self.context = AppContext(self)
        v = QVBoxLayout(self)
        v.setContentsMargins(0, 8, 0, 0)
        self.tabs = QTabWidget(objectName="appTabs")
        self.pages = {}
        for cls in PAGES:
            page = cls(state, self.context)
            self.pages[cls.TITLE] = page
            self.tabs.addTab(page, cls.TITLE)
        v.addWidget(self.tabs)
