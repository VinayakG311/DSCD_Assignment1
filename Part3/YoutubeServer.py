import pika
import socket

import sys, os,json

userSubscriptions = {}
youtuberVideos = {}

hostname = socket.gethostname()
ipAddr = socket.gethostbyname(hostname)

connection = pika.BlockingConnection(pika.ConnectionParameters(host=ipAddr))
channel = connection.channel()


def notify_users(name,video):
  message = f"New Notification: {name} uploaded {video}"
  # print(message)
  channel.basic_publish(exchange='notifications', routing_key=name, body=message,properties=pika.BasicProperties(delivery_mode=2))

def handleUserLogin(request):
  name = request["userName"]
  if(name in userSubscriptions):
    print(f"Login Requst by user {name}")
  else:
     print(f"Registration Requst by user {name}")
     userSubscriptions[name] = []
  
  print(userSubscriptions)
     
def handleUserSubscription(request):
  name = request["userName"]
  subscribe = request["subscribe"]
  youtuberName = request["youtuberName"]
  
  if(name not in userSubscriptions):
    userSubscriptions[name] = []
  
  if(youtuberName not in youtuberVideos):
    print("No such youtuber ....")
    return
  
  if(subscribe):
    
    userSubscriptions[name].append(youtuberName)
  else:
    userSubscriptions[name].remove(youtuberName)
  
  print(userSubscriptions)

def consume_youtuber_requests(ch,method,properties,body):
  request = json.loads(body.decode())
  
  
  name = request["youtuberName"]
  video = request["videoName"]
  # print(f"Registration Requst by youtuber {body.decode()}")
  
  if(name in youtuberVideos):
    print("Youtuber present adding video ....")
    youtuberVideos[name].append(video)
  else:
    print("New Youtuber, creating account .....")
    youtuberVideos[name] = []
    youtuberVideos[name].append(video)
  
  notify_users(name,video)
  
  # print(youtuberVideos)
  
def consume_user_requests(ch,method,properties,body):
  request = json.loads(body.decode())
  
  if(len(request) == 1):
    handleUserLogin(request)
  else:
    handleUserSubscription(request)
  # print(request)
  # print(f"Login Requst by user {name}")
  # if(name in userSubscriptions):
  #   print(f"Login Requst by user {name}")
  # else:
  #    print(f"Registration Requst by user {name}")
  #    userSubscriptions[name] = []
  


channel.queue_declare(queue='youtuber_request')
channel.queue_declare(queue='user_request')

channel.exchange_declare(exchange="notifications",exchange_type='direct')

channel.basic_consume(queue='youtuber_request', on_message_callback=consume_youtuber_requests, auto_ack=True)
channel.basic_consume(queue='user_request', on_message_callback=consume_user_requests, auto_ack=True)
# while(True):
#   try:
#     channel.start_consuming()
#   except KeyboardInterrupt:
#     connection.close()
#     sys.exit(0)
  
try:  
  channel.start_consuming()
except KeyboardInterrupt:
  connection.close()
  sys.exit(0)