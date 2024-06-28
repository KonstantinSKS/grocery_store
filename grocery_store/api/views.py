from rest_framework import viewsets, status, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action

from grocery.models import (
    Product, Category, Subcategory, ShoppingCart, ShoppingCartProducts)
from .pagination import LimitPagesPagination
from .serializers import (
    SubcategoryReadOnlySerializer, CategoryReadOnlySerializer,
    ProductReadOnlySerializer, ShoppingCartProductsReadOnlySerializer,
    ShoppingCartProductsSerializer, ShoppingCartReadOnlySerializer,
    ShoppingCartCreateOrUpdateSerializer)


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductReadOnlySerializer
    permission_classes = (AllowAny,)
    pagination_class = LimitPagesPagination


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    # queryset = Category.objects.prefetch_related('subcategories')
    queryset = Category.objects.all()
    serializer_class = CategoryReadOnlySerializer
    permission_classes = (AllowAny,)
    pagination_class = LimitPagesPagination


class ShoppingCartViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return ShoppingCartReadOnlySerializer
        return ShoppingCartCreateOrUpdateSerializer

    def get_queryset(self):
        return ShoppingCart.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['delete'], url_path='clear')
    def clear_cart(self, request):
        shopping_cart = self.get_queryset().first()
        if not shopping_cart:
            return Response(status=status.HTTP_404_NOT_FOUND)
        shopping_cart.products.clear()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'], url_path='details')
    def get_cart_details(self, request):
        shopping_cart = self.get_queryset().first()
        if not shopping_cart:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(shopping_cart)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        user = request.user
        data = request.data
        products = data.pop('products', [])

        if ShoppingCart.objects.filter(user=user).exists():
            return Response({'detail': 'Корзина уже существует.'},
                            status=status.HTTP_400_BAD_REQUEST)

        shopping_cart = ShoppingCart.objects.create(user=user)
        self._add_products_to_cart(shopping_cart, products)

        serializer = self.get_serializer(shopping_cart)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        data = request.data
        products = data.pop('products', [])

        instance.products.clear()
        self._add_products_to_cart(instance, products)

        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def _add_products_to_cart(self, shopping_cart, products):
        for product_data in products:
            product = Product.objects.get(id=product_data['id'])
            quantity = product_data.get('quantity', 1)
            ShoppingCartProducts.objects.create(shopping_cart=shopping_cart,
                                                product=product,
                                                quantity=quantity)
