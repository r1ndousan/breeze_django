from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify

class News(models.Model):
    title = models.CharField("Заголовок", max_length=255)
    slug = models.SlugField("Slug", max_length=255, unique=True)
    content = models.TextField("Содержание")
    image = models.ImageField("Изображение", upload_to="news/", blank=True, null=True)
    published_at = models.DateField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-published_at', '-created_at']
        verbose_name = "Новость"
        verbose_name_plural = "Новости"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('shop:news_detail', kwargs={'pk': self.pk})


class Product(models.Model):
    CAT_MONO = 'mono'
    CAT_AUTHOR = 'author'
    CAT_POPULAR = 'popular'
    CATEGORY_CHOICES = [
        (CAT_MONO, 'Моно-ароматы'),
        (CAT_AUTHOR, 'Авторские композиции'),
        (CAT_POPULAR, 'Популярные композиции'),
    ]

    name = models.CharField("Заголовок", max_length=255)
    slug = models.SlugField("Slug", max_length=255, unique=True, blank=True)
    category = models.CharField("Категория", max_length=30, choices=CATEGORY_CHOICES, default=CAT_MONO)
    description = models.TextField("Описание", blank=True)
    price = models.DecimalField("Цена", max_digits=10, decimal_places=2)
    image = models.ImageField("Изображение", upload_to='products/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    in_stock = models.BooleanField("В наличии", default=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.name)[:90]
            slug = base
            counter = 1
            while Product.objects.filter(slug=slug).exists():
                slug = f"{base}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)