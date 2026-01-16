from k8s.io.api.core.v1 import generated_pb2 as _generated_pb2
from k8s.io.apimachinery.pkg.apis.meta.v1 import generated_pb2 as _generated_pb2_1
from k8s.io.apimachinery.pkg.runtime import generated_pb2 as _generated_pb2_1_1
from k8s.io.apimachinery.pkg.runtime.schema import generated_pb2 as _generated_pb2_1_1_1
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GroupVersionResource(_message.Message):
    __slots__ = ("group", "version", "resource")
    GROUP_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_FIELD_NUMBER: _ClassVar[int]
    group: str
    version: str
    resource: str
    def __init__(self, group: _Optional[str] = ..., version: _Optional[str] = ..., resource: _Optional[str] = ...) -> None: ...

class MigrationCondition(_message.Message):
    __slots__ = ("type", "status", "lastUpdateTime", "reason", "message")
    TYPE_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    LASTUPDATETIME_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    type: str
    status: str
    lastUpdateTime: _generated_pb2_1.Time
    reason: str
    message: str
    def __init__(self, type: _Optional[str] = ..., status: _Optional[str] = ..., lastUpdateTime: _Optional[_Union[_generated_pb2_1.Time, _Mapping]] = ..., reason: _Optional[str] = ..., message: _Optional[str] = ...) -> None: ...

class StorageVersionMigration(_message.Message):
    __slots__ = ("metadata", "spec", "status")
    METADATA_FIELD_NUMBER: _ClassVar[int]
    SPEC_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    metadata: _generated_pb2_1.ObjectMeta
    spec: StorageVersionMigrationSpec
    status: StorageVersionMigrationStatus
    def __init__(self, metadata: _Optional[_Union[_generated_pb2_1.ObjectMeta, _Mapping]] = ..., spec: _Optional[_Union[StorageVersionMigrationSpec, _Mapping]] = ..., status: _Optional[_Union[StorageVersionMigrationStatus, _Mapping]] = ...) -> None: ...

class StorageVersionMigrationList(_message.Message):
    __slots__ = ("metadata", "items")
    METADATA_FIELD_NUMBER: _ClassVar[int]
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    metadata: _generated_pb2_1.ListMeta
    items: _containers.RepeatedCompositeFieldContainer[StorageVersionMigration]
    def __init__(self, metadata: _Optional[_Union[_generated_pb2_1.ListMeta, _Mapping]] = ..., items: _Optional[_Iterable[_Union[StorageVersionMigration, _Mapping]]] = ...) -> None: ...

class StorageVersionMigrationSpec(_message.Message):
    __slots__ = ("resource", "continueToken")
    RESOURCE_FIELD_NUMBER: _ClassVar[int]
    CONTINUETOKEN_FIELD_NUMBER: _ClassVar[int]
    resource: GroupVersionResource
    continueToken: str
    def __init__(self, resource: _Optional[_Union[GroupVersionResource, _Mapping]] = ..., continueToken: _Optional[str] = ...) -> None: ...

class StorageVersionMigrationStatus(_message.Message):
    __slots__ = ("conditions", "resourceVersion")
    CONDITIONS_FIELD_NUMBER: _ClassVar[int]
    RESOURCEVERSION_FIELD_NUMBER: _ClassVar[int]
    conditions: _containers.RepeatedCompositeFieldContainer[MigrationCondition]
    resourceVersion: str
    def __init__(self, conditions: _Optional[_Iterable[_Union[MigrationCondition, _Mapping]]] = ..., resourceVersion: _Optional[str] = ...) -> None: ...
