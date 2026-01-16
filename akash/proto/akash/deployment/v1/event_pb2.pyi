from gogoproto import gogo_pb2 as _gogo_pb2
from akash.deployment.v1 import deployment_pb2 as _deployment_pb2
from akash.deployment.v1 import group_pb2 as _group_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class EventDeploymentCreated(_message.Message):
    __slots__ = ("id", "hash")
    ID_FIELD_NUMBER: _ClassVar[int]
    HASH_FIELD_NUMBER: _ClassVar[int]
    id: _deployment_pb2.DeploymentID
    hash: bytes
    def __init__(self, id: _Optional[_Union[_deployment_pb2.DeploymentID, _Mapping]] = ..., hash: _Optional[bytes] = ...) -> None: ...

class EventDeploymentUpdated(_message.Message):
    __slots__ = ("id", "hash")
    ID_FIELD_NUMBER: _ClassVar[int]
    HASH_FIELD_NUMBER: _ClassVar[int]
    id: _deployment_pb2.DeploymentID
    hash: bytes
    def __init__(self, id: _Optional[_Union[_deployment_pb2.DeploymentID, _Mapping]] = ..., hash: _Optional[bytes] = ...) -> None: ...

class EventDeploymentClosed(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: _deployment_pb2.DeploymentID
    def __init__(self, id: _Optional[_Union[_deployment_pb2.DeploymentID, _Mapping]] = ...) -> None: ...

class EventGroupStarted(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: _group_pb2.GroupID
    def __init__(self, id: _Optional[_Union[_group_pb2.GroupID, _Mapping]] = ...) -> None: ...

class EventGroupPaused(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: _group_pb2.GroupID
    def __init__(self, id: _Optional[_Union[_group_pb2.GroupID, _Mapping]] = ...) -> None: ...

class EventGroupClosed(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: _group_pb2.GroupID
    def __init__(self, id: _Optional[_Union[_group_pb2.GroupID, _Mapping]] = ...) -> None: ...
