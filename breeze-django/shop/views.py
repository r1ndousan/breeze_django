# shop/views.py
from pathlib import Path
from django.shortcuts import render, redirect
from django.http import Http404, JsonResponse
from django.views.decorators.http import require_http_methods
import json
from decimal import Decimal
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import News
from .forms import NewsForm
from django.urls import reverse
from django.http import HttpResponseForbidden

# BASE_DIR — верхняя папка проекта (breeze-django/)
BASE_DIR = Path(__file__).resolve().parent.parent



def is_client_or_admin(user):
    if not user.is_authenticated:
        return False
    return user.is_superuser or getattr(user, 'profile', None) and user.profile.role == 'client'



def index(request):
    return render(request, 'shop/index.html')


def news_list(request):
    news_qs = News.objects.all()
    return render(request, 'shop/all-news.html', {'news_list': news_qs})

def news_detail(request, pk):
    n = get_object_or_404(News, pk=pk)
    return render(request, 'shop/news-page.html', {'news': n})

def is_manager_or_admin(user):
    # предполагается, что у тебя есть связанная модель Profile с полем role
    try:
        return user.is_authenticated and (user.is_superuser or getattr(user.profile, 'role', '') == 'manager')
    except Exception:
        return user.is_authenticated and user.is_superuser

# Создание новости — только для менеджера/админа
@login_required
@user_passes_test(is_manager_or_admin)
def news_create(request):
    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('shop:news_list')
    else:
        form = NewsForm()
    return render(request, 'shop/news_form.html', {'form': form, 'action': 'Создать'})

# Редактирование — только для менеджера/админа
@login_required
@user_passes_test(is_manager_or_admin)
def news_edit(request, pk):
    n = get_object_or_404(News, pk=pk)
    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES, instance=n)
        if form.is_valid():
            form.save()
            return redirect(n.get_absolute_url())
    else:
        form = NewsForm(instance=n)
    return render(request, 'shop/news_form.html', {'form': form, 'action': 'Сохранить'})

# Удаление — только для менеджера/админа
@login_required
@user_passes_test(is_manager_or_admin)
def news_delete(request, pk):
    n = get_object_or_404(News, pk=pk)
    if request.method == 'POST':
        n.delete()
        return redirect('shop:news_list')
    return render(request, 'shop/news_confirm_delete.html', {'news': n})


def catalog(request):

    return render(request, 'shop/catalog.html')


@login_required
@user_passes_test(is_client_or_admin)
def cart(request):
    return render(request, 'shop/cart.html')


def checkout(request):
    return render(request, 'shop/checkout.html')


@user_passes_test(is_manager_or_admin)
def orders(request):
    return render(request, 'shop/orders.html')


def contacts(request):
    return render(request, 'shop/contacts.html')

