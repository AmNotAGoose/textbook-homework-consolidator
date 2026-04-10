from pathlib import Path

import fitz

BASE_CACHE_PATH = Path(__file__).parent / "cache"
BASE_CACHE_PATH.mkdir(exist_ok=True)

def _upsert_image(pixmap, document_id, name_with_ext):
    (BASE_CACHE_PATH / document_id).mkdir(exist_ok=True)

    path = BASE_CACHE_PATH / document_id / name_with_ext

    if not path.exists():
        pixmap.save(path, "jpg")

    return path

def upsert_page_image_to_cache(document_id, page_idx, page):
    pixmap = page.get_pixmap(dpi=300)
    file_name = f"{page_idx}.jpg"

    return _upsert_image(pixmap, document_id, file_name)

def upsert_q_or_a_image_by_rect_to_cache(document_id, page_idx, page, rect):
    fitz_rect = fitz.Rect(rect.x(), rect.y(), rect.right(), rect.bottom())
    pixmap = page.get_pixmap(dpi=300, clip=fitz_rect)
    file_name = f"{page_idx}_{rect.x():.0f}_{rect.y():.0f}_{rect.right():.0f}_{rect.bottom():.0f}.jpg"

    return _upsert_image(pixmap, document_id, file_name)

