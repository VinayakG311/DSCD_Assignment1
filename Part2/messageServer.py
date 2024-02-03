import zmq
import time

groups = {}

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

while(1):
  message = socket.recv_json()
  request = message.get("Request")
 
  if(request == "get_group_list"):
    uuid = message.get("uuid")
    print(f"Group list request by {uuid}")
    response = ""
    for group in groups:
      curr = f"Group Name - {groups[group]}"+" "+f"IP - {group}"
      response+=curr
      response+='\n'
    socket.send_string(response)
    
  elif(request == "register_group"):
    groupName = message.get("Name")
    address = message.get("ipAddr")
    print(f"Registration by Group {groupName}, at address {address}")
    response = ""
    if(address in groups):
      response = f"FAILURE : GROUP ALREADY EXISTS AT ADDRESS {address}"
    else:
      groups[address] = groupName
      response = f"SUCCESS : GROUP CREATED AT ADDRESS {address}"
    
    socket.send_string(response)
  
  time.sleep(1)

  