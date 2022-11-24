from django.urls import path

from admin_panel.views import ProductCategoryListView, ProductCategoryUpdateView, ProductCategoryCreateView, \
    ProductCategoryDeleteView

app_name = 'admin_panel'
urlpatterns = [
    path('product-categories/', ProductCategoryListView.as_view(), name='product_category_list'),
    path('product-categories/create', ProductCategoryCreateView.as_view(), name='product_category_create'),
    path('product-categories/<int:pk>/update/', ProductCategoryUpdateView.as_view(), name='product_category_update'),
    path('product-categories/<int:pk>/delete/', ProductCategoryDeleteView.as_view(), name='product_category_delete'),
]