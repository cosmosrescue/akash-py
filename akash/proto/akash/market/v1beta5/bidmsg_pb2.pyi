from gogoproto import gogo_pb2 as _gogo_pb2
from cosmos.base.v1beta1 import coin_pb2 as _coin_pb2
from akash.market.v1beta5 import resourcesoffer_pb2 as _resourcesoffer_pb2
from akash.market.v1 import bid_pb2 as _bid_pb2
from akash.base.deposit.v1 import deposit_pb2 as _deposit_pb2
from akash.market.v1 import types_pb2 as _types_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MsgCreateBid(_message.Message):
    __slots__ = ("id", "price", "deposit", "resources_offer")
    ID_FIELD_NUMBER: _ClassVar[int]
    PRICE_FIELD_NUMBER: _ClassVar[int]
    DEPOSIT_FIELD_NUMBER: _ClassVar[int]
    RESOURCES_OFFER_FIELD_NUMBER: _ClassVar[int]
    id: _bid_pb2.BidID
    price: _coin_pb2.DecCoin
    deposit: _deposit_pb2.Deposit
    resources_offer: _containers.RepeatedCompositeFieldContainer[_resourcesoffer_pb2.ResourceOffer]
    def __init__(self, id: _Optional[_Union[_bid_pb2.BidID, _Mapping]] = ..., price: _Optional[_Union[_coin_pb2.DecCoin, _Mapping]] = ..., deposit: _Optional[_Union[_deposit_pb2.Deposit, _Mapping]] = ..., resources_offer: _Optional[_Iterable[_Union[_resourcesoffer_pb2.ResourceOffer, _Mapping]]] = ...) -> None: ...

class MsgCreateBidResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class MsgCloseBid(_message.Message):
    __slots__ = ("id", "reason")
    ID_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    id: _bid_pb2.BidID
    reason: _types_pb2.LeaseClosedReason
    def __init__(self, id: _Optional[_Union[_bid_pb2.BidID, _Mapping]] = ..., reason: _Optional[_Union[_types_pb2.LeaseClosedReason, str]] = ...) -> None: ...

class MsgCloseBidResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...
