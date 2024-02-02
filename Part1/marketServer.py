import grpc
import grpc_tools
import time
import market_pb2
import market_pb2_grpc
import uuid

from concurrent import futures

# handle the notification thing of success and failure of the operation


class MarketServicer(market_pb2_grpc.MarketServicer):

    sellerList = {}
#------------------------Seller--------------------------------- 
    def registerSeller(self, request, context):
        currAddress = request.uuid
        status = -1
        if currAddress in self.sellerList:
            status = market_pb2.Status.FAILURE
        else:
            self.sellerList[currAddress] = 1
            status = market_pb2.Status.SUCCESS
        res = market_pb2.registerSellerRes(status = status)
        print(self.sellerList)
        return res

    def sellItem(self, request, context):
        product = market_pb2.Product(name = request.name, price = request.price, quantity=request.quantity,description=request.description,seller_address=request.sellerAddress,seller_UUID=request.sellerUUID)
        #request.seller.products.append(product)
        id = str(uuid.uuid1())
        res = market_pb2.sellItemRes(productUUID=id,status = market_pb2.Status.SUCCESS)
        print(res)
        return res
    
    def addProduct(self, request, context):
        prod_name = request.name
        prod_category = request.category
        prod_quantity = request.quantity
        prod_description = request.description
        prod_price_per_unit = request.price
        prod_seller_address = request.seller_address
        prod_seller_UUID = request.seller_UUID
        prod_id = str(uuid.uuid1())
        prod_rating = 0

        # for i in context.sellers:
        #     if(i.UUID == prod_seller_UUID):
        request.products.add(prod_id=prod_id, name=prod_name, category=prod_category, quantity=prod_quantity,
                              description=prod_description, price=prod_price_per_unit, seller_address=prod_seller_address,
                              seller_UUID=prod_seller_UUID, rating=prod_rating)
                
        #     return market_pb2.void()
        
        # print("Seller not found")   #Error message

    def deleteProduct(self, request, context): 
        for product in request.products:
            if(product.prod_id == request.prod_id):
                request.products.remove(product)
                return market_pb2.void()
        print("Product not found")

    def updateProduct(self, request, context):   #need to check the item id first 
        for product in request.products:
            if(product.prod_id == request.prod_id):
                product.price = request.price
                product.quantity = request.quantity
                product.seller_address = request.seller_address
                product.description = request.description
                product.id = request.prod_id
                return market_pb2.void()
        print("Product not found")
 
 
    def displayProducts(self, request, context):   #for the seller to view the product(DisplaySellerItem)
        for product in request.products:
            if(product.seller_UUID == request.seller_UUID):
                print(product.name, product.price, product.quantity, product.description, product.rating)
                print("/n")
        

#------------------------Buyer---------------------------------

    def registerBuyer(self, request, context):
        seller_name = request.name
        seller_address = request.address
        seller_contact = request.contact
        seller_email = request.email
        seller_id = str(uuid.uuid1())
        seller_wishlist = []

        request.buyers.add(name=seller_name, address=seller_address, contact=seller_contact,
                            email=seller_email, id=seller_id, wishlist=seller_wishlist)

    def searchItem(self, request, context):
        return super().searchProduct(request, context)
    
    def viewProduct(self, request, context):   #for the customer to view the product(SearchItem one)
        for product in request.products:
            print(product.name)

    def rateProduct(self, request, context):   #for the customer to rate the product 
        if(request.rating > 5 or request.rating < 0):      #in UUID is getting used and address is just to not be NULL
            print("Invalid rating")
            return market_pb2.void()
        
        if(request.address == ""):
            print("Address not found")
            return market_pb2.void()

        for product in request.products:
            if(product.prod_id == request.prod_id):
                product.rating = request.rating
                return market_pb2.void()
        print("Product not found")

    def addtoWishlist(self, request, context):
        return super().addtoWishlist(request, context)

#------------------------buyer&seller---------------------------------
    def messaging(self, request, context):
        print("Clients message" + str(request))
        return market_pb2.serverMessage(message='{0} {1}!'.format(request.greeting, request.name))

        #  return super().addProduct(request, context)
        #  return super().viewProduct(request, context)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
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
