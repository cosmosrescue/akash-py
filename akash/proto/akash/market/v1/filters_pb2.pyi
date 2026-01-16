from gogoproto import gogo_pb2 as _gogo_pb2
from cosmos_proto import cosmos_pb2 as _cosmos_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class LeaseFilters(_message.Message):
    __slots__ = ("owner", "dseq", "gseq", "oseq", "provider", "state", "bseq")
    OWNER_FIELD_NUMBER: _ClassVar[int]
    DSEQ_FIELD_NUMBER: _ClassVar[int]
    GSEQ_FIELD_NUMBER: _ClassVar[int]
    OSEQ_FIELD_NUMBER: _ClassVar[int]
    PROVIDER_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    BSEQ_FIELD_NUMBER: _ClassVar[int]
    owner: str
    dseq: int
    gseq: int
    oseq: int
    provider: str
    state: str
    bseq: int
    def __init__(self, owner: _Optional[str] = ..., dseq: _Optional[int] = ..., gseq: _Optional[int] = ..., oseq: _Optional[int] = ..., provider: _Optional[str] = ..., state: _Optional[str] = ..., bseq: _Optional[int] = ...) -> None: ...
