from gogoproto import gogo_pb2 as _gogo_pb2
from akash.base.attributes.v1 import attribute_pb2 as _attribute_pb2
from k8s.io.apimachinery.pkg.api.resource import generated_pb2 as _generated_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ResourcePair(_message.Message):
    __slots__ = ("allocatable", "allocated", "attributes", "capacity")
    ALLOCATABLE_FIELD_NUMBER: _ClassVar[int]
    ALLOCATED_FIELD_NUMBER: _ClassVar[int]
    ATTRIBUTES_FIELD_NUMBER: _ClassVar[int]
    CAPACITY_FIELD_NUMBER: _ClassVar[int]
    allocatable: _generated_pb2.Quantity
    allocated: _generated_pb2.Quantity
    attributes: _containers.RepeatedCompositeFieldContainer[_attribute_pb2.Attribute]
    capacity: _generated_pb2.Quantity
    def __init__(self, allocatable: _Optional[_Union[_generated_pb2.Quantity, _Mapping]] = ..., allocated: _Optional[_Union[_generated_pb2.Quantity, _Mapping]] = ..., attributes: _Optional[_Iterable[_Union[_attribute_pb2.Attribute, _Mapping]]] = ..., capacity: _Optional[_Union[_generated_pb2.Quantity, _Mapping]] = ...) -> None: ...
