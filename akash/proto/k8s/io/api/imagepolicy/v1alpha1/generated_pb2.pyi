from k8s.io.apimachinery.pkg.apis.meta.v1 import generated_pb2 as _generated_pb2
from k8s.io.apimachinery.pkg.runtime import generated_pb2 as _generated_pb2_1
from k8s.io.apimachinery.pkg.runtime.schema import generated_pb2 as _generated_pb2_1_1
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ImageReview(_message.Message):
    __slots__ = ("metadata", "spec", "status")
    METADATA_FIELD_NUMBER: _ClassVar[int]
    SPEC_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    metadata: _generated_pb2.ObjectMeta
    spec: ImageReviewSpec
    status: ImageReviewStatus
    def __init__(self, metadata: _Optional[_Union[_generated_pb2.ObjectMeta, _Mapping]] = ..., spec: _Optional[_Union[ImageReviewSpec, _Mapping]] = ..., status: _Optional[_Union[ImageReviewStatus, _Mapping]] = ...) -> None: ...

class ImageReviewContainerSpec(_message.Message):
    __slots__ = ("image",)
    IMAGE_FIELD_NUMBER: _ClassVar[int]
    image: str
    def __init__(self, image: _Optional[str] = ...) -> None: ...

class ImageReviewSpec(_message.Message):
    __slots__ = ("containers", "annotations", "namespace")
    class AnnotationsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    CONTAINERS_FIELD_NUMBER: _ClassVar[int]
    ANNOTATIONS_FIELD_NUMBER: _ClassVar[int]
    NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    containers: _containers.RepeatedCompositeFieldContainer[ImageReviewContainerSpec]
    annotations: _containers.ScalarMap[str, str]
    namespace: str
    def __init__(self, containers: _Optional[_Iterable[_Union[ImageReviewContainerSpec, _Mapping]]] = ..., annotations: _Optional[_Mapping[str, str]] = ..., namespace: _Optional[str] = ...) -> None: ...

class ImageReviewStatus(_message.Message):
    __slots__ = ("allowed", "reason", "auditAnnotations")
    class AuditAnnotationsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    ALLOWED_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    AUDITANNOTATIONS_FIELD_NUMBER: _ClassVar[int]
    allowed: bool
    reason: str
    auditAnnotations: _containers.ScalarMap[str, str]
    def __init__(self, allowed: bool = ..., reason: _Optional[str] = ..., auditAnnotations: _Optional[_Mapping[str, str]] = ...) -> None: ...
