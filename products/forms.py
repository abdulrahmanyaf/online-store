from django import forms

from products.models import Product, ProductCategory


class ProductCategoryForm(forms.ModelForm):
    class Meta:
        model = ProductCategory
        fields = ['title_en', 'title_ar', 'description_en', 'description_ar']

    def __init__(self, *args, **kwargs):
        self.updated_by = kwargs.pop('updated_by')
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        if not self.instance.pk:
            self.instance.created_by = self.updated_by
        self.instance.updated_by = self.updated_by
        return super().save(commit)


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['category', 'title_en', 'title_ar', 'model_number', 'description_en', 'description_ar', 'quantity',
                  'price']

    def __init__(self, *args, **kwargs):
        self.updated_by = kwargs.pop('updated_by')
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        if not self.instance.pk:
            self.instance.created_by = self.updated_by
        self.instance.updated_by = self.updated_by
        return super().save(commit)


class SpecificationForm(forms.Form):
    name = forms.CharField(max_length=128, required=True)
    value = forms.CharField(max_length=128, required=True)


class SpecificationFormset(forms.BaseFormSet):
    @property
    def needed_forms(self):
        if self.can_delete:
            return [form for form in self.forms if not self._should_delete_form(form)]
        return self.forms

    @property
    def needed_data(self):
        return [{'name': form.cleaned_data['name'], 'value': form.cleaned_data['value']} for form in self.needed_forms]


SpecificationFormset = forms.formset_factory(form=SpecificationForm, formset=SpecificationFormset, extra=0, can_delete=True)
