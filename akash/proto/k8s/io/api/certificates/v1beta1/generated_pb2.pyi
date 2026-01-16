from k8s.io.api.core.v1 import generated_pb2 as _generated_pb2
from k8s.io.apimachinery.pkg.apis.meta.v1 import generated_pb2 as _generated_pb2_1
from k8s.io.apimachinery.pkg.runtime import generated_pb2 as _generated_pb2_1_1
from k8s.io.apimachinery.pkg.runtime.schema import generated_pb2 as _generated_pb2_1_1_1
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CertificateSigningRequest(_message.Message):
    __slots__ = ("metadata", "spec", "status")
    METADATA_FIELD_NUMBER: _ClassVar[int]
    SPEC_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    metadata: _generated_pb2_1.ObjectMeta
    spec: CertificateSigningRequestSpec
    status: CertificateSigningRequestStatus
    def __init__(self, metadata: _Optional[_Union[_generated_pb2_1.ObjectMeta, _Mapping]] = ..., spec: _Optional[_Union[CertificateSigningRequestSpec, _Mapping]] = ..., status: _Optional[_Union[CertificateSigningRequestStatus, _Mapping]] = ...) -> None: ...

class CertificateSigningRequestCondition(_message.Message):
    __slots__ = ("type", "status", "reason", "message", "lastUpdateTime", "lastTransitionTime")
    TYPE_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    LASTUPDATETIME_FIELD_NUMBER: _ClassVar[int]
    LASTTRANSITIONTIME_FIELD_NUMBER: _ClassVar[int]
    type: str
    status: str
    reason: str
    message: str
    lastUpdateTime: _generated_pb2_1.Time
    lastTransitionTime: _generated_pb2_1.Time
    def __init__(self, type: _Optional[str] = ..., status: _Optional[str] = ..., reason: _Optional[str] = ..., message: _Optional[str] = ..., lastUpdateTime: _Optional[_Union[_generated_pb2_1.Time, _Mapping]] = ..., lastTransitionTime: _Optional[_Union[_generated_pb2_1.Time, _Mapping]] = ...) -> None: ...

class CertificateSigningRequestList(_message.Message):
    __slots__ = ("metadata", "items")
    METADATA_FIELD_NUMBER: _ClassVar[int]
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    metadata: _generated_pb2_1.ListMeta
    items: _containers.RepeatedCompositeFieldContainer[CertificateSigningRequest]
    def __init__(self, metadata: _Optional[_Union[_generated_pb2_1.ListMeta, _Mapping]] = ..., items: _Optional[_Iterable[_Union[CertificateSigningRequest, _Mapping]]] = ...) -> None: ...

class CertificateSigningRequestSpec(_message.Message):
    __slots__ = ("request", "signerName", "expirationSeconds", "usages", "username", "uid", "groups", "extra")
    class ExtraEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: ExtraValue
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[ExtraValue, _Mapping]] = ...) -> None: ...
    REQUEST_FIELD_NUMBER: _ClassVar[int]
    SIGNERNAME_FIELD_NUMBER: _ClassVar[int]
    EXPIRATIONSECONDS_FIELD_NUMBER: _ClassVar[int]
    USAGES_FIELD_NUMBER: _ClassVar[int]
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    UID_FIELD_NUMBER: _ClassVar[int]
    GROUPS_FIELD_NUMBER: _ClassVar[int]
    EXTRA_FIELD_NUMBER: _ClassVar[int]
    request: bytes
    signerName: str
    expirationSeconds: int
    usages: _containers.RepeatedScalarFieldContainer[str]
    username: str
    uid: str
    groups: _containers.RepeatedScalarFieldContainer[str]
    extra: _containers.MessageMap[str, ExtraValue]
    def __init__(self, request: _Optional[bytes] = ..., signerName: _Optional[str] = ..., expirationSeconds: _Optional[int] = ..., usages: _Optional[_Iterable[str]] = ..., username: _Optional[str] = ..., uid: _Optional[str] = ..., groups: _Optional[_Iterable[str]] = ..., extra: _Optional[_Mapping[str, ExtraValue]] = ...) -> None: ...

class CertificateSigningRequestStatus(_message.Message):
    __slots__ = ("conditions", "certificate")
    CONDITIONS_FIELD_NUMBER: _ClassVar[int]
    CERTIFICATE_FIELD_NUMBER: _ClassVar[int]
    conditions: _containers.RepeatedCompositeFieldContainer[CertificateSigningRequestCondition]
    certificate: bytes
    def __init__(self, conditions: _Optional[_Iterable[_Union[CertificateSigningRequestCondition, _Mapping]]] = ..., certificate: _Optional[bytes] = ...) -> None: ...

class ExtraValue(_message.Message):
    __slots__ = ("items",)
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    items: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, items: _Optional[_Iterable[str]] = ...) -> None: ...
