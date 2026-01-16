from gogoproto import gogo_pb2 as _gogo_pb2
from akash.manifest.v2beta3 import serviceexpose_pb2 as _serviceexpose_pb2
from akash.base.resources.v1beta4 import resources_pb2 as _resources_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class StorageParams(_message.Message):
    __slots__ = ("name", "mount", "read_only")
    NAME_FIELD_NUMBER: _ClassVar[int]
    MOUNT_FIELD_NUMBER: _ClassVar[int]
    READ_ONLY_FIELD_NUMBER: _ClassVar[int]
    name: str
    mount: str
    read_only: bool
    def __init__(self, name: _Optional[str] = ..., mount: _Optional[str] = ..., read_only: bool = ...) -> None: ...

class ServiceParams(_message.Message):
    __slots__ = ("storage", "credentials")
    STORAGE_FIELD_NUMBER: _ClassVar[int]
    CREDENTIALS_FIELD_NUMBER: _ClassVar[int]
    storage: _containers.RepeatedCompositeFieldContainer[StorageParams]
    credentials: ImageCredentials
    def __init__(self, storage: _Optional[_Iterable[_Union[StorageParams, _Mapping]]] = ..., credentials: _Optional[_Union[ImageCredentials, _Mapping]] = ...) -> None: ...

class ImageCredentials(_message.Message):
    __slots__ = ("host", "email", "username", "password")
    HOST_FIELD_NUMBER: _ClassVar[int]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    PASSWORD_FIELD_NUMBER: _ClassVar[int]
    host: str
    email: str
    username: str
    password: str
    def __init__(self, host: _Optional[str] = ..., email: _Optional[str] = ..., username: _Optional[str] = ..., password: _Optional[str] = ...) -> None: ...

class Service(_message.Message):
    __slots__ = ("name", "image", "command", "args", "env", "resources", "count", "expose", "params", "credentials")
    NAME_FIELD_NUMBER: _ClassVar[int]
    IMAGE_FIELD_NUMBER: _ClassVar[int]
    COMMAND_FIELD_NUMBER: _ClassVar[int]
    ARGS_FIELD_NUMBER: _ClassVar[int]
    ENV_FIELD_NUMBER: _ClassVar[int]
    RESOURCES_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    EXPOSE_FIELD_NUMBER: _ClassVar[int]
    PARAMS_FIELD_NUMBER: _ClassVar[int]
    CREDENTIALS_FIELD_NUMBER: _ClassVar[int]
    name: str
    image: str
    command: _containers.RepeatedScalarFieldContainer[str]
    args: _containers.RepeatedScalarFieldContainer[str]
    env: _containers.RepeatedScalarFieldContainer[str]
    resources: _resources_pb2.Resources
    count: int
    expose: _containers.RepeatedCompositeFieldContainer[_serviceexpose_pb2.ServiceExpose]
    params: ServiceParams
    credentials: ImageCredentials
    def __init__(self, name: _Optional[str] = ..., image: _Optional[str] = ..., command: _Optional[_Iterable[str]] = ..., args: _Optional[_Iterable[str]] = ..., env: _Optional[_Iterable[str]] = ..., resources: _Optional[_Union[_resources_pb2.Resources, _Mapping]] = ..., count: _Optional[int] = ..., expose: _Optional[_Iterable[_Union[_serviceexpose_pb2.ServiceExpose, _Mapping]]] = ..., params: _Optional[_Union[ServiceParams, _Mapping]] = ..., credentials: _Optional[_Union[ImageCredentials, _Mapping]] = ...) -> None: ...
