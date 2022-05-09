from django import forms
from django.forms import ModelForm
from .models import Category, Product, Comment


class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = ('category_name', 'image',)
        labels = {
            'category_name': '',
            'image': '',
        }
        widgets = {
            'category_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Category Name'}),
        }


class ProductForm(ModelForm):
    # category = forms.ModelMultipleChoiceField(queryset=Category.objects.all())

    class Meta:
        # category = Category.objects.all().values_list()
        # new_list = [i[1] for i in category]
        # category = forms.MultipleChoiceField(choices=new_list)
        model = Product
        fields = ['product_name', 'category']
        labels = {
            'product_name': '',
            'category': 'Category Name',
        }
        widgets = {
            'product_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Product Name'}),
            # 'category': forms.Select(attrs={'class': 'form-select', 'placeholder': 'Category'}),
            'category': forms.SelectMultiple(attrs={'class': 'form-select-multiple', 'placeholder': 'Category'}),
            # 'category': forms.ModelMultipleChoiceField(queryset=Category.objects.all()),
        }


class ProductFormFull(ProductForm):
    images = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False)

    class Meta(ProductForm.Meta):
        labels = ProductForm.Meta.labels
        labels['images'] = ''
        fields = ProductForm.Meta.fields + ['images']
        widgets = ProductForm.Meta.widgets


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['comment', 'user', 'product']
        labels = {
            'comment': '',
            'user': '',
            'product': ','
        }
        widgets = {
            'comment': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Comment'}),
        }
