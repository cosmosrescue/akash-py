from gogoproto import gogo_pb2 as _gogo_pb2
from cosmos_proto import cosmos_pb2 as _cosmos_pb2
from cosmos.base.v1beta1 import coin_pb2 as _coin_pb2
from akash.market.v1 import types_pb2 as _types_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class LeaseID(_message.Message):
    __slots__ = ("owner", "dseq", "gseq", "oseq", "provider", "bseq")
    OWNER_FIELD_NUMBER: _ClassVar[int]
    DSEQ_FIELD_NUMBER: _ClassVar[int]
    GSEQ_FIELD_NUMBER: _ClassVar[int]
    OSEQ_FIELD_NUMBER: _ClassVar[int]
    PROVIDER_FIELD_NUMBER: _ClassVar[int]
    BSEQ_FIELD_NUMBER: _ClassVar[int]
    owner: str
    dseq: int
    gseq: int
    oseq: int
    provider: str
    bseq: int
    def __init__(self, owner: _Optional[str] = ..., dseq: _Optional[int] = ..., gseq: _Optional[int] = ..., oseq: _Optional[int] = ..., provider: _Optional[str] = ..., bseq: _Optional[int] = ...) -> None: ...

class Lease(_message.Message):
    __slots__ = ("id", "state", "price", "created_at", "closed_on", "reason")
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
    ID_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    PRICE_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    CLOSED_ON_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    id: LeaseID
    state: Lease.State
    price: _coin_pb2.DecCoin
    created_at: int
    closed_on: int
    reason: _types_pb2.LeaseClosedReason
    def __init__(self, id: _Optional[_Union[LeaseID, _Mapping]] = ..., state: _Optional[_Union[Lease.State, str]] = ..., price: _Optional[_Union[_coin_pb2.DecCoin, _Mapping]] = ..., created_at: _Optional[int] = ..., closed_on: _Optional[int] = ..., reason: _Optional[_Union[_types_pb2.LeaseClosedReason, str]] = ...) -> None: ...
