from gogoproto import gogo_pb2 as _gogo_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Scope(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    invalid: _ClassVar[Scope]
    deployment: _ClassVar[Scope]
    bid: _ClassVar[Scope]
invalid: Scope
deployment: Scope
bid: Scope

class Account(_message.Message):
    __slots__ = ("scope", "xid")
    SCOPE_FIELD_NUMBER: _ClassVar[int]
    XID_FIELD_NUMBER: _ClassVar[int]
    scope: Scope
    xid: str
    def __init__(self, scope: _Optional[_Union[Scope, str]] = ..., xid: _Optional[str] = ...) -> None: ...

class Payment(_message.Message):
    __slots__ = ("aid", "xid")
    AID_FIELD_NUMBER: _ClassVar[int]
    XID_FIELD_NUMBER: _ClassVar[int]
    aid: Account
    xid: str
    def __init__(self, aid: _Optional[_Union[Account, _Mapping]] = ..., xid: _Optional[str] = ...) -> None: ...
