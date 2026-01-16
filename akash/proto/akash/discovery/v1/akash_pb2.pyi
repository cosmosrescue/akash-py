from akash.discovery.v1 import client_info_pb2 as _client_info_pb2
from gogoproto import gogo_pb2 as _gogo_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Akash(_message.Message):
    __slots__ = ("client_info",)
    CLIENT_INFO_FIELD_NUMBER: _ClassVar[int]
    client_info: _client_info_pb2.ClientInfo
    def __init__(self, client_info: _Optional[_Union[_client_info_pb2.ClientInfo, _Mapping]] = ...) -> None: ...
