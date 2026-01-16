from gogoproto import gogo_pb2 as _gogo_pb2
from akash.deployment.v1 import deployment_pb2 as _deployment_pb2
from akash.deployment.v1beta4 import group_pb2 as _group_pb2
from akash.deployment.v1beta4 import params_pb2 as _params_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GenesisDeployment(_message.Message):
    __slots__ = ("deployment", "groups")
    DEPLOYMENT_FIELD_NUMBER: _ClassVar[int]
    GROUPS_FIELD_NUMBER: _ClassVar[int]
    deployment: _deployment_pb2.Deployment
    groups: _containers.RepeatedCompositeFieldContainer[_group_pb2.Group]
    def __init__(self, deployment: _Optional[_Union[_deployment_pb2.Deployment, _Mapping]] = ..., groups: _Optional[_Iterable[_Union[_group_pb2.Group, _Mapping]]] = ...) -> None: ...

class GenesisState(_message.Message):
    __slots__ = ("deployments", "params")
    DEPLOYMENTS_FIELD_NUMBER: _ClassVar[int]
    PARAMS_FIELD_NUMBER: _ClassVar[int]
    deployments: _containers.RepeatedCompositeFieldContainer[GenesisDeployment]
    params: _params_pb2.Params
    def __init__(self, deployments: _Optional[_Iterable[_Union[GenesisDeployment, _Mapping]]] = ..., params: _Optional[_Union[_params_pb2.Params, _Mapping]] = ...) -> None: ...
