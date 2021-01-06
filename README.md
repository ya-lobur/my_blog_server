# my_blog_server
The backend part of my_blog app.

## Первоначальная настройка проекта

### База

В проекте используется postgresql в docker-контейнере.
Для создания и запуска контейнера в корневой директории выполнить:

```shell
docker-compose up
```

Запуск и остановка (также из корневой директории):
```shell
docker-compose start
docker-compose stop
```

### Django

В корневой директории находится файл `requirements.txt` - файл с зависимостями проекта.
Установить зависимости:
```shell
pip install -r requirements.txt
```

## Запуск в режиме разработки

### Миграции
```shell
python manage.py migrate
```

### Запуск сервера
```shell
python manage.py runserver
```

### Frontend
Приложение с фронтом(`my_blog_client`) должно находится в одной директории рядом с серверным(`my_blog_server`)