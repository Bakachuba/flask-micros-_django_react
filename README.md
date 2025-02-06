DJANGO+REACT+FLASK MICROSERVICES


(flask repo)

queue logs:
sudo docker compose run queue sh
python consumer.py


Commands for migrate

1) flask --app main db init
2) docker compose run backend flask --app main db migrate -m "Initial migration"
3) docker compose run backend flask --app main db upgrade



Гайд

Flask Migrations Guide

1. Установка и настройка проекта

1.1 Установите необходимые зависимости

pip install flask flask-sqlalchemy flask-migrate mysqlclient cryptography

1.2 Создайте структуру проекта

project/
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── routes.py
│   ├── config.py
├── migrations/  # Папка появится после инициализации Alembic
├── main.py
├── requirements.txt
├── .env
└── docker-compose.yml

1.3 Настройте config.py

import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "mysql+pymysql://user:password@db/flaskdb")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

2. Настройка и инициализация Alembic

2.1 Добавьте в __init__.py поддержку миграций

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

# Инициализация Flask
app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import models  # Подключение моделей

2.2 Инициализация миграций

flask --app main db init

Если у вас проблемы с FLASK_APP, попробуйте явно указать переменную окружения:

export FLASK_APP=main.py

3. Создание и применение миграций

3.1 Добавление модели в models.py

from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

3.2 Создание миграции

flask --app main db migrate -m "Initial migration"

3.3 Применение миграций

flask --app main db upgrade

4. Работа с Docker

4.1 Запуск базы данных через Docker

docker-compose up -d

4.2 Запуск миграций внутри контейнера

docker-compose run backend flask --app main db upgrade

4.3 Пересоздание БД (если что-то пошло не так)

docker-compose down -v
flask --app main db downgrade base
flask --app main db upgrade

5. Полезные команды

Проверить текущее состояние миграций

flask --app main db history

Откатить последнюю миграцию

flask --app main db downgrade -1

Обновить до последней версии

flask --app main db upgrade

Теперь у вас есть полный гайд по настройке и использованию миграций в Flask! 🚀

