from django.contrib import admin

from .models import (Product, Category, Subcategory,
                     ShoppingCart, ShoppingCartProducts,)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    ...


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
