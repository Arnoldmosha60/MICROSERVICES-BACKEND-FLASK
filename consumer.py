import pika, json # type: ignore
from main import Product, db, app  
from sqlalchemy.orm import Session  

# Set up the connection to RabbitMQ
params = pika.URLParameters('amqps://zjqmyjmm:f1m1faiP_38J8j7JoOFGKQs-R2wmkKnW@collie.lmq.cloudamqp.com/zjqmyjmm')

connection = pika.BlockingConnection(params)
channel = connection.channel()
channel.queue_declare(queue='main')

def callback(ch, method, properties, body):
    print("Received in main: ")
    data = json.loads(body)
    print(data)

    with app.app_context(): 
        session = Session(db.engine) 

        if properties.content_type == 'product_created':
            product = Product(id=data['id'], name=data['name'], image=data['image'])
            db.session.add(product)
            db.session.commit()
            print("Product created in DB")

        elif properties.content_type == 'product_updated':
            product = session.get(Product, data['id'])  # Use Session.get() instead of query.get()
            if product:
                product.name = data['name']
                product.image = data['image']
                db.session.commit()
                print("Product updated in DB")

        elif properties.content_type == 'product_deleted':
            product = session.get(Product, data)  # Use Session.get() instead of query.get()
            if product:
                db.session.delete(product)
                db.session.commit()
                print("Product deleted from DB")

channel.basic_consume(queue='main', on_message_callback=callback, auto_ack=True)

print('Started Consuming...')
channel.start_consuming()
channel.close()
