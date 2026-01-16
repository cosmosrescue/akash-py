from gogoproto import gogo_pb2 as _gogo_pb2
from akash.deployment.v1beta3 import deployment_pb2 as _deployment_pb2
from akash.deployment.v1beta3 import groupspec_pb2 as _groupspec_pb2
from cosmos.base.v1beta1 import coin_pb2 as _coin_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MsgCreateDeployment(_message.Message):
    __slots__ = ("id", "groups", "version", "deposit", "depositor")
    ID_FIELD_NUMBER: _ClassVar[int]
    GROUPS_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    DEPOSIT_FIELD_NUMBER: _ClassVar[int]
    DEPOSITOR_FIELD_NUMBER: _ClassVar[int]
    id: _deployment_pb2.DeploymentID
    groups: _containers.RepeatedCompositeFieldContainer[_groupspec_pb2.GroupSpec]
    version: bytes
    deposit: _coin_pb2.Coin
    depositor: str
    def __init__(self, id: _Optional[_Union[_deployment_pb2.DeploymentID, _Mapping]] = ..., groups: _Optional[_Iterable[_Union[_groupspec_pb2.GroupSpec, _Mapping]]] = ..., version: _Optional[bytes] = ..., deposit: _Optional[_Union[_coin_pb2.Coin, _Mapping]] = ..., depositor: _Optional[str] = ...) -> None: ...

class MsgCreateDeploymentResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class MsgDepositDeployment(_message.Message):
    __slots__ = ("id", "amount", "depositor")
    ID_FIELD_NUMBER: _ClassVar[int]
    AMOUNT_FIELD_NUMBER: _ClassVar[int]
    DEPOSITOR_FIELD_NUMBER: _ClassVar[int]
    id: _deployment_pb2.DeploymentID
    amount: _coin_pb2.Coin
    depositor: str
    def __init__(self, id: _Optional[_Union[_deployment_pb2.DeploymentID, _Mapping]] = ..., amount: _Optional[_Union[_coin_pb2.Coin, _Mapping]] = ..., depositor: _Optional[str] = ...) -> None: ...

class MsgDepositDeploymentResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class MsgUpdateDeployment(_message.Message):
    __slots__ = ("id", "version")
    ID_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    id: _deployment_pb2.DeploymentID
    version: bytes
    def __init__(self, id: _Optional[_Union[_deployment_pb2.DeploymentID, _Mapping]] = ..., version: _Optional[bytes] = ...) -> None: ...

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
