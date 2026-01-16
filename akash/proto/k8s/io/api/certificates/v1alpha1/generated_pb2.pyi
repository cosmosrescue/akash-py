from k8s.io.apimachinery.pkg.apis.meta.v1 import generated_pb2 as _generated_pb2
from k8s.io.apimachinery.pkg.runtime import generated_pb2 as _generated_pb2_1
from k8s.io.apimachinery.pkg.runtime.schema import generated_pb2 as _generated_pb2_1_1
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ClusterTrustBundle(_message.Message):
    __slots__ = ("metadata", "spec")
    METADATA_FIELD_NUMBER: _ClassVar[int]
    SPEC_FIELD_NUMBER: _ClassVar[int]
    metadata: _generated_pb2.ObjectMeta
    spec: ClusterTrustBundleSpec
    def __init__(self, metadata: _Optional[_Union[_generated_pb2.ObjectMeta, _Mapping]] = ..., spec: _Optional[_Union[ClusterTrustBundleSpec, _Mapping]] = ...) -> None: ...

class ClusterTrustBundleList(_message.Message):
    __slots__ = ("metadata", "items")
    METADATA_FIELD_NUMBER: _ClassVar[int]
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    metadata: _generated_pb2.ListMeta
    items: _containers.RepeatedCompositeFieldContainer[ClusterTrustBundle]
    def __init__(self, metadata: _Optional[_Union[_generated_pb2.ListMeta, _Mapping]] = ..., items: _Optional[_Iterable[_Union[ClusterTrustBundle, _Mapping]]] = ...) -> None: ...

class ClusterTrustBundleSpec(_message.Message):
    __slots__ = ("signerName", "trustBundle")
    SIGNERNAME_FIELD_NUMBER: _ClassVar[int]
    TRUSTBUNDLE_FIELD_NUMBER: _ClassVar[int]
    signerName: str
    trustBundle: str
    def __init__(self, signerName: _Optional[str] = ..., trustBundle: _Optional[str] = ...) -> None: ...
