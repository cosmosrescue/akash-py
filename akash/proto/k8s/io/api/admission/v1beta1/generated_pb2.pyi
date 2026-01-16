from k8s.io.api.authentication.v1 import generated_pb2 as _generated_pb2
from k8s.io.apimachinery.pkg.apis.meta.v1 import generated_pb2 as _generated_pb2_1
from k8s.io.apimachinery.pkg.runtime import generated_pb2 as _generated_pb2_1_1
from k8s.io.apimachinery.pkg.runtime.schema import generated_pb2 as _generated_pb2_1_1_1
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class AdmissionRequest(_message.Message):
    __slots__ = ("uid", "kind", "resource", "subResource", "requestKind", "requestResource", "requestSubResource", "name", "namespace", "operation", "userInfo", "object", "oldObject", "dryRun", "options")
    UID_FIELD_NUMBER: _ClassVar[int]
    KIND_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_FIELD_NUMBER: _ClassVar[int]
    SUBRESOURCE_FIELD_NUMBER: _ClassVar[int]
    REQUESTKIND_FIELD_NUMBER: _ClassVar[int]
    REQUESTRESOURCE_FIELD_NUMBER: _ClassVar[int]
    REQUESTSUBRESOURCE_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    OPERATION_FIELD_NUMBER: _ClassVar[int]
    USERINFO_FIELD_NUMBER: _ClassVar[int]
    OBJECT_FIELD_NUMBER: _ClassVar[int]
    OLDOBJECT_FIELD_NUMBER: _ClassVar[int]
    DRYRUN_FIELD_NUMBER: _ClassVar[int]
    OPTIONS_FIELD_NUMBER: _ClassVar[int]
    uid: str
    kind: _generated_pb2_1.GroupVersionKind
    resource: _generated_pb2_1.GroupVersionResource
    subResource: str
    requestKind: _generated_pb2_1.GroupVersionKind
    requestResource: _generated_pb2_1.GroupVersionResource
    requestSubResource: str
    name: str
    namespace: str
    operation: str
    userInfo: _generated_pb2.UserInfo
    object: _generated_pb2_1_1.RawExtension
    oldObject: _generated_pb2_1_1.RawExtension
    dryRun: bool
    options: _generated_pb2_1_1.RawExtension
    def __init__(self, uid: _Optional[str] = ..., kind: _Optional[_Union[_generated_pb2_1.GroupVersionKind, _Mapping]] = ..., resource: _Optional[_Union[_generated_pb2_1.GroupVersionResource, _Mapping]] = ..., subResource: _Optional[str] = ..., requestKind: _Optional[_Union[_generated_pb2_1.GroupVersionKind, _Mapping]] = ..., requestResource: _Optional[_Union[_generated_pb2_1.GroupVersionResource, _Mapping]] = ..., requestSubResource: _Optional[str] = ..., name: _Optional[str] = ..., namespace: _Optional[str] = ..., operation: _Optional[str] = ..., userInfo: _Optional[_Union[_generated_pb2.UserInfo, _Mapping]] = ..., object: _Optional[_Union[_generated_pb2_1_1.RawExtension, _Mapping]] = ..., oldObject: _Optional[_Union[_generated_pb2_1_1.RawExtension, _Mapping]] = ..., dryRun: bool = ..., options: _Optional[_Union[_generated_pb2_1_1.RawExtension, _Mapping]] = ...) -> None: ...

class AdmissionResponse(_message.Message):
    __slots__ = ("uid", "allowed", "status", "patch", "patchType", "auditAnnotations", "warnings")
    class AuditAnnotationsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    UID_FIELD_NUMBER: _ClassVar[int]
    ALLOWED_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    PATCH_FIELD_NUMBER: _ClassVar[int]
    PATCHTYPE_FIELD_NUMBER: _ClassVar[int]
    AUDITANNOTATIONS_FIELD_NUMBER: _ClassVar[int]
    WARNINGS_FIELD_NUMBER: _ClassVar[int]
    uid: str
    allowed: bool
    status: _generated_pb2_1.Status
    patch: bytes
    patchType: str
    auditAnnotations: _containers.ScalarMap[str, str]
    warnings: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, uid: _Optional[str] = ..., allowed: bool = ..., status: _Optional[_Union[_generated_pb2_1.Status, _Mapping]] = ..., patch: _Optional[bytes] = ..., patchType: _Optional[str] = ..., auditAnnotations: _Optional[_Mapping[str, str]] = ..., warnings: _Optional[_Iterable[str]] = ...) -> None: ...

class AdmissionReview(_message.Message):
    __slots__ = ("request", "response")
    REQUEST_FIELD_NUMBER: _ClassVar[int]
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    request: AdmissionRequest
    response: AdmissionResponse
    def __init__(self, request: _Optional[_Union[AdmissionRequest, _Mapping]] = ..., response: _Optional[_Union[AdmissionResponse, _Mapping]] = ...) -> None: ...
