import zmq
import time,sys

groups = {}

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

while(1):
  try:
    message = socket.recv_json()
    request = message.get("Request")
  
    if(request == "get_group_list"):
      uuid = message.get("uuid")
      print(f"Group list request by {uuid}")
      response = ""
      for group in groups:
        curr = f"{groups[group]}"+" - "+f"{group}"
        response+=curr
        response+='\n'
      socket.send_string(response)
      
    elif(request == "register_group"):
      groupName = message.get("Name")
      address = message.get("ipAddr")
      print(f"JOIN REQUEST FROM {address}")
      response = ""
      if(address in groups):
        response = f"FAILURE : GROUP ALREADY EXISTS AT ADDRESS {address}"
      else:
        groups[address] = groupName
        response = f"SUCCESS"
      
      socket.send_string(response)
    
    time.sleep(1)

  except KeyboardInterrupt:
    sys.exit(0)
  