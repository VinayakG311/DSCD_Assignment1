import json
import sys
import pika


youtuber = sys.argv[1]
video_name = ' '.join(sys.argv[2:])

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='hello')
channel.basic_publish(exchange='', routing_key='hello', body=json.dumps({"client":"youtuber","youtuber":youtuber,"video":video_name}))
print(f" {youtuber} published video {video_name}")
connection.close()