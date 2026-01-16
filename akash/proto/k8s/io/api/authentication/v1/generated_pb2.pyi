from k8s.io.apimachinery.pkg.apis.meta.v1 import generated_pb2 as _generated_pb2
from k8s.io.apimachinery.pkg.runtime import generated_pb2 as _generated_pb2_1
from k8s.io.apimachinery.pkg.runtime.schema import generated_pb2 as _generated_pb2_1_1
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class BoundObjectReference(_message.Message):
    __slots__ = ("kind", "apiVersion", "name", "uID")
    KIND_FIELD_NUMBER: _ClassVar[int]
    APIVERSION_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    UID_FIELD_NUMBER: _ClassVar[int]
    kind: str
    apiVersion: str
    name: str
    uID: str
    def __init__(self, kind: _Optional[str] = ..., apiVersion: _Optional[str] = ..., name: _Optional[str] = ..., uID: _Optional[str] = ...) -> None: ...

class ExtraValue(_message.Message):
    __slots__ = ("items",)
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    items: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, items: _Optional[_Iterable[str]] = ...) -> None: ...

class SelfSubjectReview(_message.Message):
    __slots__ = ("metadata", "status")
    METADATA_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    metadata: _generated_pb2.ObjectMeta
    status: SelfSubjectReviewStatus
    def __init__(self, metadata: _Optional[_Union[_generated_pb2.ObjectMeta, _Mapping]] = ..., status: _Optional[_Union[SelfSubjectReviewStatus, _Mapping]] = ...) -> None: ...

class SelfSubjectReviewStatus(_message.Message):
    __slots__ = ("userInfo",)
    USERINFO_FIELD_NUMBER: _ClassVar[int]
    userInfo: UserInfo
    def __init__(self, userInfo: _Optional[_Union[UserInfo, _Mapping]] = ...) -> None: ...

class TokenRequest(_message.Message):
    __slots__ = ("metadata", "spec", "status")
    METADATA_FIELD_NUMBER: _ClassVar[int]
    SPEC_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    metadata: _generated_pb2.ObjectMeta
    spec: TokenRequestSpec
    status: TokenRequestStatus
    def __init__(self, metadata: _Optional[_Union[_generated_pb2.ObjectMeta, _Mapping]] = ..., spec: _Optional[_Union[TokenRequestSpec, _Mapping]] = ..., status: _Optional[_Union[TokenRequestStatus, _Mapping]] = ...) -> None: ...

class TokenRequestSpec(_message.Message):
    __slots__ = ("audiences", "expirationSeconds", "boundObjectRef")
    AUDIENCES_FIELD_NUMBER: _ClassVar[int]
    EXPIRATIONSECONDS_FIELD_NUMBER: _ClassVar[int]
    BOUNDOBJECTREF_FIELD_NUMBER: _ClassVar[int]
    audiences: _containers.RepeatedScalarFieldContainer[str]
    expirationSeconds: int
    boundObjectRef: BoundObjectReference
    def __init__(self, audiences: _Optional[_Iterable[str]] = ..., expirationSeconds: _Optional[int] = ..., boundObjectRef: _Optional[_Union[BoundObjectReference, _Mapping]] = ...) -> None: ...

class TokenRequestStatus(_message.Message):
    __slots__ = ("token", "expirationTimestamp")
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    EXPIRATIONTIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    token: str
    expirationTimestamp: _generated_pb2.Time
    def __init__(self, token: _Optional[str] = ..., expirationTimestamp: _Optional[_Union[_generated_pb2.Time, _Mapping]] = ...) -> None: ...

class TokenReview(_message.Message):
    __slots__ = ("metadata", "spec", "status")
    METADATA_FIELD_NUMBER: _ClassVar[int]
    SPEC_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    metadata: _generated_pb2.ObjectMeta
    spec: TokenReviewSpec
    status: TokenReviewStatus
    def __init__(self, metadata: _Optional[_Union[_generated_pb2.ObjectMeta, _Mapping]] = ..., spec: _Optional[_Union[TokenReviewSpec, _Mapping]] = ..., status: _Optional[_Union[TokenReviewStatus, _Mapping]] = ...) -> None: ...

class TokenReviewSpec(_message.Message):
    __slots__ = ("token", "audiences")
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    AUDIENCES_FIELD_NUMBER: _ClassVar[int]
    token: str
    audiences: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, token: _Optional[str] = ..., audiences: _Optional[_Iterable[str]] = ...) -> None: ...

class TokenReviewStatus(_message.Message):
    __slots__ = ("authenticated", "user", "audiences", "error")
    AUTHENTICATED_FIELD_NUMBER: _ClassVar[int]
    USER_FIELD_NUMBER: _ClassVar[int]
    AUDIENCES_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    authenticated: bool
    user: UserInfo
    audiences: _containers.RepeatedScalarFieldContainer[str]
    error: str
    def __init__(self, authenticated: bool = ..., user: _Optional[_Union[UserInfo, _Mapping]] = ..., audiences: _Optional[_Iterable[str]] = ..., error: _Optional[str] = ...) -> None: ...

class UserInfo(_message.Message):
    __slots__ = ("username", "uid", "groups", "extra")
    class ExtraEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: ExtraValue
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[ExtraValue, _Mapping]] = ...) -> None: ...
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    UID_FIELD_NUMBER: _ClassVar[int]
    GROUPS_FIELD_NUMBER: _ClassVar[int]
    EXTRA_FIELD_NUMBER: _ClassVar[int]
    username: str
    uid: str
    groups: _containers.RepeatedScalarFieldContainer[str]
    extra: _containers.MessageMap[str, ExtraValue]
    def __init__(self, username: _Optional[str] = ..., uid: _Optional[str] = ..., groups: _Optional[_Iterable[str]] = ..., extra: _Optional[_Mapping[str, ExtraValue]] = ...) -> None: ...
