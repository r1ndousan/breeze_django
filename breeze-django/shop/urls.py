from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'shop'

urlpatterns = [
    path('', views.index, name='index'),
    path('news/', views.news_list, name='news_list'),           # /news/  -> список (all-news.html)
    path('news/add/', views.news_create, name='news_create'),   # создание
    path('news/<int:pk>/', views.news_detail, name='news_detail'),  # детальная /news/1/
    path('news/<int:pk>/edit/', views.news_edit, name='news_edit'),
    path('news/<int:pk>/delete/', views.news_delete, name='news_delete'),
    path('catalog/', views.catalog, name='catalog'),
    path('product/add/', views.product_create, name='product_create'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    path('product/<slug:slug>/edit/', views.product_edit, name='product_edit'),
    path('product/<slug:slug>/delete/', views.product_delete, name='product_delete'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_view, name='cart'),
    path('cart/update/', views.update_cart, name='update_cart'),
    path('cart/remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('orders/my/', views.my_orders_view, name='my_orders'),
    path('orders/', views.orders_list_view, name='orders_list'),  # для менеджера
    path('order/<int:pk>/status/', views.order_update_status, name='order_update_status'),
    path('order/<int:pk>/delete/', views.order_delete_view, name='order_delete'),
    path('order/create/', views.order_create, name='order_create'),
    path('order/<int:pk>/cancel/', views.order_cancel_view, name='order_cancel'),
    path('orders/my/', views.my_orders_view, name='my_orders'),
    path('contacts/', views.contacts, name='contacts'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)