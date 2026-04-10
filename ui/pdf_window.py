import logging

from PySide6.QtWidgets import QMainWindow
from PySide6.QtGui import QPainter

from app.pdf_model import PDFModel
from ui.graphics_widget import GraphicsWidget
from ui_utils import load_ui_from_name

logger = logging.getLogger(__name__)


class PDFWindow(QMainWindow):
    def __init__(self, pdf_path="./../sample-local-pdf.pdf"):
        super().__init__()
        self.ui = load_ui_from_name("pdfwindow.ui", self)
        print(type(self.ui.q_GraphicsView))

        self.setCentralWidget(self.ui)
        self.setMinimumSize(1500, 1000)
        self.setGeometry(100, 100, 1500, 1000)

        self.q_graphics_widget = GraphicsWidget(pdf_path,
                                                self.ui.q_GraphicsView,
                                                self.ui.q_le_Offset,
                                                self.ui.q_le_Page,
                                                self.ui.q_btn_Prev,
                                                self.ui.q_btn_Next,
                                                self.ui.q_btn_Clear)

        self.a_graphics_widget = GraphicsWidget(pdf_path,
                                                self.ui.a_GraphicsView,
                                                self.ui.a_le_Offset,
                                                self.ui.a_le_Page,
                                                self.ui.a_btn_Prev,
                                                self.ui.a_btn_Next,
                                                self.ui.a_btn_Clear)

        self.graphics_widgets = [self.q_graphics_widget, self.a_graphics_widget]

    def fit_view(self):
        for graphics_window in self.graphics_widgets:
            graphics_window.fit_view()

    def showEvent(self, event):
        super().showEvent(event)
        self.fit_view()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.fit_view()
