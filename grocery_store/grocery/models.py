from django.db import models


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
        return str(self.name)  # ???


class Product(AbstractModel):
    category = models.ForeignKey(
        'Category',
        verbose_name='Категория',
        related_name='categories',
        on_delete=models.PROTECT   # ???
    )
    subcategory = models.ForeignKey(
        'Subcategory',
        verbose_name='Подкатегория ',
        related_name='subcategories',
        on_delete=models.PROTECT   # ???
    )
    price = models.DecimalField(
        verbose_name='Цена',
        max_digits=10,  # ВЫнести в константы 1!
        decimal_places=2  # ВЫнести в константы !
    )
    #  ImageSpecField


class Category(AbstractModel):
    ...


class Subcategory(AbstractModel):
    ...


class ShoppingCart(models.Model):
    ...


class ShoppingCartProducts(models.Model):
    ...
