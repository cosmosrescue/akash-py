from k8s.io.apimachinery.pkg.apis.meta.v1 import generated_pb2 as _generated_pb2
from k8s.io.apimachinery.pkg.runtime import generated_pb2 as _generated_pb2_1
from k8s.io.apimachinery.pkg.runtime.schema import generated_pb2 as _generated_pb2_1_1
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Lease(_message.Message):
    __slots__ = ("metadata", "spec")
    METADATA_FIELD_NUMBER: _ClassVar[int]
    SPEC_FIELD_NUMBER: _ClassVar[int]
    metadata: _generated_pb2.ObjectMeta
    spec: LeaseSpec
    def __init__(self, metadata: _Optional[_Union[_generated_pb2.ObjectMeta, _Mapping]] = ..., spec: _Optional[_Union[LeaseSpec, _Mapping]] = ...) -> None: ...

class LeaseList(_message.Message):
    __slots__ = ("metadata", "items")
    METADATA_FIELD_NUMBER: _ClassVar[int]
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    metadata: _generated_pb2.ListMeta
    items: _containers.RepeatedCompositeFieldContainer[Lease]
    def __init__(self, metadata: _Optional[_Union[_generated_pb2.ListMeta, _Mapping]] = ..., items: _Optional[_Iterable[_Union[Lease, _Mapping]]] = ...) -> None: ...

class LeaseSpec(_message.Message):
    __slots__ = ("holderIdentity", "leaseDurationSeconds", "acquireTime", "renewTime", "leaseTransitions", "strategy", "preferredHolder")
    HOLDERIDENTITY_FIELD_NUMBER: _ClassVar[int]
    LEASEDURATIONSECONDS_FIELD_NUMBER: _ClassVar[int]
    ACQUIRETIME_FIELD_NUMBER: _ClassVar[int]
    RENEWTIME_FIELD_NUMBER: _ClassVar[int]
    LEASETRANSITIONS_FIELD_NUMBER: _ClassVar[int]
    STRATEGY_FIELD_NUMBER: _ClassVar[int]
    PREFERREDHOLDER_FIELD_NUMBER: _ClassVar[int]
    holderIdentity: str
    leaseDurationSeconds: int
    acquireTime: _generated_pb2.MicroTime
    renewTime: _generated_pb2.MicroTime
    leaseTransitions: int
    strategy: str
    preferredHolder: str
    def __init__(self, holderIdentity: _Optional[str] = ..., leaseDurationSeconds: _Optional[int] = ..., acquireTime: _Optional[_Union[_generated_pb2.MicroTime, _Mapping]] = ..., renewTime: _Optional[_Union[_generated_pb2.MicroTime, _Mapping]] = ..., leaseTransitions: _Optional[int] = ..., strategy: _Optional[str] = ..., preferredHolder: _Optional[str] = ...) -> None: ...
