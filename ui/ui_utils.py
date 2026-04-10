from pathlib import Path

from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile

from ui.selectable_graphics_view import SelectableGraphicsView

BASE_DIR = Path(__file__).parent

def load_ui_from_name(name, self):
    path = get_ui_filepath(name)

    loader = QUiLoader()
    loader.registerCustomWidget(SelectableGraphicsView)

    ui_file = QFile(path)
    ui = loader.load(ui_file, self)
    ui_file.close()

    return ui

def get_ui_filepath(name):
    return BASE_DIR / "widgets" / name
