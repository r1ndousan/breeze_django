# shop/views.py
from pathlib import Path
from django.shortcuts import render, redirect
from django.http import Http404, JsonResponse
from django.views.decorators.http import require_http_methods
import json
from decimal import Decimal
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required


# BASE_DIR — верхняя папка проекта (breeze-django/)
BASE_DIR = Path(__file__).resolve().parent.parent



def is_client_or_admin(user):
    if not user.is_authenticated:
        return False
    return user.is_superuser or getattr(user, 'profile', None) and user.profile.role == 'client'

def is_manager_or_admin(user):
    if not user.is_authenticated:
        return False
    return user.is_superuser or getattr(user, 'profile', None) and user.profile.role == 'manager'


def index(request):
    return render(request, 'shop/index.html')

def all_news(request):
    return render(request, 'shop/all-news.html')

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

