# Продуктовый помощник
### Разработчик: Скуридин Андрей
#### Проект доступен по ip: 158.160.49.77

## Как запустить проект:
Перейти в каталог /infra и выполнить команду:
```sudo docker compose up -d --build```
Выполнить миграции, создайть суперпользователя и соберать статику
```sudo docker compose exec backend python manage.py migrate
sudo docker compose exec backend python manage.py createsuperuser
sudo docker compose exec backend python manage.py collectstatic --no-input```
Ресурсы проекта:
* http://localhost/ - главная страница сайта;
* http://localhost/admin/ - админ панель;
* http://localhost/api/ - API проекта
* http://localhost/api/docs/redoc.html - документация к API
