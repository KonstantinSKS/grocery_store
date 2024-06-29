from django.contrib import admin
from django.utils.safestring import mark_safe

from imagekit.admin import AdminThumbnail

from .models import Product, Category, Subcategory


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'price',
        'subcategory',
        'admin_thumbnail',
    )
    list_filter = (
        'name',
        'subcategory',)
    search_fields = ('name',)
    admin_thumbnail = AdminThumbnail(image_field='image_thumbnail')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'slug',
        'icon',
    )
    search_fields = ('name',)
    list_filter = ('name',)

    @admin.display(description='Изображение')
    def icon(self, category):
        if category.image:
            return mark_safe(f"<img src='{category.image.url}' width=100>")
        return 'Изображение отсутствует'


@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'slug',
        'category',
        'icon',
        'image'
    )
    search_fields = ('name',)
    list_filter = ('category',)
    readonly_fields = ('icon',)

    @admin.display(description='Изображение')
    def icon(self, subcategory):
        if subcategory.image:
            return mark_safe(f"<img src='{subcategory.image.url}' width=100>")
        return 'Изображение отсутствует'
