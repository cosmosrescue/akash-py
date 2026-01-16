from gogoproto import gogo_pb2 as _gogo_pb2
from cosmos_proto import cosmos_pb2 as _cosmos_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class CertificateFilter(_message.Message):
    __slots__ = ("owner", "serial", "state")
    OWNER_FIELD_NUMBER: _ClassVar[int]
    SERIAL_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    owner: str
    serial: str
    state: str
    def __init__(self, owner: _Optional[str] = ..., serial: _Optional[str] = ..., state: _Optional[str] = ...) -> None: ...
