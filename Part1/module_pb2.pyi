from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Market(_message.Message):
    __slots__ = ("buyers", "sellers", "products")
    BUYERS_FIELD_NUMBER: _ClassVar[int]
    SELLERS_FIELD_NUMBER: _ClassVar[int]
    PRODUCTS_FIELD_NUMBER: _ClassVar[int]
    buyers: _containers.RepeatedCompositeFieldContainer[Buyer]
    sellers: _containers.RepeatedCompositeFieldContainer[Seller]
    products: _containers.RepeatedCompositeFieldContainer[Product]
    def __init__(self, buyers: _Optional[_Iterable[_Union[Buyer, _Mapping]]] = ..., sellers: _Optional[_Iterable[_Union[Seller, _Mapping]]] = ..., products: _Optional[_Iterable[_Union[Product, _Mapping]]] = ...) -> None: ...

class User(_message.Message):
    __slots__ = ("address", "name", "email")
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    address: str
    name: str
    email: str
    def __init__(self, address: _Optional[str] = ..., name: _Optional[str] = ..., email: _Optional[str] = ...) -> None: ...

class Buyer(_message.Message):
    __slots__ = ("user", "wishlist", "reviews", "cart")
    USER_FIELD_NUMBER: _ClassVar[int]
    WISHLIST_FIELD_NUMBER: _ClassVar[int]
    REVIEWS_FIELD_NUMBER: _ClassVar[int]
    CART_FIELD_NUMBER: _ClassVar[int]
    user: User
    wishlist: _containers.RepeatedCompositeFieldContainer[Product]
    reviews: _containers.RepeatedCompositeFieldContainer[Rate_an_item]
    cart: _containers.RepeatedCompositeFieldContainer[Product]
    def __init__(self, user: _Optional[_Union[User, _Mapping]] = ..., wishlist: _Optional[_Iterable[_Union[Product, _Mapping]]] = ..., reviews: _Optional[_Iterable[_Union[Rate_an_item, _Mapping]]] = ..., cart: _Optional[_Iterable[_Union[Product, _Mapping]]] = ...) -> None: ...

class Seller(_message.Message):
    __slots__ = ("user", "UUID", "products")
    USER_FIELD_NUMBER: _ClassVar[int]
    UUID_FIELD_NUMBER: _ClassVar[int]
    PRODUCTS_FIELD_NUMBER: _ClassVar[int]
    user: User
    UUID: str
    products: _containers.RepeatedCompositeFieldContainer[Product]
    def __init__(self, user: _Optional[_Union[User, _Mapping]] = ..., UUID: _Optional[str] = ..., products: _Optional[_Iterable[_Union[Product, _Mapping]]] = ...) -> None: ...

class Rate_an_item(_message.Message):
    __slots__ = ("buyer", "seller", "rating", "review")
    BUYER_FIELD_NUMBER: _ClassVar[int]
    SELLER_FIELD_NUMBER: _ClassVar[int]
    RATING_FIELD_NUMBER: _ClassVar[int]
    REVIEW_FIELD_NUMBER: _ClassVar[int]
    buyer: Buyer
    seller: Seller
    rating: int
    review: str
    def __init__(self, buyer: _Optional[_Union[Buyer, _Mapping]] = ..., seller: _Optional[_Union[Seller, _Mapping]] = ..., rating: _Optional[int] = ..., review: _Optional[str] = ...) -> None: ...

class Product(_message.Message):
    __slots__ = ("name", "price", "quantity", "description", "seller_address", "seller_UUID", "reviews")
    class Category(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        ELECTRONIC: _ClassVar[Product.Category]
        FASHION: _ClassVar[Product.Category]
        OTHERS: _ClassVar[Product.Category]
    ELECTRONIC: Product.Category
    FASHION: Product.Category
    OTHERS: Product.Category
    NAME_FIELD_NUMBER: _ClassVar[int]
    PRICE_FIELD_NUMBER: _ClassVar[int]
    QUANTITY_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    SELLER_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    SELLER_UUID_FIELD_NUMBER: _ClassVar[int]
    REVIEWS_FIELD_NUMBER: _ClassVar[int]
    name: str
    price: float
    quantity: int
    description: str
    seller_address: str
    seller_UUID: str
    reviews: _containers.RepeatedCompositeFieldContainer[Rate_an_item]
    def __init__(self, name: _Optional[str] = ..., price: _Optional[float] = ..., quantity: _Optional[int] = ..., description: _Optional[str] = ..., seller_address: _Optional[str] = ..., seller_UUID: _Optional[str] = ..., reviews: _Optional[_Iterable[_Union[Rate_an_item, _Mapping]]] = ...) -> None: ...
