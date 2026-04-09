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

        self.ui.graphicsView.setRenderHint(QPainter.Antialiasing, True)
        self.ui.graphicsView.setRenderHint(QPainter.SmoothPixmapTransform, True)

        self.setCentralWidget(self.ui)
        self.setMinimumSize(1500, 1000)
        self.setGeometry(100, 100, 1500, 1000)

        self.pdf_model = PDFModel("./../sample-local-pdf.pdf")
        self.scene = QGraphicsScene()
        self.ui.graphicsView.setScene(self.scene)

        self.display_current_page()

    def display_current_page(self):
        path = self.pdf_model.get_current_page_image_path()
        pixmap = QPixmap(str(path))

        self.scene.clear()
        self.scene.addPixmap(pixmap)
        self.scene.setSceneRect(pixmap.rect().toRectF())
        self.fit_view()

    def fit_view(self):
        self.ui.graphicsView.fitInView(self.scene.sceneRect(), Qt.KeepAspectRatio)

    def showEvent(self, event):
        super().showEvent(event)
        self.fit_view()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.fit_view()


app = QApplication(sys.argv)
pdfwindow = PDFWindow()
pdfwindow.show()
app.exec()
