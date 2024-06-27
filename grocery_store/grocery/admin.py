from django.contrib import admin

from imagekit.admin import AdminThumbnail

from .models import (Product, Category, Subcategory,
                     ShoppingCart, ShoppingCartProducts,)


# class CategoryInline(admin.TabularInline):
#     model = Category
#     extra = 0


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'price',
        'subcategory',
        'admin_thumbnail',  # image_thumbnail
    )
    list_filter = (
        'name',
        'subcategory',)
    search_fields = ('name',)
    admin_thumbnail = AdminThumbnail(image_field='image_thumbnail')
    # readonly_fields = ['admin_thumbnail',]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    ...


@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    ...


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    ...


@admin.register(ShoppingCartProducts)
class ShoppingCartProductsAdmin(admin.ModelAdmin):
    ...
