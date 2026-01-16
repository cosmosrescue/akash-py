from k8s.io.apimachinery.pkg.apis.meta.v1 import generated_pb2 as _generated_pb2
from k8s.io.apimachinery.pkg.runtime import generated_pb2 as _generated_pb2_1
from k8s.io.apimachinery.pkg.runtime.schema import generated_pb2 as _generated_pb2_1_1
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class IPAddress(_message.Message):
    __slots__ = ("metadata", "spec")
    METADATA_FIELD_NUMBER: _ClassVar[int]
    SPEC_FIELD_NUMBER: _ClassVar[int]
    metadata: _generated_pb2.ObjectMeta
    spec: IPAddressSpec
    def __init__(self, metadata: _Optional[_Union[_generated_pb2.ObjectMeta, _Mapping]] = ..., spec: _Optional[_Union[IPAddressSpec, _Mapping]] = ...) -> None: ...

class IPAddressList(_message.Message):
    __slots__ = ("metadata", "items")
    METADATA_FIELD_NUMBER: _ClassVar[int]
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    metadata: _generated_pb2.ListMeta
    items: _containers.RepeatedCompositeFieldContainer[IPAddress]
    def __init__(self, metadata: _Optional[_Union[_generated_pb2.ListMeta, _Mapping]] = ..., items: _Optional[_Iterable[_Union[IPAddress, _Mapping]]] = ...) -> None: ...

class IPAddressSpec(_message.Message):
    __slots__ = ("parentRef",)
    PARENTREF_FIELD_NUMBER: _ClassVar[int]
    parentRef: ParentReference
    def __init__(self, parentRef: _Optional[_Union[ParentReference, _Mapping]] = ...) -> None: ...

class ParentReference(_message.Message):
    __slots__ = ("group", "resource", "namespace", "name")
    GROUP_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_FIELD_NUMBER: _ClassVar[int]
    NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    group: str
    resource: str
    namespace: str
    name: str
    def __init__(self, group: _Optional[str] = ..., resource: _Optional[str] = ..., namespace: _Optional[str] = ..., name: _Optional[str] = ...) -> None: ...

class ServiceCIDR(_message.Message):
    __slots__ = ("metadata", "spec", "status")
    METADATA_FIELD_NUMBER: _ClassVar[int]
    SPEC_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    metadata: _generated_pb2.ObjectMeta
    spec: ServiceCIDRSpec
    status: ServiceCIDRStatus
    def __init__(self, metadata: _Optional[_Union[_generated_pb2.ObjectMeta, _Mapping]] = ..., spec: _Optional[_Union[ServiceCIDRSpec, _Mapping]] = ..., status: _Optional[_Union[ServiceCIDRStatus, _Mapping]] = ...) -> None: ...

class ServiceCIDRList(_message.Message):
    __slots__ = ("metadata", "items")
    METADATA_FIELD_NUMBER: _ClassVar[int]
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    metadata: _generated_pb2.ListMeta
    items: _containers.RepeatedCompositeFieldContainer[ServiceCIDR]
    def __init__(self, metadata: _Optional[_Union[_generated_pb2.ListMeta, _Mapping]] = ..., items: _Optional[_Iterable[_Union[ServiceCIDR, _Mapping]]] = ...) -> None: ...

class ServiceCIDRSpec(_message.Message):
    __slots__ = ("cidrs",)
    CIDRS_FIELD_NUMBER: _ClassVar[int]
    cidrs: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, cidrs: _Optional[_Iterable[str]] = ...) -> None: ...

class ServiceCIDRStatus(_message.Message):
    __slots__ = ("conditions",)
    CONDITIONS_FIELD_NUMBER: _ClassVar[int]
    conditions: _containers.RepeatedCompositeFieldContainer[_generated_pb2.Condition]
    def __init__(self, conditions: _Optional[_Iterable[_Union[_generated_pb2.Condition, _Mapping]]] = ...) -> None: ...
