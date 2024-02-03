import time
import zmq

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

while True:

    message = socket.recv_pyobj()
    print("Received request: %s" % message)
    print(message.uuid)

    time.sleep(1)

    socket.send(b"World")