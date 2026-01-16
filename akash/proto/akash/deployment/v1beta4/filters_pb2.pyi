from gogoproto import gogo_pb2 as _gogo_pb2
from cosmos_proto import cosmos_pb2 as _cosmos_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class DeploymentFilters(_message.Message):
    __slots__ = ("owner", "dseq", "state")
    OWNER_FIELD_NUMBER: _ClassVar[int]
    DSEQ_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    owner: str
    dseq: int
    state: str
    def __init__(self, owner: _Optional[str] = ..., dseq: _Optional[int] = ..., state: _Optional[str] = ...) -> None: ...

class GroupFilters(_message.Message):
    __slots__ = ("owner", "dseq", "gseq", "state")
    OWNER_FIELD_NUMBER: _ClassVar[int]
    DSEQ_FIELD_NUMBER: _ClassVar[int]
    GSEQ_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    owner: str
    dseq: int
    gseq: int
    state: str
    def __init__(self, owner: _Optional[str] = ..., dseq: _Optional[int] = ..., gseq: _Optional[int] = ..., state: _Optional[str] = ...) -> None: ...
