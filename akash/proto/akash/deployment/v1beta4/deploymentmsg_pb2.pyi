from gogoproto import gogo_pb2 as _gogo_pb2
from akash.deployment.v1 import deployment_pb2 as _deployment_pb2
from akash.deployment.v1beta4 import groupspec_pb2 as _groupspec_pb2
from akash.base.deposit.v1 import deposit_pb2 as _deposit_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MsgCreateDeployment(_message.Message):
    __slots__ = ("id", "groups", "hash", "deposit")
    ID_FIELD_NUMBER: _ClassVar[int]
    GROUPS_FIELD_NUMBER: _ClassVar[int]
    HASH_FIELD_NUMBER: _ClassVar[int]
    DEPOSIT_FIELD_NUMBER: _ClassVar[int]
    id: _deployment_pb2.DeploymentID
    groups: _containers.RepeatedCompositeFieldContainer[_groupspec_pb2.GroupSpec]
    hash: bytes
    deposit: _deposit_pb2.Deposit
    def __init__(self, id: _Optional[_Union[_deployment_pb2.DeploymentID, _Mapping]] = ..., groups: _Optional[_Iterable[_Union[_groupspec_pb2.GroupSpec, _Mapping]]] = ..., hash: _Optional[bytes] = ..., deposit: _Optional[_Union[_deposit_pb2.Deposit, _Mapping]] = ...) -> None: ...

class MsgCreateDeploymentResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class MsgUpdateDeployment(_message.Message):
    __slots__ = ("id", "hash")
    ID_FIELD_NUMBER: _ClassVar[int]
    HASH_FIELD_NUMBER: _ClassVar[int]
    id: _deployment_pb2.DeploymentID
    hash: bytes
    def __init__(self, id: _Optional[_Union[_deployment_pb2.DeploymentID, _Mapping]] = ..., hash: _Optional[bytes] = ...) -> None: ...

class MsgUpdateDeploymentResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class MsgCloseDeployment(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: _deployment_pb2.DeploymentID
    def __init__(self, id: _Optional[_Union[_deployment_pb2.DeploymentID, _Mapping]] = ...) -> None: ...

class MsgCloseDeploymentResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...
