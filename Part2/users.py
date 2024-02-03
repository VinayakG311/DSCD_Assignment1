import zmq
import time
import uuid
from datetime import datetime

context = zmq.Context()
serverSocket = context.socket(zmq.REQ)
serverSocket.connect("tcp://localhost:5555")

uuid = str(uuid.uuid1())


serverSocket.send_json({"Request":"get_group_list","uuid":uuid})
response = serverSocket.recv_string()
print(response)

#Need to take ip addr of grp from response

groupSocket = context.socket(zmq.REQ)
groupSocket.connect("tcp://localhost:5566")

groupSocket.send_json({"Action":"Join","uuid":uuid})
# print(request)
response = groupSocket.recv_string()

print(response)

while(1):
  currTime = str(datetime.now())
  messageBody = input("Enter your message : ")
  groupSocket.send_json({"Action":"Message","Time":currTime,"Data":messageBody,"uuid":uuid})
  response = groupSocket.recv_string()
  print(response)
  time.sleep(1)