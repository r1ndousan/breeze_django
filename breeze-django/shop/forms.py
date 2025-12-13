from django import forms
from .models import News

class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['title', 'slug', 'content', 'image', 'published_at']
        widgets = {
            'published_at': forms.DateInput(attrs={'type': 'date'}),
        }