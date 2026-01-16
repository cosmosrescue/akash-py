from gogoproto import gogo_pb2 as _gogo_pb2
from cosmos_proto import cosmos_pb2 as _cosmos_pb2
from cosmos.base.v1beta1 import coin_pb2 as _coin_pb2
from akash.escrow.id.v1 import id_pb2 as _id_pb2
from akash.escrow.types.v1 import balance_pb2 as _balance_pb2
from akash.escrow.types.v1 import deposit_pb2 as _deposit_pb2
from akash.escrow.types.v1 import state_pb2 as _state_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class AccountState(_message.Message):
    __slots__ = ("owner", "state", "transferred", "settled_at", "funds", "deposits")
    OWNER_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    TRANSFERRED_FIELD_NUMBER: _ClassVar[int]
    SETTLED_AT_FIELD_NUMBER: _ClassVar[int]
    FUNDS_FIELD_NUMBER: _ClassVar[int]
    DEPOSITS_FIELD_NUMBER: _ClassVar[int]
    owner: str
    state: _state_pb2.State
    transferred: _containers.RepeatedCompositeFieldContainer[_coin_pb2.DecCoin]
    settled_at: int
    funds: _containers.RepeatedCompositeFieldContainer[_balance_pb2.Balance]
    deposits: _containers.RepeatedCompositeFieldContainer[_deposit_pb2.Depositor]
    def __init__(self, owner: _Optional[str] = ..., state: _Optional[_Union[_state_pb2.State, str]] = ..., transferred: _Optional[_Iterable[_Union[_coin_pb2.DecCoin, _Mapping]]] = ..., settled_at: _Optional[int] = ..., funds: _Optional[_Iterable[_Union[_balance_pb2.Balance, _Mapping]]] = ..., deposits: _Optional[_Iterable[_Union[_deposit_pb2.Depositor, _Mapping]]] = ...) -> None: ...

class Account(_message.Message):
    __slots__ = ("id", "state")
    ID_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    id: _id_pb2.Account
    state: AccountState
    def __init__(self, id: _Optional[_Union[_id_pb2.Account, _Mapping]] = ..., state: _Optional[_Union[AccountState, _Mapping]] = ...) -> None: ...
