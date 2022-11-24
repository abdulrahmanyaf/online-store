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



