from django.urls import path

from admin_panel.views.prodcut_views import ProductListView, ProductCreateView, ProductUpdateView, ProductDeleteView
from admin_panel.views.product_category_views import ProductCategoryListView, ProductCategoryCreateView, \
    ProductCategoryUpdateView, ProductCategoryDeleteView

app_name = 'admin_panel'

urlpatterns = [
    path('product-categories/', ProductCategoryListView.as_view(), name='product_category_list'),
    path('product-categories/create', ProductCategoryCreateView.as_view(), name='product_category_create'),
    path('product-categories/<int:pk>/update/', ProductCategoryUpdateView.as_view(), name='product_category_update'),
    path('product-categories/<int:pk>/delete/', ProductCategoryDeleteView.as_view(), name='product_category_delete'),

    path('products/', ProductListView.as_view(), name='product_list'),
    path('products/create', ProductCreateView.as_view(), name='product_create'),
    path('products/<int:pk>/update/', ProductUpdateView.as_view(), name='product_update'),
    path('products/<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),
]
