# <span style="color: orange;">Конвертер WAV в MP3</span>

---

## Стек:

1. Python 3.10
2. Postgresql 11
3. Docker
4. Docker-compose

<span style="text-indent: 1em; display: block; margin-left: 1em;">Проект включает создание пользователя с
присвоением ему уникального идентификатора и токена, возможность загрузить файл в формате WAV, перекодировать в MP3
и скачать по ссылке

---
<span style="text-indent: 1em; display: block; margin-left: 1em;">Для запуска проекта клонируйте код и выполните
команду <span>*docker-compose up*<span> после чего выполнится загрузка docker-контейнера и приложением можно
пользоваться.

<span style="text-indent: 1em; display: block; margin-left: 1em;">Для начала необходимо создать пользователя. Для этого
выполнить POST запрос по адресу <span>*127.0.0.1:8086/create/*<span> в теле запроса передать JSON имя
пользователя <span>*{"user_name":
"имя вашего пользователя"}*<span> ответом будет уникальный идентификатор и токен, а пользователь будет сохранен в базе
данных.

<span style="text-indent: 1em; display: block; margin-left: 1em;">Для конвертации аудио файла с форматом WAV в MP3
необходимо выполнить POST запрос по адресу <span>*127.0.0.1:8086/load/*<span>  в теле запроса используя Postman передать
form-data user_name - <имя вашего пользователя> ; audio - <файл с форматом WAV>; token - <токен вашего пользователя>.
Ответом будет ссылка для скачивания файла в формате MP3, а сам файл будет сохранен в базе данных. Полученную ссылку
вставте в браузер и выполните запрос. Для сохранности данных после остановки контейнера используются volumes.

<span style="text-indent: 1em; display: block; margin-left: 1em;">PS: знаю что передавать в публичный репозиторий .env
нельзя, это для демонстрации использования переменных окружения