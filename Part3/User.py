import pika,socket,sys,json

hostname = socket.gethostname()
ipAddr = socket.gethostbyname(hostname)

connection = pika.BlockingConnection(pika.ConnectionParameters(host=ipAddr))
channel = connection.channel()

channel.queue_declare(queue='user_request')

if(len(sys.argv) == 2):
  name = sys.argv[1]
  request_obj = {"userName":name}
  request = json.dumps(request_obj)
  channel.basic_publish(exchange='', routing_key='user_request', body=request)
  print(f"Login request sent by {name}")

  connection.close()
  
elif(len(sys.argv) == 4):
  name = sys.argv[1]
  option = sys.argv[2]
  youtuber = sys.argv[3]
  
  request_obj = {"userName":name, "option":option, "youtuberName":youtuber}
  request = json.dumps(request_obj)
  channel.basic_publish(exchange='', routing_key='user_request', body=request)