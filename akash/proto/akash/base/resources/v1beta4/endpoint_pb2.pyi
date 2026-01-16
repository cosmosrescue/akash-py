from gogoproto import gogo_pb2 as _gogo_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Endpoint(_message.Message):
    __slots__ = ("kind", "sequence_number")
    class Kind(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        SHARED_HTTP: _ClassVar[Endpoint.Kind]
        RANDOM_PORT: _ClassVar[Endpoint.Kind]
        LEASED_IP: _ClassVar[Endpoint.Kind]
    SHARED_HTTP: Endpoint.Kind
    RANDOM_PORT: Endpoint.Kind
    LEASED_IP: Endpoint.Kind
    KIND_FIELD_NUMBER: _ClassVar[int]
    SEQUENCE_NUMBER_FIELD_NUMBER: _ClassVar[int]
    kind: Endpoint.Kind
    sequence_number: int
    def __init__(self, kind: _Optional[_Union[Endpoint.Kind, str]] = ..., sequence_number: _Optional[int] = ...) -> None: ...
