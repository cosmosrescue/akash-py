from gogoproto import gogo_pb2 as _gogo_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class ServiceExposeHTTPOptions(_message.Message):
    __slots__ = ("max_body_size", "read_timeout", "send_timeout", "next_tries", "next_timeout", "next_cases")
    MAX_BODY_SIZE_FIELD_NUMBER: _ClassVar[int]
    READ_TIMEOUT_FIELD_NUMBER: _ClassVar[int]
    SEND_TIMEOUT_FIELD_NUMBER: _ClassVar[int]
    NEXT_TRIES_FIELD_NUMBER: _ClassVar[int]
    NEXT_TIMEOUT_FIELD_NUMBER: _ClassVar[int]
    NEXT_CASES_FIELD_NUMBER: _ClassVar[int]
    max_body_size: int
    read_timeout: int
    send_timeout: int
    next_tries: int
    next_timeout: int
    next_cases: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, max_body_size: _Optional[int] = ..., read_timeout: _Optional[int] = ..., send_timeout: _Optional[int] = ..., next_tries: _Optional[int] = ..., next_timeout: _Optional[int] = ..., next_cases: _Optional[_Iterable[str]] = ...) -> None: ...
