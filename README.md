# PetProject_Docker
Для того щоб підняти проект локально потрібно:

1) Клонувати проект на пристрій:
           $ git clone 
2) В проекті перейти до директорії "pet" в якій знаходиться Dockerfile:
           $ cd pet
3) В цій директорії створити файл .env.dev в якому потрібно вказати наступні дані: 

DEBUG=1 або 0
DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]
SECRET_KEY = створити власний

SQL_ENGINE=django.db.backends.postgresql
SQL_DATABASE=створити власний
SQL_USER=створити власний
SQL_PASSWORD=створити власний
SQL_HOST=db
SQL_PORT=5432
DATABASE=postgres

LOCAL_DOMAIN = "http://127.0.0.1:8000"

4) Створити докер контейнери за допомогою команди:
           $ docker-compose build
5) Запустити контейнери за допомогою команди:
           $ docker-compose up
   Зупинити:
           $ docker-compose down
6) Для запуску функції автоматичного парсингу інформації зі стороннєго ресурсу - треба у мене запросити додаткові інструкції.
