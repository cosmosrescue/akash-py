from k8s.io.api.authentication.v1 import generated_pb2 as _generated_pb2
from k8s.io.apimachinery.pkg.apis.meta.v1 import generated_pb2 as _generated_pb2_1
from k8s.io.apimachinery.pkg.runtime import generated_pb2 as _generated_pb2_1_1
from k8s.io.apimachinery.pkg.runtime.schema import generated_pb2 as _generated_pb2_1_1_1
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SelfSubjectReview(_message.Message):
    __slots__ = ("metadata", "status")
    METADATA_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    metadata: _generated_pb2_1.ObjectMeta
    status: SelfSubjectReviewStatus
    def __init__(self, metadata: _Optional[_Union[_generated_pb2_1.ObjectMeta, _Mapping]] = ..., status: _Optional[_Union[SelfSubjectReviewStatus, _Mapping]] = ...) -> None: ...

class SelfSubjectReviewStatus(_message.Message):
    __slots__ = ("userInfo",)
    USERINFO_FIELD_NUMBER: _ClassVar[int]
    userInfo: _generated_pb2.UserInfo
    def __init__(self, userInfo: _Optional[_Union[_generated_pb2.UserInfo, _Mapping]] = ...) -> None: ...
