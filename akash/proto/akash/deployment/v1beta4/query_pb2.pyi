from gogoproto import gogo_pb2 as _gogo_pb2
from amino import amino_pb2 as _amino_pb2
from google.api import annotations_pb2 as _annotations_pb2
from cosmos.base.query.v1beta1 import pagination_pb2 as _pagination_pb2
from akash.escrow.types.v1 import account_pb2 as _account_pb2
from akash.deployment.v1beta4 import filters_pb2 as _filters_pb2
from akash.deployment.v1beta4 import group_pb2 as _group_pb2
from akash.deployment.v1beta4 import params_pb2 as _params_pb2
from akash.deployment.v1 import deployment_pb2 as _deployment_pb2
from akash.deployment.v1 import group_pb2 as _group_pb2_1
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class QueryDeploymentsRequest(_message.Message):
    __slots__ = ("filters", "pagination")
    FILTERS_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    filters: _filters_pb2.DeploymentFilters
    pagination: _pagination_pb2.PageRequest
    def __init__(self, filters: _Optional[_Union[_filters_pb2.DeploymentFilters, _Mapping]] = ..., pagination: _Optional[_Union[_pagination_pb2.PageRequest, _Mapping]] = ...) -> None: ...

class QueryDeploymentsResponse(_message.Message):
    __slots__ = ("deployments", "pagination")
    DEPLOYMENTS_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    deployments: _containers.RepeatedCompositeFieldContainer[QueryDeploymentResponse]
    pagination: _pagination_pb2.PageResponse
    def __init__(self, deployments: _Optional[_Iterable[_Union[QueryDeploymentResponse, _Mapping]]] = ..., pagination: _Optional[_Union[_pagination_pb2.PageResponse, _Mapping]] = ...) -> None: ...

class QueryDeploymentRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: _deployment_pb2.DeploymentID
    def __init__(self, id: _Optional[_Union[_deployment_pb2.DeploymentID, _Mapping]] = ...) -> None: ...

class QueryDeploymentResponse(_message.Message):
    __slots__ = ("deployment", "groups", "escrow_account")
    DEPLOYMENT_FIELD_NUMBER: _ClassVar[int]
    GROUPS_FIELD_NUMBER: _ClassVar[int]
    ESCROW_ACCOUNT_FIELD_NUMBER: _ClassVar[int]
    deployment: _deployment_pb2.Deployment
    groups: _containers.RepeatedCompositeFieldContainer[_group_pb2.Group]
    escrow_account: _account_pb2.Account
    def __init__(self, deployment: _Optional[_Union[_deployment_pb2.Deployment, _Mapping]] = ..., groups: _Optional[_Iterable[_Union[_group_pb2.Group, _Mapping]]] = ..., escrow_account: _Optional[_Union[_account_pb2.Account, _Mapping]] = ...) -> None: ...

class QueryGroupRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: _group_pb2_1.GroupID
    def __init__(self, id: _Optional[_Union[_group_pb2_1.GroupID, _Mapping]] = ...) -> None: ...

class QueryGroupResponse(_message.Message):
    __slots__ = ("group",)
    GROUP_FIELD_NUMBER: _ClassVar[int]
    group: _group_pb2.Group
    def __init__(self, group: _Optional[_Union[_group_pb2.Group, _Mapping]] = ...) -> None: ...

class QueryParamsRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class QueryParamsResponse(_message.Message):
    __slots__ = ("params",)
    PARAMS_FIELD_NUMBER: _ClassVar[int]
    params: _params_pb2.Params
    def __init__(self, params: _Optional[_Union[_params_pb2.Params, _Mapping]] = ...) -> None: ...
