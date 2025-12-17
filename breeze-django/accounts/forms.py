# accounts/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, label="E-mail")
    first_name = forms.CharField(required=True, label="Имя")

    class Meta:
        model = User
        # Если в проекте логин выполняется по email — можешь убрать 'username' и заменить логику
        fields = ("username", "email", "password1", "password2")

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if email and User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Пользователь с таким email уже существует.")
        return email

class LoginForm(forms.Form):
    username_or_email = forms.CharField(label='E-mail или имя', max_length=150)
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)