from django import forms
from .models import News, Product

class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['title', 'slug', 'content', 'image', 'published_at']
        widgets = {
            'published_at': forms.DateInput(attrs={'type': 'date'}),
            'title': forms.TextInput(attrs={
                'class': 'input news-title-input',
                'style': 'width: 100%; height: 48px;',
                'placeholder': 'Введите заголовок новости'
            }),
            'slug': forms.TextInput(attrs={
                'class': 'input',
                'style': 'width: 100%; height: 48px;',
                'placeholder': 'Slug'
            }),
            'content': forms.Textarea(attrs={
                'class': 'input news-form__content',
                'placeholder': 'Введите текст новости',
                'rows': 10,
                'style': 'width: 100%; resize: vertical;',
            }),
        }

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'slug', 'category', 'price', 'image', 'description', 'in_stock']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'input', 'style': 'width:100%; max-width:600px;', 'placeholder': 'Заголовок'}),
            'price': forms.NumberInput(attrs={'class': 'input', 'step': '0.01', 'placeholder': 'Цена'}),
            'slug': forms.TextInput(attrs={
                'class': 'input',
                'style': 'width: 100%; height: 48px;',
                'placeholder': 'Slug'
            }),
            'description': forms.Textarea(attrs={'class': 'input', 'rows': 8, 'style': 'width:100%; max-width:800px;', 'placeholder': 'Описание'}),
            'category': forms.Select(attrs={'class': 'select'}),
            'in_stock': forms.CheckboxInput(),
        }