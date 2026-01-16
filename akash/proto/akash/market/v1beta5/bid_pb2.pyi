from gogoproto import gogo_pb2 as _gogo_pb2
from cosmos.base.v1beta1 import coin_pb2 as _coin_pb2
from akash.market.v1beta5 import resourcesoffer_pb2 as _resourcesoffer_pb2
from akash.market.v1 import bid_pb2 as _bid_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Bid(_message.Message):
    __slots__ = ("id", "state", "price", "created_at", "resources_offer")
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
    ID_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    PRICE_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    RESOURCES_OFFER_FIELD_NUMBER: _ClassVar[int]
    id: _bid_pb2.BidID
    state: Bid.State
    price: _coin_pb2.DecCoin
    created_at: int
    resources_offer: _containers.RepeatedCompositeFieldContainer[_resourcesoffer_pb2.ResourceOffer]
    def __init__(self, id: _Optional[_Union[_bid_pb2.BidID, _Mapping]] = ..., state: _Optional[_Union[Bid.State, str]] = ..., price: _Optional[_Union[_coin_pb2.DecCoin, _Mapping]] = ..., created_at: _Optional[int] = ..., resources_offer: _Optional[_Iterable[_Union[_resourcesoffer_pb2.ResourceOffer, _Mapping]]] = ...) -> None: ...
