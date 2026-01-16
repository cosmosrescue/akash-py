from gogoproto import gogo_pb2 as _gogo_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from typing import ClassVar as _ClassVar

DESCRIPTOR: _descriptor.FileDescriptor

class State(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    invalid: _ClassVar[State]
    open: _ClassVar[State]
    closed: _ClassVar[State]
    overdrawn: _ClassVar[State]
invalid: State
open: State
closed: State
overdrawn: State
