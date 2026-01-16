from k8s.io.api.core.v1 import generated_pb2 as _generated_pb2
from k8s.io.apimachinery.pkg.api.resource import generated_pb2 as _generated_pb2_1
from k8s.io.apimachinery.pkg.apis.meta.v1 import generated_pb2 as _generated_pb2_1_1
from k8s.io.apimachinery.pkg.runtime import generated_pb2 as _generated_pb2_1_1_1
from k8s.io.apimachinery.pkg.runtime.schema import generated_pb2 as _generated_pb2_1_1_1_1
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ContainerResourceMetricSource(_message.Message):
    __slots__ = ("name", "targetAverageUtilization", "targetAverageValue", "container")
    NAME_FIELD_NUMBER: _ClassVar[int]
    TARGETAVERAGEUTILIZATION_FIELD_NUMBER: _ClassVar[int]
    TARGETAVERAGEVALUE_FIELD_NUMBER: _ClassVar[int]
    CONTAINER_FIELD_NUMBER: _ClassVar[int]
    name: str
    targetAverageUtilization: int
    targetAverageValue: _generated_pb2_1.Quantity
    container: str
    def __init__(self, name: _Optional[str] = ..., targetAverageUtilization: _Optional[int] = ..., targetAverageValue: _Optional[_Union[_generated_pb2_1.Quantity, _Mapping]] = ..., container: _Optional[str] = ...) -> None: ...

class ContainerResourceMetricStatus(_message.Message):
    __slots__ = ("name", "currentAverageUtilization", "currentAverageValue", "container")
    NAME_FIELD_NUMBER: _ClassVar[int]
    CURRENTAVERAGEUTILIZATION_FIELD_NUMBER: _ClassVar[int]
    CURRENTAVERAGEVALUE_FIELD_NUMBER: _ClassVar[int]
    CONTAINER_FIELD_NUMBER: _ClassVar[int]
    name: str
    currentAverageUtilization: int
    currentAverageValue: _generated_pb2_1.Quantity
    container: str
    def __init__(self, name: _Optional[str] = ..., currentAverageUtilization: _Optional[int] = ..., currentAverageValue: _Optional[_Union[_generated_pb2_1.Quantity, _Mapping]] = ..., container: _Optional[str] = ...) -> None: ...

class CrossVersionObjectReference(_message.Message):
    __slots__ = ("kind", "name", "apiVersion")
    KIND_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    APIVERSION_FIELD_NUMBER: _ClassVar[int]
    kind: str
    name: str
    apiVersion: str
    def __init__(self, kind: _Optional[str] = ..., name: _Optional[str] = ..., apiVersion: _Optional[str] = ...) -> None: ...

class ExternalMetricSource(_message.Message):
    __slots__ = ("metricName", "metricSelector", "targetValue", "targetAverageValue")
    METRICNAME_FIELD_NUMBER: _ClassVar[int]
    METRICSELECTOR_FIELD_NUMBER: _ClassVar[int]
    TARGETVALUE_FIELD_NUMBER: _ClassVar[int]
    TARGETAVERAGEVALUE_FIELD_NUMBER: _ClassVar[int]
    metricName: str
    metricSelector: _generated_pb2_1_1.LabelSelector
    targetValue: _generated_pb2_1.Quantity
    targetAverageValue: _generated_pb2_1.Quantity
    def __init__(self, metricName: _Optional[str] = ..., metricSelector: _Optional[_Union[_generated_pb2_1_1.LabelSelector, _Mapping]] = ..., targetValue: _Optional[_Union[_generated_pb2_1.Quantity, _Mapping]] = ..., targetAverageValue: _Optional[_Union[_generated_pb2_1.Quantity, _Mapping]] = ...) -> None: ...

class ExternalMetricStatus(_message.Message):
    __slots__ = ("metricName", "metricSelector", "currentValue", "currentAverageValue")
    METRICNAME_FIELD_NUMBER: _ClassVar[int]
    METRICSELECTOR_FIELD_NUMBER: _ClassVar[int]
    CURRENTVALUE_FIELD_NUMBER: _ClassVar[int]
    CURRENTAVERAGEVALUE_FIELD_NUMBER: _ClassVar[int]
    metricName: str
    metricSelector: _generated_pb2_1_1.LabelSelector
    currentValue: _generated_pb2_1.Quantity
    currentAverageValue: _generated_pb2_1.Quantity
    def __init__(self, metricName: _Optional[str] = ..., metricSelector: _Optional[_Union[_generated_pb2_1_1.LabelSelector, _Mapping]] = ..., currentValue: _Optional[_Union[_generated_pb2_1.Quantity, _Mapping]] = ..., currentAverageValue: _Optional[_Union[_generated_pb2_1.Quantity, _Mapping]] = ...) -> None: ...

class HorizontalPodAutoscaler(_message.Message):
    __slots__ = ("metadata", "spec", "status")
    METADATA_FIELD_NUMBER: _ClassVar[int]
    SPEC_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    metadata: _generated_pb2_1_1.ObjectMeta
    spec: HorizontalPodAutoscalerSpec
    status: HorizontalPodAutoscalerStatus
    def __init__(self, metadata: _Optional[_Union[_generated_pb2_1_1.ObjectMeta, _Mapping]] = ..., spec: _Optional[_Union[HorizontalPodAutoscalerSpec, _Mapping]] = ..., status: _Optional[_Union[HorizontalPodAutoscalerStatus, _Mapping]] = ...) -> None: ...

class HorizontalPodAutoscalerCondition(_message.Message):
    __slots__ = ("type", "status", "lastTransitionTime", "reason", "message")
    TYPE_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    LASTTRANSITIONTIME_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    type: str
    status: str
    lastTransitionTime: _generated_pb2_1_1.Time
    reason: str
    message: str
    def __init__(self, type: _Optional[str] = ..., status: _Optional[str] = ..., lastTransitionTime: _Optional[_Union[_generated_pb2_1_1.Time, _Mapping]] = ..., reason: _Optional[str] = ..., message: _Optional[str] = ...) -> None: ...

class HorizontalPodAutoscalerList(_message.Message):
    __slots__ = ("metadata", "items")
    METADATA_FIELD_NUMBER: _ClassVar[int]
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    metadata: _generated_pb2_1_1.ListMeta
    items: _containers.RepeatedCompositeFieldContainer[HorizontalPodAutoscaler]
    def __init__(self, metadata: _Optional[_Union[_generated_pb2_1_1.ListMeta, _Mapping]] = ..., items: _Optional[_Iterable[_Union[HorizontalPodAutoscaler, _Mapping]]] = ...) -> None: ...

class HorizontalPodAutoscalerSpec(_message.Message):
    __slots__ = ("scaleTargetRef", "minReplicas", "maxReplicas", "metrics")
    SCALETARGETREF_FIELD_NUMBER: _ClassVar[int]
    MINREPLICAS_FIELD_NUMBER: _ClassVar[int]
    MAXREPLICAS_FIELD_NUMBER: _ClassVar[int]
    METRICS_FIELD_NUMBER: _ClassVar[int]
    scaleTargetRef: CrossVersionObjectReference
    minReplicas: int
    maxReplicas: int
    metrics: _containers.RepeatedCompositeFieldContainer[MetricSpec]
    def __init__(self, scaleTargetRef: _Optional[_Union[CrossVersionObjectReference, _Mapping]] = ..., minReplicas: _Optional[int] = ..., maxReplicas: _Optional[int] = ..., metrics: _Optional[_Iterable[_Union[MetricSpec, _Mapping]]] = ...) -> None: ...

class HorizontalPodAutoscalerStatus(_message.Message):
    __slots__ = ("observedGeneration", "lastScaleTime", "currentReplicas", "desiredReplicas", "currentMetrics", "conditions")
    OBSERVEDGENERATION_FIELD_NUMBER: _ClassVar[int]
    LASTSCALETIME_FIELD_NUMBER: _ClassVar[int]
    CURRENTREPLICAS_FIELD_NUMBER: _ClassVar[int]
    DESIREDREPLICAS_FIELD_NUMBER: _ClassVar[int]
    CURRENTMETRICS_FIELD_NUMBER: _ClassVar[int]
    CONDITIONS_FIELD_NUMBER: _ClassVar[int]
    observedGeneration: int
    lastScaleTime: _generated_pb2_1_1.Time
    currentReplicas: int
    desiredReplicas: int
    currentMetrics: _containers.RepeatedCompositeFieldContainer[MetricStatus]
    conditions: _containers.RepeatedCompositeFieldContainer[HorizontalPodAutoscalerCondition]
    def __init__(self, observedGeneration: _Optional[int] = ..., lastScaleTime: _Optional[_Union[_generated_pb2_1_1.Time, _Mapping]] = ..., currentReplicas: _Optional[int] = ..., desiredReplicas: _Optional[int] = ..., currentMetrics: _Optional[_Iterable[_Union[MetricStatus, _Mapping]]] = ..., conditions: _Optional[_Iterable[_Union[HorizontalPodAutoscalerCondition, _Mapping]]] = ...) -> None: ...

class MetricSpec(_message.Message):
    __slots__ = ("type", "object", "pods", "resource", "containerResource", "external")
    TYPE_FIELD_NUMBER: _ClassVar[int]
    OBJECT_FIELD_NUMBER: _ClassVar[int]
    PODS_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_FIELD_NUMBER: _ClassVar[int]
    CONTAINERRESOURCE_FIELD_NUMBER: _ClassVar[int]
    EXTERNAL_FIELD_NUMBER: _ClassVar[int]
    type: str
    object: ObjectMetricSource
    pods: PodsMetricSource
    resource: ResourceMetricSource
    containerResource: ContainerResourceMetricSource
    external: ExternalMetricSource
    def __init__(self, type: _Optional[str] = ..., object: _Optional[_Union[ObjectMetricSource, _Mapping]] = ..., pods: _Optional[_Union[PodsMetricSource, _Mapping]] = ..., resource: _Optional[_Union[ResourceMetricSource, _Mapping]] = ..., containerResource: _Optional[_Union[ContainerResourceMetricSource, _Mapping]] = ..., external: _Optional[_Union[ExternalMetricSource, _Mapping]] = ...) -> None: ...

class MetricStatus(_message.Message):
    __slots__ = ("type", "object", "pods", "resource", "containerResource", "external")
    TYPE_FIELD_NUMBER: _ClassVar[int]
    OBJECT_FIELD_NUMBER: _ClassVar[int]
    PODS_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_FIELD_NUMBER: _ClassVar[int]
    CONTAINERRESOURCE_FIELD_NUMBER: _ClassVar[int]
    EXTERNAL_FIELD_NUMBER: _ClassVar[int]
    type: str
    object: ObjectMetricStatus
    pods: PodsMetricStatus
    resource: ResourceMetricStatus
    containerResource: ContainerResourceMetricStatus
    external: ExternalMetricStatus
    def __init__(self, type: _Optional[str] = ..., object: _Optional[_Union[ObjectMetricStatus, _Mapping]] = ..., pods: _Optional[_Union[PodsMetricStatus, _Mapping]] = ..., resource: _Optional[_Union[ResourceMetricStatus, _Mapping]] = ..., containerResource: _Optional[_Union[ContainerResourceMetricStatus, _Mapping]] = ..., external: _Optional[_Union[ExternalMetricStatus, _Mapping]] = ...) -> None: ...

class ObjectMetricSource(_message.Message):
    __slots__ = ("target", "metricName", "targetValue", "selector", "averageValue")
    TARGET_FIELD_NUMBER: _ClassVar[int]
    METRICNAME_FIELD_NUMBER: _ClassVar[int]
    TARGETVALUE_FIELD_NUMBER: _ClassVar[int]
    SELECTOR_FIELD_NUMBER: _ClassVar[int]
    AVERAGEVALUE_FIELD_NUMBER: _ClassVar[int]
    target: CrossVersionObjectReference
    metricName: str
    targetValue: _generated_pb2_1.Quantity
    selector: _generated_pb2_1_1.LabelSelector
    averageValue: _generated_pb2_1.Quantity
    def __init__(self, target: _Optional[_Union[CrossVersionObjectReference, _Mapping]] = ..., metricName: _Optional[str] = ..., targetValue: _Optional[_Union[_generated_pb2_1.Quantity, _Mapping]] = ..., selector: _Optional[_Union[_generated_pb2_1_1.LabelSelector, _Mapping]] = ..., averageValue: _Optional[_Union[_generated_pb2_1.Quantity, _Mapping]] = ...) -> None: ...

class ObjectMetricStatus(_message.Message):
    __slots__ = ("target", "metricName", "currentValue", "selector", "averageValue")
    TARGET_FIELD_NUMBER: _ClassVar[int]
    METRICNAME_FIELD_NUMBER: _ClassVar[int]
    CURRENTVALUE_FIELD_NUMBER: _ClassVar[int]
    SELECTOR_FIELD_NUMBER: _ClassVar[int]
    AVERAGEVALUE_FIELD_NUMBER: _ClassVar[int]
    target: CrossVersionObjectReference
    metricName: str
    currentValue: _generated_pb2_1.Quantity
    selector: _generated_pb2_1_1.LabelSelector
    averageValue: _generated_pb2_1.Quantity
    def __init__(self, target: _Optional[_Union[CrossVersionObjectReference, _Mapping]] = ..., metricName: _Optional[str] = ..., currentValue: _Optional[_Union[_generated_pb2_1.Quantity, _Mapping]] = ..., selector: _Optional[_Union[_generated_pb2_1_1.LabelSelector, _Mapping]] = ..., averageValue: _Optional[_Union[_generated_pb2_1.Quantity, _Mapping]] = ...) -> None: ...

class PodsMetricSource(_message.Message):
    __slots__ = ("metricName", "targetAverageValue", "selector")
    METRICNAME_FIELD_NUMBER: _ClassVar[int]
    TARGETAVERAGEVALUE_FIELD_NUMBER: _ClassVar[int]
    SELECTOR_FIELD_NUMBER: _ClassVar[int]
    metricName: str
    targetAverageValue: _generated_pb2_1.Quantity
    selector: _generated_pb2_1_1.LabelSelector
    def __init__(self, metricName: _Optional[str] = ..., targetAverageValue: _Optional[_Union[_generated_pb2_1.Quantity, _Mapping]] = ..., selector: _Optional[_Union[_generated_pb2_1_1.LabelSelector, _Mapping]] = ...) -> None: ...

class PodsMetricStatus(_message.Message):
    __slots__ = ("metricName", "currentAverageValue", "selector")
    METRICNAME_FIELD_NUMBER: _ClassVar[int]
    CURRENTAVERAGEVALUE_FIELD_NUMBER: _ClassVar[int]
    SELECTOR_FIELD_NUMBER: _ClassVar[int]
    metricName: str
    currentAverageValue: _generated_pb2_1.Quantity
    selector: _generated_pb2_1_1.LabelSelector
    def __init__(self, metricName: _Optional[str] = ..., currentAverageValue: _Optional[_Union[_generated_pb2_1.Quantity, _Mapping]] = ..., selector: _Optional[_Union[_generated_pb2_1_1.LabelSelector, _Mapping]] = ...) -> None: ...

class ResourceMetricSource(_message.Message):
    __slots__ = ("name", "targetAverageUtilization", "targetAverageValue")
    NAME_FIELD_NUMBER: _ClassVar[int]
    TARGETAVERAGEUTILIZATION_FIELD_NUMBER: _ClassVar[int]
    TARGETAVERAGEVALUE_FIELD_NUMBER: _ClassVar[int]
    name: str
    targetAverageUtilization: int
    targetAverageValue: _generated_pb2_1.Quantity
    def __init__(self, name: _Optional[str] = ..., targetAverageUtilization: _Optional[int] = ..., targetAverageValue: _Optional[_Union[_generated_pb2_1.Quantity, _Mapping]] = ...) -> None: ...

class ResourceMetricStatus(_message.Message):
    __slots__ = ("name", "currentAverageUtilization", "currentAverageValue")
    NAME_FIELD_NUMBER: _ClassVar[int]
    CURRENTAVERAGEUTILIZATION_FIELD_NUMBER: _ClassVar[int]
    CURRENTAVERAGEVALUE_FIELD_NUMBER: _ClassVar[int]
    name: str
    currentAverageUtilization: int
    currentAverageValue: _generated_pb2_1.Quantity
    def __init__(self, name: _Optional[str] = ..., currentAverageUtilization: _Optional[int] = ..., currentAverageValue: _Optional[_Union[_generated_pb2_1.Quantity, _Mapping]] = ...) -> None: ...
