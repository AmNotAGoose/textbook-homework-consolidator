from pathlib import Path


BASE_CACHE_PATH = Path(__file__).parent / "cache"
BASE_CACHE_PATH.mkdir(exist_ok=True)

def upsert_page_image_to_cache(page, page_idx, document_id):
    pixmap = page.get_pixmap(dpi=400)

    path = BASE_CACHE_PATH / f"{document_id}-{page_idx}.jpg"

    if not path.exists():
        pixmap.save(path, "jpg")

    return path
