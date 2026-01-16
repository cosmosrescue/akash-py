from gogoproto import gogo_pb2 as _gogo_pb2
from cosmos.base.v1beta1 import coin_pb2 as _coin_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Params(_message.Message):
    __slots__ = ("bid_min_deposit", "order_max_bids")
    BID_MIN_DEPOSIT_FIELD_NUMBER: _ClassVar[int]
    ORDER_MAX_BIDS_FIELD_NUMBER: _ClassVar[int]
    bid_min_deposit: _coin_pb2.Coin
    order_max_bids: int
    def __init__(self, bid_min_deposit: _Optional[_Union[_coin_pb2.Coin, _Mapping]] = ..., order_max_bids: _Optional[int] = ...) -> None: ...
