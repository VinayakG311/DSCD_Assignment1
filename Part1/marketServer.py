import grpc
import grpc_tools
import time
import market_pb2
import market_pb2_grpc
import concurrent

class MarketServicer(market_pb2_grpc.MarketServicer) :
  def registerSeller(self, request, context):
    # return super().registerSeller(request, context)
    print(request.UUID)
  
  def viewProduct(self, request, context):
      for product in request.products:
        print(product.name)
  
  def messaging(self,request,context):
    print("Clients message"+str(request))
    return market_pb2.serverMessage(message='{0} {1}!'.format(request.greeting, request.name))

    #  return super().addProduct(request, context)
    #  return super().viewProduct(request, context)
    
def serve():
  server = grpc.server(concurrent.futures.ThreadPoolExecutor(max_workers=2))
  market_pb2_grpc.add_MarketServicer_to_server(MarketServicer(),server)
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