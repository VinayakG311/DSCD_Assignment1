import grpc
import grpc_tools
import time
import market_pb2
import market_pb2_grpc
import concurrent
import uuid
# https://www.tutorialspoint.com/python-program-to-find-the-ip-address-of-the-client
import socket

hostname = socket.gethostname()
ipAddr = socket.gethostbyname(hostname)
seller = market_pb2.Seller(UUID="-1", address="1", products=[])

s_id = ""
s_addr = ""
s = seller

#---------------------------------Seller---------------------------------
def registerSeller(stub):
    global s,s_id,s_addr
    id = str(uuid.uuid1())
    s_id = id
    seller = market_pb2.Seller(UUID=str(id), address=ipAddr, products=[])
    req = market_pb2.registerSellerReq(address=ipAddr, uuid=id)
    res = stub.registerSeller(req)
    if (res.status == 0):
        print(f"Success,Seller registered with uuid : {id}")
        s_addr = ipAddr
        s = seller
    else:

        print(f"Failure,Seller with address {ipAddr} already exists")


def addItem(stub):
    global s
    name = input("Enter product name : ")
    qty = int(input("Enter product quantity : "))
    description = input("Enter product description : ")
    sellerAddress = ipAddr
    price = float(input("Enter prodcut price : "))
    sellerUUID = s_id
    category = int(input("Enter category (Elec 0, Fas 1, Oth 2)"))

    req = market_pb2.sellItemReq(name=name, quantity=qty, description=description, sellerAddress=sellerAddress,
                                 price=price, sellerUUID=sellerUUID, Category=market_pb2.Category.Name(category),seller=s)
    res = stub.sellItem(req)

    if res!=None:
        print('SUCCESS')
        s=res
    else:
        print('FAILURE')
   # print(f"Product added with UUID : {res.productUUID}")


def DeleteItem(stub):
    id = input("Enter product id of the product to be deleted : ")
    s_uuid = input('Enter Seller id : ')
    s_aadr = input('Enter Seller Address : ')

    req=market_pb2.DeleteItemReq(Product_UUID=id,seller_UUID=s_uuid,seller_address=s_aadr)
    res=stub.deleteProduct(req)
    if res.status=='SUCCESS':
        for p in s.products:
            if p.Product_UUID==id:
                s.products.remove(p)
        print('SUCCESS')
    else:
        print('FAILURE')


def UpdateItem(stub):
    global s
    p_id = input("Enter product id of the product to be Updated : ")
    s_uuid = input('Enter Seller id : ')
    s_aadr = input('Enter Seller Address : ')
    Price = int(input('Enter Updated price : '))
    Quant = int(input('Enter Updated Quant : '))
    Desc = input('Enter Updated Desc : ')

    req = market_pb2.UpdateItemReq(Product_UUID=p_id,seller_UUID=s_uuid,seller_address=s_aadr,price=Price,quantity=Quant,description=Desc,seller=s)
    res = stub.updateProduct(req)

    if(res.status=='SUCCESS'):
        print('SUCCESS')
        for p in s.products:
            if p.Product_UUID==p_id:
                p.price=Price
                p.description=Desc
                p.quantity=Quant
    else:
        print('FAILURE')


def DisplayItem(stub):
    s_uuid = input('Enter Seller id : ')
    s_aadr = input('Enter Seller Address : ')
    res = stub.displayProducts(s)
    print(res)

#-----------------------------------------------------------------------

#---------------------------------Buyer---------------------------------
# def registerBuyer(stub):
#     global s,s_id,s_addr
#     id = str(uuid.uuid1())
#     s_id = id
#     seller = market_pb2.Buyer(UUID=str(id), address=ipAddr, products=[])
#     req = market_pb2.registerSellerReq(address=ipAddr, uuid=id)
#     res = stub.registerSeller(req)
#     if (res.status == 0):
#         print(f"Success,Seller registered with uuid : {id}")
#         s_addr = ipAddr
#         s = seller
#     else:

#         print(f"Failure,Seller with address {ipAddr} already exists")
    
def searchItem(stub):  #searchItem for "sale?"
    item_name = input("Enter the name of the product to be searched : ")
    item_category = input("Enter the category of the product to be searched : ")
    if(item_name==""):\
        #return all items
        pass

    else:
        req = market_pb2.searchItemReq(name=item_name , category=item_category)
        res = stub.searchItem(req)
        print(res)

def buyProduct(stub):
    p_id = input("Enter product id of the product to be bought : ")
    s_uuid = input('Enter Seller id : ')
    s_aadr = input('Enter Seller Address : ')
    qty = int(input("Enter the quantity to be bought : "))

    req = market_pb2.BuyItemReq(Product_UUID=p_id,seller_UUID=s_uuid,seller_address=s_aadr,quantity=qty,buyer=s)
    res = stub.buyItem(req)
    if res.status=='SUCCESS':
        print('SUCCESS')
    else:
        print('FAILURE')

def addtoWishlist(stub):    #subsrcribe to the product and get notified when the product is updated
    p_id = input("Enter product id of the product to be added to wishlist : ")
    s_uuid = input('Enter Seller id : ')


def addRating(stub):       #item can be rated only once
    p_id = input("Enter product id of the product to be rated : ")
    buyer_addr = input("Enter the address of the buyer : ")
    rating = int(input("Enter the rating of the product : "))
    req = market_pb2.rateProductReq(prod_id=p_id, rating=rating, address=buyer_addr)
    res = stub.rateProduct(req)
    if res.status=='SUCCESS':
        print('SUCCESS')
    else:
        print('FAILURE')


#------------------------------------------------------------
def menu_seller():
    menu = """1: Register
    2: Add Product
    3: Delete Product
    4: Update Product
    5: Display Products
    6: Exit
    """
    return menu
    # print('1: Register\n 2: Add Product\n 3: Delete Product\n 4: Update Product\n 5: Display Products\n 6: Exit\n')

def menu_buyer():
    menu = """1: Register
    2: Search Product
    3: Buy Product
    4: Add to Wishlist
    5: Rate Product
    6: Exit

    """

    return menu

def ask_choice():
    menu = """1: Buyer
    2: Seller 
    3: Exit
    """
    return menu


def seller(stub):
    try:
        while True:
            print(menu_seller())
            a = int(input('Enter Choice : '))
            if a == 1:
                registerSeller(stub)
            elif a == 2:
                addItem(stub)
            elif a == 3:
                DeleteItem(stub)
            elif a == 4:
                UpdateItem(stub)
            elif a == 5:
                DisplayItem(stub)
            else:
                break
    except KeyboardInterrupt:
        return



def buyer(stub):
    try:
        while True:
            print(menu_buyer())
            a = int(input('Enter Choice : '))
            if a == 1:
                registerSeller(stub)
            elif a == 2:
                searchItem(stub)
            elif a == 3:
                buyProduct(stub)
            elif a == 4:
                addtoWishlist(stub)
            elif a == 5:
                addRating(stub)
            else:
                break
    except KeyboardInterrupt:
        return

def run():
    client_flag = 0
    seller_flag = 0
    try:
        while True:
            with grpc.insecure_channel('localhost:50051') as channel:
                print(ask_choice())
                stub = market_pb2_grpc.MarketStub(channel)
                print(
                    '1: Register\n 2: Add Product\n 3: Delete Product\n 4: Update Product\n 5: Display Products\n 6: Exit\n')
                a = int(input('Enter Choice : '))
                if a == 1:
                    registerSeller(stub)
                elif a == 2:
                    addItem(stub)
                elif a == 3:
                    DeleteItem(stub)
                elif a == 4:
                    UpdateItem(stub)
                elif a == 5:
                    DisplayItem(stub)
                else:
                    break
    except KeyboardInterrupt:
        return


if __name__ == '__main__':
    run()
