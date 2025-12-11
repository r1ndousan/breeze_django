# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from django.contrib import messages
from .forms import LoginForm, RegisterForm
from django.contrib.auth.decorators import login_required
from accounts.models import Profile
from django.db import transaction

def login_view(request):
    if request.user.is_authenticated:
        return redirect('shop:index')
    form = LoginForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        identifier = form.cleaned_data['username_or_email']
        password = form.cleaned_data['password']
        # пробуем аутентифицировать сначала по username, затем по email
        user = authenticate(request, username=identifier, password=password)
        if user is None:
            # найти username по email
            try:
                u = User.objects.get(email__iexact=identifier)
                user = authenticate(request, username=u.username, password=password)
            except User.DoesNotExist:
                user = None
        if user:
            login(request, user)
            messages.success(request, f'Добро пожаловать, {user.first_name or user.username}!')
            return redirect(request.GET.get('next') or '/')
        else:
            messages.error(request, 'Неверный логин или пароль')
    return render(request, 'accounts/login.html', {'form': form})

@login_required
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        messages.info(request, 'Вы вышли из аккаунта')
        return redirect('shop:index')
    # если GET — можно показать confirm-страницу или выполнить logout через POST только
    return render(request, 'accounts/logout_confirm.html')


def register_view(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip().lower()
        password = request.POST.get('password')
        password2 = request.POST.get('repassword')

        if not email or not password:
            messages.error(request, "Заполните email и пароль.")
            return redirect('accounts:register')

        if password != password2:
            messages.error(request, "Пароли не совпадают.")
            return redirect('accounts:register')

        if User.objects.filter(username=email).exists():
            messages.error(request, "Пользователь с таким email уже существует.")
            return redirect('accounts:register')

        try:
            with transaction.atomic():
                user = User.objects.create_user(username=email, email=email, password=password, first_name=name)
                # защищённо создаём профиль: если сигнал уже создаёт профиль, get_or_create не создаст второй
                Profile.objects.get_or_create(user=user, defaults={'role': 'client'})  # заменяй defaults по модели
                # опционально — логиним пользователя сразу
                user = authenticate(request, username=email, password=password)
                if user:
                    login(request, user)
                messages.success(request, "Регистрация успешна.")
                return redirect('shop:index')
        except Exception as e:
            # логирование можно добавить
            messages.error(request, f"Ошибка регистрации: {e}")
            return redirect('accounts:register')
    else:
        return render(request, 'accounts/register.html')

@login_required
def profile_view(request):
    # простая страница профиля (можно расширить)
    return render(request, 'accounts/profile.html')
