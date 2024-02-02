import grpc
import grpc_tools
import time
import market_pb2
import market_pb2_grpc
import concurrent
import uuid
#https://www.tutorialspoint.com/python-program-to-find-the-ip-address-of-the-client
import socket

hostname = socket.gethostname()
ipAddr = socket.gethostbyname(hostname)
seller = market_pb2.Seller(UUID="-1",address="1",products=[])

def registerSeller(stub):
    # print(seller)

    id = str(uuid.uuid1())
    seller = market_pb2.Seller(UUID=str(id), address=ipAddr, products=[])
    
    req = market_pb2.registerSellerReq(address = ipAddr,uuid = id)
    res = stub.registerSeller(req)
   
    if(res.status == 0):
        print(f"Success, Seller registered with uuid : {id}")
        
        # print(seller)
    else:
        
         print(f"Failure, Seller with address {ipAddr} already exists")
    
def addItem(stub):
    # print(seller)
    if(seller.address == "-1"):
        print("No seller currently")
        return
    name = input("Enter product name : ")
    qty = int(input("Enter product quantity : "))
    description = input("Enter product description : ")
    sellerAddress = seller.address
    price = float(input("Enter prodcut price : "))
    sellerUUID = seller.UUID
    category = int(input("Enter category (Elec 0, Fas 1, Oth 2)"))
    
    req = market_pb2.sellItemReq(name = name,quantity=qty,description=description,sellerAddress=sellerAddress,price = price,sellerUUID=sellerUUID)
    res = stub.sellItem(req)
    # print(f"Product added with UUID : {res.productUUID}")

def run():
    try:
        while True:
            with grpc.insecure_channel('localhost:50051') as channel:
                stub = market_pb2_grpc.MarketStub(channel)
                print('1: Register\n 2: Add Product\n')
                a = int(input('Enter Choice : '))
                if a == 1:
                    registerSeller(stub)
                    # id = str(uuid.uuid1())
                    # seller = market_pb2.Seller(UUID=id)
                    # stub.registerSeller(seller)
                    # print('You are Registered with uuid', id)
                elif a == 2:
                    addItem(stub)
                    # response = stub.messaging(market_pb2.clientMessage(name='John', greeting="Yo"))
                #     # print("Greeter client received following from server: " + response.message)
                else:
                    break
    except KeyboardInterrupt:
        return


if __name__ == '__main__':

    run()

