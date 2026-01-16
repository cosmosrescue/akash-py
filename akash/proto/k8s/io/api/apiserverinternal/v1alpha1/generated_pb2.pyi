from k8s.io.apimachinery.pkg.apis.meta.v1 import generated_pb2 as _generated_pb2
from k8s.io.apimachinery.pkg.runtime import generated_pb2 as _generated_pb2_1
from k8s.io.apimachinery.pkg.runtime.schema import generated_pb2 as _generated_pb2_1_1
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ServerStorageVersion(_message.Message):
    __slots__ = ("apiServerID", "encodingVersion", "decodableVersions", "servedVersions")
    APISERVERID_FIELD_NUMBER: _ClassVar[int]
    ENCODINGVERSION_FIELD_NUMBER: _ClassVar[int]
    DECODABLEVERSIONS_FIELD_NUMBER: _ClassVar[int]
    SERVEDVERSIONS_FIELD_NUMBER: _ClassVar[int]
    apiServerID: str
    encodingVersion: str
    decodableVersions: _containers.RepeatedScalarFieldContainer[str]
    servedVersions: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, apiServerID: _Optional[str] = ..., encodingVersion: _Optional[str] = ..., decodableVersions: _Optional[_Iterable[str]] = ..., servedVersions: _Optional[_Iterable[str]] = ...) -> None: ...

class StorageVersion(_message.Message):
    __slots__ = ("metadata", "spec", "status")
    METADATA_FIELD_NUMBER: _ClassVar[int]
    SPEC_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    metadata: _generated_pb2.ObjectMeta
    spec: StorageVersionSpec
    status: StorageVersionStatus
    def __init__(self, metadata: _Optional[_Union[_generated_pb2.ObjectMeta, _Mapping]] = ..., spec: _Optional[_Union[StorageVersionSpec, _Mapping]] = ..., status: _Optional[_Union[StorageVersionStatus, _Mapping]] = ...) -> None: ...

class StorageVersionCondition(_message.Message):
    __slots__ = ("type", "status", "observedGeneration", "lastTransitionTime", "reason", "message")
    TYPE_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    OBSERVEDGENERATION_FIELD_NUMBER: _ClassVar[int]
    LASTTRANSITIONTIME_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    type: str
    status: str
    observedGeneration: int
    lastTransitionTime: _generated_pb2.Time
    reason: str
    message: str
    def __init__(self, type: _Optional[str] = ..., status: _Optional[str] = ..., observedGeneration: _Optional[int] = ..., lastTransitionTime: _Optional[_Union[_generated_pb2.Time, _Mapping]] = ..., reason: _Optional[str] = ..., message: _Optional[str] = ...) -> None: ...

class StorageVersionList(_message.Message):
    __slots__ = ("metadata", "items")
    METADATA_FIELD_NUMBER: _ClassVar[int]
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    metadata: _generated_pb2.ListMeta
    items: _containers.RepeatedCompositeFieldContainer[StorageVersion]
    def __init__(self, metadata: _Optional[_Union[_generated_pb2.ListMeta, _Mapping]] = ..., items: _Optional[_Iterable[_Union[StorageVersion, _Mapping]]] = ...) -> None: ...

class StorageVersionSpec(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class StorageVersionStatus(_message.Message):
    __slots__ = ("storageVersions", "commonEncodingVersion", "conditions")
    STORAGEVERSIONS_FIELD_NUMBER: _ClassVar[int]
    COMMONENCODINGVERSION_FIELD_NUMBER: _ClassVar[int]
    CONDITIONS_FIELD_NUMBER: _ClassVar[int]
    storageVersions: _containers.RepeatedCompositeFieldContainer[ServerStorageVersion]
    commonEncodingVersion: str
    conditions: _containers.RepeatedCompositeFieldContainer[StorageVersionCondition]
    def __init__(self, storageVersions: _Optional[_Iterable[_Union[ServerStorageVersion, _Mapping]]] = ..., commonEncodingVersion: _Optional[str] = ..., conditions: _Optional[_Iterable[_Union[StorageVersionCondition, _Mapping]]] = ...) -> None: ...
