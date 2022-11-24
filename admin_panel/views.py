from django.contrib import messages
from django.db.models import Count
from django.http import HttpResponseBadRequest
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, UpdateView, CreateView, DeleteView
from django.utils.translation import gettext as _

from products.models import ProductCategory


# Create your views here.

class ProductCategoryListView(ListView):
    model = ProductCategory
    template_name = 'admin_panel/product_categories/product_categories_list.html'
    context_object_name = 'product_categories'

    def get_queryset(self):
        return super().get_queryset().annotate(products_count=Count('products'))


class ProductCategoryUpdateView(UpdateView):
    model = ProductCategory
    fields = ['title_en', 'title_ar', 'description_en', 'description_ar']
    template_name = 'admin_panel/product_categories/product_category_update.html'
    success_url = reverse_lazy('admin_panel:product_category_list')
    context_object_name = 'product_category'


class ProductCategoryCreateView(CreateView):
    model = ProductCategory
    fields = ['title_en', 'title_ar', 'description_en', 'description_ar']
    template_name = 'admin_panel/product_categories/product_category_create.html'
    success_url = reverse_lazy('admin_panel:product_category_list')


class ProductCategoryDeleteView(DeleteView):
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




