import zmq
import time,socket
import uuid
from datetime import datetime

context = zmq.Context()
serverSocket = context.socket(zmq.REQ)


uuid = str(uuid.uuid1())


hostname = socket.gethostname()
ipAddr = socket.gethostbyname(hostname)

#Need to take ip addr of grp from response

groupSocket1 = context.socket(zmq.REQ)
groupSocket2 = context.socket(zmq.REQ)
groupSocket3 = context.socket(zmq.REQ)

groupSockets = [groupSocket1,groupSocket2,groupSocket3]



while(1):
  choice = int(input("Enter your choice :  \n  1) View Groups\n 2) Join Group \n  3) Send Message\n 4) Retrieve Messages \n 5) Leave Group \n "))
  if(choice == 1):
    serverSocket.connect("tcp://localhost:5555")
    serverSocket.send_json({"Request":"get_group_list","uuid":uuid})
    response = serverSocket.recv_string()
    print(response)
    
  elif(choice == 2):
    ip = input("Enter Group IP Address followed by port number (IP:PORT) :  ")
    address = ip.split(':')
    ip = address[0]
    groupPort = address[1]
    ind = int(groupPort)-5010
    groupSockets[ind].connect(f"tcp://{ip}:{groupPort}")
    # groupSocket.send_json({"Action":"Join","uuid":uuid})
    # print(request)
    
    groupSockets[ind].send_json({"Action":"Join","uuid":uuid})
    # print(request)
    response = groupSockets[ind].recv_string()

    print(response)
  
  
  elif(choice == 3):
    ip = input("Enter Group IP Address followed by port number (IP:PORT) :  ")
    address = ip.split(':')
    ip = address[0]
    groupPort = address[1]
    ind = int(groupPort)-5010
    currTime = str(datetime.now())
    messageBody = input("Enter your message : ")
    groupSockets[ind].send_json({"Action":"Message","Time":currTime,"Data":messageBody,"uuid":uuid})
    response = groupSockets[ind].recv_string()
    print(response)
    
  elif (choice == 4):
    ip = input("Enter Group IP Address followed by port number (IP:PORT) :  ")
    address = ip.split(':')
    ip = address[0]
    groupPort = address[1]
    ind = int(groupPort)-5010
    timestamp = input("Enter the timestamp : (-) for no specific timing")
    groupSockets[ind].send_json({"Action" : "Retrieve","uuid":uuid,"Timestamp":timestamp})
    response = groupSockets[ind].recv_string()
    print(response)
    
  elif(choice == 5):
    ip = input("Enter Group IP Address followed by port number (IP:PORT) :  ")
    address = ip.split(':')
    ip = address[0]
    groupPort = address[1]
    ind = int(groupPort)-5010
    groupSockets[ind].send_json({"Action":"Leave","uuid":uuid})
    response = groupSockets[ind].recv_string()
    print(response)
  time.sleep(1)