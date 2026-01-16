from gogoproto import gogo_pb2 as _gogo_pb2
from akash.audit.v1 import audit_pb2 as _audit_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GenesisState(_message.Message):
    __slots__ = ("providers",)
    PROVIDERS_FIELD_NUMBER: _ClassVar[int]
    providers: _containers.RepeatedCompositeFieldContainer[_audit_pb2.AuditedProvider]
    def __init__(self, providers: _Optional[_Iterable[_Union[_audit_pb2.AuditedProvider, _Mapping]]] = ...) -> None: ...
