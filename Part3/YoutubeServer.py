import pika
import socket

import sys, os,json

userSubscriptions = {}
youtuberVideos = {}

hostname = socket.gethostname()
ipAddr = socket.gethostbyname(hostname)

connection = pika.BlockingConnection(pika.ConnectionParameters(host=ipAddr))
channel = connection.channel()

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
  option = request["option"]
  youtuberName = request["youtuberName"]
  
  if(name not in userSubscriptions):
    userSubscriptions[name] = []
  
  if(youtuberName not in youtuberVideos):
    print("No such youtuber ....")
    return
  
  if(option == 's'):
    
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
  
  print(youtuberVideos)
  
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

channel.basic_consume(queue='youtuber_request', on_message_callback=consume_youtuber_requests, auto_ack=True)
channel.basic_consume(queue='user_request', on_message_callback=consume_user_requests, auto_ack=True)
while(True):
  channel.start_consuming()