# shop/views.py
from pathlib import Path
from django.shortcuts import render, redirect
from django.http import Http404, JsonResponse
from django.views.decorators.http import require_http_methods
import json
from decimal import Decimal

# BASE_DIR — верхняя папка проекта (breeze-django/)
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / 'data' / 'products.json'


# ---------- Загрузка товаров (из data/products.json) ----------
def load_products():
    """
    Попытаться загрузить список товаров из data/products.json.
    Если файл не найден — возвращаем небольшой набор тестовых товаров.
    """
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            # Ожидаем, что это список словарей с полями id, name, slug, price, image, description...
            return data
    except FileNotFoundError:
        # Минимальные тестовые данные для разработки
        return [
            {"id": 1, "name": "Rose & Oud — 50ml", "slug": "rose-oud-50", "price": 89.99,
             "image": "images/showcase_1.jpg", "description": "Деревянно-пряный аромат с нотами розы."},
            {"id": 2, "name": "Citrus Breeze — 30ml", "slug": "citrus-breeze-30", "price": 49.99,
             "image": "images/showcase_2.jpg", "description": "Свежий цитрусовый аромат."},
            {"id": 3, "name": "Amber Mist — 50ml", "slug": "amber-mist-50", "price": 69.99,
             "image": "images/showcase_3.jpg", "description": "Тёплый амбровый шлейф."}
        ]


# ---------- Утилиты для корзины (сессия) ----------
def _get_cart_from_session(request):
    """
    Возвращает корзину в виде словаря {product_id_str: qty}.
    Использует request.session['cart'].
    """
    return request.session.get('cart', {})


def _save_cart_to_session(request, cart):
    request.session['cart'] = cart
    # помечаем сессию как изменённую (не всегда нужно, но безопасно)
    request.session.modified = True


def _cart_items_with_products(cart_dict):
    """
    Получает cart_dict и возвращает список позиций:
    [{'product': product_dict, 'qty': qty, 'line_total': Decimal}, ...]
    """
    products = load_products()
    items = []
    total = Decimal('0.00')
    for pid_str, qty in cart_dict.items():
        # совпадение по id (в data файле id может быть int)
        p = next((x for x in products if str(x.get('id')) == str(pid_str) or x.get('slug') == str(pid_str)), None)
        if not p:
            continue
        # безопасное чтение цены
        price = Decimal(str(p.get('price', '0') or '0'))
        line_total = price * int(qty)
        items.append({'product': p, 'qty': int(qty), 'line_total': line_total})
        total += line_total
    return items, total


# ---------- Views ----------

def index(request):
    """
    Главная страница. Передаём небольшой набор товаров для превью.
    """
    products = load_products()
    preview = products[:3] if products else []
    cart = _get_cart_from_session(request)
    cart_count = sum(int(v) for v in cart.values()) if cart else 0
    context = {
        'products': preview,
        'cart_count': cart_count,
    }
    return render(request, 'shop/index.html', context)


def catalog(request):
    """
    Страница каталога. Поддерживает очень простой поиск по ?q= и фильтр ?tag=.
    """
    products = load_products()
    q = request.GET.get('q', '').strip().lower()
    tag = request.GET.get('tag', '').strip().lower()

    filtered = products
    if q:
        filtered = [p for p in filtered if q in p.get('name', '').lower() or q in p.get('description', '').lower()]
    if tag:
        # ожидается, что в product есть поле 'tags': ['woody','floral'] или 'category'
        filtered = [p for p in filtered if tag in ','.join(p.get('tags', [])).lower() or tag == str(p.get('category', '')).lower()]

    cart = _get_cart_from_session(request)
    cart_count = sum(int(v) for v in cart.values()) if cart else 0

    context = {
        'products': filtered,
        'query': q,
        'tag': tag,
        'cart_count': cart_count,
    }
    return render(request, 'shop/catalog.html', context)


def product_detail(request, slug):
    """
    Страница товара по slug. Если товара нет — 404.
    """
    products = load_products()
    product = next((p for p in products if p.get('slug') == slug or str(p.get('id')) == str(slug)), None)
    if not product:
        raise Http404("Товар не найден")
    cart = _get_cart_from_session(request)
    cart_count = sum(int(v) for v in cart.values()) if cart else 0
    return render(request, 'shop/product_detail.html', {'product': product, 'cart_count': cart_count})


@require_http_methods(["GET", "POST"])
def add_to_cart(request, product_id=None):
    """
    Добавляет товар в корзину.
    Маршрут может быть настроен как:
      path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart')
    или отправлять POST на /cart/add/ с form-данными: product_id, qty
    Возвращает редирект на cart или JSON если AJAX (application/json).
    """
    # получим product_id: либо из аргумента, либо из POST/GET
    pid = product_id or request.POST.get('product_id') or request.GET.get('product_id')
    if pid is None:
        return redirect('shop:catalog')  # нечего добавлять

    qty = request.POST.get('qty') or request.GET.get('qty') or 1
    try:
        qty = int(qty)
    except (ValueError, TypeError):
        qty = 1
    if qty < 1:
        qty = 1

    # проверим, что такой товар существует (необязательно, но полезно)
    products = load_products()
    prod = next((p for p in products if str(p.get('id')) == str(pid) or p.get('slug') == str(pid)), None)
    if not prod:
        # можно вернуть 404 или редирект с сообщением; здесь — редирект
        return redirect('shop:catalog')

    cart = _get_cart_from_session(request)
    key = str(prod.get('id'))  # используем id как ключ
    cart[key] = int(cart.get(key, 0)) + qty
    _save_cart_to_session(request, cart)

    # Если AJAX-запрос (JSON) — вернуть JSON
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.content_type == 'application/json':
        items, total = _cart_items_with_products(cart)
        return JsonResponse({
            'success': True,
            'cart_count': sum(i['qty'] for i in items),
            'cart_total': str(total)
        })

    # иначе редирект на страницу корзины
    return redirect('shop:cart')


def cart_view(request):
    """
    Отображение корзины — берём данные из сессии, подставляем поля товара из data/products.json.
    """
    cart = _get_cart_from_session(request)
    items, total = _cart_items_with_products(cart)
    context = {
        'items': items,
        'total': total,
    }
    return render(request, 'shop/cart.html', context)


@require_http_methods(["POST"])
def remove_from_cart(request, product_id):
    """
    Удалить позицию из корзины (POST).
    Маршрут: path('cart/remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart')
    """
    cart = _get_cart_from_session(request)
    key = str(product_id)
    if key in cart:
        del cart[key]
        _save_cart_to_session(request, cart)

    # при AJAX можно вернуть JSON
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.content_type == 'application/json':
        items, total = _cart_items_with_products(cart)
        return JsonResponse({'success': True, 'cart_count': sum(i['qty'] for i in items), 'cart_total': str(total)})

    return redirect('shop:cart')
