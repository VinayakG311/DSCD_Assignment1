import grpc

import market_pb2_grpc, market_pb2


def SearchItem(stub):
    print("Search Request initiated")
    item_name = input("Enter Item name (leave blank to display all items): ")
    category = input("Enter Category : ")
    req = market_pb2.SearchReq(item_name=item_name,category=category)
    res = stub.searchProduct(req)
    print(res)

def BuyItem(stub):
    item_id = input("Enter Item id : ")
    quantity = int(input("Enter Item quantity"))
    address = input("Enter your address")
    req = market_pb2.BuyItemReq(item_id=item_id,quantity=quantity,address=address)
    res=stub.buyProduct(req)
    print(res)

#Incomplete
def AddToWishList(stub):
    item_id = input("Enter Item id : ")
    address = input("Enter your address")
    req= market_pb2.WishListReq(productUUID=item_id,address=address)
    res=stub.addtoWishlist(req)
    print(res)

def RateItem(stub):
    item_id = input("Enter Item id : ")
    address = input("Enter your address")
    rating = int(input("Enter Rating (1 to 5) : "))
    item = market_pb2.Rate_an_item(ProductUUID=item_id,address=address,rating=rating)
    res = stub.addRating(item)
    print(res)

def run():
    try:
        while True:
            with grpc.insecure_channel('localhost:50051') as channel:
                stub = market_pb2_grpc.MarketStub(channel)
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


if __name__ == '__main__':
    run()
