from django.contrib import admin
from products.models import *
# Register your models here.

admin.site.register(ProductCategory)
admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShoppingSession)
admin.site.register(CartItem)
