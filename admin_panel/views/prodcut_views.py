from django.core.checks import messages
from django.db.models import Sum, Count
from django.http import HttpResponseBadRequest
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, CreateView, DeleteView
from django.utils.translation import gettext as _

from admin_panel.forms import ProductForm
from products.models import Product


class ProductListView(ListView):
    model = Product
    template_name = 'admin_panel/products/product_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        return super().get_queryset().annotate(order_sum=Sum('orders__quantity', distinct=True, default=0),
                                               cart_items_count=Count("cart_items", distinct=True))


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'admin_panel/products/product_create.html'
    success_url = reverse_lazy('admin_panel:product_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['updated_by'] = self.request.user
        return kwargs


class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'admin_panel/products/product_update.html'
    success_url = reverse_lazy('admin_panel:product_list')
    context_object_name = 'product'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['updated_by'] = self.request.user
        return kwargs


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy('admin_panel:product_list')

    def get_queryset(self):
        return super().get_queryset().annotate(order_sum=Sum('orders__quantity', distinct=True),
                                               cart_items_count=Count("cart_items", distinct=True))

    def delete(self, request, *args, **kwargs):
        product_category = self.get_object()
        if product_category.product_count != 0 or product_category.cart_items_count !=0:
            return HttpResponseBadRequest()
        response = super().delete(request, *args, **kwargs)
        messages.success(request, _('Product is deleted successfully'))
        return response
