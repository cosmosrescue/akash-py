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

class IPAddress(_message.Message):
    __slots__ = ("metadata", "spec")
    METADATA_FIELD_NUMBER: _ClassVar[int]
    SPEC_FIELD_NUMBER: _ClassVar[int]
    metadata: _generated_pb2_1.ObjectMeta
    spec: IPAddressSpec
    def __init__(self, metadata: _Optional[_Union[_generated_pb2_1.ObjectMeta, _Mapping]] = ..., spec: _Optional[_Union[IPAddressSpec, _Mapping]] = ...) -> None: ...

class IPAddressList(_message.Message):
    __slots__ = ("metadata", "items")
    METADATA_FIELD_NUMBER: _ClassVar[int]
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    metadata: _generated_pb2_1.ListMeta
    items: _containers.RepeatedCompositeFieldContainer[IPAddress]
    def __init__(self, metadata: _Optional[_Union[_generated_pb2_1.ListMeta, _Mapping]] = ..., items: _Optional[_Iterable[_Union[IPAddress, _Mapping]]] = ...) -> None: ...

class IPAddressSpec(_message.Message):
    __slots__ = ("parentRef",)
    PARENTREF_FIELD_NUMBER: _ClassVar[int]
    parentRef: ParentReference
    def __init__(self, parentRef: _Optional[_Union[ParentReference, _Mapping]] = ...) -> None: ...

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

class IngressClass(_message.Message):
    __slots__ = ("metadata", "spec")
    METADATA_FIELD_NUMBER: _ClassVar[int]
    SPEC_FIELD_NUMBER: _ClassVar[int]
    metadata: _generated_pb2_1.ObjectMeta
    spec: IngressClassSpec
    def __init__(self, metadata: _Optional[_Union[_generated_pb2_1.ObjectMeta, _Mapping]] = ..., spec: _Optional[_Union[IngressClassSpec, _Mapping]] = ...) -> None: ...

class IngressClassList(_message.Message):
    __slots__ = ("metadata", "items")
    METADATA_FIELD_NUMBER: _ClassVar[int]
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    metadata: _generated_pb2_1.ListMeta
    items: _containers.RepeatedCompositeFieldContainer[IngressClass]
    def __init__(self, metadata: _Optional[_Union[_generated_pb2_1.ListMeta, _Mapping]] = ..., items: _Optional[_Iterable[_Union[IngressClass, _Mapping]]] = ...) -> None: ...

class IngressClassParametersReference(_message.Message):
    __slots__ = ("aPIGroup", "kind", "name", "scope", "namespace")
    APIGROUP_FIELD_NUMBER: _ClassVar[int]
    KIND_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    SCOPE_FIELD_NUMBER: _ClassVar[int]
    NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    aPIGroup: str
    kind: str
    name: str
    scope: str
    namespace: str
    def __init__(self, aPIGroup: _Optional[str] = ..., kind: _Optional[str] = ..., name: _Optional[str] = ..., scope: _Optional[str] = ..., namespace: _Optional[str] = ...) -> None: ...

class IngressClassSpec(_message.Message):
    __slots__ = ("controller", "parameters")
    CONTROLLER_FIELD_NUMBER: _ClassVar[int]
    PARAMETERS_FIELD_NUMBER: _ClassVar[int]
    controller: str
    parameters: IngressClassParametersReference
    def __init__(self, controller: _Optional[str] = ..., parameters: _Optional[_Union[IngressClassParametersReference, _Mapping]] = ...) -> None: ...

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

class ParentReference(_message.Message):
    __slots__ = ("group", "resource", "namespace", "name")
    GROUP_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_FIELD_NUMBER: _ClassVar[int]
    NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    group: str
    resource: str
    namespace: str
    name: str
    def __init__(self, group: _Optional[str] = ..., resource: _Optional[str] = ..., namespace: _Optional[str] = ..., name: _Optional[str] = ...) -> None: ...

class ServiceCIDR(_message.Message):
    __slots__ = ("metadata", "spec", "status")
    METADATA_FIELD_NUMBER: _ClassVar[int]
    SPEC_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    metadata: _generated_pb2_1.ObjectMeta
    spec: ServiceCIDRSpec
    status: ServiceCIDRStatus
    def __init__(self, metadata: _Optional[_Union[_generated_pb2_1.ObjectMeta, _Mapping]] = ..., spec: _Optional[_Union[ServiceCIDRSpec, _Mapping]] = ..., status: _Optional[_Union[ServiceCIDRStatus, _Mapping]] = ...) -> None: ...

class ServiceCIDRList(_message.Message):
    __slots__ = ("metadata", "items")
    METADATA_FIELD_NUMBER: _ClassVar[int]
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    metadata: _generated_pb2_1.ListMeta
    items: _containers.RepeatedCompositeFieldContainer[ServiceCIDR]
    def __init__(self, metadata: _Optional[_Union[_generated_pb2_1.ListMeta, _Mapping]] = ..., items: _Optional[_Iterable[_Union[ServiceCIDR, _Mapping]]] = ...) -> None: ...

class ServiceCIDRSpec(_message.Message):
    __slots__ = ("cidrs",)
    CIDRS_FIELD_NUMBER: _ClassVar[int]
    cidrs: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, cidrs: _Optional[_Iterable[str]] = ...) -> None: ...

class ServiceCIDRStatus(_message.Message):
    __slots__ = ("conditions",)
    CONDITIONS_FIELD_NUMBER: _ClassVar[int]
    conditions: _containers.RepeatedCompositeFieldContainer[_generated_pb2_1.Condition]
    def __init__(self, conditions: _Optional[_Iterable[_Union[_generated_pb2_1.Condition, _Mapping]]] = ...) -> None: ...
