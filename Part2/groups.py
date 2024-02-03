import zmq
import time
import uuid
import socket


context = zmq.Context()
serverSocket = context.socket(zmq.REQ)
serverSocket.connect("tcp://localhost:5555")

messageSocket = context.socket(zmq.REP)
messageSocket.bind("tcp://*:5566")

uuid = str(uuid.uuid1())

hostname = socket.gethostname()
ipAddr = socket.gethostbyname(hostname)
groupName = input("Enter Group Name : ")
serverSocket.send_json({"Request":"register_group","Name":groupName,"ipAddr":ipAddr})
response = serverSocket.recv_string()
print(response)

messages = {}
users = {}

while(1):
  request = messageSocket.recv_json()
  action = request["Action"]
  userId = request["uuid"]
  
  if(action == "Join"):
    print("Request to Join....")
    response = ""
    if(userId in users):
      response = "FAILURE, USER ALREADY EXISTS"
    
    else:
      users[userId] = 1
      response = "GROUP JOINED SUCCESFULLY"
    
    messageSocket.send_string(response)
    
  elif(action == "Message"):
    if(userId not in users):
      response = "USER DOES NOT EXIST IN GROUP!!!!"
      messageSocket.send_string(response)
      continue
    messageTime = request["Time"]
    messageBody = request["Data"]
    
    
    messages[messageTime] = messageBody
    print(messages)
    
    response = f"Message received at {messageTime} by user {userId}"
    messageSocket.send_string(response)
    time.sleep(1)
  
