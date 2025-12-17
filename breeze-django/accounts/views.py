# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from django.contrib import messages
from .forms import LoginForm, RegisterForm
from django.contrib.auth.decorators import login_required
from accounts.models import Profile
from django.db import transaction
from django.contrib.auth import logout

def login_view(request):
    error = None
    form = LoginForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        identifier = form.cleaned_data['username_or_email'].strip()
        password = form.cleaned_data['password']

        username = None
        # если это email — найдём пользователя по email и возьмём username
        if '@' in identifier:
            try:
                user_obj = User.objects.get(email__iexact=identifier)
                username = user_obj.get_username()
            except User.DoesNotExist:
                username = None
        else:
            username = identifier

        user = None
        if username:
            user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('shop:index')
        else:
            error = "Неверный email/имя или пароль"

    return render(request, 'accounts/login.html', {'form': form, 'error': error})


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # при необходимости можно заполнить дополнительные поля
            user.email = form.cleaned_data.get('email')
            user.first_name = form.cleaned_data.get('first_name')
            user.save()

            # Профиль будет создан сигналом accounts.signals.create_or_update_user_profile,
            # поэтому здесь создавать профиль не нужно (и не нужно — чтобы не было дублей).

            # Автоматический вход
            login(request, user)

            return redirect('shop:index')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})

@login_required
def profile_view(request):
    # простая страница профиля (можно расширить)
    return render(request, 'accounts/profile.html')

def logout_view(request):
    logout(request)
    return redirect('shop:index')

