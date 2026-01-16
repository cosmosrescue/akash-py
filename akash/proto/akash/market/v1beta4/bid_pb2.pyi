from gogoproto import gogo_pb2 as _gogo_pb2
from cosmos.base.v1beta1 import coin_pb2 as _coin_pb2
from akash.base.v1beta3 import resources_pb2 as _resources_pb2
from akash.market.v1beta4 import order_pb2 as _order_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ResourceOffer(_message.Message):
    __slots__ = ("resources", "count")
    RESOURCES_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    resources: _resources_pb2.Resources
    count: int
    def __init__(self, resources: _Optional[_Union[_resources_pb2.Resources, _Mapping]] = ..., count: _Optional[int] = ...) -> None: ...

class MsgCreateBid(_message.Message):
    __slots__ = ("order", "provider", "price", "deposit", "resources_offer")
    ORDER_FIELD_NUMBER: _ClassVar[int]
    PROVIDER_FIELD_NUMBER: _ClassVar[int]
    PRICE_FIELD_NUMBER: _ClassVar[int]
    DEPOSIT_FIELD_NUMBER: _ClassVar[int]
    RESOURCES_OFFER_FIELD_NUMBER: _ClassVar[int]
    order: _order_pb2.OrderID
    provider: str
    price: _coin_pb2.DecCoin
    deposit: _coin_pb2.Coin
    resources_offer: _containers.RepeatedCompositeFieldContainer[ResourceOffer]
    def __init__(self, order: _Optional[_Union[_order_pb2.OrderID, _Mapping]] = ..., provider: _Optional[str] = ..., price: _Optional[_Union[_coin_pb2.DecCoin, _Mapping]] = ..., deposit: _Optional[_Union[_coin_pb2.Coin, _Mapping]] = ..., resources_offer: _Optional[_Iterable[_Union[ResourceOffer, _Mapping]]] = ...) -> None: ...

class MsgCreateBidResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class MsgCloseBid(_message.Message):
    __slots__ = ("bid_id",)
    BID_ID_FIELD_NUMBER: _ClassVar[int]
    bid_id: BidID
    def __init__(self, bid_id: _Optional[_Union[BidID, _Mapping]] = ...) -> None: ...

class MsgCloseBidResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class BidID(_message.Message):
    __slots__ = ("owner", "dseq", "gseq", "oseq", "provider")
    OWNER_FIELD_NUMBER: _ClassVar[int]
    DSEQ_FIELD_NUMBER: _ClassVar[int]
    GSEQ_FIELD_NUMBER: _ClassVar[int]
    OSEQ_FIELD_NUMBER: _ClassVar[int]
    PROVIDER_FIELD_NUMBER: _ClassVar[int]
    owner: str
    dseq: int
    gseq: int
    oseq: int
    provider: str
    def __init__(self, owner: _Optional[str] = ..., dseq: _Optional[int] = ..., gseq: _Optional[int] = ..., oseq: _Optional[int] = ..., provider: _Optional[str] = ...) -> None: ...

class Bid(_message.Message):
    __slots__ = ("bid_id", "state", "price", "created_at", "resources_offer")
    class State(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        invalid: _ClassVar[Bid.State]
        open: _ClassVar[Bid.State]
        active: _ClassVar[Bid.State]
        lost: _ClassVar[Bid.State]
        closed: _ClassVar[Bid.State]
    invalid: Bid.State
    open: Bid.State
    active: Bid.State
    lost: Bid.State
    closed: Bid.State
    BID_ID_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    PRICE_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    RESOURCES_OFFER_FIELD_NUMBER: _ClassVar[int]
    bid_id: BidID
    state: Bid.State
    price: _coin_pb2.DecCoin
    created_at: int
    resources_offer: _containers.RepeatedCompositeFieldContainer[ResourceOffer]
    def __init__(self, bid_id: _Optional[_Union[BidID, _Mapping]] = ..., state: _Optional[_Union[Bid.State, str]] = ..., price: _Optional[_Union[_coin_pb2.DecCoin, _Mapping]] = ..., created_at: _Optional[int] = ..., resources_offer: _Optional[_Iterable[_Union[ResourceOffer, _Mapping]]] = ...) -> None: ...

class BidFilters(_message.Message):
    __slots__ = ("owner", "dseq", "gseq", "oseq", "provider", "state")
    OWNER_FIELD_NUMBER: _ClassVar[int]
    DSEQ_FIELD_NUMBER: _ClassVar[int]
    GSEQ_FIELD_NUMBER: _ClassVar[int]
    OSEQ_FIELD_NUMBER: _ClassVar[int]
    PROVIDER_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    owner: str
    dseq: int
    gseq: int
    oseq: int
    provider: str
    state: str
    def __init__(self, owner: _Optional[str] = ..., dseq: _Optional[int] = ..., gseq: _Optional[int] = ..., oseq: _Optional[int] = ..., provider: _Optional[str] = ..., state: _Optional[str] = ...) -> None: ...
