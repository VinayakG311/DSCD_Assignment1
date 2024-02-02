import zmq

context = zmq.Context()

socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")
l=[5]

for request in range(10):
    print("Sending request %s …" % request)
    socket.send_pyobj(l)

    message = socket.recv()
    print("Received reply %s [ %s ]" % (request, message))