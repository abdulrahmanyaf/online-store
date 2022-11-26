from django.contrib import messages
from django.db.models import Count
from django.http import HttpResponseBadRequest
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, CreateView
from django.utils.translation import gettext as _

from admin_panel.mixins import SystemAdminAccessMixin
from admin_panel.views.base import DeleteView
from products.forms import ProductCategoryForm
from products.models import ProductCategory


# Create your views here.

class ProductCategoryListView(SystemAdminAccessMixin, ListView):
    model = ProductCategory
    template_name = 'admin_panel/product_categories/product_categories_list.html'
    context_object_name = 'product_categories'

    def get_queryset(self):
        return super().get_queryset().annotate(products_count=Count('products'))


class ProductCategoryCreateView(SystemAdminAccessMixin, CreateView):
    model = ProductCategory
    form_class = ProductCategoryForm
    template_name = 'admin_panel/product_categories/product_category_create.html'
    success_url = reverse_lazy('admin_panel:product_category_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['updated_by'] = self.request.user
        return kwargs


class ProductCategoryUpdateView(SystemAdminAccessMixin, UpdateView):
    model = ProductCategory
    form_class = ProductCategoryForm
    template_name = 'admin_panel/product_categories/product_category_update.html'
    success_url = reverse_lazy('admin_panel:product_category_list')
    context_object_name = 'product_category'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['updated_by'] = self.request.user
        return kwargs


class ProductCategoryDeleteView(SystemAdminAccessMixin, DeleteView):
    model = ProductCategory
    success_url = reverse_lazy('admin_panel:product_category_list')

    def get_queryset(self):
        return super().get_queryset().annotate(product_count=Count('products'))

    def delete(self, request, *args, **kwargs):
        product_category = self.get_object()
        if product_category.product_count != 0:
            return HttpResponseBadRequest()
        response = super().delete(request, *args, **kwargs)
        messages.success(request, _('Product category is deleted successfully'))
        return response






