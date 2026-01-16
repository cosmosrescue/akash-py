from gogoproto import gogo_pb2 as _gogo_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class ClientInfo(_message.Message):
    __slots__ = ("api_version",)
    API_VERSION_FIELD_NUMBER: _ClassVar[int]
    api_version: str
    def __init__(self, api_version: _Optional[str] = ...) -> None: ...
