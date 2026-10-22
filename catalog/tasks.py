from celery import shared_task
from celery.utils.log import get_task_logger
from django.db.models import Count, Q

from .models import ProductImage

logger = get_task_logger(__name__)


@shared_task
def log_product_images_count():
    stats = ProductImage.objects.aggregate(
        total=Count("id"),
        remote=Count("id", filter=Q(image__istartswith="http")),
    )
    total = stats["total"]
    remote = stats["remote"]
    local = total - remote

    logger.info(
        "ProductImage records: total=%s, local=%s, remote=%s",
        total, local, remote,
    )
    return {"total": total, "local": local, "remote": remote}