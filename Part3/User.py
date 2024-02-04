import json
import sys
import pika

user_name = sys.argv[1]
sub_unsub= sys.argv[2]
youtuber_name= sys.argv[3]
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='hello')
if sub_unsub=='s':
    channel.basic_publish(exchange='', routing_key='hello', body=json.dumps({"client":"user","user":user_name,"youtuber":youtuber_name,"subscription":1}))
    print(f"{user_name} subscribed to {youtuber_name}")
elif sub_unsub=='u':
    channel.basic_publish(exchange='', routing_key='hello', body=json.dumps({"client":"user","user":user_name,"youtuber":youtuber_name,"subscription":0}))
    print(f"{user_name} unsubscribed to {youtuber_name}")
else:
    print('enter valid arguments')

connection.close()