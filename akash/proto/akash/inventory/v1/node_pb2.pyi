from gogoproto import gogo_pb2 as _gogo_pb2
from akash.inventory.v1 import resources_pb2 as _resources_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class NodeCapabilities(_message.Message):
    __slots__ = ("storage_classes",)
    STORAGE_CLASSES_FIELD_NUMBER: _ClassVar[int]
    storage_classes: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, storage_classes: _Optional[_Iterable[str]] = ...) -> None: ...

class Node(_message.Message):
    __slots__ = ("name", "resources", "capabilities")
    NAME_FIELD_NUMBER: _ClassVar[int]
    RESOURCES_FIELD_NUMBER: _ClassVar[int]
    CAPABILITIES_FIELD_NUMBER: _ClassVar[int]
    name: str
    resources: _resources_pb2.NodeResources
    capabilities: NodeCapabilities
    def __init__(self, name: _Optional[str] = ..., resources: _Optional[_Union[_resources_pb2.NodeResources, _Mapping]] = ..., capabilities: _Optional[_Union[NodeCapabilities, _Mapping]] = ...) -> None: ...
