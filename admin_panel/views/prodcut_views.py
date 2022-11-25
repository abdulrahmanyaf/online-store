from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.db import transaction
from django.db.models import Sum, Count
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, CreateView, DeleteView
from django.utils.translation import gettext as _

from products.forms import ProductForm, SpecificationFormset, ProductImageFormset
from products.models import Product, ProductImage


class ProductListView(ListView):
    model = Product
    template_name = 'admin_panel/products/product_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        return super().get_queryset().annotate(order_sum=Sum('orders__quantity', distinct=True, default=0),
                                               cart_items_count=Count("cart_items", distinct=True))


class ProductBaseFormMixin:
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('admin_panel:product_list')
    formsets_prefixes = ('specification_en_formset', 'specification_ar_formset', 'product_image_formset')

    def get_specification_formset(self, formset_prefix, initial=None):
        kwargs = {
            'data': self.request.POST if self.request.method in ("POST", "PUT") else None,
            'prefix': formset_prefix,
            'initial': initial
        }
        return SpecificationFormset(**kwargs)

    def get_specification_en_formset(self):
        return self.get_specification_formset(
            formset_prefix="specification_en_formset",
            initial=self.object.specifications_en if self.object else None
        )

    def get_specification_ar_formset(self):
        return self.get_specification_formset(
            formset_prefix="specification_ar_formset",
            initial=self.object.specifications_ar if self.object else None
        )

    def get_product_image_formset(self):
        kwargs = {
            "prefix": 'product_image_formset',
            "queryset": self.object.product_images.all() if self.object else ProductImage.objects.none(),
            "form_kwargs": {'updated_by': self.request.user, 'product': self.object},
        }
        if self.request.method in ("POST", "PUT"):
            kwargs.update({
                "data": self.request.POST,
                'files': self.request.FILES
            })
        return ProductImageFormset(**kwargs)

    def get_formsets(self):
        return {formset_prefix: getattr(self, f"get_{formset_prefix}")() for formset_prefix in self.formsets_prefixes}

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['updated_by'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        for formset_prefix, formset in self.get_formsets().items():
            if formset_prefix not in kwargs:
                kwargs[formset_prefix] = formset
        return super().get_context_data(**kwargs)

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        formsets = self.get_formsets()
        if form.is_valid() and all((formset.is_valid() for formset in formsets.values())):
            return self.forms_valid(form, **formsets)
        else:
            return self.forms_invalid(form, **formsets)

    def forms_valid(self, form, **kwargs):
        self.object = form.save(commit=False)
        self.object.specifications_en = kwargs['specification_en_formset'].needed_data
        self.object.specifications_ar = kwargs['specification_ar_formset'].needed_data
        with transaction.atomic():
            self.object.save()
            self.save_product_images(kwargs['product_image_formset'])
        messages.success(self.request, self.success_message)
        return HttpResponseRedirect(self.get_success_url())

    def save_product_images(self, product_image_formset):
        product_image_formset.save()

    def forms_invalid(self, form, specification_en_formset, specification_ar_formset, product_image_formset):
        return self.render_to_response(
            self.get_context_data(
                form=form,
                specification_en_formset=specification_en_formset,
                specification_ar_formset=specification_ar_formset,
                product_image_formset=product_image_formset
            ))


class ProductCreateView(SuccessMessageMixin, ProductBaseFormMixin, CreateView):
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


class ProductUpdateView(ProductBaseFormMixin, UpdateView):
    template_name = 'admin_panel/products/product_update.html'
    context_object_name = 'product'
    success_message = _('Product was updated successfully')

    def get_queryset(self):
        return super().get_queryset().prefetch_related('product_images')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy('admin_panel:product_list')
    success_message = _('Product was deleted successfully')

    def get_queryset(self):
        return super().get_queryset().annotate(order_sum=Sum('orders__quantity', distinct=True),
                                               cart_items_count=Count("cart_items", distinct=True))

    def delete(self, request, *args, **kwargs):
        product_category = self.get_object()
        if product_category.product_count != 0 or product_category.cart_items_count != 0:
            return HttpResponseBadRequest()
        response = super().delete(request, *args, **kwargs)
        messages.success(request, self.success_message)
        return response
