# Продуктовый помощник

Дипломный проект курса Backend-разработчик на Python от Яндекс.

Проект доступен по ip: 158.160.49.77 (10.05.2023 сервер отключён)

#### Разработчик: Скуридин Андрей


## Как запустить проект:
Перейти в каталог /infra и выполнить команду:

```sudo docker compose up -d --build```

Выполнить миграции, создать суперпользователя и соберать статику:

```
sudo docker compose exec backend python manage.py migrate
sudo docker compose exec backend python manage.py createsuperuser
sudo docker compose exec backend python manage.py collectstatic --no-input
```

Ресурсы проекта:
* http://localhost/ - главная страница сайта;
* http://localhost/admin/ - админ панель;
* http://localhost/api/ - API проекта;
* http://localhost/api/docs/redoc.html - документация к API.

## Функционал проекта:

Сайт, позволяющий размещать кулинарные рецепты и подписываться на их авторов. Есть функция корзины, позволяющая отметить заинтересовавшие пользователя рецепты и в дальнейшем скачать список ингредиентов, необходимый для их готовки.
