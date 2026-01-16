from gogoproto import gogo_pb2 as _gogo_pb2
from cosmos_proto import cosmos_pb2 as _cosmos_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class EventTrustedAuditorCreated(_message.Message):
    __slots__ = ("owner", "auditor")
    OWNER_FIELD_NUMBER: _ClassVar[int]
    AUDITOR_FIELD_NUMBER: _ClassVar[int]
    owner: str
    auditor: str
    def __init__(self, owner: _Optional[str] = ..., auditor: _Optional[str] = ...) -> None: ...

class EventTrustedAuditorDeleted(_message.Message):
    __slots__ = ("owner", "auditor")
    OWNER_FIELD_NUMBER: _ClassVar[int]
    AUDITOR_FIELD_NUMBER: _ClassVar[int]
    owner: str
    auditor: str
    def __init__(self, owner: _Optional[str] = ..., auditor: _Optional[str] = ...) -> None: ...
