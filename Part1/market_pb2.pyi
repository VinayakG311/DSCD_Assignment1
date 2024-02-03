from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Status(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SUCCESS: _ClassVar[Status]
    FAILURE: _ClassVar[Status]

class Category(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ELECTRONIC: _ClassVar[Category]
    FASHION: _ClassVar[Category]
    OTHERS: _ClassVar[Category]
SUCCESS: Status
FAILURE: Status
ELECTRONIC: Category
FASHION: Category
OTHERS: Category

class void(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class Buyer(_message.Message):
    __slots__ = ("UUID", "address")
    UUID_FIELD_NUMBER: _ClassVar[int]
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    UUID: str
    address: str
    def __init__(self, UUID: _Optional[str] = ..., address: _Optional[str] = ...) -> None: ...

class Seller(_message.Message):
    __slots__ = ("UUID", "address", "products")
    UUID_FIELD_NUMBER: _ClassVar[int]
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    PRODUCTS_FIELD_NUMBER: _ClassVar[int]
    UUID: str
    address: str
    products: _containers.RepeatedCompositeFieldContainer[Product]
    def __init__(self, UUID: _Optional[str] = ..., address: _Optional[str] = ..., products: _Optional[_Iterable[_Union[Product, _Mapping]]] = ...) -> None: ...

class Sellers(_message.Message):
    __slots__ = ("sellers",)
    SELLERS_FIELD_NUMBER: _ClassVar[int]
    sellers: _containers.RepeatedCompositeFieldContainer[Seller]
    def __init__(self, sellers: _Optional[_Iterable[_Union[Seller, _Mapping]]] = ...) -> None: ...

class Rate_an_item(_message.Message):
    __slots__ = ("buyer", "rating", "review")
    BUYER_FIELD_NUMBER: _ClassVar[int]
    RATING_FIELD_NUMBER: _ClassVar[int]
    REVIEW_FIELD_NUMBER: _ClassVar[int]
    buyer: Buyer
    rating: int
    review: str
    def __init__(self, buyer: _Optional[_Union[Buyer, _Mapping]] = ..., rating: _Optional[int] = ..., review: _Optional[str] = ...) -> None: ...

class Product(_message.Message):
    __slots__ = ("name", "price", "quantity", "description", "seller_address", "seller_UUID", "seller", "category")
    NAME_FIELD_NUMBER: _ClassVar[int]
    PRICE_FIELD_NUMBER: _ClassVar[int]
    QUANTITY_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    SELLER_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    SELLER_UUID_FIELD_NUMBER: _ClassVar[int]
    SELLER_FIELD_NUMBER: _ClassVar[int]
    CATEGORY_FIELD_NUMBER: _ClassVar[int]
    name: str
    price: float
    quantity: int
    description: str
    seller_address: str
    seller_UUID: str
    seller: Seller
    category: Category
    def __init__(self, name: _Optional[str] = ..., price: _Optional[float] = ..., quantity: _Optional[int] = ..., description: _Optional[str] = ..., seller_address: _Optional[str] = ..., seller_UUID: _Optional[str] = ..., seller: _Optional[_Union[Seller, _Mapping]] = ..., category: _Optional[_Union[Category, str]] = ...) -> None: ...

class Products(_message.Message):
    __slots__ = ("products",)
    PRODUCTS_FIELD_NUMBER: _ClassVar[int]
    products: _containers.RepeatedCompositeFieldContainer[Product]
    def __init__(self, products: _Optional[_Iterable[_Union[Product, _Mapping]]] = ...) -> None: ...

class registerSellerReq(_message.Message):
    __slots__ = ("address", "uuid")
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    UUID_FIELD_NUMBER: _ClassVar[int]
    address: str
    uuid: str
    def __init__(self, address: _Optional[str] = ..., uuid: _Optional[str] = ...) -> None: ...

class registerSellerRes(_message.Message):
    __slots__ = ("status",)
    STATUS_FIELD_NUMBER: _ClassVar[int]
    status: Status
    def __init__(self, status: _Optional[_Union[Status, str]] = ...) -> None: ...

class sellItemReq(_message.Message):
    __slots__ = ("name", "quantity", "description", "sellerAddress", "price", "sellerUUID", "Category")
    NAME_FIELD_NUMBER: _ClassVar[int]
    QUANTITY_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    SELLERADDRESS_FIELD_NUMBER: _ClassVar[int]
    PRICE_FIELD_NUMBER: _ClassVar[int]
    SELLERUUID_FIELD_NUMBER: _ClassVar[int]
    CATEGORY_FIELD_NUMBER: _ClassVar[int]
    name: str
    quantity: int
    description: str
    sellerAddress: str
    price: float
    sellerUUID: str
    Category: Category
    def __init__(self, name: _Optional[str] = ..., quantity: _Optional[int] = ..., description: _Optional[str] = ..., sellerAddress: _Optional[str] = ..., price: _Optional[float] = ..., sellerUUID: _Optional[str] = ..., Category: _Optional[_Union[Category, str]] = ...) -> None: ...

class sellItemRes(_message.Message):
    __slots__ = ("productUUID", "status")
    PRODUCTUUID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    productUUID: str
    status: Status
    def __init__(self, productUUID: _Optional[str] = ..., status: _Optional[_Union[Status, str]] = ...) -> None: ...
