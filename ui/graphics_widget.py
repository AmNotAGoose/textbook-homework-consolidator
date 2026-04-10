import logging

from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QGraphicsScene

from app.pdf_model import PDFModel
from storage.storage import upsert_q_or_a_image_by_rect_to_cache

logger = logging.getLogger(__name__)


class GraphicsWidget:
    def __init__(self, pdf_path, graphicsView, leOffset, lePage, btnPrev, btnNext, btnClear):
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

    def display_current_page(self):
        path = self.pdf_model.get_current_page_image_path()
        pixmap = QPixmap(str(path))

        self.scene.clear()
        self.scene.addPixmap(pixmap)
        self.scene.setSceneRect(pixmap.rect().toRectF())
        self.fit_view()

    def fit_view(self):
        self.graphicsView.fitInView(self.scene.sceneRect(), Qt.KeepAspectRatio)

    def _on_region_selected(self, rect):
        self.selected_rect = rect
