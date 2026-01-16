from k8s.io.api.core.v1 import generated_pb2 as _generated_pb2
from k8s.io.apimachinery.pkg.api.resource import generated_pb2 as _generated_pb2_1
from k8s.io.apimachinery.pkg.apis.meta.v1 import generated_pb2 as _generated_pb2_1_1
from k8s.io.apimachinery.pkg.runtime import generated_pb2 as _generated_pb2_1_1_1
from k8s.io.apimachinery.pkg.runtime.schema import generated_pb2 as _generated_pb2_1_1_1_1
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Overhead(_message.Message):
    __slots__ = ("podFixed",)
    class PodFixedEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: _generated_pb2_1.Quantity
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[_generated_pb2_1.Quantity, _Mapping]] = ...) -> None: ...
    PODFIXED_FIELD_NUMBER: _ClassVar[int]
    podFixed: _containers.MessageMap[str, _generated_pb2_1.Quantity]
    def __init__(self, podFixed: _Optional[_Mapping[str, _generated_pb2_1.Quantity]] = ...) -> None: ...

class RuntimeClass(_message.Message):
    __slots__ = ("metadata", "spec")
    METADATA_FIELD_NUMBER: _ClassVar[int]
    SPEC_FIELD_NUMBER: _ClassVar[int]
    metadata: _generated_pb2_1_1.ObjectMeta
    spec: RuntimeClassSpec
    def __init__(self, metadata: _Optional[_Union[_generated_pb2_1_1.ObjectMeta, _Mapping]] = ..., spec: _Optional[_Union[RuntimeClassSpec, _Mapping]] = ...) -> None: ...

class RuntimeClassList(_message.Message):
    __slots__ = ("metadata", "items")
    METADATA_FIELD_NUMBER: _ClassVar[int]
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    metadata: _generated_pb2_1_1.ListMeta
    items: _containers.RepeatedCompositeFieldContainer[RuntimeClass]
    def __init__(self, metadata: _Optional[_Union[_generated_pb2_1_1.ListMeta, _Mapping]] = ..., items: _Optional[_Iterable[_Union[RuntimeClass, _Mapping]]] = ...) -> None: ...

class RuntimeClassSpec(_message.Message):
    __slots__ = ("runtimeHandler", "overhead", "scheduling")
    RUNTIMEHANDLER_FIELD_NUMBER: _ClassVar[int]
    OVERHEAD_FIELD_NUMBER: _ClassVar[int]
    SCHEDULING_FIELD_NUMBER: _ClassVar[int]
    runtimeHandler: str
    overhead: Overhead
    scheduling: Scheduling
    def __init__(self, runtimeHandler: _Optional[str] = ..., overhead: _Optional[_Union[Overhead, _Mapping]] = ..., scheduling: _Optional[_Union[Scheduling, _Mapping]] = ...) -> None: ...

class Scheduling(_message.Message):
    __slots__ = ("nodeSelector", "tolerations")
    class NodeSelectorEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    NODESELECTOR_FIELD_NUMBER: _ClassVar[int]
    TOLERATIONS_FIELD_NUMBER: _ClassVar[int]
    nodeSelector: _containers.ScalarMap[str, str]
    tolerations: _containers.RepeatedCompositeFieldContainer[_generated_pb2.Toleration]
    def __init__(self, nodeSelector: _Optional[_Mapping[str, str]] = ..., tolerations: _Optional[_Iterable[_Union[_generated_pb2.Toleration, _Mapping]]] = ...) -> None: ...
