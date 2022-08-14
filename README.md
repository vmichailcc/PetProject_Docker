# PetProject_Docker
Для того щоб запустити проект локально потрібно:

1) Клонувати проект на пристрій:\
           $ git clone https://github.com/vmichailcc/PetProject_Docker.git
2) В проекті перейти до директорії "pet" в якій знаходиться файл "Dockerfile":\
           $ cd pet
3) В цій директорії створити файл .env.dev в якому потрібно вказати наступні дані: 

DEBUG=1 або 0\
DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]\
SECRET_KEY = створити власний

SQL_ENGINE=django.db.backends.postgresql\
SQL_DATABASE=docker_pet_project\
SQL_USER=docker_pet_project\
SQL_PASSWORD=docker1pet1project\
SQL_HOST=db\
SQL_PORT=5432\
DATABASE=postgres

LOCAL_DOMAIN = "http://127.0.0.1:8000"

4) Створити докер контейнери за допомогою команди:\
           $ docker-compose build
5) Запустити контейнери за допомогою команди:\
           $ docker-compose up -d \
   Зупинити:\
           $ docker-compose down
6) Для запуску функції автоматичного парсингу інформації зі стороннєго ресурсу - треба у мене запросити додаткові інструкції.

P.S. Це стабільна версія. Якщо цікавлять етапи розробки - можно переглянути інший репозиторій: https://github.com/vmichailcc/PetProject
