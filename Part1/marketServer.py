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
    Sellers=[]
    Products= []
    Users=[]


#------------------------Seller--------------------------------- 
    def registerSeller(self, request, context):
        currAddress = request.uuid
        status = -1
        if currAddress in self.sellerList:
            status = market_pb2.Status.FAILURE
        else:
            self.sellerList[currAddress] = 1
            self.Sellers.append(market_pb2.Seller(address=request.address,UUID=request.uuid))
            status = market_pb2.Status.SUCCESS
        res = market_pb2.registerSellerRes(status = status)
        print(f'seller join request from {request.address} with uuid {request.uuid}')
        return res

    def sellItem(self, request, context):
        id = str(uuid.uuid1())
        product = market_pb2.Product(Product_UUID=id,category=request.Category,name = request.name, price = request.price, quantity=request.quantity,description=request.description,seller_address=request.sellerAddress,seller_UUID=request.sellerUUID)
        request.seller.products.append(product)
        self.Products.append(product)
        res = market_pb2.sellItemRes(productUUID=id,status = market_pb2.Status.SUCCESS)
        print(f'Product with {res.productUUID} has been registered by seller {request.sellerUUID}')
        return request.seller


    def deleteProduct(self, request, context): 
        for product in self.Products:
            if product.Product_UUID == request.Product_UUID:
                if request.seller_address == product.seller_address and request.seller_UUID == product.seller_UUID:
                    self.Products.remove(product)
                    print(f'Deleted item {request.Product_UUID} on request from seller {request.seller_UUID}')
                    print(self.Products)
                    return market_pb2.DeleteItemRes(productUUID=request.Product_UUID,status='SUCCESS')

        print("Product not found")
        return market_pb2.DeleteItemRes(productUUID=request.Product_UUID,status='FAILURE')

    def updateProduct(self, request, context):   #need to check the item id first
        res=None
        for product in self.Products:
            if product.Product_UUID == request.Product_UUID:
                if(request.seller_address==product.seller_address and request.seller_UUID == product.seller_UUID):
                    product.price = request.price
                    product.quantity = request.quantity
                    product.description = request.description
                    res=market_pb2.UpdateItemRes(productUUID=product.Product_UUID,status='SUCCESS')
                    print(f'Product with uuid {product.Product_UUID} has been updated by seller with uuid {request.seller_UUID}')
                    return res
                else:
                    res = market_pb2.UpdateItemRes(productUUID=request.Product_UUID,status= 'FAILURE')
                    print('Incorrect Seller Credentials')
                break
            else:
                res = market_pb2.UpdateItemRes(productUUID=request.Product_UUID, status='FAILURE')
                print("Product not found")

        return res
 
    def displayProducts(self, request, context):   #for the seller to view the product(DisplaySellerItem)

        p = market_pb2.Products(products=[])
        for i in self.Products:
            if i.seller_UUID==request.UUID:
                p.products.append(i)
        return p
        

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
        return market_pb2.void()

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
