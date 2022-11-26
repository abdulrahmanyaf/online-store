from rest_framework import serializers

from products.models import ProductCategory, Product


class ProductCategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ['id', 'title_en', 'title_ar']


class ProductCategoryDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ['id', 'title_en', 'title_ar', 'description_en', 'description_ar']


class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title_en', 'title_ar', 'model_number', 'quantity', 'price']


class ProductDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title_en', 'title_ar', 'model_number', 'description_en', 'description_ar', 'quantity', 'price',
                  'specifications_en', 'specifications_ar']
