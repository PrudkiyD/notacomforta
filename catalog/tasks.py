import os

from celery import shared_task
from celery.utils.log import get_task_logger
from django.conf import settings
from django.db.models import Count, Q

from .models import ProductImage

logger = get_task_logger(__name__)


def scan_media_root():
    """Файли безпосередньо в MEDIA_ROOT (без вкладених тек): {ім'я: розмір}."""
    media_root = str(settings.MEDIA_ROOT)
    if not os.path.isdir(media_root):
        logger.warning("MEDIA_ROOT does not exist: %s", media_root)
        return None

    files = {}
    with os.scandir(media_root) as entries:
        for entry in entries:
            if entry.is_file():
                files[entry.name] = entry.stat().st_size
    return files


def get_local_image_names():
    """Множина шляхів локальних зображень з БД (без http-записів)."""
    names = (
        ProductImage.objects
        .exclude(image__istartswith="http")
        .values_list("image", flat=True)
        .iterator(chunk_size=5000)
    )
    return {name.lstrip("/") for name in names if name}


@shared_task
def log_product_images_count():
    stats = ProductImage.objects.aggregate(
        total=Count("id"),
        remote=Count("id", filter=Q(image__istartswith="http")),
    )
    total = stats["total"]
    remote = stats["remote"]
    local = total - remote

    files = scan_media_root()
    files_in_media = len(files) if files is not None else None

    orphans_count = None
    orphans_size_mb = None
    if files is not None:
        db_names = get_local_image_names()
        orphans = [name for name in files if name not in db_names]
        orphans_count = len(orphans)
        orphans_size_mb = round(sum(files[n] for n in orphans) / 1024 / 1024, 1)
        if orphans:
            logger.info("Orphan files sample: %s", orphans[:5])

    logger.info(
        "ProductImage records: total=%s, local=%s, remote=%s | files in media root: %s "
        "| orphans (not in DB): %s (%s MB)",
        total, local, remote, files_in_media, orphans_count, orphans_size_mb,
    )
    return {
        "total": total,
        "local": local,
        "remote": remote,
        "files_in_media": files_in_media,
        "orphans": orphans_count,
        "orphans_size_mb": orphans_size_mb,
    }