import uuid


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