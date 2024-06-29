from django.urls import include, path

from rest_framework.routers import DefaultRouter

from .views import (ProductViewSet, CategoryViewSet,
                    ShoppingCartViewSet)

app_name = 'api'


router_v1 = DefaultRouter()

router_v1.register(r'products', ProductViewSet, basename='products')
router_v1.register(r'categories', CategoryViewSet, basename='categories')
router_v1.register(r'shopping-cart', ShoppingCartViewSet,
                   basename='shopping-cart')

urlpatterns = [
    path('', include(router_v1.urls)),
    path('', include('djoser.urls')),
    path('', include('djoser.urls.authtoken')),
]
