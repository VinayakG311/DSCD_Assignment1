import grpc
import grpc_tools
import time
import market_pb2
import market_pb2_grpc
import concurrent

def run():
   with grpc.insecure_channel('localhost:50051') as channel:
     stub = market_pb2_grpc.MarketStub(channel)
     response = stub.messaging(market_pb2.clientMessage(name='John', greeting = "Yo"))
     print("Greeter client received following from server: " + response.message)   

if __name__ == '__main__':
    run()