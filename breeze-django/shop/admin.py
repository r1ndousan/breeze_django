from django.contrib import admin
from .models import News
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    readonly_fields = ('name', 'price', 'quantity', 'product')
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at', 'total', 'delivery_type', 'status')
    list_filter = ('status', 'delivery_type', 'created_at')
    inlines = [OrderItemInline]
    
@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('id','title','published_at','created_at')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title','content')
    list_filter = ('published_at',)
