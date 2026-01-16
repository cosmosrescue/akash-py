from gogoproto import gogo_pb2 as _gogo_pb2
from akash.market.v1 import bid_pb2 as _bid_pb2
from akash.market.v1 import lease_pb2 as _lease_pb2
from akash.market.v1 import types_pb2 as _types_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MsgCreateLease(_message.Message):
    __slots__ = ("bid_id",)
    BID_ID_FIELD_NUMBER: _ClassVar[int]
    bid_id: _bid_pb2.BidID
    def __init__(self, bid_id: _Optional[_Union[_bid_pb2.BidID, _Mapping]] = ...) -> None: ...

class MsgCreateLeaseResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class MsgWithdrawLease(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: _lease_pb2.LeaseID
    def __init__(self, id: _Optional[_Union[_lease_pb2.LeaseID, _Mapping]] = ...) -> None: ...

class MsgWithdrawLeaseResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class MsgCloseLease(_message.Message):
    __slots__ = ("id", "reason")
    ID_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    id: _lease_pb2.LeaseID
    reason: _types_pb2.LeaseClosedReason
    def __init__(self, id: _Optional[_Union[_lease_pb2.LeaseID, _Mapping]] = ..., reason: _Optional[_Union[_types_pb2.LeaseClosedReason, str]] = ...) -> None: ...

class MsgCloseLeaseResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...
