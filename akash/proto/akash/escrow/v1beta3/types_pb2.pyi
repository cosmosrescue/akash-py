from gogoproto import gogo_pb2 as _gogo_pb2
from cosmos.base.v1beta1 import coin_pb2 as _coin_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class AccountID(_message.Message):
    __slots__ = ("scope", "xid")
    SCOPE_FIELD_NUMBER: _ClassVar[int]
    XID_FIELD_NUMBER: _ClassVar[int]
    scope: str
    xid: str
    def __init__(self, scope: _Optional[str] = ..., xid: _Optional[str] = ...) -> None: ...

class Account(_message.Message):
    __slots__ = ("id", "owner", "state", "balance", "transferred", "settled_at", "depositor", "funds")
    class State(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        invalid: _ClassVar[Account.State]
        open: _ClassVar[Account.State]
        closed: _ClassVar[Account.State]
        overdrawn: _ClassVar[Account.State]
    invalid: Account.State
    open: Account.State
    closed: Account.State
    overdrawn: Account.State
    ID_FIELD_NUMBER: _ClassVar[int]
    OWNER_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    BALANCE_FIELD_NUMBER: _ClassVar[int]
    TRANSFERRED_FIELD_NUMBER: _ClassVar[int]
    SETTLED_AT_FIELD_NUMBER: _ClassVar[int]
    DEPOSITOR_FIELD_NUMBER: _ClassVar[int]
    FUNDS_FIELD_NUMBER: _ClassVar[int]
    id: AccountID
    owner: str
    state: Account.State
    balance: _coin_pb2.DecCoin
    transferred: _coin_pb2.DecCoin
    settled_at: int
    depositor: str
    funds: _coin_pb2.DecCoin
    def __init__(self, id: _Optional[_Union[AccountID, _Mapping]] = ..., owner: _Optional[str] = ..., state: _Optional[_Union[Account.State, str]] = ..., balance: _Optional[_Union[_coin_pb2.DecCoin, _Mapping]] = ..., transferred: _Optional[_Union[_coin_pb2.DecCoin, _Mapping]] = ..., settled_at: _Optional[int] = ..., depositor: _Optional[str] = ..., funds: _Optional[_Union[_coin_pb2.DecCoin, _Mapping]] = ...) -> None: ...

class FractionalPayment(_message.Message):
    __slots__ = ("account_id", "payment_id", "owner", "state", "rate", "balance", "withdrawn")
    class State(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        invalid: _ClassVar[FractionalPayment.State]
        open: _ClassVar[FractionalPayment.State]
        closed: _ClassVar[FractionalPayment.State]
        overdrawn: _ClassVar[FractionalPayment.State]
    invalid: FractionalPayment.State
    open: FractionalPayment.State
    closed: FractionalPayment.State
    overdrawn: FractionalPayment.State
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    PAYMENT_ID_FIELD_NUMBER: _ClassVar[int]
    OWNER_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    RATE_FIELD_NUMBER: _ClassVar[int]
    BALANCE_FIELD_NUMBER: _ClassVar[int]
    WITHDRAWN_FIELD_NUMBER: _ClassVar[int]
    account_id: AccountID
    payment_id: str
    owner: str
    state: FractionalPayment.State
    rate: _coin_pb2.DecCoin
    balance: _coin_pb2.DecCoin
    withdrawn: _coin_pb2.Coin
    def __init__(self, account_id: _Optional[_Union[AccountID, _Mapping]] = ..., payment_id: _Optional[str] = ..., owner: _Optional[str] = ..., state: _Optional[_Union[FractionalPayment.State, str]] = ..., rate: _Optional[_Union[_coin_pb2.DecCoin, _Mapping]] = ..., balance: _Optional[_Union[_coin_pb2.DecCoin, _Mapping]] = ..., withdrawn: _Optional[_Union[_coin_pb2.Coin, _Mapping]] = ...) -> None: ...
