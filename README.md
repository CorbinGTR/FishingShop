## Описание проекта
Веб-приложение для представления ассортимента магазина рыболовных снастей.

## Основной функционал
- Каталог товаров с фильтрацией по категориям
- Корзина и оформление заказа
- Админ-панель (управление товарами, заказами, пользователями)

## Установка и запуск проекта
pip install -r requirements.txt

В проекте используется PostgreSQL. Необходимо создать базу данных и указать параметры подключения в файле `settings.py`:
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "fishing_shop",
        "USER": "postgres",
        "PASSWORD": "password",
        "HOST": "localhost",
        "PORT": "5432",
    }
}

python manage.py migrate

python manage.py createsuperuser

python manage.py runserver

После запуска сайт будет доступен по адресу: http://127.0.0.1:8000

Административная панель доступна по адресу:http://127.0.0.1:8000/admin
