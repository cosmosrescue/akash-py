from gogoproto import gogo_pb2 as _gogo_pb2
from cosmos_proto import cosmos_pb2 as _cosmos_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DeploymentID(_message.Message):
    __slots__ = ("owner", "dseq")
    OWNER_FIELD_NUMBER: _ClassVar[int]
    DSEQ_FIELD_NUMBER: _ClassVar[int]
    owner: str
    dseq: int
    def __init__(self, owner: _Optional[str] = ..., dseq: _Optional[int] = ...) -> None: ...

class Deployment(_message.Message):
    __slots__ = ("id", "state", "hash", "created_at")
    class State(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        invalid: _ClassVar[Deployment.State]
        active: _ClassVar[Deployment.State]
        closed: _ClassVar[Deployment.State]
    invalid: Deployment.State
    active: Deployment.State
    closed: Deployment.State
    ID_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    HASH_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    id: DeploymentID
    state: Deployment.State
    hash: bytes
    created_at: int
    def __init__(self, id: _Optional[_Union[DeploymentID, _Mapping]] = ..., state: _Optional[_Union[Deployment.State, str]] = ..., hash: _Optional[bytes] = ..., created_at: _Optional[int] = ...) -> None: ...
