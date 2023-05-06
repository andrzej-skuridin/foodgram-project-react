# Продуктовый помощник
### Разработчик: Скуридин Андрей
#### Проект доступен по ip: 158.160.49.77

## Как запустить проект (backend):

Клонировать репозиторий и перейти в него в командной строке:

```
https://github.com/morhond/foodgram-project-react.git
```

```
cd backend
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv env
```

* Если у вас Linux/macOS

    ```
    source env/bin/activate
    ```

* Если у вас windows

    ```
    source env/scripts/activate
    ```

```
python -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python manage.py migrate
```

Запустить проект:

```
python manage.py runserver
```

## Как запустить проект (frontend):
TBA

## Запуск проекта из контейнеров:
TBA