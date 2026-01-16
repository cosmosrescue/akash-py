from gogoproto import gogo_pb2 as _gogo_pb2
from akash.inventory.v1 import node_pb2 as _node_pb2
from akash.inventory.v1 import storage_pb2 as _storage_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Cluster(_message.Message):
    __slots__ = ("nodes", "storage")
    NODES_FIELD_NUMBER: _ClassVar[int]
    STORAGE_FIELD_NUMBER: _ClassVar[int]
    nodes: _containers.RepeatedCompositeFieldContainer[_node_pb2.Node]
    storage: _containers.RepeatedCompositeFieldContainer[_storage_pb2.Storage]
    def __init__(self, nodes: _Optional[_Iterable[_Union[_node_pb2.Node, _Mapping]]] = ..., storage: _Optional[_Iterable[_Union[_storage_pb2.Storage, _Mapping]]] = ...) -> None: ...
