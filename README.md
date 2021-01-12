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

### .env файл
В файле хранятся переменные среды, которые нежелательно светить в коде и/или эти переменные
могут различаться на компьютерах разных разработчиков.
Пример моего `.env` файла:
```dotenv
SECRET_KEY=f&*ntf&h-7zqpeuo2#xm365r0+(lyvcfe0c0ek=@mnz0u1i6_x
DB_USER=my_blog
DB_PASSWORD=my_blog
```

Сам файл следует разместить в корневой директории проекта


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