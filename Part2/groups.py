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
    print(f"Request to Join by user {userId}")
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
      # continue
    messageTime = request["Time"]
    messageBody = request["Data"]
    
    
    messages[messageTime] = messageBody
    print(messages)
    
    response = f"Message received at {messageTime} by user {userId}"
    messageSocket.send_string(response)
    
  
  elif(action == "Retrieve"):
    timestamp = request["Timestamp"]
    if(timestamp == '-'):
      timestamp = '0'
    response = ""
    for t in messages :
      if(t >= timestamp):
        response+=t+" "+messages[t]+'\n'
    messageSocket.send_string(response)
  
  elif(action == "Leave"):
    print(f"Request to Leave by user {userId}")
    if(userId not in users):
      response = "FAILURE, USER DOES NOT EXIST IN THE GROUP"
      
    else:
      users.pop(userId)
      response = f"SUCCESS, USER {userId} has successfully left the group at address {ipAddr} "
  
  time.sleep(1)