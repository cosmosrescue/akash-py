from gogoproto import gogo_pb2 as _gogo_pb2
from google.api import annotations_pb2 as _annotations_pb2
from cosmos.base.query.v1beta1 import pagination_pb2 as _pagination_pb2
from akash.escrow.v1beta3 import types_pb2 as _types_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class QueryAccountsRequest(_message.Message):
    __slots__ = ("scope", "xid", "owner", "state", "pagination")
    SCOPE_FIELD_NUMBER: _ClassVar[int]
    XID_FIELD_NUMBER: _ClassVar[int]
    OWNER_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    scope: str
    xid: str
    owner: str
    state: str
    pagination: _pagination_pb2.PageRequest
    def __init__(self, scope: _Optional[str] = ..., xid: _Optional[str] = ..., owner: _Optional[str] = ..., state: _Optional[str] = ..., pagination: _Optional[_Union[_pagination_pb2.PageRequest, _Mapping]] = ...) -> None: ...

class QueryAccountsResponse(_message.Message):
    __slots__ = ("accounts", "pagination")
    ACCOUNTS_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    accounts: _containers.RepeatedCompositeFieldContainer[_types_pb2.Account]
    pagination: _pagination_pb2.PageResponse
    def __init__(self, accounts: _Optional[_Iterable[_Union[_types_pb2.Account, _Mapping]]] = ..., pagination: _Optional[_Union[_pagination_pb2.PageResponse, _Mapping]] = ...) -> None: ...

class QueryPaymentsRequest(_message.Message):
    __slots__ = ("scope", "xid", "id", "owner", "state", "pagination")
    SCOPE_FIELD_NUMBER: _ClassVar[int]
    XID_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    OWNER_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    scope: str
    xid: str
    id: str
    owner: str
    state: str
    pagination: _pagination_pb2.PageRequest
    def __init__(self, scope: _Optional[str] = ..., xid: _Optional[str] = ..., id: _Optional[str] = ..., owner: _Optional[str] = ..., state: _Optional[str] = ..., pagination: _Optional[_Union[_pagination_pb2.PageRequest, _Mapping]] = ...) -> None: ...

class QueryPaymentsResponse(_message.Message):
    __slots__ = ("payments", "pagination")
    PAYMENTS_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    payments: _containers.RepeatedCompositeFieldContainer[_types_pb2.FractionalPayment]
    pagination: _pagination_pb2.PageResponse
    def __init__(self, payments: _Optional[_Iterable[_Union[_types_pb2.FractionalPayment, _Mapping]]] = ..., pagination: _Optional[_Union[_pagination_pb2.PageResponse, _Mapping]] = ...) -> None: ...
