import sys
import os
from pathlib import Path
import logging

import fitz
from PySide6.QtCore import Qt
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import QApplication, QFileDialog, QLabel, QMainWindow, QPushButton, QScrollArea, QHBoxLayout, QVBoxLayout, QWidget, QSpinBox

from ui_utils import load_ui_from_name

logger = logging.getLogger(__name__)


class PDFWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 1000, 1000)
        load_ui_from_name("pdfwindow.ui", self)


app = QApplication(sys.argv)
pdfwindow = PDFWindow()
pdfwindow.show()
app.exec()
