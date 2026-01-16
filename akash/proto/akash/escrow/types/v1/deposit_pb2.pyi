from cosmos.base.v1beta1 import coin_pb2 as _coin_pb2
from cosmos_proto import cosmos_pb2 as _cosmos_pb2
from gogoproto import gogo_pb2 as _gogo_pb2
from akash.base.deposit.v1 import deposit_pb2 as _deposit_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Depositor(_message.Message):
    __slots__ = ("owner", "height", "source", "balance")
    OWNER_FIELD_NUMBER: _ClassVar[int]
    HEIGHT_FIELD_NUMBER: _ClassVar[int]
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    BALANCE_FIELD_NUMBER: _ClassVar[int]
    owner: str
    height: int
    source: _deposit_pb2.Source
    balance: _coin_pb2.DecCoin
    def __init__(self, owner: _Optional[str] = ..., height: _Optional[int] = ..., source: _Optional[_Union[_deposit_pb2.Source, str]] = ..., balance: _Optional[_Union[_coin_pb2.DecCoin, _Mapping]] = ...) -> None: ...
