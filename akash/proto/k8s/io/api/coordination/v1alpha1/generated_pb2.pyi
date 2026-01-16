from k8s.io.api.coordination.v1 import generated_pb2 as _generated_pb2
from k8s.io.apimachinery.pkg.apis.meta.v1 import generated_pb2 as _generated_pb2_1
from k8s.io.apimachinery.pkg.runtime import generated_pb2 as _generated_pb2_1_1
from k8s.io.apimachinery.pkg.runtime.schema import generated_pb2 as _generated_pb2_1_1_1
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class LeaseCandidate(_message.Message):
    __slots__ = ("metadata", "spec")
    METADATA_FIELD_NUMBER: _ClassVar[int]
    SPEC_FIELD_NUMBER: _ClassVar[int]
    metadata: _generated_pb2_1.ObjectMeta
    spec: LeaseCandidateSpec
    def __init__(self, metadata: _Optional[_Union[_generated_pb2_1.ObjectMeta, _Mapping]] = ..., spec: _Optional[_Union[LeaseCandidateSpec, _Mapping]] = ...) -> None: ...

class LeaseCandidateList(_message.Message):
    __slots__ = ("metadata", "items")
    METADATA_FIELD_NUMBER: _ClassVar[int]
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    metadata: _generated_pb2_1.ListMeta
    items: _containers.RepeatedCompositeFieldContainer[LeaseCandidate]
    def __init__(self, metadata: _Optional[_Union[_generated_pb2_1.ListMeta, _Mapping]] = ..., items: _Optional[_Iterable[_Union[LeaseCandidate, _Mapping]]] = ...) -> None: ...

class LeaseCandidateSpec(_message.Message):
    __slots__ = ("leaseName", "pingTime", "renewTime", "binaryVersion", "emulationVersion", "preferredStrategies")
    LEASENAME_FIELD_NUMBER: _ClassVar[int]
    PINGTIME_FIELD_NUMBER: _ClassVar[int]
    RENEWTIME_FIELD_NUMBER: _ClassVar[int]
    BINARYVERSION_FIELD_NUMBER: _ClassVar[int]
    EMULATIONVERSION_FIELD_NUMBER: _ClassVar[int]
    PREFERREDSTRATEGIES_FIELD_NUMBER: _ClassVar[int]
    leaseName: str
    pingTime: _generated_pb2_1.MicroTime
    renewTime: _generated_pb2_1.MicroTime
    binaryVersion: str
    emulationVersion: str
    preferredStrategies: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, leaseName: _Optional[str] = ..., pingTime: _Optional[_Union[_generated_pb2_1.MicroTime, _Mapping]] = ..., renewTime: _Optional[_Union[_generated_pb2_1.MicroTime, _Mapping]] = ..., binaryVersion: _Optional[str] = ..., emulationVersion: _Optional[str] = ..., preferredStrategies: _Optional[_Iterable[str]] = ...) -> None: ...
