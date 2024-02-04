import zmq
import time
import uuid
from datetime import datetime

context = zmq.Context()
serverSocket = context.socket(zmq.REQ)


uuid = str(uuid.uuid1())




#Need to take ip addr of grp from response

groupSocket = context.socket(zmq.REQ)




while(1):
  choice = int(input("Enter your choice :  \n  1) View Groups\n 2) Join Group \n  3) Send Message\n 4) Retrieve Messages \n 5) Leave Group \n "))
  if(choice == 1):
    serverSocket.connect("tcp://localhost:5555")
    serverSocket.send_json({"Request":"get_group_list","uuid":uuid})
    response = serverSocket.recv_string()
    print(response)
    
  elif(choice == 2):
    ip = input("Enter Group IP Address :  ")
    groupSocket.connect(f"tcp://{ip}:5566")
    # groupSocket.send_json({"Action":"Join","uuid":uuid})
    # print(request)
    
    groupSocket.send_json({"Action":"Join","uuid":uuid})
    # print(request)
    response = groupSocket.recv_string()

    print(response)
  
  
  elif(choice == 3):
    
    currTime = str(datetime.now())
    messageBody = input("Enter your message : ")
    groupSocket.send_json({"Action":"Message","Time":currTime,"Data":messageBody,"uuid":uuid})
    response = groupSocket.recv_string()
    print(response)
    
  elif (choice == 4):
    timestamp = input("Enter the timestamp : (-) for no specific timing")
    groupSocket.send_json({"Action" : "Retrieve","uuid":uuid,"Timestamp":timestamp})
    response = groupSocket.recv_string()
    print(response)
    
  elif(choice == 5):
    groupSocket.send_json({"Action":"Leave","uuid":uuid})
    response = groupSocket.recv_string()
    print(response)
  time.sleep(1)