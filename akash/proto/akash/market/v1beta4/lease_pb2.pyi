from gogoproto import gogo_pb2 as _gogo_pb2
from cosmos.base.v1beta1 import coin_pb2 as _coin_pb2
from akash.market.v1beta4 import bid_pb2 as _bid_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class LeaseID(_message.Message):
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

class Lease(_message.Message):
    __slots__ = ("lease_id", "state", "price", "created_at", "closed_on")
    class State(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        invalid: _ClassVar[Lease.State]
        active: _ClassVar[Lease.State]
        insufficient_funds: _ClassVar[Lease.State]
        closed: _ClassVar[Lease.State]
    invalid: Lease.State
    active: Lease.State
    insufficient_funds: Lease.State
    closed: Lease.State
    LEASE_ID_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    PRICE_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    CLOSED_ON_FIELD_NUMBER: _ClassVar[int]
    lease_id: LeaseID
    state: Lease.State
    price: _coin_pb2.DecCoin
    created_at: int
    closed_on: int
    def __init__(self, lease_id: _Optional[_Union[LeaseID, _Mapping]] = ..., state: _Optional[_Union[Lease.State, str]] = ..., price: _Optional[_Union[_coin_pb2.DecCoin, _Mapping]] = ..., created_at: _Optional[int] = ..., closed_on: _Optional[int] = ...) -> None: ...

class LeaseFilters(_message.Message):
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

class MsgCreateLease(_message.Message):
    __slots__ = ("bid_id",)
    BID_ID_FIELD_NUMBER: _ClassVar[int]
    bid_id: _bid_pb2.BidID
    def __init__(self, bid_id: _Optional[_Union[_bid_pb2.BidID, _Mapping]] = ...) -> None: ...

class MsgCreateLeaseResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class MsgWithdrawLease(_message.Message):
    __slots__ = ("bid_id",)
    BID_ID_FIELD_NUMBER: _ClassVar[int]
    bid_id: LeaseID
    def __init__(self, bid_id: _Optional[_Union[LeaseID, _Mapping]] = ...) -> None: ...

class MsgWithdrawLeaseResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class MsgCloseLease(_message.Message):
    __slots__ = ("lease_id",)
    LEASE_ID_FIELD_NUMBER: _ClassVar[int]
    lease_id: LeaseID
    def __init__(self, lease_id: _Optional[_Union[LeaseID, _Mapping]] = ...) -> None: ...

class MsgCloseLeaseResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...
