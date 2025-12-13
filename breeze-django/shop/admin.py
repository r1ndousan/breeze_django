from django.contrib import admin
from .models import News

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('id','title','published_at','created_at')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title','content')
    list_filter = ('published_at',)
