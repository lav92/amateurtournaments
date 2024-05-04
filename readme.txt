pip install fastapi[all] --- установка fastapi

uvicorn app.main:app --reload --- запуск приложения

pip install sqlalchemy alembic asyncpg --- библиотеки для БД

alembic init migrations --- инициализация алембика
!!!--инициализируем алембик в корневой папке проекта--!!!
"""
    migrations/env.py
        - target_metadata = Base.metadata (Base импортируем из нашего модуля database)
        - импортируем наши модели

    alembic.ini
        - засетить наш url db в переменую "sqlalchemy.url"
            для этого в migrations/env.py прописываем "config.set_main_option('sqlalchemy.url', f'{DATABASE_URL}?async_fallback=True')"
"""

alembic revision --autogenerate -m "Название миграции" - создание миграции
"""
    прогоняем миграции
        alembic upgrade head - прогоняет послденюю миграцию
        alembic upgrade 557dfeaeb251 - прогоняем мигрцию с "id"(переменая "revision" в файле миграции) 557dfeaeb251
"""


************* АУТЕНТИФИКАЦИЯ И АВТОРИЗАЦИЯ *************

pip install passlib python-jose -- устанавливаем библотеки

в модуле auth создаем функции для создания jwt токена(параметры key, algorithm в функции encode надо скрывать!!!), хеширования пароля и вирификации пароля



************* СКРЫТИЕ ЧУВСТВИТЕЛЬНЫХ ДАННЫХ *************

--- Создаем config.py в корне ПРИЛОЖЕНИЯ
--- Создаем .env в корне ПРОЕКТА где храним чувствительные данные


************* ЗАПУСК CELERY *************

celery -A app.tasks.celery_config:celery_app worker --loglevel=INFO
