from django.db import models
from django.dispatch import receiver

from online_store.utils import delete_file
from products.models import ProductImage


@receiver(models.signals.post_delete, sender=ProductImage)
def delete_product_image_file(sender, instance, *args, **kwargs):
    if instance.file:
        delete_file(instance.file.path)