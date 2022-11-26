from django.contrib import messages
from django.db.models import Sum, Count
from django.http import HttpResponseBadRequest
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, CreateView
from django.utils.translation import gettext as _

from admin_panel.mixins import SystemAdminAccessMixin, ProductBaseFormMixin
from admin_panel.views.base import DeleteView
from products.models import Product, ProductImage


class ProductListView(SystemAdminAccessMixin, ListView):
    model = Product
    template_name = 'admin_panel/products/product_list.html'
    context_object_name = 'products'
    paginate_by = 10

    def get_queryset(self):
        return super().get_queryset().annotate(order_sum=Sum('orders__quantity', distinct=True, default=0),
                                               cart_items_count=Count("cart_items", distinct=True))


class ProductCreateView(SystemAdminAccessMixin, ProductBaseFormMixin, CreateView):
    template_name = 'admin_panel/products/product_create.html'
    success_message = _('Product was created successfully')

    def post(self, request, *args, **kwargs):
        self.object = None
        return super().post(request, *args, **kwargs)

    def save_product_images(self, product_image_formset):
        product_images = product_image_formset.save(commit=False)
        for product_image in product_images:
            product_image.product = self.object
        ProductImage.objects.bulk_create(product_images, update_fields='file', unique_fields='id')


class ProductUpdateView(SystemAdminAccessMixin, ProductBaseFormMixin, UpdateView):
    template_name = 'admin_panel/products/product_update.html'
    context_object_name = 'product'
    success_message = _('Product was updated successfully')

    def get_queryset(self):
        return super().get_queryset().prefetch_related('product_images')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)


class ProductDeleteView(SystemAdminAccessMixin, DeleteView):
    model = Product
    success_url = reverse_lazy('admin_panel:product_list')
    success_message = _('Product was deleted successfully')

    def get_queryset(self):
        return super().get_queryset().annotate(order_sum=Sum('orders__quantity', distinct=True, default=0),
                                               cart_items_count=Count("cart_items", distinct=True))

    def delete(self, request, *args, **kwargs):
        product = self.get_object()
        if product.order_sum != 0 or product.cart_items_count != 0:
            return HttpResponseBadRequest()
        response = super().delete(request, *args, **kwargs)
        messages.success(request, self.success_message)
        return response
