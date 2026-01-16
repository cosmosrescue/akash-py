from gogoproto import gogo_pb2 as _gogo_pb2
from akash.manifest.v2beta3 import service_pb2 as _service_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Group(_message.Message):
    __slots__ = ("name", "services")
    NAME_FIELD_NUMBER: _ClassVar[int]
    SERVICES_FIELD_NUMBER: _ClassVar[int]
    name: str
    services: _containers.RepeatedCompositeFieldContainer[_service_pb2.Service]
    def __init__(self, name: _Optional[str] = ..., services: _Optional[_Iterable[_Union[_service_pb2.Service, _Mapping]]] = ...) -> None: ...
