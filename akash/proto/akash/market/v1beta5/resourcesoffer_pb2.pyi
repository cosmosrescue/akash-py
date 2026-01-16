from gogoproto import gogo_pb2 as _gogo_pb2
from akash.base.resources.v1beta4 import resources_pb2 as _resources_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ResourceOffer(_message.Message):
    __slots__ = ("resources", "count")
    RESOURCES_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    resources: _resources_pb2.Resources
    count: int
    def __init__(self, resources: _Optional[_Union[_resources_pb2.Resources, _Mapping]] = ..., count: _Optional[int] = ...) -> None: ...
