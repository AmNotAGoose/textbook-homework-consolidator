from PySide6.QtWidgets import QGraphicsView, QGraphicsRectItem
from PySide6.QtGui import QPen, QColor
from PySide6.QtCore import QRectF, QPointF, Signal
from PySide6.QtCore import Qt

class SelectableGraphicsView(QGraphicsView):
    region_selected = Signal(QRectF)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._drag_start: QPointF | None = None
        self._rect_item: QGraphicsRectItem | None = None
        self._selection_pen = QPen(QColor(0, 100, 100), 2)
        self._selection_pen.setCosmetic(True)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._drag_start = self.mapToScene(event.pos())
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self._drag_start is not None:
            current = self.mapToScene(event.pos())
            rect = QRectF(self._drag_start, current).normalized()
            self.update_rect(rect)

        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton and self._drag_start is not None:
            current = self.mapToScene(event.pos())
            final_rect = QRectF(self._drag_start, current).normalized()
            self.region_selected.emit(final_rect)
            self._drag_start = None

        super().mouseReleaseEvent(event)

    def clear_selection(self):
        if self._rect_item is not None:
            if self.scene():
                self.scene().removeItem(self._rect_item)
            self._rect_item = None

    def update_rect(self, rect: QRectF):
        try:
            if self._rect_item is None:
                self._rect_item = self.scene().addRect(rect, self._selection_pen)
            else:
                self._rect_item.setRect(rect)
        except RuntimeError:
            self._rect_item = self.scene().addRect(rect, self._selection_pen)