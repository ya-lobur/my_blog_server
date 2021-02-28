# my_blog_server

The backend part of my_blog app.

## Первоначальная настройка проекта

### Django

В корневой директории находится файл `requirements.txt` - файл с зависимостями проекта. Установить зависимости:

```shell
pip install -r requirements.txt
```

### .env файл

В файле хранятся переменные среды, которые нежелательно светить в коде и/или эти переменные могут различаться на компьютерах разных
разработчиков. Пример моего `.env` файла:

```dotenv
# Django
SECRET_KEY=<YOUR_SECRET_KEY>

# Database
DB_USER=<YOUR_DB_USER>
DB_PASSWORD=<YOUR_DB_PASSWORD>

# E-mail
EMAIL_HOST=<YOUR_EMAIL_HOST> 
EMAIL_HOST_USER=<YOUR_EMAIL_HOST_USER> 
EMAIL_HOST_PASSWORD=<YOUR_EMAIL_HOST_PASSWORD> 
EMAIL_PORT=<YOUR_EMAIL_PORT> 

# Redis
REDIS_HOST=<YOUR_REDIS_HOST> 
REDIS_PORT=<YOUR_REDIS_PORT> 
```

Сам файл следует разместить в корневой директории проекта

## Запуск в режиме разработки

### База

В проекте используется postgresql в docker-контейнере. Для создания и запуска контейнера в корневой директории выполнить:

```shell
docker-compose up
```

Запуск и остановка (также из корневой директории):

```shell
docker-compose start
docker-compose stop
```

### Миграции

```shell
python manage.py migrate
```

### Запуск сервера

```shell
python manage.py runserver
```

### Redis

Живет в контейнере, стартует при запуске контейнера

### Celery

Запустит четыре процесса воркеров Celery:

```bash
celery -A my_blog_server worker --loglevel=debug --concurrency=4
```

### Flower

```bash
flower -A my_blog_server --port=5555
```

### Frontend

Приложение с фронтом(`my_blog_client`) должно находится в одной директории рядом с серверным(`my_blog_server`)