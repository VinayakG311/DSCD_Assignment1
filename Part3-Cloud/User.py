import pika,socket,sys,json

hostname = socket.gethostname()
ipAddr = socket.gethostbyname(hostname)
credentials = pika.PlainCredentials('user1','user1')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='10.128.0.3',credentials=credentials))
channel = connection.channel()

# result = channel.queue_declare(queue='',durable=True)
# queue_name = result.method.queue

queue_name = ""

channel.queue_declare(queue='user_request')
# channel.queue_declare(queue=queue_name)

channel.exchange_declare(exchange="notifications",exchange_type='direct')

def notificationCallback(ch,method,properties,body):
  message = body.decode()
  
  print(message)

def updateSubscription(name,option,youtuber):
  subscribe = False
  if(option == 's'):
    subscribe = True
  request_obj = {"userName":name,"youtuberName":youtuber,"subscribe":subscribe}
  request = json.dumps(request_obj)
  channel.basic_publish(exchange='', routing_key='user_request', body=request)
  
  if(option == 's'):
    print(youtuber)
    channel.queue_bind(exchange="notifications",queue=queue_name,routing_key=youtuber)
  
  else:
    print(youtuber)
    channel.queue_unbind(exchange="notifications",queue=queue_name,routing_key=youtuber)
    
  print("Success, Request Sent")
    
    
    


try:
  
  if(len(sys.argv) == 2):
    name = sys.argv[1]
    request_obj = {"userName":name}
    request = json.dumps(request_obj)
    channel.basic_publish(exchange='', routing_key='user_request', body=request)
    print(f"Login request sent by {name}")
    queue_name = f"{name}_notification"
    channel.queue_declare(queue=queue_name,durable=True)
    # queue_name = result.method.queue

    # connection.close()
    
  elif(len(sys.argv) == 4):
    
    
    name = sys.argv[1]
    option = sys.argv[2]
    youtuber = sys.argv[3]
    queue_name = f"{name}_notification"
    channel.queue_declare(queue=queue_name,durable=True)
    updateSubscription(name,option,youtuber)
    
  channel.basic_consume(queue=queue_name, on_message_callback=notificationCallback, auto_ack=True)
  channel.start_consuming()

except KeyboardInterrupt:
  # connection.close()
  sys.exit(0)
