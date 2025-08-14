from django import forms
from .models import Product, Category

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['category', 'name', 'description', 'price', 'image', 'stock']
        widgets = {
            'description': forms.Textarea(attrs={'rows':4}),
        }
