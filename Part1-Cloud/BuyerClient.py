import threading
import uuid,sys,time

import grpc

import market_pb2_grpc, market_pb2
import sys, socket
import Notification_pb2
import Notification_pb2_grpc
from concurrent import futures

port = sys.argv[1]
hostname = socket.gethostname()
ipAddr = socket.gethostbyname(hostname)
notification_server_ip = ipAddr + ":60051"
ipAddr = ipAddr + ":" + port

id = str(uuid.uuid1())


def SearchItem(stub):
    print("Search Request initiated")
    item_name = input("Enter Item name (leave blank to display all items): ")
    category = input("Enter Category : ")
    if item_name == "":
        item_name = "_"
    req = market_pb2.SearchReq(item_name=item_name, category=category)
    print(req)
    res = stub.searchProduct(req)
    print(res)


def BuyItem(stub):
    item_id = input("Enter Item id : ")
    quantity = int(input("Enter Item quantity"))
    address = input("Enter your address")
    req = market_pb2.BuyItemReq(item_id=item_id, quantity=quantity, address=address)
    res = stub.buyProduct(req)
    print(res)


# Incomplete
def AddToWishList(stub):
    item_id = input("Enter Item id : ")
    address = input("Enter your address")

    req = market_pb2.WishListReq(uuid=id, productUUID=item_id, address=address, notif_ip=notification_server_ip)
    res = stub.addtoWishlist(req)
    print(res)


def RateItem(stub):
    item_id = input("Enter Item id : ")
    address = input("Enter your address")
    rating = int(input("Enter Rating (1 to 5) : "))
    item = market_pb2.Rate_an_item(ProductUUID=item_id, address=address, rating=rating)
    res = stub.addRating(item)
    print(res)


def notifs(stub, address, uuid):
    req = market_pb2.NotificationReq(UUID=uuid, address=address)
    res = stub.NotifyClient(req)
    print(res)


def run():
    try:
        address = ipAddr
        print(f"Buyer has entered with address: {address} and uuid: {id} ")
        while True:
            with grpc.insecure_channel('10.128.0.3:50051') as channel:
                stub = market_pb2_grpc.MarketStub(channel)

                # print(f"Buyer has entered with address: {address} and uuid: {id} ")
                # thread = threading.Thread(target=notifs,args=(stub,address,uuid))
                # thread.start()

                print(
                    '1: Search Item\n 2: Buy Product\n 3: Add Product to Wishlist\n 4: Rate Product\n 5: Exit\n')
                a = int(input('Enter Choice : '))
                if a == 1:
                    SearchItem(stub)
                elif a == 2:
                    BuyItem(stub)
                elif a == 3:
                    AddToWishList(stub)
                elif a == 4:
                    RateItem(stub)
                else:
                    break
    except KeyboardInterrupt:
        return


class NotificationServicer(Notification_pb2_grpc.NotificationServicer):

    def Notif1(self, request, context):
        print(request.message)
        return Notification_pb2.void2()


def runserver():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=5))
    Notification_pb2_grpc.add_NotificationServicer_to_server(NotificationServicer(), server)
    server.add_insecure_port('[::]:60051')
    server.start()
    print("Notification server started...")
    try:
        while True:
            time.sleep(3600)  # One hour
    except KeyboardInterrupt:
        server.stop(0)


t = []
if __name__ == '__main__':
    th = threading.Thread(target=run)
    th2 = threading.Thread(target=runserver)
    t.append(th)
    t.append(th2)
    try:
        for i in t:
            i.start()
        for i in t:
            i.join()
    except KeyboardInterrupt:
        sys.exit(0)
