from gogoproto import gogo_pb2 as _gogo_pb2
from akash.base.attributes.v1 import attribute_pb2 as _attribute_pb2
from akash.deployment.v1beta4 import resourceunit_pb2 as _resourceunit_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GroupSpec(_message.Message):
    __slots__ = ("name", "requirements", "resources")
    NAME_FIELD_NUMBER: _ClassVar[int]
    REQUIREMENTS_FIELD_NUMBER: _ClassVar[int]
    RESOURCES_FIELD_NUMBER: _ClassVar[int]
    name: str
    requirements: _attribute_pb2.PlacementRequirements
    resources: _containers.RepeatedCompositeFieldContainer[_resourceunit_pb2.ResourceUnit]
    def __init__(self, name: _Optional[str] = ..., requirements: _Optional[_Union[_attribute_pb2.PlacementRequirements, _Mapping]] = ..., resources: _Optional[_Iterable[_Union[_resourceunit_pb2.ResourceUnit, _Mapping]]] = ...) -> None: ...
