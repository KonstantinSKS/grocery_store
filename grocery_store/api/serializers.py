from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.password_validation import validate_password
from django.shortcuts import get_object_or_404
from djoser.serializers import UserSerializer, UserCreateSerializer
# from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from grocery.models import (Product, Category, Subcategory,
                            ShoppingCart, ShoppingCartProducts,
                            MIN_UNIT_AMOUNT, MAX_UNIT_AMOUNT)
from users.models import User


class SubcategoryReadOnlySerializer(serializers.ModelSerializer):
    class Meta:
        model = Subcategory
        exclude = ('category',)


class CategoryReadOnlySerializer(serializers.ModelSerializer):
    subcategories = SubcategoryReadOnlySerializer(many=True, read_only=True,)

    class Meta:
        model = Category
        fields = ('id', 'name', 'slug', 'image', 'subcategories')


class ProductReadOnlySerializer(serializers.ModelSerializer):
    subcategory = SubcategoryReadOnlySerializer(source='subcategories',
                                                read_only=True)
    category = CategoryReadOnlySerializer(source='categories',
                                          read_only=True)
    image_list = serializers.ListSerializer(child=serializers.ImageField(),
                                            read_only=True)

    class Meta:
        model = Product
        fields = (
            'id',
            'name',
            'slug',
            'category',
            'subcategory',
            'price',
            'image_list,'
        )


class ShoppingCartProductsReadOnlySerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='product.id')
    name = serializers.ReadOnlyField(source='product.name')
    price = serializers.ReadOnlyField(source='product.price')
    total_price = serializers.IntegerField()

    class Meta:
        model = ShoppingCartProducts
        fields = (
            'id',
            'name',
            'price',
            'amount',
            'total_price'
        )


class ShoppingCartProductsSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = ShoppingCartProducts
        fields = (
            'id',
            'quantity',
        )


class ShoppingCartReadOnlySerializer(serializers.ModelSerializer):
    products = ShoppingCartProductsReadOnlySerializer(source='cart_products',
                                                      many=True)
    product_quantity = serializers.SerializerMethodField()

    class Meta:
        model = ShoppingCart
        fields = ('id',
                  'products',
                  'product_quantity')

    def get_product_quantity(self, obj):
        return obj.cart_products.count()


class ShoppingCartCreateOrUpdateSerializer(serializers.ModelSerializer):
    ...
