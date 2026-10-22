import os

from celery import shared_task
from celery.utils.log import get_task_logger
from django.conf import settings
from django.db.models import Count, Q

from .models import ProductImage

logger = get_task_logger(__name__)


def count_files_in_media_root():
    """Рахує лише файли безпосередньо в MEDIA_ROOT, без вкладених тек."""
    media_root = str(settings.MEDIA_ROOT)
    if not os.path.isdir(media_root):
        logger.warning("MEDIA_ROOT does not exist: %s", media_root)
        return None

    with os.scandir(media_root) as entries:
        return sum(1 for entry in entries if entry.is_file())


@shared_task
def log_product_images_count():
    stats = ProductImage.objects.aggregate(
        total=Count("id"),
        remote=Count("id", filter=Q(image__istartswith="http")),
    )
    total = stats["total"]
    remote = stats["remote"]
    local = total - remote

    files_in_media = count_files_in_media_root()

    logger.info(
        "ProductImage records: total=%s, local=%s, remote=%s | files in media root: %s",
        total, local, remote, files_in_media,
    )
    return {
        "total": total,
        "local": local,
        "remote": remote,
        "files_in_media": files_in_media,
    }