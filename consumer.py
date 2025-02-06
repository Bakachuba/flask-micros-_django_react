import json
import pika

from main import app, Product, db  # Импортируем приложение, модели и БД

# Настройка подключения к очереди
params = pika.URLParameters('amqps://mmztoxid:TQVZqXcDQ_flhn9wAFD0WtxsnSfjiF1Q@hawk.rmq.cloudamqp.com/mmztoxid')
connection = pika.BlockingConnection(params)
channel = connection.channel()
channel.queue_declare(queue='main')

def callback(ch, method, properties, body):
    with app.app_context():
        print("Receive in main")
        data = json.loads(body)
        print(data)

        try:
            if properties.content_type == "product_created":
                product = Product(id=data['id'], title=data['title'], image=data['image'])
                db.session.add(product)
                db.session.commit()
                print("Product created")

            elif properties.content_type == 'product_updated':
                product = db.session.get(Product, data['id'])
                product.title = data['title']
                product.image = data['image']
                db.session.commit()
                print("Product updated")

            elif properties.content_type == 'product_destroyed':
                product = db.session.get(Product, data)
                db.session.delete(product)
                db.session.commit()
                print("Product destroyed")
        except Exception as e:
            db.session.rollback()
            print("Error during DB operation:", e)


channel.basic_consume(queue='main', on_message_callback=callback, auto_ack=True)

print('Started consuming')
channel.start_consuming()
channel.close()
