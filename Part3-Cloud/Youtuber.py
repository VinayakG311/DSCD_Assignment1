import pika
import sys,socket,json

hostname = socket.gethostname()
ipAddr = socket.gethostbyname(hostname)
credentials = pika.PlainCredentials('user1','user1')
connection= pika.BlockingConnection(pika.ConnectionParameters(host='10.128.0.3',credentials=credentials))
channel = connection.channel()

channel.queue_declare(queue='youtuber_request')


name = sys.argv[1]
videoName = ""
n = len(sys.argv)
for i in range(2,n-1):
  videoName+=sys.argv[i]
  videoName+=" "
videoName+=sys.argv[n-1]

request_obj = {"youtuberName":name,"videoName":videoName}

request = json.dumps(request_obj)
channel.basic_publish(exchange='', routing_key='youtuber_request', body=request)
# print(f"Login request sent by {name}")

# name = input("Enter your name : ")

# channel.basic_publish(exchange='', routing_key='youtuber_request', body=name)
# print(f"Registration request sent by {name}")

# connection.close()
