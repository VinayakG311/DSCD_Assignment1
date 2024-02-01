import grpc
import grpc_tools
import time
import market_pb2
import market_pb2_grpc
import concurrent
import uuid


def run():
    try:
        while True:
            with grpc.insecure_channel('localhost:50051') as channel:
                stub = market_pb2_grpc.MarketStub(channel)
                print('1: Register 2: Greet')
                a = int(input('enter choice'))
                if a == 1:
                    id = str(uuid.uuid1())
                    seller = market_pb2.Seller(UUID=id)
                    stub.registerSeller(seller)
                    print('You are Registered with uuid', id)
                elif a == 2:
                    response = stub.messaging(market_pb2.clientMessage(name='John', greeting="Yo"))
                    print("Greeter client received following from server: " + response.message)
                else:
                    break
    except KeyboardInterrupt:
        return


if __name__ == '__main__':
    run()
