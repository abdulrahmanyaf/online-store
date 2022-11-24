from django.conf import settings
from django.db import models
from django.db.models import TextChoices
from django_fsm import FSMField


# Create your models here.

class ProductCategory(models.Model):
    title_ar = models.CharField(max_length=256)
    title_en = models.CharField(max_length=256, null=True, blank=True)
    description_ar = models.TextField()
    description_en = models.TextField(null=True, blank=True)

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT,
                                   related_name='categories_created')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title_ar


class Product(models.Model):
    category = models.ForeignKey(ProductCategory, on_delete=models.RESTRICT, related_name='products')
    title_ar = models.CharField(max_length=256)
    title_en = models.CharField(max_length=256, null=True, blank=True)
    model_number = models.CharField(max_length=256)
    description_ar = models.TextField()
    description_en = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    specifications_ar = models.JSONField(null=True, blank=True)
    specifications_en = models.JSONField(null=True, blank=True)

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, related_name='products_created')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title_ar


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    file = models.ImageField(upload_to='products-images/')

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT,
                                   related_name='products_images_created')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.file.name} for {self.product.title_ar} product"


class Order(models.Model):
    class Status(TextChoices):
        AWAITING_SHIPMENT = 'awaiting_shipment', 'Awaiting Shipment'
        SHIPPED = 'shipped', 'Shipped'
        CANCELED = 'canceled', 'Canceled'
        REFUNDED = 'refunded', 'Refunded'

    status = FSMField(default=Status.AWAITING_SHIPMENT, choices=Status.choices)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, related_name='orders')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Created by {self.created_by} at {self.created_at}"

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.RESTRICT)
    order = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_items')
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"Ordered {self.quantity} units from {self.product.title_ar}"


class ShoppingSession(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, related_name='shopping_session')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Created by {self.user} at {self.created_at}"


class CartItem(models.Model):
    shopping_session = models.ForeignKey(ShoppingSession, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.RESTRICT)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.quantity} units from {self.product.title_ar}"