import grpc
import grpc_tools
import time
import market_pb2
import market_pb2_grpc
import Notification_pb2
import Notification_pb2_grpc

import uuid

from concurrent import futures


# handle the notification thing of success and failure of the operation

def sendNotificationBuyer(request):
        print(request)
        with grpc.insecure_channel('localhost:60051') as channel:
            stub = Notification_pb2_grpc.NotificationStub(channel)
            res = stub.Notif1(Notification_pb2.Notif(message="Product Updated ..."))
            # print(stub.Notif1())
         #   res=stub.Notif1(Notification_pb2.Notif(message="Notification received"))
        return "Notiification Sent"
        # return market_pb2.NotificationRes(message = 'SUCCESS')
        
def sendNotificationSeller(request):
        print(request)
        with grpc.insecure_channel('localhost:50052') as channel:
            stub = Notification_pb2_grpc.NotificationStub(channel)
            res = stub.Notif1(Notification_pb2.Notif(message="Product Bought by client ..."))
            # print(stub.Notif1())
         #   res=stub.Notif1(Notification_pb2.Notif(message="Notification received"))
        return "Notiification Sent"
class MarketServicer(market_pb2_grpc.MarketServicer):
    sellerList = {}
    Sellers = []
    Products = []
    Users = []
    
    
    
    def NotifySeller(self,request):
        print(request)
        return market_pb2.NotificationRes(message='SUCCESS')
    # ------------------------Seller---------------------------------
    def registerSeller(self, request, context):
        currAddress = request.uuid
        status = -1
        if currAddress in self.sellerList:
            status = market_pb2.Status.FAILURE
        else:
            self.sellerList[currAddress] = 1
            self.Sellers.append(market_pb2.Seller(address=request.address, UUID=request.uuid))
            status = market_pb2.Status.SUCCESS
        res = market_pb2.registerSellerRes(status=status)
        print(f'seller join request from {request.address} with uuid {request.uuid}')
        return res

    def sellItem(self, request, context):
        id = str(uuid.uuid1())

        product = market_pb2.Product(Product_UUID=id, category=request.Category, name=request.name, price=request.price,
                                     quantity=request.quantity, description=request.description,
                                     seller_address=request.sellerAddress, seller_UUID=request.sellerUUID,wishlist=[])
        request.seller.products.append(product)
        self.Products.append(product)
        res = market_pb2.sellItemRes(productUUID=id, status=market_pb2.Status.SUCCESS)
        print(f'Product with {res.productUUID} has been registered by seller {request.sellerUUID}')
        
        return request.seller

    def deleteProduct(self, request, context):
        for product in self.Products:
            if product.Product_UUID == request.Product_UUID:
                if request.seller_address == product.seller_address and request.seller_UUID == product.seller_UUID:
                    self.Products.remove(product)
                    print(f'Deleted item {request.Product_UUID} on request from seller {request.seller_UUID}')
                    print(self.Products)
                    return market_pb2.DeleteItemRes(productUUID=request.Product_UUID, status='SUCCESS')

        print("Product not found")
        return market_pb2.DeleteItemRes(productUUID=request.Product_UUID, status='FAILURE')

    def updateProduct(self, request, context):  # need to check the item id first
        res = None
        for product in self.Products:
            if product.Product_UUID == request.Product_UUID:
                if (request.seller_address == product.seller_address and request.seller_UUID == product.seller_UUID):
                    product.price = request.price
                    product.quantity = request.quantity
                    product.description = request.description
                    res = market_pb2.UpdateItemRes(productUUID=product.Product_UUID, status='SUCCESS')
                    for i in product.wishlist:

                        req = market_pb2.NotificationReq(address=i.address,UUID=i.UUID,notif_ip = i.notif_ip)
                        sendNotificationBuyer("Update Product")

                    print(
                        f'Product with uuid {product.Product_UUID} has been updated by seller with uuid {request.seller_UUID}')
                    return market_pb2.UpdateItemRes(productUUID=product.Product_UUID, status='SUCCESS')
                else:
                    res = market_pb2.UpdateItemRes(productUUID=request.Product_UUID, status='FAILURE')
                    print('Incorrect Seller Credentials')
                break
            else:
                res = market_pb2.UpdateItemRes(productUUID=request.Product_UUID, status='FAILURE')
                print("Product not found")

        return res

    def displayProducts(self, request, context):  # for the seller to view the product(DisplaySellerItem)

        p = market_pb2.Products(products=[])
        for i in self.Products:
            if i.seller_UUID == request.UUID:
                p.products.append(i)
        return p

    # ------------------------Buyer---------------------------------

    def registerBuyer(self, request, context):
        seller_name = request.name
        seller_address = request.address
        seller_contact = request.contact
        seller_email = request.email
        seller_id = str(uuid.uuid1())
        seller_wishlist = []

        request.buyers.add(name=seller_name, address=seller_address, contact=seller_contact,
                           email=seller_email, id=seller_id, wishlist=seller_wishlist)
        return market_pb2.void()

    def searchProduct(self, request, context):

        prods=market_pb2.Products()

        if request.item_name == '_':
            if request.category == 'ANY':
                for i in self.Products:
                    prods.products.append(i)
                return prods
            else:
                for product in self.Products:
                    if product.category == request.category:
                        prods.products.append(product)
        else:
            for product in self.Products:
                if product.name == request.item_name:

                    if request.category == 'ANY':
                        prods.products.append(product)
                    else:
                        print(product.category,request.category)
                        if request.category == str(product.category):
                            prods.products.append(product)

        return prods

    def viewProduct(self, request, context):  # for the customer to view the product(SearchItem one)
        for product in request.products:
            print(product.name)

    def addRating(self, request, context):  # for the customer to rate the product

        if (request.rating > 5 or request.rating < 0):  # in UUID is getting used and address is just to not be NULL
            print("Invalid rating")
            return market_pb2.UpdateItemRes(status='FAILURE', productUUID=request.ProductUUID)

        if (request.address == ""):
            print("Address not found")
            return market_pb2.UpdateItemRes(status='FAILURE', productUUID=request.ProductUUID)

        for product in self.Products:
            if (product.Product_UUID == request.ProductUUID):
                val = product.rating * product.rating_count
                product.rating_count += 1

                product.rating = (request.rating + val) / product.rating_count
                print(self.Products)
                print(f"{request.address} rated item {request.ProductUUID} with rating of {request.rating} stars")
                return market_pb2.UpdateItemRes(status='SUCCESS', productUUID=request.ProductUUID)
        return market_pb2.UpdateItemRes(status='FAILURE', productUUID=request.ProductUUID)

    def addtoWishlist(self, request, context):
        m=0
        for user in self.Users:
            if user.address == request.address:
                m=1
                for prod in self.Products:
                    if prod.Product_UUID == request.productUUID:
                        user.wishlist.append(prod)
                        prod.wishlist.append(user)

                        return market_pb2.WishListRes(status='SUCCESS', productUUID=request.productUUID)
        if m==0:
            new_user = market_pb2.Buyer(UUID=request.uuid,wishlist=[],address=request.address,notif_ip=request.notif_ip)
            for prod in self.Products:
                if prod.Product_UUID == request.productUUID:
                    new_user.wishlist.append(prod)
                    prod.wishlist.append(new_user)
            self.Users.append(new_user)

            return market_pb2.WishListRes(status='SUCCESS', productUUID=request.productUUID)
        return market_pb2.WishListRes(status='Failure', productUUID=request.productUUID)

    def buyProduct(self, request, context):

        for product in self.Products:
            if product.Product_UUID == request.item_id:
                print(product.quantity)
                if product.quantity >= request.quantity:
                    product.quantity -= request.quantity
                    print(
                        f"Buy request from {request.address} for item {request.item_id} with quantity {request.quantity}")
                    print(self.Products)
                    sendNotificationSeller(request)
                    return market_pb2.WishListRes(status='SUCCESS', productUUID=request.item_id)
            
        return market_pb2.WishListRes(status='FAILURE', productUUID=request.item_id)
    


# ------------------------buyer&seller---------------------------------

#  return super().addProduct(request, context)
#  return super().viewProduct(request, context)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=5))
    market_pb2_grpc.add_MarketServicer_to_server(MarketServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Market server started...")
    try:
        while True:
            time.sleep(3600)  # One hour
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':

    serve()
