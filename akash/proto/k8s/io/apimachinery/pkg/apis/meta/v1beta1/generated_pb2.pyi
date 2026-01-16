from k8s.io.apimachinery.pkg.apis.meta.v1 import generated_pb2 as _generated_pb2
from k8s.io.apimachinery.pkg.runtime.schema import generated_pb2 as _generated_pb2_1
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class PartialObjectMetadataList(_message.Message):
    __slots__ = ("metadata", "items")
    METADATA_FIELD_NUMBER: _ClassVar[int]
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    metadata: _generated_pb2.ListMeta
    items: _containers.RepeatedCompositeFieldContainer[_generated_pb2.PartialObjectMetadata]
    def __init__(self, metadata: _Optional[_Union[_generated_pb2.ListMeta, _Mapping]] = ..., items: _Optional[_Iterable[_Union[_generated_pb2.PartialObjectMetadata, _Mapping]]] = ...) -> None: ...
