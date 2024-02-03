import zmq
from Classes import Group
context = zmq.Context()


def run_as_client():
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5555")
def run_as_server():
    sock2 = context.socket(zmq.REP)
    sock2.bind("tcp://*:8888")

if __name__ == 'main':
    run_as_server()
    run_as_client()