from gogoproto import gogo_pb2 as _gogo_pb2
from google.api import annotations_pb2 as _annotations_pb2
from cosmos.base.query.v1beta1 import pagination_pb2 as _pagination_pb2
from akash.escrow.types.v1 import account_pb2 as _account_pb2
from akash.escrow.types.v1 import payment_pb2 as _payment_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class QueryAccountsRequest(_message.Message):
    __slots__ = ("state", "xid", "pagination")
    STATE_FIELD_NUMBER: _ClassVar[int]
    XID_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    state: str
    xid: str
    pagination: _pagination_pb2.PageRequest
    def __init__(self, state: _Optional[str] = ..., xid: _Optional[str] = ..., pagination: _Optional[_Union[_pagination_pb2.PageRequest, _Mapping]] = ...) -> None: ...

class QueryAccountsResponse(_message.Message):
    __slots__ = ("accounts", "pagination")
    ACCOUNTS_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    accounts: _containers.RepeatedCompositeFieldContainer[_account_pb2.Account]
    pagination: _pagination_pb2.PageResponse
    def __init__(self, accounts: _Optional[_Iterable[_Union[_account_pb2.Account, _Mapping]]] = ..., pagination: _Optional[_Union[_pagination_pb2.PageResponse, _Mapping]] = ...) -> None: ...

class QueryPaymentsRequest(_message.Message):
    __slots__ = ("state", "xid", "pagination")
    STATE_FIELD_NUMBER: _ClassVar[int]
    XID_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    state: str
    xid: str
    pagination: _pagination_pb2.PageRequest
    def __init__(self, state: _Optional[str] = ..., xid: _Optional[str] = ..., pagination: _Optional[_Union[_pagination_pb2.PageRequest, _Mapping]] = ...) -> None: ...

class QueryPaymentsResponse(_message.Message):
    __slots__ = ("payments", "pagination")
    PAYMENTS_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    payments: _containers.RepeatedCompositeFieldContainer[_payment_pb2.Payment]
    pagination: _pagination_pb2.PageResponse
    def __init__(self, payments: _Optional[_Iterable[_Union[_payment_pb2.Payment, _Mapping]]] = ..., pagination: _Optional[_Union[_pagination_pb2.PageResponse, _Mapping]] = ...) -> None: ...
