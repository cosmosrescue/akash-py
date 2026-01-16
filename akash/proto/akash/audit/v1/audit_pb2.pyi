from gogoproto import gogo_pb2 as _gogo_pb2
from akash.base.attributes.v1 import attribute_pb2 as _attribute_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class AuditedProvider(_message.Message):
    __slots__ = ("owner", "auditor", "attributes")
    OWNER_FIELD_NUMBER: _ClassVar[int]
    AUDITOR_FIELD_NUMBER: _ClassVar[int]
    ATTRIBUTES_FIELD_NUMBER: _ClassVar[int]
    owner: str
    auditor: str
    attributes: _containers.RepeatedCompositeFieldContainer[_attribute_pb2.Attribute]
    def __init__(self, owner: _Optional[str] = ..., auditor: _Optional[str] = ..., attributes: _Optional[_Iterable[_Union[_attribute_pb2.Attribute, _Mapping]]] = ...) -> None: ...

class AuditedAttributesStore(_message.Message):
    __slots__ = ("attributes",)
    ATTRIBUTES_FIELD_NUMBER: _ClassVar[int]
    attributes: _containers.RepeatedCompositeFieldContainer[_attribute_pb2.Attribute]
    def __init__(self, attributes: _Optional[_Iterable[_Union[_attribute_pb2.Attribute, _Mapping]]] = ...) -> None: ...

class AttributesFilters(_message.Message):
    __slots__ = ("auditors", "owners")
    AUDITORS_FIELD_NUMBER: _ClassVar[int]
    OWNERS_FIELD_NUMBER: _ClassVar[int]
    auditors: _containers.RepeatedScalarFieldContainer[str]
    owners: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, auditors: _Optional[_Iterable[str]] = ..., owners: _Optional[_Iterable[str]] = ...) -> None: ...
