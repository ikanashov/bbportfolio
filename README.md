# Blackoard Portfolio

## Порядок запуска сервисов
Для работы системы необходимо наличие docker и docker-compose

Для запуска проекта необходимо создать в корневой папке проекта файл .env следующего содержимого:
```shell
DOCKER_PREFIX=BBLEARN_
DOCKER_NETWORK_ADDRESS=NETWORK/MASK
SOAP1CLINK=url
SOAP1CUSER=user
SOAP1CPASSWORD=<>
POSTGRES_DB=cinema
POSTGRES_USER=yandex
POSTGRES_PASSWORD=<>
POSTGRES_SCHEMA=public,bb
FLASK_SECRET_KEY=<>
BB_DATABASE_HOST=IP_ADDRESS
BB_DATABASE=BBLEARN
BB_DATABASE_USER=user
BB_DATABASE_PASSWORD=<>
GUNICORN_HOST=0.0.0.0
GUNICORN_PORT=8000
GUNICORN_WORKERS=10
GUNICORN_LOGLEVEL=DEBUG
```

DOCKER_PREFIX - Префикс для всех сервисов docker-compose (если запускается более одного экемпляра)  
DOCKER_NETWORK_ADDRESS - Подсеть для сервисов (например 192.168.10.0/24)  
SOAP1CLINK - адрес веб-сервиса 1С  
SOAP1CUSER - имя пользователя для подключения к веб-сервису  
SOAP1CPASSWORD - пароль лдя подлючения к веб-сервису  
POSTGRES_DB - имя базы данных  
POSTGRES_USER - имя пользователя базы данных  
POSTGRES_PASSWORD - пароль пользователя (можно сгенерировать с помощью команды ```openssl rand -hex 32```)  
POSTGRES_SCHEMA - схема postgres  
FLASK_SECRET_KEY - ключ flask необходим для генерации формы поиска  
BB_DATABASE_HOST - адрес сервера баз данных BlackBoard (MS SQL)  
BB_DATABASE=BBLEARN - имя базы данных по умолчанию для BlackBoard  
BB_DATABASE_USER -  пользователь с правом чтения данных из баз данных BlackBoard (основная база, хранилище документов, база данных со статистикой)  
BB_DATABASE_PASSWORD - пароль пользователя
GUNICORN_HOST - хост на котором gunicorn принимает запросы  
GUNICORN_PORT - порт gunicorn  
GUNICORN_WORKERS - количество запущенных процессов (если не указать, то автоматически создатся количество ядер * 2 + 1)  
GUNICORN_LOGLEVEL - уровень логов для gunicorn  

## После создания конфигурационного файла:

Для запуска всех сервисов необходимо выполнить команду ```./start```

После запуска система буде доступна по протколу http и порту указанному в настройках GUNICORN_

Для корректной работы авторизации, необходимо запусть сервис на том же URL что и Blackboard (например с помощью reverse proxy  на apache или  nginx)  

Логи доступа к системе появятся в паке logs в корне проекта  

Для остановки всех сервисов необходимо выполнить команду ```./stop```
