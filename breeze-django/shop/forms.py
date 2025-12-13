from django import forms
from .models import News

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