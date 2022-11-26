from rest_framework import generics
from rest_framework.renderers import JSONRenderer

from products.models import ProductCategory, Product
from rest_api.permissions import APIPermissionBaseView
from rest_api.serializers import ProductDetailsSerializer, ProductListSerializer, ProductCategoryListSerializer, \
    ProductCategoryDetailsSerializer


class BaseAPIMixin:
    permission = APIPermissionBaseView
    endpoint_permission = None

    def __init__(self):
        super().__init__()
        self.set_permission()
        self.set_renderer()

    def set_permission(self):
        if self.endpoint_permission:
            self.permission = APIPermissionBaseView
            self.permission.endpoint_permission = self.endpoint_permission
            self.permission_classes = (self.permission,)

    def set_renderer(self):
        self.renderer_classes = (JSONRenderer,)


class ProductCategoryListView(BaseAPIMixin, generics.ListAPIView):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategoryListSerializer
    endpoint_permission = 'rest_api.can_access_product_category'


class ProductCategoryDetailsView(BaseAPIMixin, generics.RetrieveAPIView):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategoryDetailsSerializer
    endpoint_permission = 'rest_api.can_access_product_category'


class ProductCategoryCreateView(BaseAPIMixin, generics.CreateAPIView):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategoryDetailsSerializer
    endpoint_permission = 'rest_api.can_create_product_category'

    def perform_create(self, serializer):
        kwargs = {
            'created_by': self.request.user,
            'updated_by': self.request.user,
        }
        serializer.save(**kwargs)


class ProductCategoryUpdateView(BaseAPIMixin, generics.UpdateAPIView):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategoryDetailsSerializer
    endpoint_permission = 'rest_api.can_update_product_category'

    def perform_update(self, serializer):
        kwargs = {
            'updated_by': self.request.user,
        }
        serializer.save(**kwargs)


class ProductListView(BaseAPIMixin, generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer
    endpoint_permission = 'rest_api.can_access_product'


class ProductDetailsView(BaseAPIMixin, generics.RetrieveAPIView,):
    queryset = Product
    serializer_class = ProductDetailsSerializer
    endpoint_permission = 'rest_api.can_access_product'
