from dataclasses import dataclass

import requests
from flask import Flask, jsonify, abort
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint
from flask_migrate import Migrate

from producer import publish

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+pymysql://root:root@db/main'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  # Отключаем лишние уведомления

app.config["SQLALCHEMY_POOL_PRE_PING"] = True  # Проверка соединения перед использованием
app.config["SQLALCHEMY_POOL_RECYCLE"] = 280  # Пересоздавать соединение, если оно старше 280 секунд (примерное значение)

CORS(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)  # Добавляем миграции


@dataclass
class Product(db.Model):
    id: int
    title: str
    image: str

    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    title = db.Column(db.String(200))
    image = db.Column(db.String(200))


@dataclass
class ProductUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    product_id = db.Column(db.Integer)

    UniqueConstraint('user_id', 'product_id', name='user_product_unique')


@app.route('/api/products')
def index():
    return jsonify(Product.query.all())


@app.route('/api/products/<int:id>/like', methods=['POST'])
def like(id):
    try:
        response = requests.get('http://host.docker.internal:8000/api/users')
        if response.status_code != 200:
            return jsonify({"error": "API вернул ошибку", "status": response.status_code}), 500
        json = response.json()

        try:
            productUser = ProductUser(user_id=json['id'], product_id=id)
            db.session.add(productUser)
            db.session.commit()

            publish('product_liked', id)

            return jsonify({
                'message': 'success'
            })


        except Exception as e:
            abort(400, f'You already liked this product, {e}')



    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Ошибка запроса", "details": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
