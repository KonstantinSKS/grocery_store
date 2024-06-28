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
    subcategories = SubcategoryReadOnlySerializer(many=True, read_only=True)
    # subcategories = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ('id',
                  'name',
                  'slug',
                  'image',
                  'subcategories')

    # def get_subcategories(self, obj):
    #     subcategories = obj.subcategory_set.all()
    #     return SubcategoryReadOnlySerializer(subcategories, many=True).data


class ProductReadOnlySerializer(serializers.ModelSerializer):
    subcategory = SubcategoryReadOnlySerializer(source='subcategories',
                                                read_only=True)
    category = CategoryReadOnlySerializer(source='categories',
                                          read_only=True)
    # image_list = serializers.ListSerializer(child=serializers.ImageField(),
    #                                         read_only=True)
    image_list = serializers.ListSerializer(child=serializers.URLField(),
                                            # source='image_list',
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
            'image_list'
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
            'quantity',
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
    products = ShoppingCartProductsSerializer(many=True)

    class Meta:
        model = ShoppingCart
        exclude = ('user',)
        read_only_fields = ('user',)

    def validate_products(self, products):
        user = self.instance
        curent_user = self.context.get('request').user
        if user.users.filter(user=curent_user).exists():
            raise serializers.ValidationError(
                'Корзина уже существует!'
            )
        if not products:
            raise serializers.ValidationError(
                'В корзине должен быть минимум 1 товар!'
            )
        # products_list = set()
        # for product in products:
        #     product = get_object_or_404(Product, id=product['id'])
        #     if product in products_list:
        #         raise serializers.ValidationError(
        #             'В корзине не может быть два одинаковых продукта!'
        #         )
        #     products_list.add(product)

        product_ids = [product['id'] for product in products]
        if len(product_ids) != len(set(product_ids)):
            raise serializers.ValidationError(
                'В корзине не может быть два одинаковых продукта!'
            )
        return products

    def create_products_amounts(self, products, shopping_cart):
        ShoppingCartProducts.objects.bulk_create(
            [ShoppingCartProducts(
                shopping_cart=shopping_cart,
                product_id=product['id'],
                # product=Product.objects.get(id=product['id']),
                quantity=product['quantity']
            ) for product in products]
        )

    def create(self, validated_data):
        products = validated_data.pop('products')
        shopping_cart = ShoppingCart.objects.create(**validated_data)
        self.create_products_amounts(products=products,
                                     shopping_cart=shopping_cart)
        return shopping_cart

    def update(self, instance, validated_data):
        products = validated_data.pop('products')
        instance.products.clear()
        self.create_products_amounts(products=products,
                                     shopping_cart=instance)
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        return ShoppingCartReadOnlySerializer(
            instance,
            context=self.context
        ).data
