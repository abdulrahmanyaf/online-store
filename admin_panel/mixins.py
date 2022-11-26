from django.contrib import messages
from django.contrib.auth.mixins import AccessMixin, LoginRequiredMixin
from django.db import transaction
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy

from products.forms import ProductForm, SpecificationFormset, ProductImageFormset
from products.models import Product, ProductImage


class SystemAdminAccessMixinImplementation(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_system_admin:
            return super().dispatch(request, *args, **kwargs)
        return self.handle_no_permission()


class SystemAdminAccessMixin(LoginRequiredMixin, SystemAdminAccessMixinImplementation):
    pass


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
