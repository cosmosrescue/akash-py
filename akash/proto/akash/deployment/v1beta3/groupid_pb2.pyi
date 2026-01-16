from gogoproto import gogo_pb2 as _gogo_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class GroupID(_message.Message):
    __slots__ = ("owner", "dseq", "gseq")
    OWNER_FIELD_NUMBER: _ClassVar[int]
    DSEQ_FIELD_NUMBER: _ClassVar[int]
    GSEQ_FIELD_NUMBER: _ClassVar[int]
    owner: str
    dseq: int
    gseq: int
    def __init__(self, owner: _Optional[str] = ..., dseq: _Optional[int] = ..., gseq: _Optional[int] = ...) -> None: ...
