import zmq
from Part2.misc.Classes import Group
context = zmq.Context()



def run_as_client():
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5555")
    try:
        while True:
            print("1. Register Group")
            a=int(input("Enter your choice"))
            if a==1:
                group = Group(address="1",uuid="1")
                socket.send(B"REGISTER")
                socket.recv_string()
                group.Req_Register(socket)
                if(group.Status==1):
                    print("REGISTERED")
    except KeyboardInterrupt:
        return
def run_as_server():
    sock2 = context.socket(zmq.REP)
    sock2.bind("tcp://*:8888")


if __name__ == '__main__':
    run_as_client()
    run_as_server()