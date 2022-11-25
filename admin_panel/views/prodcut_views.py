from django.core.checks import messages
from django.db.models import Sum, Count
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, CreateView, DeleteView
from django.utils.translation import gettext as _

from products.forms import ProductForm, SpecificationFormset
from products.models import Product


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

    def get_specification_formset(self, formset_prefix, initial=None):
        return SpecificationFormset(
            data=self.request.POST if self.request.method in ("POST", "PUT") else None,
            prefix=formset_prefix,
            initial=initial
        )

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

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['updated_by'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        if "specification_en_formset" not in kwargs:
            kwargs["specification_en_formset"] = self.get_specification_en_formset()
        if "specification_ar_formset" not in kwargs:
            kwargs["specification_ar_formset"] = self.get_specification_ar_formset()
        context = super().get_context_data(**kwargs)
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        specification_en_formset = self.get_specification_en_formset()
        specification_ar_formset = self.get_specification_ar_formset()
        if form.is_valid() and specification_en_formset.is_valid() and specification_ar_formset.is_valid():
            return self.forms_valid(form, specification_en_formset, specification_ar_formset)
        else:
            return self.forms_invalid(form, specification_en_formset, specification_ar_formset)

    def forms_valid(self, form, specification_en_formset, specification_ar_formset):
        self.object = form.save(commit=False)
        self.object.specifications_en = specification_en_formset.needed_data
        self.object.specifications_ar = specification_ar_formset.needed_data
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def forms_invalid(self, form, specification_en_formset, specification_ar_formset):
        return self.render_to_response(
            self.get_context_data(form=form, specification_en_formset=specification_en_formset,
                                  specification_ar_formset=specification_ar_formset))


class ProductCreateView(ProductBaseFormMixin, CreateView):
    template_name = 'admin_panel/products/product_create.html'


class ProductUpdateView(ProductBaseFormMixin, UpdateView):
    template_name = 'admin_panel/products/product_update.html'
    context_object_name = 'product'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)




class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy('admin_panel:product_list')

    def get_queryset(self):
        return super().get_queryset().annotate(order_sum=Sum('orders__quantity', distinct=True),
                                               cart_items_count=Count("cart_items", distinct=True))

    def delete(self, request, *args, **kwargs):
        product_category = self.get_object()
        if product_category.product_count != 0 or product_category.cart_items_count != 0:
            return HttpResponseBadRequest()
        response = super().delete(request, *args, **kwargs)
        messages.success(request, _('Product is deleted successfully'))
        return response
