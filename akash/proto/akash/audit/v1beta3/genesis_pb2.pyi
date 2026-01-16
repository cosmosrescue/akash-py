from gogoproto import gogo_pb2 as _gogo_pb2
from akash.audit.v1beta3 import audit_pb2 as _audit_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GenesisState(_message.Message):
    __slots__ = ("attributes",)
    ATTRIBUTES_FIELD_NUMBER: _ClassVar[int]
    attributes: _containers.RepeatedCompositeFieldContainer[_audit_pb2.AuditedAttributes]
    def __init__(self, attributes: _Optional[_Iterable[_Union[_audit_pb2.AuditedAttributes, _Mapping]]] = ...) -> None: ...
