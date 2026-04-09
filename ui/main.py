import sys
import os
from pathlib import Path
import logging

import fitz
from PySide6.QtCore import Qt
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import QApplication, QFileDialog, QLabel, QMainWindow, QPushButton, QScrollArea, QHBoxLayout, \
    QVBoxLayout, QWidget, QSpinBox, QGraphicsScene
from PySide6.QtGui import QPainter

from app.pdf_model import PDFModel
from ui_utils import load_ui_from_name

logger = logging.getLogger(__name__)


class PDFWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = load_ui_from_name("pdfwindow.ui", self)

        self.ui.q_GraphicsView.setRenderHint(QPainter.Antialiasing, True)
        self.ui.q_GraphicsView.setRenderHint(QPainter.SmoothPixmapTransform, True)

        self.setCentralWidget(self.ui)
        self.setMinimumSize(1500, 1000)
        self.setGeometry(100, 100, 1500, 1000)

        self.pdf_model = PDFModel("./../sample-local-pdf.pdf")

        self.q_graphics_window = GraphicsWindow(self.pdf_model,
                                                self.ui.q_GraphicsView,
                                                self.ui.q_le_Offset,
                                                self.ui.q_le_Page,
                                                self.ui.q_btn_Prev,
                                                self.ui.q_btn_Next)

        self.a_graphics_window = GraphicsWindow(self.pdf_model,
                                                self.ui.a_GraphicsView,
                                                self.ui.a_le_Offset,
                                                self.ui.a_le_Page,
                                                self.ui.a_btn_Prev,
                                                self.ui.a_btn_Next)

        self.graphics_windows = [self.q_graphics_window, self.a_graphics_window]

    def fit_view(self):
        for graphics_window in self.graphics_windows:
            graphics_window.fit_view()

    def showEvent(self, event):
        super().showEvent(event)
        self.fit_view()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.fit_view()


class GraphicsWindow:
    def __init__(self, pdf_model, graphicsView, leOffset, lePage, btnPrev, btnNext):
        self.pdf_model = pdf_model

        self.graphicsView = graphicsView
        self.leOffset = leOffset
        self.lePage = lePage
        self.btnPrev = btnPrev
        self.btnNext = btnNext

        self.scene = QGraphicsScene()
        self.graphicsView.setScene(self.scene)
        self.display_current_page()

    def display_current_page(self):
        path = self.pdf_model.get_current_page_image_path()
        pixmap = QPixmap(str(path))

        self.scene.clear()
        self.scene.addPixmap(pixmap)
        self.scene.setSceneRect(pixmap.rect().toRectF())
        self.fit_view()

    def fit_view(self):
        self.graphicsView.fitInView(self.scene.sceneRect(), Qt.KeepAspectRatio)


app = QApplication(sys.argv)
pdfwindow = PDFWindow()
pdfwindow.show()
app.exec()
