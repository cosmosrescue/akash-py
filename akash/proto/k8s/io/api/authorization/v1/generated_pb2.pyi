from k8s.io.apimachinery.pkg.apis.meta.v1 import generated_pb2 as _generated_pb2
from k8s.io.apimachinery.pkg.runtime import generated_pb2 as _generated_pb2_1
from k8s.io.apimachinery.pkg.runtime.schema import generated_pb2 as _generated_pb2_1_1
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ExtraValue(_message.Message):
    __slots__ = ("items",)
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    items: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, items: _Optional[_Iterable[str]] = ...) -> None: ...

class FieldSelectorAttributes(_message.Message):
    __slots__ = ("rawSelector", "requirements")
    RAWSELECTOR_FIELD_NUMBER: _ClassVar[int]
    REQUIREMENTS_FIELD_NUMBER: _ClassVar[int]
    rawSelector: str
    requirements: _containers.RepeatedCompositeFieldContainer[_generated_pb2.FieldSelectorRequirement]
    def __init__(self, rawSelector: _Optional[str] = ..., requirements: _Optional[_Iterable[_Union[_generated_pb2.FieldSelectorRequirement, _Mapping]]] = ...) -> None: ...

class LabelSelectorAttributes(_message.Message):
    __slots__ = ("rawSelector", "requirements")
    RAWSELECTOR_FIELD_NUMBER: _ClassVar[int]
    REQUIREMENTS_FIELD_NUMBER: _ClassVar[int]
    rawSelector: str
    requirements: _containers.RepeatedCompositeFieldContainer[_generated_pb2.LabelSelectorRequirement]
    def __init__(self, rawSelector: _Optional[str] = ..., requirements: _Optional[_Iterable[_Union[_generated_pb2.LabelSelectorRequirement, _Mapping]]] = ...) -> None: ...

class LocalSubjectAccessReview(_message.Message):
    __slots__ = ("metadata", "spec", "status")
    METADATA_FIELD_NUMBER: _ClassVar[int]
    SPEC_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    metadata: _generated_pb2.ObjectMeta
    spec: SubjectAccessReviewSpec
    status: SubjectAccessReviewStatus
    def __init__(self, metadata: _Optional[_Union[_generated_pb2.ObjectMeta, _Mapping]] = ..., spec: _Optional[_Union[SubjectAccessReviewSpec, _Mapping]] = ..., status: _Optional[_Union[SubjectAccessReviewStatus, _Mapping]] = ...) -> None: ...

class NonResourceAttributes(_message.Message):
    __slots__ = ("path", "verb")
    PATH_FIELD_NUMBER: _ClassVar[int]
    VERB_FIELD_NUMBER: _ClassVar[int]
    path: str
    verb: str
    def __init__(self, path: _Optional[str] = ..., verb: _Optional[str] = ...) -> None: ...

class NonResourceRule(_message.Message):
    __slots__ = ("verbs", "nonResourceURLs")
    VERBS_FIELD_NUMBER: _ClassVar[int]
    NONRESOURCEURLS_FIELD_NUMBER: _ClassVar[int]
    verbs: _containers.RepeatedScalarFieldContainer[str]
    nonResourceURLs: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, verbs: _Optional[_Iterable[str]] = ..., nonResourceURLs: _Optional[_Iterable[str]] = ...) -> None: ...

class ResourceAttributes(_message.Message):
    __slots__ = ("namespace", "verb", "group", "version", "resource", "subresource", "name", "fieldSelector", "labelSelector")
    NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    VERB_FIELD_NUMBER: _ClassVar[int]
    GROUP_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_FIELD_NUMBER: _ClassVar[int]
    SUBRESOURCE_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    FIELDSELECTOR_FIELD_NUMBER: _ClassVar[int]
    LABELSELECTOR_FIELD_NUMBER: _ClassVar[int]
    namespace: str
    verb: str
    group: str
    version: str
    resource: str
    subresource: str
    name: str
    fieldSelector: FieldSelectorAttributes
    labelSelector: LabelSelectorAttributes
    def __init__(self, namespace: _Optional[str] = ..., verb: _Optional[str] = ..., group: _Optional[str] = ..., version: _Optional[str] = ..., resource: _Optional[str] = ..., subresource: _Optional[str] = ..., name: _Optional[str] = ..., fieldSelector: _Optional[_Union[FieldSelectorAttributes, _Mapping]] = ..., labelSelector: _Optional[_Union[LabelSelectorAttributes, _Mapping]] = ...) -> None: ...

class ResourceRule(_message.Message):
    __slots__ = ("verbs", "apiGroups", "resources", "resourceNames")
    VERBS_FIELD_NUMBER: _ClassVar[int]
    APIGROUPS_FIELD_NUMBER: _ClassVar[int]
    RESOURCES_FIELD_NUMBER: _ClassVar[int]
    RESOURCENAMES_FIELD_NUMBER: _ClassVar[int]
    verbs: _containers.RepeatedScalarFieldContainer[str]
    apiGroups: _containers.RepeatedScalarFieldContainer[str]
    resources: _containers.RepeatedScalarFieldContainer[str]
    resourceNames: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, verbs: _Optional[_Iterable[str]] = ..., apiGroups: _Optional[_Iterable[str]] = ..., resources: _Optional[_Iterable[str]] = ..., resourceNames: _Optional[_Iterable[str]] = ...) -> None: ...

class SelfSubjectAccessReview(_message.Message):
    __slots__ = ("metadata", "spec", "status")
    METADATA_FIELD_NUMBER: _ClassVar[int]
    SPEC_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    metadata: _generated_pb2.ObjectMeta
    spec: SelfSubjectAccessReviewSpec
    status: SubjectAccessReviewStatus
    def __init__(self, metadata: _Optional[_Union[_generated_pb2.ObjectMeta, _Mapping]] = ..., spec: _Optional[_Union[SelfSubjectAccessReviewSpec, _Mapping]] = ..., status: _Optional[_Union[SubjectAccessReviewStatus, _Mapping]] = ...) -> None: ...

class SelfSubjectAccessReviewSpec(_message.Message):
    __slots__ = ("resourceAttributes", "nonResourceAttributes")
    RESOURCEATTRIBUTES_FIELD_NUMBER: _ClassVar[int]
    NONRESOURCEATTRIBUTES_FIELD_NUMBER: _ClassVar[int]
    resourceAttributes: ResourceAttributes
    nonResourceAttributes: NonResourceAttributes
    def __init__(self, resourceAttributes: _Optional[_Union[ResourceAttributes, _Mapping]] = ..., nonResourceAttributes: _Optional[_Union[NonResourceAttributes, _Mapping]] = ...) -> None: ...

class SelfSubjectRulesReview(_message.Message):
    __slots__ = ("metadata", "spec", "status")
    METADATA_FIELD_NUMBER: _ClassVar[int]
    SPEC_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    metadata: _generated_pb2.ObjectMeta
    spec: SelfSubjectRulesReviewSpec
    status: SubjectRulesReviewStatus
    def __init__(self, metadata: _Optional[_Union[_generated_pb2.ObjectMeta, _Mapping]] = ..., spec: _Optional[_Union[SelfSubjectRulesReviewSpec, _Mapping]] = ..., status: _Optional[_Union[SubjectRulesReviewStatus, _Mapping]] = ...) -> None: ...

class SelfSubjectRulesReviewSpec(_message.Message):
    __slots__ = ("namespace",)
    NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    namespace: str
    def __init__(self, namespace: _Optional[str] = ...) -> None: ...

class SubjectAccessReview(_message.Message):
    __slots__ = ("metadata", "spec", "status")
    METADATA_FIELD_NUMBER: _ClassVar[int]
    SPEC_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    metadata: _generated_pb2.ObjectMeta
    spec: SubjectAccessReviewSpec
    status: SubjectAccessReviewStatus
    def __init__(self, metadata: _Optional[_Union[_generated_pb2.ObjectMeta, _Mapping]] = ..., spec: _Optional[_Union[SubjectAccessReviewSpec, _Mapping]] = ..., status: _Optional[_Union[SubjectAccessReviewStatus, _Mapping]] = ...) -> None: ...

class SubjectAccessReviewSpec(_message.Message):
    __slots__ = ("resourceAttributes", "nonResourceAttributes", "user", "groups", "extra", "uid")
    class ExtraEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: ExtraValue
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[ExtraValue, _Mapping]] = ...) -> None: ...
    RESOURCEATTRIBUTES_FIELD_NUMBER: _ClassVar[int]
    NONRESOURCEATTRIBUTES_FIELD_NUMBER: _ClassVar[int]
    USER_FIELD_NUMBER: _ClassVar[int]
    GROUPS_FIELD_NUMBER: _ClassVar[int]
    EXTRA_FIELD_NUMBER: _ClassVar[int]
    UID_FIELD_NUMBER: _ClassVar[int]
    resourceAttributes: ResourceAttributes
    nonResourceAttributes: NonResourceAttributes
    user: str
    groups: _containers.RepeatedScalarFieldContainer[str]
    extra: _containers.MessageMap[str, ExtraValue]
    uid: str
    def __init__(self, resourceAttributes: _Optional[_Union[ResourceAttributes, _Mapping]] = ..., nonResourceAttributes: _Optional[_Union[NonResourceAttributes, _Mapping]] = ..., user: _Optional[str] = ..., groups: _Optional[_Iterable[str]] = ..., extra: _Optional[_Mapping[str, ExtraValue]] = ..., uid: _Optional[str] = ...) -> None: ...

class SubjectAccessReviewStatus(_message.Message):
    __slots__ = ("allowed", "denied", "reason", "evaluationError")
    ALLOWED_FIELD_NUMBER: _ClassVar[int]
    DENIED_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    EVALUATIONERROR_FIELD_NUMBER: _ClassVar[int]
    allowed: bool
    denied: bool
    reason: str
    evaluationError: str
    def __init__(self, allowed: bool = ..., denied: bool = ..., reason: _Optional[str] = ..., evaluationError: _Optional[str] = ...) -> None: ...

class SubjectRulesReviewStatus(_message.Message):
    __slots__ = ("resourceRules", "nonResourceRules", "incomplete", "evaluationError")
    RESOURCERULES_FIELD_NUMBER: _ClassVar[int]
    NONRESOURCERULES_FIELD_NUMBER: _ClassVar[int]
    INCOMPLETE_FIELD_NUMBER: _ClassVar[int]
    EVALUATIONERROR_FIELD_NUMBER: _ClassVar[int]
    resourceRules: _containers.RepeatedCompositeFieldContainer[ResourceRule]
    nonResourceRules: _containers.RepeatedCompositeFieldContainer[NonResourceRule]
    incomplete: bool
    evaluationError: str
    def __init__(self, resourceRules: _Optional[_Iterable[_Union[ResourceRule, _Mapping]]] = ..., nonResourceRules: _Optional[_Iterable[_Union[NonResourceRule, _Mapping]]] = ..., incomplete: bool = ..., evaluationError: _Optional[str] = ...) -> None: ...
