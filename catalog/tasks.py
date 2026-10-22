from celery import shared_task
from celery.utils.log import get_task_logger

from .models import ProductImage

logger = get_task_logger(__name__)


@shared_task
def log_product_images_count():
    count = ProductImage.objects.count()
    logger.info("ProductImage records count: %s", count)
    return count