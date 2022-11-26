from django.db import models


class WebService(models.Model):
    class Meta:
        managed = False
        permissions = (
            ('can_access_product_category', 'Can access product categories'),
            ('can_create_product_category', 'Can create product categories'),
            ('can_update_product_category', 'Can update product categories'),
            ('can_access_product', 'Can access products'),
        )

