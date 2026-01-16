from gogoproto import gogo_pb2 as _gogo_pb2
from akash.base.v1beta3 import attribute_pb2 as _attribute_pb2
from akash.base.v1beta3 import resourcevalue_pb2 as _resourcevalue_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GPU(_message.Message):
    __slots__ = ("units", "attributes")
    UNITS_FIELD_NUMBER: _ClassVar[int]
    ATTRIBUTES_FIELD_NUMBER: _ClassVar[int]
    units: _resourcevalue_pb2.ResourceValue
    attributes: _containers.RepeatedCompositeFieldContainer[_attribute_pb2.Attribute]
    def __init__(self, units: _Optional[_Union[_resourcevalue_pb2.ResourceValue, _Mapping]] = ..., attributes: _Optional[_Iterable[_Union[_attribute_pb2.Attribute, _Mapping]]] = ...) -> None: ...
