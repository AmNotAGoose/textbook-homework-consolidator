import logging
from math import trunc

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QGraphicsScene, QPushButton, QLineEdit


from app.pdf_model import PDFModel
from storage.storage import upsert_q_or_a_image_by_rect_to_cache
from ui.selectable_graphics_view import SelectableGraphicsView

logger = logging.getLogger(__name__)


class GraphicsWidget:
    def __init__(self,
                 pdf_path: str,
                 graphicsView: SelectableGraphicsView,
                 leOffset: QLineEdit,
                 lePage: QLineEdit,
                 btnPrev: QPushButton,
                 btnNext: QPushButton,
                 btnClear: QPushButton):
        self.pdf_model = PDFModel(pdf_path)

        self.graphicsView = graphicsView
        self.leOffset = leOffset
        self.lePage = lePage
        self.btnPrev = btnPrev
        self.btnNext = btnNext
        self.btnClear = btnClear

        self.scene = QGraphicsScene()
        self.graphicsView.setScene(self.scene)
        self.display_current_page()

        self.selected_rect = None

        self.graphicsView.region_selected.connect(self._on_region_selected)
        self.btnPrev.clicked.connect(lambda : self._on_flip_page(forward=False))
        self.btnNext.clicked.connect(lambda : self._on_flip_page(forward=True))
        self.btnClear.clicked.connect(self.graphicsView.clear_selection)
        self.lePage.editingFinished.connect(self._on_flip_to_page)

    def display_current_page(self):
        path = self.pdf_model.get_current_page_image_path()
        pixmap = QPixmap(str(path))

        self.scene.clear()
        self.scene.addPixmap(pixmap)
        self.scene.setSceneRect(pixmap.rect().toRectF())
        self.fit_view()

        self.lePage.setText(str(self.pdf_model.get_current_page_number()))

    def fit_view(self):
        self.graphicsView.fitInView(self.scene.sceneRect(), Qt.KeepAspectRatio)

    def _on_region_selected(self, rect):
        self.selected_rect = rect

    def _on_flip_page(self, forward):
        self.pdf_model.flip_page(forward=forward)
        self.display_current_page()

    def _on_flip_to_page(self):
        page_number = self.lePage.text()

        if not page_number.isnumeric(): return

        page_number = int(page_number)

        self.pdf_model.flip_to_page(page_number)
        self.display_current_page()
