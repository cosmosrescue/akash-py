from k8s.io.api.core.v1 import generated_pb2 as _generated_pb2
from k8s.io.apimachinery.pkg.apis.meta.v1 import generated_pb2 as _generated_pb2_1
from k8s.io.apimachinery.pkg.runtime import generated_pb2 as _generated_pb2_1_1
from k8s.io.apimachinery.pkg.runtime.schema import generated_pb2 as _generated_pb2_1_1_1
from k8s.io.apimachinery.pkg.util.intstr import generated_pb2 as _generated_pb2_1_1_1_1
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DaemonSet(_message.Message):
    __slots__ = ("metadata", "spec", "status")
    METADATA_FIELD_NUMBER: _ClassVar[int]
    SPEC_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    metadata: _generated_pb2_1.ObjectMeta
    spec: DaemonSetSpec
    status: DaemonSetStatus
    def __init__(self, metadata: _Optional[_Union[_generated_pb2_1.ObjectMeta, _Mapping]] = ..., spec: _Optional[_Union[DaemonSetSpec, _Mapping]] = ..., status: _Optional[_Union[DaemonSetStatus, _Mapping]] = ...) -> None: ...

class DaemonSetCondition(_message.Message):
    __slots__ = ("type", "status", "lastTransitionTime", "reason", "message")
    TYPE_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    LASTTRANSITIONTIME_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    type: str
    status: str
    lastTransitionTime: _generated_pb2_1.Time
    reason: str
    message: str
    def __init__(self, type: _Optional[str] = ..., status: _Optional[str] = ..., lastTransitionTime: _Optional[_Union[_generated_pb2_1.Time, _Mapping]] = ..., reason: _Optional[str] = ..., message: _Optional[str] = ...) -> None: ...

class DaemonSetList(_message.Message):
    __slots__ = ("metadata", "items")
    METADATA_FIELD_NUMBER: _ClassVar[int]
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    metadata: _generated_pb2_1.ListMeta
    items: _containers.RepeatedCompositeFieldContainer[DaemonSet]
    def __init__(self, metadata: _Optional[_Union[_generated_pb2_1.ListMeta, _Mapping]] = ..., items: _Optional[_Iterable[_Union[DaemonSet, _Mapping]]] = ...) -> None: ...

class DaemonSetSpec(_message.Message):
    __slots__ = ("selector", "template", "updateStrategy", "minReadySeconds", "templateGeneration", "revisionHistoryLimit")
    SELECTOR_FIELD_NUMBER: _ClassVar[int]
    TEMPLATE_FIELD_NUMBER: _ClassVar[int]
    UPDATESTRATEGY_FIELD_NUMBER: _ClassVar[int]
    MINREADYSECONDS_FIELD_NUMBER: _ClassVar[int]
    TEMPLATEGENERATION_FIELD_NUMBER: _ClassVar[int]
    REVISIONHISTORYLIMIT_FIELD_NUMBER: _ClassVar[int]
    selector: _generated_pb2_1.LabelSelector
    template: _generated_pb2.PodTemplateSpec
    updateStrategy: DaemonSetUpdateStrategy
    minReadySeconds: int
    templateGeneration: int
    revisionHistoryLimit: int
    def __init__(self, selector: _Optional[_Union[_generated_pb2_1.LabelSelector, _Mapping]] = ..., template: _Optional[_Union[_generated_pb2.PodTemplateSpec, _Mapping]] = ..., updateStrategy: _Optional[_Union[DaemonSetUpdateStrategy, _Mapping]] = ..., minReadySeconds: _Optional[int] = ..., templateGeneration: _Optional[int] = ..., revisionHistoryLimit: _Optional[int] = ...) -> None: ...

class DaemonSetStatus(_message.Message):
    __slots__ = ("currentNumberScheduled", "numberMisscheduled", "desiredNumberScheduled", "numberReady", "observedGeneration", "updatedNumberScheduled", "numberAvailable", "numberUnavailable", "collisionCount", "conditions")
    CURRENTNUMBERSCHEDULED_FIELD_NUMBER: _ClassVar[int]
    NUMBERMISSCHEDULED_FIELD_NUMBER: _ClassVar[int]
    DESIREDNUMBERSCHEDULED_FIELD_NUMBER: _ClassVar[int]
    NUMBERREADY_FIELD_NUMBER: _ClassVar[int]
    OBSERVEDGENERATION_FIELD_NUMBER: _ClassVar[int]
    UPDATEDNUMBERSCHEDULED_FIELD_NUMBER: _ClassVar[int]
    NUMBERAVAILABLE_FIELD_NUMBER: _ClassVar[int]
    NUMBERUNAVAILABLE_FIELD_NUMBER: _ClassVar[int]
    COLLISIONCOUNT_FIELD_NUMBER: _ClassVar[int]
    CONDITIONS_FIELD_NUMBER: _ClassVar[int]
    currentNumberScheduled: int
    numberMisscheduled: int
    desiredNumberScheduled: int
    numberReady: int
    observedGeneration: int
    updatedNumberScheduled: int
    numberAvailable: int
    numberUnavailable: int
    collisionCount: int
    conditions: _containers.RepeatedCompositeFieldContainer[DaemonSetCondition]
    def __init__(self, currentNumberScheduled: _Optional[int] = ..., numberMisscheduled: _Optional[int] = ..., desiredNumberScheduled: _Optional[int] = ..., numberReady: _Optional[int] = ..., observedGeneration: _Optional[int] = ..., updatedNumberScheduled: _Optional[int] = ..., numberAvailable: _Optional[int] = ..., numberUnavailable: _Optional[int] = ..., collisionCount: _Optional[int] = ..., conditions: _Optional[_Iterable[_Union[DaemonSetCondition, _Mapping]]] = ...) -> None: ...

class DaemonSetUpdateStrategy(_message.Message):
    __slots__ = ("type", "rollingUpdate")
    TYPE_FIELD_NUMBER: _ClassVar[int]
    ROLLINGUPDATE_FIELD_NUMBER: _ClassVar[int]
    type: str
    rollingUpdate: RollingUpdateDaemonSet
    def __init__(self, type: _Optional[str] = ..., rollingUpdate: _Optional[_Union[RollingUpdateDaemonSet, _Mapping]] = ...) -> None: ...

class Deployment(_message.Message):
    __slots__ = ("metadata", "spec", "status")
    METADATA_FIELD_NUMBER: _ClassVar[int]
    SPEC_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    metadata: _generated_pb2_1.ObjectMeta
    spec: DeploymentSpec
    status: DeploymentStatus
    def __init__(self, metadata: _Optional[_Union[_generated_pb2_1.ObjectMeta, _Mapping]] = ..., spec: _Optional[_Union[DeploymentSpec, _Mapping]] = ..., status: _Optional[_Union[DeploymentStatus, _Mapping]] = ...) -> None: ...

class DeploymentCondition(_message.Message):
    __slots__ = ("type", "status", "lastUpdateTime", "lastTransitionTime", "reason", "message")
    TYPE_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    LASTUPDATETIME_FIELD_NUMBER: _ClassVar[int]
    LASTTRANSITIONTIME_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    type: str
    status: str
    lastUpdateTime: _generated_pb2_1.Time
    lastTransitionTime: _generated_pb2_1.Time
    reason: str
    message: str
    def __init__(self, type: _Optional[str] = ..., status: _Optional[str] = ..., lastUpdateTime: _Optional[_Union[_generated_pb2_1.Time, _Mapping]] = ..., lastTransitionTime: _Optional[_Union[_generated_pb2_1.Time, _Mapping]] = ..., reason: _Optional[str] = ..., message: _Optional[str] = ...) -> None: ...

class DeploymentList(_message.Message):
    __slots__ = ("metadata", "items")
    METADATA_FIELD_NUMBER: _ClassVar[int]
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    metadata: _generated_pb2_1.ListMeta
    items: _containers.RepeatedCompositeFieldContainer[Deployment]
    def __init__(self, metadata: _Optional[_Union[_generated_pb2_1.ListMeta, _Mapping]] = ..., items: _Optional[_Iterable[_Union[Deployment, _Mapping]]] = ...) -> None: ...

class DeploymentRollback(_message.Message):
    __slots__ = ("name", "updatedAnnotations", "rollbackTo")
    class UpdatedAnnotationsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    NAME_FIELD_NUMBER: _ClassVar[int]
    UPDATEDANNOTATIONS_FIELD_NUMBER: _ClassVar[int]
    ROLLBACKTO_FIELD_NUMBER: _ClassVar[int]
    name: str
    updatedAnnotations: _containers.ScalarMap[str, str]
    rollbackTo: RollbackConfig
    def __init__(self, name: _Optional[str] = ..., updatedAnnotations: _Optional[_Mapping[str, str]] = ..., rollbackTo: _Optional[_Union[RollbackConfig, _Mapping]] = ...) -> None: ...

class DeploymentSpec(_message.Message):
    __slots__ = ("replicas", "selector", "template", "strategy", "minReadySeconds", "revisionHistoryLimit", "paused", "rollbackTo", "progressDeadlineSeconds")
    REPLICAS_FIELD_NUMBER: _ClassVar[int]
    SELECTOR_FIELD_NUMBER: _ClassVar[int]
    TEMPLATE_FIELD_NUMBER: _ClassVar[int]
    STRATEGY_FIELD_NUMBER: _ClassVar[int]
    MINREADYSECONDS_FIELD_NUMBER: _ClassVar[int]
    REVISIONHISTORYLIMIT_FIELD_NUMBER: _ClassVar[int]
    PAUSED_FIELD_NUMBER: _ClassVar[int]
    ROLLBACKTO_FIELD_NUMBER: _ClassVar[int]
    PROGRESSDEADLINESECONDS_FIELD_NUMBER: _ClassVar[int]
    replicas: int
    selector: _generated_pb2_1.LabelSelector
    template: _generated_pb2.PodTemplateSpec
    strategy: DeploymentStrategy
    minReadySeconds: int
    revisionHistoryLimit: int
    paused: bool
    rollbackTo: RollbackConfig
    progressDeadlineSeconds: int
    def __init__(self, replicas: _Optional[int] = ..., selector: _Optional[_Union[_generated_pb2_1.LabelSelector, _Mapping]] = ..., template: _Optional[_Union[_generated_pb2.PodTemplateSpec, _Mapping]] = ..., strategy: _Optional[_Union[DeploymentStrategy, _Mapping]] = ..., minReadySeconds: _Optional[int] = ..., revisionHistoryLimit: _Optional[int] = ..., paused: bool = ..., rollbackTo: _Optional[_Union[RollbackConfig, _Mapping]] = ..., progressDeadlineSeconds: _Optional[int] = ...) -> None: ...

class DeploymentStatus(_message.Message):
    __slots__ = ("observedGeneration", "replicas", "updatedReplicas", "readyReplicas", "availableReplicas", "unavailableReplicas", "conditions", "collisionCount")
    OBSERVEDGENERATION_FIELD_NUMBER: _ClassVar[int]
    REPLICAS_FIELD_NUMBER: _ClassVar[int]
    UPDATEDREPLICAS_FIELD_NUMBER: _ClassVar[int]
    READYREPLICAS_FIELD_NUMBER: _ClassVar[int]
    AVAILABLEREPLICAS_FIELD_NUMBER: _ClassVar[int]
    UNAVAILABLEREPLICAS_FIELD_NUMBER: _ClassVar[int]
    CONDITIONS_FIELD_NUMBER: _ClassVar[int]
    COLLISIONCOUNT_FIELD_NUMBER: _ClassVar[int]
    observedGeneration: int
    replicas: int
    updatedReplicas: int
    readyReplicas: int
    availableReplicas: int
    unavailableReplicas: int
    conditions: _containers.RepeatedCompositeFieldContainer[DeploymentCondition]
    collisionCount: int
    def __init__(self, observedGeneration: _Optional[int] = ..., replicas: _Optional[int] = ..., updatedReplicas: _Optional[int] = ..., readyReplicas: _Optional[int] = ..., availableReplicas: _Optional[int] = ..., unavailableReplicas: _Optional[int] = ..., conditions: _Optional[_Iterable[_Union[DeploymentCondition, _Mapping]]] = ..., collisionCount: _Optional[int] = ...) -> None: ...

class DeploymentStrategy(_message.Message):
    __slots__ = ("type", "rollingUpdate")
    TYPE_FIELD_NUMBER: _ClassVar[int]
    ROLLINGUPDATE_FIELD_NUMBER: _ClassVar[int]
    type: str
    rollingUpdate: RollingUpdateDeployment
    def __init__(self, type: _Optional[str] = ..., rollingUpdate: _Optional[_Union[RollingUpdateDeployment, _Mapping]] = ...) -> None: ...

class HTTPIngressPath(_message.Message):
    __slots__ = ("path", "pathType", "backend")
    PATH_FIELD_NUMBER: _ClassVar[int]
    PATHTYPE_FIELD_NUMBER: _ClassVar[int]
    BACKEND_FIELD_NUMBER: _ClassVar[int]
    path: str
    pathType: str
    backend: IngressBackend
    def __init__(self, path: _Optional[str] = ..., pathType: _Optional[str] = ..., backend: _Optional[_Union[IngressBackend, _Mapping]] = ...) -> None: ...

class HTTPIngressRuleValue(_message.Message):
    __slots__ = ("paths",)
    PATHS_FIELD_NUMBER: _ClassVar[int]
    paths: _containers.RepeatedCompositeFieldContainer[HTTPIngressPath]
    def __init__(self, paths: _Optional[_Iterable[_Union[HTTPIngressPath, _Mapping]]] = ...) -> None: ...

class IPBlock(_message.Message):
    __slots__ = ("cidr",)
    CIDR_FIELD_NUMBER: _ClassVar[int]
    EXCEPT_FIELD_NUMBER: _ClassVar[int]
    cidr: str
    def __init__(self, cidr: _Optional[str] = ..., **kwargs) -> None: ...

class Ingress(_message.Message):
    __slots__ = ("metadata", "spec", "status")
    METADATA_FIELD_NUMBER: _ClassVar[int]
    SPEC_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    metadata: _generated_pb2_1.ObjectMeta
    spec: IngressSpec
    status: IngressStatus
    def __init__(self, metadata: _Optional[_Union[_generated_pb2_1.ObjectMeta, _Mapping]] = ..., spec: _Optional[_Union[IngressSpec, _Mapping]] = ..., status: _Optional[_Union[IngressStatus, _Mapping]] = ...) -> None: ...

class IngressBackend(_message.Message):
    __slots__ = ("serviceName", "servicePort", "resource")
    SERVICENAME_FIELD_NUMBER: _ClassVar[int]
    SERVICEPORT_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_FIELD_NUMBER: _ClassVar[int]
    serviceName: str
    servicePort: _generated_pb2_1_1_1_1.IntOrString
    resource: _generated_pb2.TypedLocalObjectReference
    def __init__(self, serviceName: _Optional[str] = ..., servicePort: _Optional[_Union[_generated_pb2_1_1_1_1.IntOrString, _Mapping]] = ..., resource: _Optional[_Union[_generated_pb2.TypedLocalObjectReference, _Mapping]] = ...) -> None: ...

class IngressList(_message.Message):
    __slots__ = ("metadata", "items")
    METADATA_FIELD_NUMBER: _ClassVar[int]
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    metadata: _generated_pb2_1.ListMeta
    items: _containers.RepeatedCompositeFieldContainer[Ingress]
    def __init__(self, metadata: _Optional[_Union[_generated_pb2_1.ListMeta, _Mapping]] = ..., items: _Optional[_Iterable[_Union[Ingress, _Mapping]]] = ...) -> None: ...

class IngressLoadBalancerIngress(_message.Message):
    __slots__ = ("ip", "hostname", "ports")
    IP_FIELD_NUMBER: _ClassVar[int]
    HOSTNAME_FIELD_NUMBER: _ClassVar[int]
    PORTS_FIELD_NUMBER: _ClassVar[int]
    ip: str
    hostname: str
    ports: _containers.RepeatedCompositeFieldContainer[IngressPortStatus]
    def __init__(self, ip: _Optional[str] = ..., hostname: _Optional[str] = ..., ports: _Optional[_Iterable[_Union[IngressPortStatus, _Mapping]]] = ...) -> None: ...

class IngressLoadBalancerStatus(_message.Message):
    __slots__ = ("ingress",)
    INGRESS_FIELD_NUMBER: _ClassVar[int]
    ingress: _containers.RepeatedCompositeFieldContainer[IngressLoadBalancerIngress]
    def __init__(self, ingress: _Optional[_Iterable[_Union[IngressLoadBalancerIngress, _Mapping]]] = ...) -> None: ...

class IngressPortStatus(_message.Message):
    __slots__ = ("port", "protocol", "error")
    PORT_FIELD_NUMBER: _ClassVar[int]
    PROTOCOL_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    port: int
    protocol: str
    error: str
    def __init__(self, port: _Optional[int] = ..., protocol: _Optional[str] = ..., error: _Optional[str] = ...) -> None: ...

class IngressRule(_message.Message):
    __slots__ = ("host", "ingressRuleValue")
    HOST_FIELD_NUMBER: _ClassVar[int]
    INGRESSRULEVALUE_FIELD_NUMBER: _ClassVar[int]
    host: str
    ingressRuleValue: IngressRuleValue
    def __init__(self, host: _Optional[str] = ..., ingressRuleValue: _Optional[_Union[IngressRuleValue, _Mapping]] = ...) -> None: ...

class IngressRuleValue(_message.Message):
    __slots__ = ("http",)
    HTTP_FIELD_NUMBER: _ClassVar[int]
    http: HTTPIngressRuleValue
    def __init__(self, http: _Optional[_Union[HTTPIngressRuleValue, _Mapping]] = ...) -> None: ...

class IngressSpec(_message.Message):
    __slots__ = ("ingressClassName", "backend", "tls", "rules")
    INGRESSCLASSNAME_FIELD_NUMBER: _ClassVar[int]
    BACKEND_FIELD_NUMBER: _ClassVar[int]
    TLS_FIELD_NUMBER: _ClassVar[int]
    RULES_FIELD_NUMBER: _ClassVar[int]
    ingressClassName: str
    backend: IngressBackend
    tls: _containers.RepeatedCompositeFieldContainer[IngressTLS]
    rules: _containers.RepeatedCompositeFieldContainer[IngressRule]
    def __init__(self, ingressClassName: _Optional[str] = ..., backend: _Optional[_Union[IngressBackend, _Mapping]] = ..., tls: _Optional[_Iterable[_Union[IngressTLS, _Mapping]]] = ..., rules: _Optional[_Iterable[_Union[IngressRule, _Mapping]]] = ...) -> None: ...

class IngressStatus(_message.Message):
    __slots__ = ("loadBalancer",)
    LOADBALANCER_FIELD_NUMBER: _ClassVar[int]
    loadBalancer: IngressLoadBalancerStatus
    def __init__(self, loadBalancer: _Optional[_Union[IngressLoadBalancerStatus, _Mapping]] = ...) -> None: ...

class IngressTLS(_message.Message):
    __slots__ = ("hosts", "secretName")
    HOSTS_FIELD_NUMBER: _ClassVar[int]
    SECRETNAME_FIELD_NUMBER: _ClassVar[int]
    hosts: _containers.RepeatedScalarFieldContainer[str]
    secretName: str
    def __init__(self, hosts: _Optional[_Iterable[str]] = ..., secretName: _Optional[str] = ...) -> None: ...

class NetworkPolicy(_message.Message):
    __slots__ = ("metadata", "spec")
    METADATA_FIELD_NUMBER: _ClassVar[int]
    SPEC_FIELD_NUMBER: _ClassVar[int]
    metadata: _generated_pb2_1.ObjectMeta
    spec: NetworkPolicySpec
    def __init__(self, metadata: _Optional[_Union[_generated_pb2_1.ObjectMeta, _Mapping]] = ..., spec: _Optional[_Union[NetworkPolicySpec, _Mapping]] = ...) -> None: ...

class NetworkPolicyEgressRule(_message.Message):
    __slots__ = ("ports", "to")
    PORTS_FIELD_NUMBER: _ClassVar[int]
    TO_FIELD_NUMBER: _ClassVar[int]
    ports: _containers.RepeatedCompositeFieldContainer[NetworkPolicyPort]
    to: _containers.RepeatedCompositeFieldContainer[NetworkPolicyPeer]
    def __init__(self, ports: _Optional[_Iterable[_Union[NetworkPolicyPort, _Mapping]]] = ..., to: _Optional[_Iterable[_Union[NetworkPolicyPeer, _Mapping]]] = ...) -> None: ...

class NetworkPolicyIngressRule(_message.Message):
    __slots__ = ("ports",)
    PORTS_FIELD_NUMBER: _ClassVar[int]
    FROM_FIELD_NUMBER: _ClassVar[int]
    ports: _containers.RepeatedCompositeFieldContainer[NetworkPolicyPort]
    def __init__(self, ports: _Optional[_Iterable[_Union[NetworkPolicyPort, _Mapping]]] = ..., **kwargs) -> None: ...

class NetworkPolicyList(_message.Message):
    __slots__ = ("metadata", "items")
    METADATA_FIELD_NUMBER: _ClassVar[int]
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    metadata: _generated_pb2_1.ListMeta
    items: _containers.RepeatedCompositeFieldContainer[NetworkPolicy]
    def __init__(self, metadata: _Optional[_Union[_generated_pb2_1.ListMeta, _Mapping]] = ..., items: _Optional[_Iterable[_Union[NetworkPolicy, _Mapping]]] = ...) -> None: ...

class NetworkPolicyPeer(_message.Message):
    __slots__ = ("podSelector", "namespaceSelector", "ipBlock")
    PODSELECTOR_FIELD_NUMBER: _ClassVar[int]
    NAMESPACESELECTOR_FIELD_NUMBER: _ClassVar[int]
    IPBLOCK_FIELD_NUMBER: _ClassVar[int]
    podSelector: _generated_pb2_1.LabelSelector
    namespaceSelector: _generated_pb2_1.LabelSelector
    ipBlock: IPBlock
    def __init__(self, podSelector: _Optional[_Union[_generated_pb2_1.LabelSelector, _Mapping]] = ..., namespaceSelector: _Optional[_Union[_generated_pb2_1.LabelSelector, _Mapping]] = ..., ipBlock: _Optional[_Union[IPBlock, _Mapping]] = ...) -> None: ...

class NetworkPolicyPort(_message.Message):
    __slots__ = ("protocol", "port", "endPort")
    PROTOCOL_FIELD_NUMBER: _ClassVar[int]
    PORT_FIELD_NUMBER: _ClassVar[int]
    ENDPORT_FIELD_NUMBER: _ClassVar[int]
    protocol: str
    port: _generated_pb2_1_1_1_1.IntOrString
    endPort: int
    def __init__(self, protocol: _Optional[str] = ..., port: _Optional[_Union[_generated_pb2_1_1_1_1.IntOrString, _Mapping]] = ..., endPort: _Optional[int] = ...) -> None: ...

class NetworkPolicySpec(_message.Message):
    __slots__ = ("podSelector", "ingress", "egress", "policyTypes")
    PODSELECTOR_FIELD_NUMBER: _ClassVar[int]
    INGRESS_FIELD_NUMBER: _ClassVar[int]
    EGRESS_FIELD_NUMBER: _ClassVar[int]
    POLICYTYPES_FIELD_NUMBER: _ClassVar[int]
    podSelector: _generated_pb2_1.LabelSelector
    ingress: _containers.RepeatedCompositeFieldContainer[NetworkPolicyIngressRule]
    egress: _containers.RepeatedCompositeFieldContainer[NetworkPolicyEgressRule]
    policyTypes: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, podSelector: _Optional[_Union[_generated_pb2_1.LabelSelector, _Mapping]] = ..., ingress: _Optional[_Iterable[_Union[NetworkPolicyIngressRule, _Mapping]]] = ..., egress: _Optional[_Iterable[_Union[NetworkPolicyEgressRule, _Mapping]]] = ..., policyTypes: _Optional[_Iterable[str]] = ...) -> None: ...

class ReplicaSet(_message.Message):
    __slots__ = ("metadata", "spec", "status")
    METADATA_FIELD_NUMBER: _ClassVar[int]
    SPEC_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    metadata: _generated_pb2_1.ObjectMeta
    spec: ReplicaSetSpec
    status: ReplicaSetStatus
    def __init__(self, metadata: _Optional[_Union[_generated_pb2_1.ObjectMeta, _Mapping]] = ..., spec: _Optional[_Union[ReplicaSetSpec, _Mapping]] = ..., status: _Optional[_Union[ReplicaSetStatus, _Mapping]] = ...) -> None: ...

class ReplicaSetCondition(_message.Message):
    __slots__ = ("type", "status", "lastTransitionTime", "reason", "message")
    TYPE_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    LASTTRANSITIONTIME_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    type: str
    status: str
    lastTransitionTime: _generated_pb2_1.Time
    reason: str
    message: str
    def __init__(self, type: _Optional[str] = ..., status: _Optional[str] = ..., lastTransitionTime: _Optional[_Union[_generated_pb2_1.Time, _Mapping]] = ..., reason: _Optional[str] = ..., message: _Optional[str] = ...) -> None: ...

class ReplicaSetList(_message.Message):
    __slots__ = ("metadata", "items")
    METADATA_FIELD_NUMBER: _ClassVar[int]
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    metadata: _generated_pb2_1.ListMeta
    items: _containers.RepeatedCompositeFieldContainer[ReplicaSet]
    def __init__(self, metadata: _Optional[_Union[_generated_pb2_1.ListMeta, _Mapping]] = ..., items: _Optional[_Iterable[_Union[ReplicaSet, _Mapping]]] = ...) -> None: ...

class ReplicaSetSpec(_message.Message):
    __slots__ = ("replicas", "minReadySeconds", "selector", "template")
    REPLICAS_FIELD_NUMBER: _ClassVar[int]
    MINREADYSECONDS_FIELD_NUMBER: _ClassVar[int]
    SELECTOR_FIELD_NUMBER: _ClassVar[int]
    TEMPLATE_FIELD_NUMBER: _ClassVar[int]
    replicas: int
    minReadySeconds: int
    selector: _generated_pb2_1.LabelSelector
    template: _generated_pb2.PodTemplateSpec
    def __init__(self, replicas: _Optional[int] = ..., minReadySeconds: _Optional[int] = ..., selector: _Optional[_Union[_generated_pb2_1.LabelSelector, _Mapping]] = ..., template: _Optional[_Union[_generated_pb2.PodTemplateSpec, _Mapping]] = ...) -> None: ...

class ReplicaSetStatus(_message.Message):
    __slots__ = ("replicas", "fullyLabeledReplicas", "readyReplicas", "availableReplicas", "observedGeneration", "conditions")
    REPLICAS_FIELD_NUMBER: _ClassVar[int]
    FULLYLABELEDREPLICAS_FIELD_NUMBER: _ClassVar[int]
    READYREPLICAS_FIELD_NUMBER: _ClassVar[int]
    AVAILABLEREPLICAS_FIELD_NUMBER: _ClassVar[int]
    OBSERVEDGENERATION_FIELD_NUMBER: _ClassVar[int]
    CONDITIONS_FIELD_NUMBER: _ClassVar[int]
    replicas: int
    fullyLabeledReplicas: int
    readyReplicas: int
    availableReplicas: int
    observedGeneration: int
    conditions: _containers.RepeatedCompositeFieldContainer[ReplicaSetCondition]
    def __init__(self, replicas: _Optional[int] = ..., fullyLabeledReplicas: _Optional[int] = ..., readyReplicas: _Optional[int] = ..., availableReplicas: _Optional[int] = ..., observedGeneration: _Optional[int] = ..., conditions: _Optional[_Iterable[_Union[ReplicaSetCondition, _Mapping]]] = ...) -> None: ...

class RollbackConfig(_message.Message):
    __slots__ = ("revision",)
    REVISION_FIELD_NUMBER: _ClassVar[int]
    revision: int
    def __init__(self, revision: _Optional[int] = ...) -> None: ...

class RollingUpdateDaemonSet(_message.Message):
    __slots__ = ("maxUnavailable", "maxSurge")
    MAXUNAVAILABLE_FIELD_NUMBER: _ClassVar[int]
    MAXSURGE_FIELD_NUMBER: _ClassVar[int]
    maxUnavailable: _generated_pb2_1_1_1_1.IntOrString
    maxSurge: _generated_pb2_1_1_1_1.IntOrString
    def __init__(self, maxUnavailable: _Optional[_Union[_generated_pb2_1_1_1_1.IntOrString, _Mapping]] = ..., maxSurge: _Optional[_Union[_generated_pb2_1_1_1_1.IntOrString, _Mapping]] = ...) -> None: ...

class RollingUpdateDeployment(_message.Message):
    __slots__ = ("maxUnavailable", "maxSurge")
    MAXUNAVAILABLE_FIELD_NUMBER: _ClassVar[int]
    MAXSURGE_FIELD_NUMBER: _ClassVar[int]
    maxUnavailable: _generated_pb2_1_1_1_1.IntOrString
    maxSurge: _generated_pb2_1_1_1_1.IntOrString
    def __init__(self, maxUnavailable: _Optional[_Union[_generated_pb2_1_1_1_1.IntOrString, _Mapping]] = ..., maxSurge: _Optional[_Union[_generated_pb2_1_1_1_1.IntOrString, _Mapping]] = ...) -> None: ...

class Scale(_message.Message):
    __slots__ = ("metadata", "spec", "status")
    METADATA_FIELD_NUMBER: _ClassVar[int]
    SPEC_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    metadata: _generated_pb2_1.ObjectMeta
    spec: ScaleSpec
    status: ScaleStatus
    def __init__(self, metadata: _Optional[_Union[_generated_pb2_1.ObjectMeta, _Mapping]] = ..., spec: _Optional[_Union[ScaleSpec, _Mapping]] = ..., status: _Optional[_Union[ScaleStatus, _Mapping]] = ...) -> None: ...

class ScaleSpec(_message.Message):
    __slots__ = ("replicas",)
    REPLICAS_FIELD_NUMBER: _ClassVar[int]
    replicas: int
    def __init__(self, replicas: _Optional[int] = ...) -> None: ...

class ScaleStatus(_message.Message):
    __slots__ = ("replicas", "selector", "targetSelector")
    class SelectorEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    REPLICAS_FIELD_NUMBER: _ClassVar[int]
    SELECTOR_FIELD_NUMBER: _ClassVar[int]
    TARGETSELECTOR_FIELD_NUMBER: _ClassVar[int]
    replicas: int
    selector: _containers.ScalarMap[str, str]
    targetSelector: str
    def __init__(self, replicas: _Optional[int] = ..., selector: _Optional[_Mapping[str, str]] = ..., targetSelector: _Optional[str] = ...) -> None: ...
