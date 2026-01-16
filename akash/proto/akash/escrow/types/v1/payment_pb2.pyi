from cosmos.base.v1beta1 import coin_pb2 as _coin_pb2
from cosmos_proto import cosmos_pb2 as _cosmos_pb2
from gogoproto import gogo_pb2 as _gogo_pb2
from akash.escrow.id.v1 import id_pb2 as _id_pb2
from akash.escrow.types.v1 import state_pb2 as _state_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class PaymentState(_message.Message):
    __slots__ = ("owner", "state", "rate", "balance", "unsettled", "withdrawn")
    OWNER_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    RATE_FIELD_NUMBER: _ClassVar[int]
    BALANCE_FIELD_NUMBER: _ClassVar[int]
    UNSETTLED_FIELD_NUMBER: _ClassVar[int]
    WITHDRAWN_FIELD_NUMBER: _ClassVar[int]
    owner: str
    state: _state_pb2.State
    rate: _coin_pb2.DecCoin
    balance: _coin_pb2.DecCoin
    unsettled: _coin_pb2.DecCoin
    withdrawn: _coin_pb2.Coin
    def __init__(self, owner: _Optional[str] = ..., state: _Optional[_Union[_state_pb2.State, str]] = ..., rate: _Optional[_Union[_coin_pb2.DecCoin, _Mapping]] = ..., balance: _Optional[_Union[_coin_pb2.DecCoin, _Mapping]] = ..., unsettled: _Optional[_Union[_coin_pb2.DecCoin, _Mapping]] = ..., withdrawn: _Optional[_Union[_coin_pb2.Coin, _Mapping]] = ...) -> None: ...

class Payment(_message.Message):
    __slots__ = ("id", "state")
    ID_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    id: _id_pb2.Payment
    state: PaymentState
    def __init__(self, id: _Optional[_Union[_id_pb2.Payment, _Mapping]] = ..., state: _Optional[_Union[PaymentState, _Mapping]] = ...) -> None: ...
