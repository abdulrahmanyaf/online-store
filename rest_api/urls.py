from django.urls import path

from rest_api.views import ProductCategoryListView, ProductListView, ProductDetailsView, ProductCategoryDetailsView, \
    ProductCategoryCreateView, ProductCategoryUpdateView

app_name = 'rest_api'

urlpatterns = [
    path('product-categories', ProductCategoryListView.as_view(), name='product_category_list'),
    path('product-categories/create', ProductCategoryCreateView.as_view(), name='product_category_create'),
    path('product-categories/<int:pk>', ProductCategoryDetailsView.as_view(), name='product_category_details'),
    path('product-categories/<int:pk>/update', ProductCategoryUpdateView.as_view(), name='product_category_update'),
    path('products', ProductListView.as_view(), name='product_list'),
    path('products/<int:pk>', ProductDetailsView.as_view(), name='product_details'),
]
