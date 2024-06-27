from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.db import models
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

from users.models import User

PRICE_MAX_DIGITS: int = 10
PRICE_DECIMAL_PLACES: int = 2
MIN_UNIT_AMOUNT: int = 1
MAX_UNIT_AMOUNT: int = 32000


class AbstractModel(models.Model):
    """Абстрактная модель.
    Добавляет наименование, slug и изображение."""
    name = models.CharField(
        verbose_name='Наименование',
        unique=True,
        max_length=200
    )
    slug = models.SlugField(
        verbose_name='Уникальный слаг',
        unique=True,
        max_length=50
    )
    image = models.ImageField(
        verbose_name='Изображение',
        upload_to='grocery_images/',
    )

    class Meta:
        abstract = True

    def __str__(self):
        return f'{self.name}, {self.slug}'


class Product(AbstractModel):
    """Модель продукта."""
    # category = models.ForeignKey(
    #     'Category',
    #     verbose_name='Категория',
    #     related_name='products',
    #     on_delete=models.PROTECT
    # )
    subcategory = models.ForeignKey(
        'Subcategory',
        verbose_name='Подкатегория ',
        related_name='subcategories',
        on_delete=models.PROTECT
    )
    price = models.DecimalField(
        verbose_name='Цена',
        max_digits=PRICE_MAX_DIGITS,
        decimal_places=PRICE_DECIMAL_PLACES,
        validators=[MinValueValidator(0)],  # Вынести в константы!
    )
    image_thumbnail = ImageSpecField(
        source='image',
        processors=[ResizeToFill(100, 50)],  # Вынести в константы!
        format='JPEG',
        options={'quality': 60})
    image_medium = ImageSpecField(
        source='image',
        processors=[ResizeToFill(300, 300)],
        format='JPEG',
        options={'quality': 90})
    image_large = ImageSpecField(
        source='image',
        processors=[ResizeToFill(800, 800)],
        format='JPEG',
        options={'quality': 90})

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return f'{self.name} - {self.price} р.'

    @property
    def image_list(self):
        return [self.image, self.image_medium, self.image_large]

    # def clean(self):
    #     super().clean()
    #     if self.subcategory.category != self.category:
    #         raise ValidationError(
    #             'Подкатегория должна быть связана с родительсокй категорией!')


class Category(AbstractModel):
    """Модель категории."""

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Subcategory(AbstractModel):
    """Модель подкатегории."""
    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        related_name='categories',
        on_delete=models.CASCADE   # on_delete=models.PROTECT
    )

    class Meta:
        verbose_name = 'Подкатегория'
        verbose_name_plural = 'Подкатегории'


class ShoppingCart(models.Model):
    """Модель корзины."""
    user = models.ForeignKey(
        User,
        verbose_name='Пользователь корзины',
        on_delete=models.CASCADE,
        related_name='users'
    )
    products = models.ManyToManyField(
        Product,
        through='ShoppingCartProducts',
        verbose_name='Список продуктов',
    )

    class Meta:
        verbose_name = 'Корзина покупок'
        verbose_name_plural = 'Корзины покупок'


class ShoppingCartProducts(models.Model):
    """Промежуточная таблица для модели корзины.
    Устанавливает связь M:M с таблицей ShoppingCart"""
    shopping_cart = models.ForeignKey(
        ShoppingCart,
        verbose_name='Корзина покупок',
        on_delete=models.CASCADE,
        related_name='users'
    )
    product = models.ForeignKey(
        Product,
        verbose_name='Продукты',
        on_delete=models.CASCADE,   # on_delete=models.PROTECT
        related_name='products'
    )
    quantity = models.PositiveIntegerField(
        verbose_name='Количенство',
        default=1,
        validators=[
            MinValueValidator(
                MIN_UNIT_AMOUNT,
                message='Количество не может быть меньше 1 единицы!'),
            MaxValueValidator(
                MAX_UNIT_AMOUNT,
                message='Количество не может быть больше 32000 единиц!'
            )
        ]
    )

    class Meta:
        verbose_name_plural = 'Количество продуктов'
        constraints = [
            models.UniqueConstraint(
                fields=['shopping_cart', 'product'],
                name='unique_shopping_cart_product',
                violation_error_message='Товар уже есть в корзине!'
            )
        ]

    def __str__(self):
        return f'{self.product.name}: {self.quantity} шт.'

    @property
    def total_price(self):
        return self.product.price * self.quantity
