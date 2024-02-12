import zmq
import time,sys
import uuid
import socket
import threading

NO_OF_GROUPS = 3
BASE_PORT = 5010

context = zmq.Context()
serverSocket = context.socket(zmq.REQ)
serverSocket.connect("tcp://localhost:5555")

# messageSocket = context.socket(zmq.REP)
# messageSocket.bind("tcp://*:5566")

# uuid = str(uuid.uuid1())

hostname = socket.gethostname()
ipAddr = socket.gethostbyname(hostname)
# groupName = input("Enter Group Name : ")
# serverSocket.send_json({"Request":"register_group","Name":groupName,"ipAddr":ipAddr})
# response = serverSocket.recv_string()
# print(response)


groupSockets = []
thr = []


def registerGroup(ip,port):
  groupName = input("Enter Group Name : ")
  address = ipAddr+":"+str(port)
  serverSocket.send_json({"Request":"register_group","Name":groupName,"ipAddr":address})
  response = serverSocket.recv_string()
  
  print(response)
  
  currSocket = context.socket(zmq.REP)
  currSocket.bind(f"tcp://*:{port}")
  groupSockets.append([currSocket,port])
  

def handleGroupUserInteraction(messageSocket,port):
  messages = {}
  users = {}
  while(1):
    try:
      request = messageSocket.recv_json()
      action = request["Action"]
      userId = request["uuid"]
      
      if(action == "Join"):
        print(f"JOIN REQUEST FROM {userId} for {ipAddr}:{port}")
        response = ""
        if(userId in users):
          response = "FAILURE, USER ALREADY EXISTS"
        
        else:
          users[userId] = 1
          response = "SUCCESS"
        
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
        print(f"Request to Leave group {ipAddr}:{port} by user {userId}")
        if(userId not in users):
          response = "FAILURE, USER DOES NOT EXIST IN THE GROUP"
          
        else:
          users.pop(userId)
          response = f"SUCCESS, USER {userId} has successfully left the group at address {ipAddr}:{port} "
        messageSocket.send_string(response)
      
      time.sleep(1)
    except KeyboardInterrupt:
      for th in thr:
        th.join()

      for socket in groupSockets:
        socket.close()

      sys.exit(0)
    
  


try:
    
  for groupNum in range(NO_OF_GROUPS):
    currPort = groupNum+BASE_PORT
    registerGroup(ipAddr,currPort)
    
  for [socket,port] in groupSockets:
    thread = threading.Thread(target=handleGroupUserInteraction, args=(socket,port,) )
    thread.start()
    thr.append(thread)
    

  for th in thr:
    th.join()

  for socket in groupSockets:
    socket.close()

except KeyboardInterrupt:
  for th in thr:
    th.join()

  for socket in groupSockets:
    socket.close()

  sys.exit(0)
    