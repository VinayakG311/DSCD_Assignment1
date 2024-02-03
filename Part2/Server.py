import time
import zmq

from Classes import Server

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")


def run():
    server = Server()
    try:
        while True:

            message = socket.recv()

            socket.send_string('hi')
            if message==B"REGISTER":
                time.sleep(1)
                server.res_group_reg(socket)
            print("BYE")












    except KeyboardInterrupt:
        return


if __name__ == '__main__':
    run()
