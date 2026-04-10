import fitz
import hashlib
from pathlib import Path

from storage.storage import upsert_page_image_to_cache


class PDFModel:
    def __init__(self, document_path):
        self.document = fitz.open(document_path)
        self.document_path = document_path
        self.page_count = self.document.page_count
        self.page_idx = 0
        self.page_offset = 0

        self.document_id = self.get_document_id()

    def get_document_id(self):
        with open(self.document_path, "rb") as f:
            return hashlib.md5(f.read(65536)).hexdigest()

    def get_current_page_number(self):
        return self.page_idx + 1

    def get_current_page_image_path(self):
        image = upsert_page_image_to_cache(self.document_id, self.page_idx, self.get_current_page())
        return image

    def get_current_page(self):
        return self.document[self.page_idx]

    def flip_page(self, forward=True):
        if self.page_count <= 1: return

        if forward:
            self.page_idx += 1
        else:
            self.page_idx -= 1

        self.page_idx = self.page_idx % self.page_count

    def flip_to_page(self, page_number):
        page_idx = page_number - 1
        if 0 <= page_idx < self.document.page_count:
            self.page_idx = page_idx
