from k8s.io.api.admissionregistration.v1 import generated_pb2 as _generated_pb2
from k8s.io.apimachinery.pkg.apis.meta.v1 import generated_pb2 as _generated_pb2_1
from k8s.io.apimachinery.pkg.runtime import generated_pb2 as _generated_pb2_1_1
from k8s.io.apimachinery.pkg.runtime.schema import generated_pb2 as _generated_pb2_1_1_1
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class AuditAnnotation(_message.Message):
    __slots__ = ("key", "valueExpression")
    KEY_FIELD_NUMBER: _ClassVar[int]
    VALUEEXPRESSION_FIELD_NUMBER: _ClassVar[int]
    key: str
    valueExpression: str
    def __init__(self, key: _Optional[str] = ..., valueExpression: _Optional[str] = ...) -> None: ...

class ExpressionWarning(_message.Message):
    __slots__ = ("fieldRef", "warning")
    FIELDREF_FIELD_NUMBER: _ClassVar[int]
    WARNING_FIELD_NUMBER: _ClassVar[int]
    fieldRef: str
    warning: str
    def __init__(self, fieldRef: _Optional[str] = ..., warning: _Optional[str] = ...) -> None: ...

class MatchCondition(_message.Message):
    __slots__ = ("name", "expression")
    NAME_FIELD_NUMBER: _ClassVar[int]
    EXPRESSION_FIELD_NUMBER: _ClassVar[int]
    name: str
    expression: str
    def __init__(self, name: _Optional[str] = ..., expression: _Optional[str] = ...) -> None: ...

class MatchResources(_message.Message):
    __slots__ = ("namespaceSelector", "objectSelector", "resourceRules", "excludeResourceRules", "matchPolicy")
    NAMESPACESELECTOR_FIELD_NUMBER: _ClassVar[int]
    OBJECTSELECTOR_FIELD_NUMBER: _ClassVar[int]
    RESOURCERULES_FIELD_NUMBER: _ClassVar[int]
    EXCLUDERESOURCERULES_FIELD_NUMBER: _ClassVar[int]
    MATCHPOLICY_FIELD_NUMBER: _ClassVar[int]
    namespaceSelector: _generated_pb2_1.LabelSelector
    objectSelector: _generated_pb2_1.LabelSelector
    resourceRules: _containers.RepeatedCompositeFieldContainer[NamedRuleWithOperations]
    excludeResourceRules: _containers.RepeatedCompositeFieldContainer[NamedRuleWithOperations]
    matchPolicy: str
    def __init__(self, namespaceSelector: _Optional[_Union[_generated_pb2_1.LabelSelector, _Mapping]] = ..., objectSelector: _Optional[_Union[_generated_pb2_1.LabelSelector, _Mapping]] = ..., resourceRules: _Optional[_Iterable[_Union[NamedRuleWithOperations, _Mapping]]] = ..., excludeResourceRules: _Optional[_Iterable[_Union[NamedRuleWithOperations, _Mapping]]] = ..., matchPolicy: _Optional[str] = ...) -> None: ...

class NamedRuleWithOperations(_message.Message):
    __slots__ = ("resourceNames", "ruleWithOperations")
    RESOURCENAMES_FIELD_NUMBER: _ClassVar[int]
    RULEWITHOPERATIONS_FIELD_NUMBER: _ClassVar[int]
    resourceNames: _containers.RepeatedScalarFieldContainer[str]
    ruleWithOperations: _generated_pb2.RuleWithOperations
    def __init__(self, resourceNames: _Optional[_Iterable[str]] = ..., ruleWithOperations: _Optional[_Union[_generated_pb2.RuleWithOperations, _Mapping]] = ...) -> None: ...

class ParamKind(_message.Message):
    __slots__ = ("apiVersion", "kind")
    APIVERSION_FIELD_NUMBER: _ClassVar[int]
    KIND_FIELD_NUMBER: _ClassVar[int]
    apiVersion: str
    kind: str
    def __init__(self, apiVersion: _Optional[str] = ..., kind: _Optional[str] = ...) -> None: ...

class ParamRef(_message.Message):
    __slots__ = ("name", "namespace", "selector", "parameterNotFoundAction")
    NAME_FIELD_NUMBER: _ClassVar[int]
    NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    SELECTOR_FIELD_NUMBER: _ClassVar[int]
    PARAMETERNOTFOUNDACTION_FIELD_NUMBER: _ClassVar[int]
    name: str
    namespace: str
    selector: _generated_pb2_1.LabelSelector
    parameterNotFoundAction: str
    def __init__(self, name: _Optional[str] = ..., namespace: _Optional[str] = ..., selector: _Optional[_Union[_generated_pb2_1.LabelSelector, _Mapping]] = ..., parameterNotFoundAction: _Optional[str] = ...) -> None: ...

class TypeChecking(_message.Message):
    __slots__ = ("expressionWarnings",)
    EXPRESSIONWARNINGS_FIELD_NUMBER: _ClassVar[int]
    expressionWarnings: _containers.RepeatedCompositeFieldContainer[ExpressionWarning]
    def __init__(self, expressionWarnings: _Optional[_Iterable[_Union[ExpressionWarning, _Mapping]]] = ...) -> None: ...

class ValidatingAdmissionPolicy(_message.Message):
    __slots__ = ("metadata", "spec", "status")
    METADATA_FIELD_NUMBER: _ClassVar[int]
    SPEC_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    metadata: _generated_pb2_1.ObjectMeta
    spec: ValidatingAdmissionPolicySpec
    status: ValidatingAdmissionPolicyStatus
    def __init__(self, metadata: _Optional[_Union[_generated_pb2_1.ObjectMeta, _Mapping]] = ..., spec: _Optional[_Union[ValidatingAdmissionPolicySpec, _Mapping]] = ..., status: _Optional[_Union[ValidatingAdmissionPolicyStatus, _Mapping]] = ...) -> None: ...

class ValidatingAdmissionPolicyBinding(_message.Message):
    __slots__ = ("metadata", "spec")
    METADATA_FIELD_NUMBER: _ClassVar[int]
    SPEC_FIELD_NUMBER: _ClassVar[int]
    metadata: _generated_pb2_1.ObjectMeta
    spec: ValidatingAdmissionPolicyBindingSpec
    def __init__(self, metadata: _Optional[_Union[_generated_pb2_1.ObjectMeta, _Mapping]] = ..., spec: _Optional[_Union[ValidatingAdmissionPolicyBindingSpec, _Mapping]] = ...) -> None: ...

class ValidatingAdmissionPolicyBindingList(_message.Message):
    __slots__ = ("metadata", "items")
    METADATA_FIELD_NUMBER: _ClassVar[int]
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    metadata: _generated_pb2_1.ListMeta
    items: _containers.RepeatedCompositeFieldContainer[ValidatingAdmissionPolicyBinding]
    def __init__(self, metadata: _Optional[_Union[_generated_pb2_1.ListMeta, _Mapping]] = ..., items: _Optional[_Iterable[_Union[ValidatingAdmissionPolicyBinding, _Mapping]]] = ...) -> None: ...

class ValidatingAdmissionPolicyBindingSpec(_message.Message):
    __slots__ = ("policyName", "paramRef", "matchResources", "validationActions")
    POLICYNAME_FIELD_NUMBER: _ClassVar[int]
    PARAMREF_FIELD_NUMBER: _ClassVar[int]
    MATCHRESOURCES_FIELD_NUMBER: _ClassVar[int]
    VALIDATIONACTIONS_FIELD_NUMBER: _ClassVar[int]
    policyName: str
    paramRef: ParamRef
    matchResources: MatchResources
    validationActions: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, policyName: _Optional[str] = ..., paramRef: _Optional[_Union[ParamRef, _Mapping]] = ..., matchResources: _Optional[_Union[MatchResources, _Mapping]] = ..., validationActions: _Optional[_Iterable[str]] = ...) -> None: ...

class ValidatingAdmissionPolicyList(_message.Message):
    __slots__ = ("metadata", "items")
    METADATA_FIELD_NUMBER: _ClassVar[int]
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    metadata: _generated_pb2_1.ListMeta
    items: _containers.RepeatedCompositeFieldContainer[ValidatingAdmissionPolicy]
    def __init__(self, metadata: _Optional[_Union[_generated_pb2_1.ListMeta, _Mapping]] = ..., items: _Optional[_Iterable[_Union[ValidatingAdmissionPolicy, _Mapping]]] = ...) -> None: ...

class ValidatingAdmissionPolicySpec(_message.Message):
    __slots__ = ("paramKind", "matchConstraints", "validations", "failurePolicy", "auditAnnotations", "matchConditions", "variables")
    PARAMKIND_FIELD_NUMBER: _ClassVar[int]
    MATCHCONSTRAINTS_FIELD_NUMBER: _ClassVar[int]
    VALIDATIONS_FIELD_NUMBER: _ClassVar[int]
    FAILUREPOLICY_FIELD_NUMBER: _ClassVar[int]
    AUDITANNOTATIONS_FIELD_NUMBER: _ClassVar[int]
    MATCHCONDITIONS_FIELD_NUMBER: _ClassVar[int]
    VARIABLES_FIELD_NUMBER: _ClassVar[int]
    paramKind: ParamKind
    matchConstraints: MatchResources
    validations: _containers.RepeatedCompositeFieldContainer[Validation]
    failurePolicy: str
    auditAnnotations: _containers.RepeatedCompositeFieldContainer[AuditAnnotation]
    matchConditions: _containers.RepeatedCompositeFieldContainer[MatchCondition]
    variables: _containers.RepeatedCompositeFieldContainer[Variable]
    def __init__(self, paramKind: _Optional[_Union[ParamKind, _Mapping]] = ..., matchConstraints: _Optional[_Union[MatchResources, _Mapping]] = ..., validations: _Optional[_Iterable[_Union[Validation, _Mapping]]] = ..., failurePolicy: _Optional[str] = ..., auditAnnotations: _Optional[_Iterable[_Union[AuditAnnotation, _Mapping]]] = ..., matchConditions: _Optional[_Iterable[_Union[MatchCondition, _Mapping]]] = ..., variables: _Optional[_Iterable[_Union[Variable, _Mapping]]] = ...) -> None: ...

class ValidatingAdmissionPolicyStatus(_message.Message):
    __slots__ = ("observedGeneration", "typeChecking", "conditions")
    OBSERVEDGENERATION_FIELD_NUMBER: _ClassVar[int]
    TYPECHECKING_FIELD_NUMBER: _ClassVar[int]
    CONDITIONS_FIELD_NUMBER: _ClassVar[int]
    observedGeneration: int
    typeChecking: TypeChecking
    conditions: _containers.RepeatedCompositeFieldContainer[_generated_pb2_1.Condition]
    def __init__(self, observedGeneration: _Optional[int] = ..., typeChecking: _Optional[_Union[TypeChecking, _Mapping]] = ..., conditions: _Optional[_Iterable[_Union[_generated_pb2_1.Condition, _Mapping]]] = ...) -> None: ...

class Validation(_message.Message):
    __slots__ = ("Expression", "message", "reason", "messageExpression")
    EXPRESSION_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    MESSAGEEXPRESSION_FIELD_NUMBER: _ClassVar[int]
    Expression: str
    message: str
    reason: str
    messageExpression: str
    def __init__(self, Expression: _Optional[str] = ..., message: _Optional[str] = ..., reason: _Optional[str] = ..., messageExpression: _Optional[str] = ...) -> None: ...

class Variable(_message.Message):
    __slots__ = ("Name", "Expression")
    NAME_FIELD_NUMBER: _ClassVar[int]
    EXPRESSION_FIELD_NUMBER: _ClassVar[int]
    Name: str
    Expression: str
    def __init__(self, Name: _Optional[str] = ..., Expression: _Optional[str] = ...) -> None: ...
