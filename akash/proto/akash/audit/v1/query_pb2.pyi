from gogoproto import gogo_pb2 as _gogo_pb2
from google.api import annotations_pb2 as _annotations_pb2
from cosmos.base.query.v1beta1 import pagination_pb2 as _pagination_pb2
from akash.audit.v1 import audit_pb2 as _audit_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class QueryProvidersResponse(_message.Message):
    __slots__ = ("providers", "pagination")
    PROVIDERS_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    providers: _containers.RepeatedCompositeFieldContainer[_audit_pb2.AuditedProvider]
    pagination: _pagination_pb2.PageResponse
    def __init__(self, providers: _Optional[_Iterable[_Union[_audit_pb2.AuditedProvider, _Mapping]]] = ..., pagination: _Optional[_Union[_pagination_pb2.PageResponse, _Mapping]] = ...) -> None: ...

class QueryProviderRequest(_message.Message):
    __slots__ = ("auditor", "owner")
    AUDITOR_FIELD_NUMBER: _ClassVar[int]
    OWNER_FIELD_NUMBER: _ClassVar[int]
    auditor: str
    owner: str
    def __init__(self, auditor: _Optional[str] = ..., owner: _Optional[str] = ...) -> None: ...

class QueryAllProvidersAttributesRequest(_message.Message):
    __slots__ = ("pagination",)
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    pagination: _pagination_pb2.PageRequest
    def __init__(self, pagination: _Optional[_Union[_pagination_pb2.PageRequest, _Mapping]] = ...) -> None: ...

class QueryProviderAttributesRequest(_message.Message):
    __slots__ = ("owner", "pagination")
    OWNER_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    owner: str
    pagination: _pagination_pb2.PageRequest
    def __init__(self, owner: _Optional[str] = ..., pagination: _Optional[_Union[_pagination_pb2.PageRequest, _Mapping]] = ...) -> None: ...

class QueryProviderAuditorRequest(_message.Message):
    __slots__ = ("auditor", "owner")
    AUDITOR_FIELD_NUMBER: _ClassVar[int]
    OWNER_FIELD_NUMBER: _ClassVar[int]
    auditor: str
    owner: str
    def __init__(self, auditor: _Optional[str] = ..., owner: _Optional[str] = ...) -> None: ...

class QueryAuditorAttributesRequest(_message.Message):
    __slots__ = ("auditor", "pagination")
    AUDITOR_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    auditor: str
    pagination: _pagination_pb2.PageRequest
    def __init__(self, auditor: _Optional[str] = ..., pagination: _Optional[_Union[_pagination_pb2.PageRequest, _Mapping]] = ...) -> None: ...
