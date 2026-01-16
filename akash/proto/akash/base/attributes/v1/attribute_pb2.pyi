from gogoproto import gogo_pb2 as _gogo_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Attribute(_message.Message):
    __slots__ = ("key", "value")
    KEY_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    key: str
    value: str
    def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...

class SignedBy(_message.Message):
    __slots__ = ("all_of", "any_of")
    ALL_OF_FIELD_NUMBER: _ClassVar[int]
    ANY_OF_FIELD_NUMBER: _ClassVar[int]
    all_of: _containers.RepeatedScalarFieldContainer[str]
    any_of: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, all_of: _Optional[_Iterable[str]] = ..., any_of: _Optional[_Iterable[str]] = ...) -> None: ...

class PlacementRequirements(_message.Message):
    __slots__ = ("signed_by", "attributes")
    SIGNED_BY_FIELD_NUMBER: _ClassVar[int]
    ATTRIBUTES_FIELD_NUMBER: _ClassVar[int]
    signed_by: SignedBy
    attributes: _containers.RepeatedCompositeFieldContainer[Attribute]
    def __init__(self, signed_by: _Optional[_Union[SignedBy, _Mapping]] = ..., attributes: _Optional[_Iterable[_Union[Attribute, _Mapping]]] = ...) -> None: ...
