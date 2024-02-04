import signal
import time
import zmq


signal.signal(signal.SIGINT, signal.SIG_DFL)

context = zmq.Context()



def connect_to_MessageServer():
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5555")
def connect_to_GroupServer():
    socket2 = context.socket(zmq.REQ)
    socket2.connect("tcp://localhost:8888")


if __name__ == '__main__':
    connect_to_MessageServer()


