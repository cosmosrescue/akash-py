from k8s.io.api.core.v1 import generated_pb2 as _generated_pb2
from k8s.io.apimachinery.pkg.apis.meta.v1 import generated_pb2 as _generated_pb2_1
from k8s.io.apimachinery.pkg.runtime import generated_pb2 as _generated_pb2_1_1
from k8s.io.apimachinery.pkg.runtime.schema import generated_pb2 as _generated_pb2_1_1_1
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Endpoint(_message.Message):
    __slots__ = ("addresses", "conditions", "hostname", "targetRef", "deprecatedTopology", "nodeName", "zone", "hints")
    class DeprecatedTopologyEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    ADDRESSES_FIELD_NUMBER: _ClassVar[int]
    CONDITIONS_FIELD_NUMBER: _ClassVar[int]
    HOSTNAME_FIELD_NUMBER: _ClassVar[int]
    TARGETREF_FIELD_NUMBER: _ClassVar[int]
    DEPRECATEDTOPOLOGY_FIELD_NUMBER: _ClassVar[int]
    NODENAME_FIELD_NUMBER: _ClassVar[int]
    ZONE_FIELD_NUMBER: _ClassVar[int]
    HINTS_FIELD_NUMBER: _ClassVar[int]
    addresses: _containers.RepeatedScalarFieldContainer[str]
    conditions: EndpointConditions
    hostname: str
    targetRef: _generated_pb2.ObjectReference
    deprecatedTopology: _containers.ScalarMap[str, str]
    nodeName: str
    zone: str
    hints: EndpointHints
    def __init__(self, addresses: _Optional[_Iterable[str]] = ..., conditions: _Optional[_Union[EndpointConditions, _Mapping]] = ..., hostname: _Optional[str] = ..., targetRef: _Optional[_Union[_generated_pb2.ObjectReference, _Mapping]] = ..., deprecatedTopology: _Optional[_Mapping[str, str]] = ..., nodeName: _Optional[str] = ..., zone: _Optional[str] = ..., hints: _Optional[_Union[EndpointHints, _Mapping]] = ...) -> None: ...

class EndpointConditions(_message.Message):
    __slots__ = ("ready", "serving", "terminating")
    READY_FIELD_NUMBER: _ClassVar[int]
    SERVING_FIELD_NUMBER: _ClassVar[int]
    TERMINATING_FIELD_NUMBER: _ClassVar[int]
    ready: bool
    serving: bool
    terminating: bool
    def __init__(self, ready: bool = ..., serving: bool = ..., terminating: bool = ...) -> None: ...

class EndpointHints(_message.Message):
    __slots__ = ("forZones",)
    FORZONES_FIELD_NUMBER: _ClassVar[int]
    forZones: _containers.RepeatedCompositeFieldContainer[ForZone]
    def __init__(self, forZones: _Optional[_Iterable[_Union[ForZone, _Mapping]]] = ...) -> None: ...

class EndpointPort(_message.Message):
    __slots__ = ("name", "protocol", "port", "appProtocol")
    NAME_FIELD_NUMBER: _ClassVar[int]
    PROTOCOL_FIELD_NUMBER: _ClassVar[int]
    PORT_FIELD_NUMBER: _ClassVar[int]
    APPPROTOCOL_FIELD_NUMBER: _ClassVar[int]
    name: str
    protocol: str
    port: int
    appProtocol: str
    def __init__(self, name: _Optional[str] = ..., protocol: _Optional[str] = ..., port: _Optional[int] = ..., appProtocol: _Optional[str] = ...) -> None: ...

class EndpointSlice(_message.Message):
    __slots__ = ("metadata", "addressType", "endpoints", "ports")
    METADATA_FIELD_NUMBER: _ClassVar[int]
    ADDRESSTYPE_FIELD_NUMBER: _ClassVar[int]
    ENDPOINTS_FIELD_NUMBER: _ClassVar[int]
    PORTS_FIELD_NUMBER: _ClassVar[int]
    metadata: _generated_pb2_1.ObjectMeta
    addressType: str
    endpoints: _containers.RepeatedCompositeFieldContainer[Endpoint]
    ports: _containers.RepeatedCompositeFieldContainer[EndpointPort]
    def __init__(self, metadata: _Optional[_Union[_generated_pb2_1.ObjectMeta, _Mapping]] = ..., addressType: _Optional[str] = ..., endpoints: _Optional[_Iterable[_Union[Endpoint, _Mapping]]] = ..., ports: _Optional[_Iterable[_Union[EndpointPort, _Mapping]]] = ...) -> None: ...

class EndpointSliceList(_message.Message):
    __slots__ = ("metadata", "items")
    METADATA_FIELD_NUMBER: _ClassVar[int]
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    metadata: _generated_pb2_1.ListMeta
    items: _containers.RepeatedCompositeFieldContainer[EndpointSlice]
    def __init__(self, metadata: _Optional[_Union[_generated_pb2_1.ListMeta, _Mapping]] = ..., items: _Optional[_Iterable[_Union[EndpointSlice, _Mapping]]] = ...) -> None: ...

class ForZone(_message.Message):
    __slots__ = ("name",)
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    def __init__(self, name: _Optional[str] = ...) -> None: ...
