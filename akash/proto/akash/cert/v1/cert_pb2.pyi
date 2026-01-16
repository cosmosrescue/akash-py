from gogoproto import gogo_pb2 as _gogo_pb2
from cosmos_proto import cosmos_pb2 as _cosmos_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class State(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    invalid: _ClassVar[State]
    valid: _ClassVar[State]
    revoked: _ClassVar[State]
invalid: State
valid: State
revoked: State

class ID(_message.Message):
    __slots__ = ("owner", "serial")
    OWNER_FIELD_NUMBER: _ClassVar[int]
    SERIAL_FIELD_NUMBER: _ClassVar[int]
    owner: str
    serial: str
    def __init__(self, owner: _Optional[str] = ..., serial: _Optional[str] = ...) -> None: ...

class Certificate(_message.Message):
    __slots__ = ("state", "cert", "pubkey")
    STATE_FIELD_NUMBER: _ClassVar[int]
    CERT_FIELD_NUMBER: _ClassVar[int]
    PUBKEY_FIELD_NUMBER: _ClassVar[int]
    state: State
    cert: bytes
    pubkey: bytes
    def __init__(self, state: _Optional[_Union[State, str]] = ..., cert: _Optional[bytes] = ..., pubkey: _Optional[bytes] = ...) -> None: ...
