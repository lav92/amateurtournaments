## Приложение для поиска команды-оппонента онлайн игры Dota 2, а так же для получение подробной статистики матчей

### Стек технологий:
* Python
* FastApi
* ORM - SQLalchemy
* PostgreSQL
* Aiohttp
* Asyncio
* SMTP
* Redis(в данном проекте используется только в качестве брокера Celery)
* Celery
* Flower
* Docker & Docker Compose

### Функционал:
* users
  * регистрация, аутентификация и авторизация
  * просмотр личного профиля
* teams
  * создание команды(Название, описание, капитан записывается автоматически - создатель команды)
  * добавление пользователей в команду по ролям(по полю email)
  * просмотр всех команд которые заполнены всеми ролями(из поиска исключена своя собственная команда)
* stats
  * извлечние подробной статистики игры через личный профиль. Используется API сайта stratz.com.
  Всего делается 4 запроса. Полученные данные записываются в БД.
  * уведеление на почту пользователя что отчет по матчу готов
  * просмотр всех отчетов в личном профиле пользователя

### Frontend взят с сайта с шаблонами

## Для запуска
* Скачайте репозиторий 
* Создать свой файл .env-non-dev(пример файла в репозитории)
* С помощью команд docker compose build и docker compose up можно создать и запустить все ообразы
* http://localhost:7777/ - домашняя страница приложения
* http://localhost:5556/ - flower
