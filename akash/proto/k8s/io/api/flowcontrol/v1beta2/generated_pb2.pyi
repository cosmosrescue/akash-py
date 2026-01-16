from k8s.io.apimachinery.pkg.apis.meta.v1 import generated_pb2 as _generated_pb2
from k8s.io.apimachinery.pkg.runtime import generated_pb2 as _generated_pb2_1
from k8s.io.apimachinery.pkg.runtime.schema import generated_pb2 as _generated_pb2_1_1
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ExemptPriorityLevelConfiguration(_message.Message):
    __slots__ = ("nominalConcurrencyShares", "lendablePercent")
    NOMINALCONCURRENCYSHARES_FIELD_NUMBER: _ClassVar[int]
    LENDABLEPERCENT_FIELD_NUMBER: _ClassVar[int]
    nominalConcurrencyShares: int
    lendablePercent: int
    def __init__(self, nominalConcurrencyShares: _Optional[int] = ..., lendablePercent: _Optional[int] = ...) -> None: ...

class FlowDistinguisherMethod(_message.Message):
    __slots__ = ("type",)
    TYPE_FIELD_NUMBER: _ClassVar[int]
    type: str
    def __init__(self, type: _Optional[str] = ...) -> None: ...

class FlowSchema(_message.Message):
    __slots__ = ("metadata", "spec", "status")
    METADATA_FIELD_NUMBER: _ClassVar[int]
    SPEC_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    metadata: _generated_pb2.ObjectMeta
    spec: FlowSchemaSpec
    status: FlowSchemaStatus
    def __init__(self, metadata: _Optional[_Union[_generated_pb2.ObjectMeta, _Mapping]] = ..., spec: _Optional[_Union[FlowSchemaSpec, _Mapping]] = ..., status: _Optional[_Union[FlowSchemaStatus, _Mapping]] = ...) -> None: ...

class FlowSchemaCondition(_message.Message):
    __slots__ = ("type", "status", "lastTransitionTime", "reason", "message")
    TYPE_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    LASTTRANSITIONTIME_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    type: str
    status: str
    lastTransitionTime: _generated_pb2.Time
    reason: str
    message: str
    def __init__(self, type: _Optional[str] = ..., status: _Optional[str] = ..., lastTransitionTime: _Optional[_Union[_generated_pb2.Time, _Mapping]] = ..., reason: _Optional[str] = ..., message: _Optional[str] = ...) -> None: ...

class FlowSchemaList(_message.Message):
    __slots__ = ("metadata", "items")
    METADATA_FIELD_NUMBER: _ClassVar[int]
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    metadata: _generated_pb2.ListMeta
    items: _containers.RepeatedCompositeFieldContainer[FlowSchema]
    def __init__(self, metadata: _Optional[_Union[_generated_pb2.ListMeta, _Mapping]] = ..., items: _Optional[_Iterable[_Union[FlowSchema, _Mapping]]] = ...) -> None: ...

class FlowSchemaSpec(_message.Message):
    __slots__ = ("priorityLevelConfiguration", "matchingPrecedence", "distinguisherMethod", "rules")
    PRIORITYLEVELCONFIGURATION_FIELD_NUMBER: _ClassVar[int]
    MATCHINGPRECEDENCE_FIELD_NUMBER: _ClassVar[int]
    DISTINGUISHERMETHOD_FIELD_NUMBER: _ClassVar[int]
    RULES_FIELD_NUMBER: _ClassVar[int]
    priorityLevelConfiguration: PriorityLevelConfigurationReference
    matchingPrecedence: int
    distinguisherMethod: FlowDistinguisherMethod
    rules: _containers.RepeatedCompositeFieldContainer[PolicyRulesWithSubjects]
    def __init__(self, priorityLevelConfiguration: _Optional[_Union[PriorityLevelConfigurationReference, _Mapping]] = ..., matchingPrecedence: _Optional[int] = ..., distinguisherMethod: _Optional[_Union[FlowDistinguisherMethod, _Mapping]] = ..., rules: _Optional[_Iterable[_Union[PolicyRulesWithSubjects, _Mapping]]] = ...) -> None: ...

class FlowSchemaStatus(_message.Message):
    __slots__ = ("conditions",)
    CONDITIONS_FIELD_NUMBER: _ClassVar[int]
    conditions: _containers.RepeatedCompositeFieldContainer[FlowSchemaCondition]
    def __init__(self, conditions: _Optional[_Iterable[_Union[FlowSchemaCondition, _Mapping]]] = ...) -> None: ...

class GroupSubject(_message.Message):
    __slots__ = ("name",)
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    def __init__(self, name: _Optional[str] = ...) -> None: ...

class LimitResponse(_message.Message):
    __slots__ = ("type", "queuing")
    TYPE_FIELD_NUMBER: _ClassVar[int]
    QUEUING_FIELD_NUMBER: _ClassVar[int]
    type: str
    queuing: QueuingConfiguration
    def __init__(self, type: _Optional[str] = ..., queuing: _Optional[_Union[QueuingConfiguration, _Mapping]] = ...) -> None: ...

class LimitedPriorityLevelConfiguration(_message.Message):
    __slots__ = ("assuredConcurrencyShares", "limitResponse", "lendablePercent", "borrowingLimitPercent")
    ASSUREDCONCURRENCYSHARES_FIELD_NUMBER: _ClassVar[int]
    LIMITRESPONSE_FIELD_NUMBER: _ClassVar[int]
    LENDABLEPERCENT_FIELD_NUMBER: _ClassVar[int]
    BORROWINGLIMITPERCENT_FIELD_NUMBER: _ClassVar[int]
    assuredConcurrencyShares: int
    limitResponse: LimitResponse
    lendablePercent: int
    borrowingLimitPercent: int
    def __init__(self, assuredConcurrencyShares: _Optional[int] = ..., limitResponse: _Optional[_Union[LimitResponse, _Mapping]] = ..., lendablePercent: _Optional[int] = ..., borrowingLimitPercent: _Optional[int] = ...) -> None: ...

class NonResourcePolicyRule(_message.Message):
    __slots__ = ("verbs", "nonResourceURLs")
    VERBS_FIELD_NUMBER: _ClassVar[int]
    NONRESOURCEURLS_FIELD_NUMBER: _ClassVar[int]
    verbs: _containers.RepeatedScalarFieldContainer[str]
    nonResourceURLs: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, verbs: _Optional[_Iterable[str]] = ..., nonResourceURLs: _Optional[_Iterable[str]] = ...) -> None: ...

class PolicyRulesWithSubjects(_message.Message):
    __slots__ = ("subjects", "resourceRules", "nonResourceRules")
    SUBJECTS_FIELD_NUMBER: _ClassVar[int]
    RESOURCERULES_FIELD_NUMBER: _ClassVar[int]
    NONRESOURCERULES_FIELD_NUMBER: _ClassVar[int]
    subjects: _containers.RepeatedCompositeFieldContainer[Subject]
    resourceRules: _containers.RepeatedCompositeFieldContainer[ResourcePolicyRule]
    nonResourceRules: _containers.RepeatedCompositeFieldContainer[NonResourcePolicyRule]
    def __init__(self, subjects: _Optional[_Iterable[_Union[Subject, _Mapping]]] = ..., resourceRules: _Optional[_Iterable[_Union[ResourcePolicyRule, _Mapping]]] = ..., nonResourceRules: _Optional[_Iterable[_Union[NonResourcePolicyRule, _Mapping]]] = ...) -> None: ...

class PriorityLevelConfiguration(_message.Message):
    __slots__ = ("metadata", "spec", "status")
    METADATA_FIELD_NUMBER: _ClassVar[int]
    SPEC_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    metadata: _generated_pb2.ObjectMeta
    spec: PriorityLevelConfigurationSpec
    status: PriorityLevelConfigurationStatus
    def __init__(self, metadata: _Optional[_Union[_generated_pb2.ObjectMeta, _Mapping]] = ..., spec: _Optional[_Union[PriorityLevelConfigurationSpec, _Mapping]] = ..., status: _Optional[_Union[PriorityLevelConfigurationStatus, _Mapping]] = ...) -> None: ...

class PriorityLevelConfigurationCondition(_message.Message):
    __slots__ = ("type", "status", "lastTransitionTime", "reason", "message")
    TYPE_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    LASTTRANSITIONTIME_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    type: str
    status: str
    lastTransitionTime: _generated_pb2.Time
    reason: str
    message: str
    def __init__(self, type: _Optional[str] = ..., status: _Optional[str] = ..., lastTransitionTime: _Optional[_Union[_generated_pb2.Time, _Mapping]] = ..., reason: _Optional[str] = ..., message: _Optional[str] = ...) -> None: ...

class PriorityLevelConfigurationList(_message.Message):
    __slots__ = ("metadata", "items")
    METADATA_FIELD_NUMBER: _ClassVar[int]
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    metadata: _generated_pb2.ListMeta
    items: _containers.RepeatedCompositeFieldContainer[PriorityLevelConfiguration]
    def __init__(self, metadata: _Optional[_Union[_generated_pb2.ListMeta, _Mapping]] = ..., items: _Optional[_Iterable[_Union[PriorityLevelConfiguration, _Mapping]]] = ...) -> None: ...

class PriorityLevelConfigurationReference(_message.Message):
    __slots__ = ("name",)
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    def __init__(self, name: _Optional[str] = ...) -> None: ...

class PriorityLevelConfigurationSpec(_message.Message):
    __slots__ = ("type", "limited", "exempt")
    TYPE_FIELD_NUMBER: _ClassVar[int]
    LIMITED_FIELD_NUMBER: _ClassVar[int]
    EXEMPT_FIELD_NUMBER: _ClassVar[int]
    type: str
    limited: LimitedPriorityLevelConfiguration
    exempt: ExemptPriorityLevelConfiguration
    def __init__(self, type: _Optional[str] = ..., limited: _Optional[_Union[LimitedPriorityLevelConfiguration, _Mapping]] = ..., exempt: _Optional[_Union[ExemptPriorityLevelConfiguration, _Mapping]] = ...) -> None: ...

class PriorityLevelConfigurationStatus(_message.Message):
    __slots__ = ("conditions",)
    CONDITIONS_FIELD_NUMBER: _ClassVar[int]
    conditions: _containers.RepeatedCompositeFieldContainer[PriorityLevelConfigurationCondition]
    def __init__(self, conditions: _Optional[_Iterable[_Union[PriorityLevelConfigurationCondition, _Mapping]]] = ...) -> None: ...

class QueuingConfiguration(_message.Message):
    __slots__ = ("queues", "handSize", "queueLengthLimit")
    QUEUES_FIELD_NUMBER: _ClassVar[int]
    HANDSIZE_FIELD_NUMBER: _ClassVar[int]
    QUEUELENGTHLIMIT_FIELD_NUMBER: _ClassVar[int]
    queues: int
    handSize: int
    queueLengthLimit: int
    def __init__(self, queues: _Optional[int] = ..., handSize: _Optional[int] = ..., queueLengthLimit: _Optional[int] = ...) -> None: ...

class ResourcePolicyRule(_message.Message):
    __slots__ = ("verbs", "apiGroups", "resources", "clusterScope", "namespaces")
    VERBS_FIELD_NUMBER: _ClassVar[int]
    APIGROUPS_FIELD_NUMBER: _ClassVar[int]
    RESOURCES_FIELD_NUMBER: _ClassVar[int]
    CLUSTERSCOPE_FIELD_NUMBER: _ClassVar[int]
    NAMESPACES_FIELD_NUMBER: _ClassVar[int]
    verbs: _containers.RepeatedScalarFieldContainer[str]
    apiGroups: _containers.RepeatedScalarFieldContainer[str]
    resources: _containers.RepeatedScalarFieldContainer[str]
    clusterScope: bool
    namespaces: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, verbs: _Optional[_Iterable[str]] = ..., apiGroups: _Optional[_Iterable[str]] = ..., resources: _Optional[_Iterable[str]] = ..., clusterScope: bool = ..., namespaces: _Optional[_Iterable[str]] = ...) -> None: ...

class ServiceAccountSubject(_message.Message):
    __slots__ = ("namespace", "name")
    NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    namespace: str
    name: str
    def __init__(self, namespace: _Optional[str] = ..., name: _Optional[str] = ...) -> None: ...

class Subject(_message.Message):
    __slots__ = ("kind", "user", "group", "serviceAccount")
    KIND_FIELD_NUMBER: _ClassVar[int]
    USER_FIELD_NUMBER: _ClassVar[int]
    GROUP_FIELD_NUMBER: _ClassVar[int]
    SERVICEACCOUNT_FIELD_NUMBER: _ClassVar[int]
    kind: str
    user: UserSubject
    group: GroupSubject
    serviceAccount: ServiceAccountSubject
    def __init__(self, kind: _Optional[str] = ..., user: _Optional[_Union[UserSubject, _Mapping]] = ..., group: _Optional[_Union[GroupSubject, _Mapping]] = ..., serviceAccount: _Optional[_Union[ServiceAccountSubject, _Mapping]] = ...) -> None: ...

class UserSubject(_message.Message):
    __slots__ = ("name",)
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    def __init__(self, name: _Optional[str] = ...) -> None: ...
