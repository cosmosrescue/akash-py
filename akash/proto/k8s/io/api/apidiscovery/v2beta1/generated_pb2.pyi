from k8s.io.apimachinery.pkg.apis.meta.v1 import generated_pb2 as _generated_pb2
from k8s.io.apimachinery.pkg.runtime import generated_pb2 as _generated_pb2_1
from k8s.io.apimachinery.pkg.runtime.schema import generated_pb2 as _generated_pb2_1_1
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class APIGroupDiscovery(_message.Message):
    __slots__ = ("metadata", "versions")
    METADATA_FIELD_NUMBER: _ClassVar[int]
    VERSIONS_FIELD_NUMBER: _ClassVar[int]
    metadata: _generated_pb2.ObjectMeta
    versions: _containers.RepeatedCompositeFieldContainer[APIVersionDiscovery]
    def __init__(self, metadata: _Optional[_Union[_generated_pb2.ObjectMeta, _Mapping]] = ..., versions: _Optional[_Iterable[_Union[APIVersionDiscovery, _Mapping]]] = ...) -> None: ...

class APIGroupDiscoveryList(_message.Message):
    __slots__ = ("metadata", "items")
    METADATA_FIELD_NUMBER: _ClassVar[int]
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    metadata: _generated_pb2.ListMeta
    items: _containers.RepeatedCompositeFieldContainer[APIGroupDiscovery]
    def __init__(self, metadata: _Optional[_Union[_generated_pb2.ListMeta, _Mapping]] = ..., items: _Optional[_Iterable[_Union[APIGroupDiscovery, _Mapping]]] = ...) -> None: ...

class APIResourceDiscovery(_message.Message):
    __slots__ = ("resource", "responseKind", "scope", "singularResource", "verbs", "shortNames", "categories", "subresources")
    RESOURCE_FIELD_NUMBER: _ClassVar[int]
    RESPONSEKIND_FIELD_NUMBER: _ClassVar[int]
    SCOPE_FIELD_NUMBER: _ClassVar[int]
    SINGULARRESOURCE_FIELD_NUMBER: _ClassVar[int]
    VERBS_FIELD_NUMBER: _ClassVar[int]
    SHORTNAMES_FIELD_NUMBER: _ClassVar[int]
    CATEGORIES_FIELD_NUMBER: _ClassVar[int]
    SUBRESOURCES_FIELD_NUMBER: _ClassVar[int]
    resource: str
    responseKind: _generated_pb2.GroupVersionKind
    scope: str
    singularResource: str
    verbs: _containers.RepeatedScalarFieldContainer[str]
    shortNames: _containers.RepeatedScalarFieldContainer[str]
    categories: _containers.RepeatedScalarFieldContainer[str]
    subresources: _containers.RepeatedCompositeFieldContainer[APISubresourceDiscovery]
    def __init__(self, resource: _Optional[str] = ..., responseKind: _Optional[_Union[_generated_pb2.GroupVersionKind, _Mapping]] = ..., scope: _Optional[str] = ..., singularResource: _Optional[str] = ..., verbs: _Optional[_Iterable[str]] = ..., shortNames: _Optional[_Iterable[str]] = ..., categories: _Optional[_Iterable[str]] = ..., subresources: _Optional[_Iterable[_Union[APISubresourceDiscovery, _Mapping]]] = ...) -> None: ...

class APISubresourceDiscovery(_message.Message):
    __slots__ = ("subresource", "responseKind", "acceptedTypes", "verbs")
    SUBRESOURCE_FIELD_NUMBER: _ClassVar[int]
    RESPONSEKIND_FIELD_NUMBER: _ClassVar[int]
    ACCEPTEDTYPES_FIELD_NUMBER: _ClassVar[int]
    VERBS_FIELD_NUMBER: _ClassVar[int]
    subresource: str
    responseKind: _generated_pb2.GroupVersionKind
    acceptedTypes: _containers.RepeatedCompositeFieldContainer[_generated_pb2.GroupVersionKind]
    verbs: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, subresource: _Optional[str] = ..., responseKind: _Optional[_Union[_generated_pb2.GroupVersionKind, _Mapping]] = ..., acceptedTypes: _Optional[_Iterable[_Union[_generated_pb2.GroupVersionKind, _Mapping]]] = ..., verbs: _Optional[_Iterable[str]] = ...) -> None: ...

class APIVersionDiscovery(_message.Message):
    __slots__ = ("version", "resources", "freshness")
    VERSION_FIELD_NUMBER: _ClassVar[int]
    RESOURCES_FIELD_NUMBER: _ClassVar[int]
    FRESHNESS_FIELD_NUMBER: _ClassVar[int]
    version: str
    resources: _containers.RepeatedCompositeFieldContainer[APIResourceDiscovery]
    freshness: str
    def __init__(self, version: _Optional[str] = ..., resources: _Optional[_Iterable[_Union[APIResourceDiscovery, _Mapping]]] = ..., freshness: _Optional[str] = ...) -> None: ...
