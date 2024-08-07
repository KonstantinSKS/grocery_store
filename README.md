# grocery_store

## Описание:
Тестовое задание отдел бэкенд Сарафан:
Django-проект магазина продуктов 

grocery_store представляет собой backend-проект, в котором реализован следующий функционал:
- создание, редактирование, удаление категорий и подкатегорий товаров в админке.
- категории и подкатегории имеют наименование, slug-имя, изображение.
- подкатегории связаны с родительской категорией.
- реализован эндпоинт для просмотра всех категорий с подкатегориями. Предусмотрена пагинация
- реализована возможность добавления, изменения, удаления продуктов в админ-панели.
- реализован эндпоинт вывода продуктов с пагинацией. Каждый продукт имеет поля: наименование, slug, категория подкатегория, цена, список изображений
- реализован эндпоинт добавления, изменения (изменение количества), удаления продукта в корзине.
- реализован эндпоинт вывода  состава корзины с подсчетом количества товаров и суммы стоимости товаров в корзине.
- реализована возможность полной очистки корзины.
- операции по эндпоинтам категорий и продуктов может осуществлять любой пользователь.
- операции по эндпоинтам корзины может осуществлять только авторизированный пользователь и только со своей корзиной.
- реализована авторизацию по токену.

## Технологии:
- Python 3.11
- Django 4.2
- djangorestframework 3.15
- Djoser 2.2
- Django-Imagekit 5.0

## Как запустить проект:
Клонировать репозиторий и перейти в него в командной строке:
```
git clone https://github.com/KonstantinSKS/grocery_store.git
```
```
cd grocery_store
```
Cоздать и активировать виртуальное окружение:
```
py -3.11 -m venv venv
```
```
source venv/Scripts/activate
```
Установить зависимости из файла requirements.txt:
```
python -m pip install --upgrade pip
```
```
pip install -r requirements.txt
```
В корне проекта создать файл .env
```
touch .env
```
и заполнить его по следующему образцу:
```
SECRET_KEY='Your secret key'
DEBUG=True
```
Перейти в папку проекта grocery_store/ и выполнить миграции:
```
cd grocery_store && python manage.py migrate
```
Создать супрепользователя для доступа в админ-панель:
```
python manage.py createsuperuser
```
Запустить проект:
```
python manage.py runserver
```

После запуска сервера документация к API и примеры запросов будут доступны по ссылкам:
http://127.0.0.1:8000/redoc/
и
http://127.0.0.1:8000/swagger/



Автор: Стеблев Константин
