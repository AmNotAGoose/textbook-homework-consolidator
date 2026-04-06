from pathlib import Path

from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile


BASE_DIR = Path(__file__).parent

def load_ui_from_name(name, self):
    path = get_ui_filepath(name)

    loader = QUiLoader()

    ui_file = QFile(path)
    ui = loader.load(ui_file, self)
    ui_file.close()

    return ui

def get_ui_filepath(name):
    return BASE_DIR / "widgets" / name
