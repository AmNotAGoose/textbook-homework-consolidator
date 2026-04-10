import sys
import logging

from PySide6.QtWidgets import QApplication
from ui.pdf_window import PDFWindow

logger = logging.getLogger(__name__)

app = QApplication(sys.argv)
pdfwindow = PDFWindow()
pdfwindow.show()
app.exec()
