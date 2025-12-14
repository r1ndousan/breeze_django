# shop/views.py
from pathlib import Path
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import News
from .forms import NewsForm
from django.core.paginator import Paginator
from django.db.models import Q


# BASE_DIR — верхняя папка проекта (breeze-django/)
BASE_DIR = Path(__file__).resolve().parent.parent



def is_client_or_admin(user):
    if not user.is_authenticated:
        return False
    return user.is_superuser or getattr(user, 'profile', None) and user.profile.role == 'client'



def index(request):
    # Получаем три последние новости
    latest_news = []
    if News is not None:
        # модель есть — используем ORM
        latest_news = list(News.objects.filter(published_at__isnull=False).order_by('-published_at')[:3])

    # остальные данные для главной — (products и т.п.)
    # products = ...
    context = {
        'latest_news': latest_news,
        # 'products': products,
    }
    return render(request, 'shop/index.html', context)


def news_list(request):
    q = request.GET.get('q', '').strip()
    order = request.GET.get('order', 'newest')  # 'newest' или 'oldest'
    page_number = request.GET.get('page', 1)

    qs = News.objects.all()

    # Поиск по заголовку и содержанию
    if q:
        qs = qs.filter(Q(title__icontains=q) | Q(content__icontains=q))

    # Сортировка по дате
    if order == 'oldest':
        qs = qs.order_by('published_at')
    else:
        qs = qs.order_by('-published_at')

    # Пагинация (6 на страницу — поменяй по желанию)
    paginator = Paginator(qs, 4)
    page_obj = paginator.get_page(page_number)

    # Сформируем базовую строку запроса без page, чтобы сохранять фильтры в ссылках
    params = request.GET.copy()
    if 'page' in params:
        params.pop('page')
    base_qs = params.urlencode()  # может быть пустой строкой

    context = {
        'news_list': page_obj.object_list,  # список новостей текущей страницы
        'page_obj': page_obj,
        'paginator': paginator,
        'base_qs': base_qs,
        'q': q,
        'order': order,
    }
    return render(request, 'shop/all-news.html', context)

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

