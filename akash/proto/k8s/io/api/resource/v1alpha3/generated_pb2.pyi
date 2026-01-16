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

class AllocationResult(_message.Message):
    __slots__ = ("devices", "nodeSelector", "controller")
    DEVICES_FIELD_NUMBER: _ClassVar[int]
    NODESELECTOR_FIELD_NUMBER: _ClassVar[int]
    CONTROLLER_FIELD_NUMBER: _ClassVar[int]
    devices: DeviceAllocationResult
    nodeSelector: _generated_pb2.NodeSelector
    controller: str
    def __init__(self, devices: _Optional[_Union[DeviceAllocationResult, _Mapping]] = ..., nodeSelector: _Optional[_Union[_generated_pb2.NodeSelector, _Mapping]] = ..., controller: _Optional[str] = ...) -> None: ...

class BasicDevice(_message.Message):
    __slots__ = ("attributes", "capacity")
    class AttributesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: DeviceAttribute
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[DeviceAttribute, _Mapping]] = ...) -> None: ...
    class CapacityEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: _generated_pb2_1.Quantity
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[_generated_pb2_1.Quantity, _Mapping]] = ...) -> None: ...
    ATTRIBUTES_FIELD_NUMBER: _ClassVar[int]
    CAPACITY_FIELD_NUMBER: _ClassVar[int]
    attributes: _containers.MessageMap[str, DeviceAttribute]
    capacity: _containers.MessageMap[str, _generated_pb2_1.Quantity]
    def __init__(self, attributes: _Optional[_Mapping[str, DeviceAttribute]] = ..., capacity: _Optional[_Mapping[str, _generated_pb2_1.Quantity]] = ...) -> None: ...

class CELDeviceSelector(_message.Message):
    __slots__ = ("expression",)
    EXPRESSION_FIELD_NUMBER: _ClassVar[int]
    expression: str
    def __init__(self, expression: _Optional[str] = ...) -> None: ...

class Device(_message.Message):
    __slots__ = ("name", "basic")
    NAME_FIELD_NUMBER: _ClassVar[int]
    BASIC_FIELD_NUMBER: _ClassVar[int]
    name: str
    basic: BasicDevice
    def __init__(self, name: _Optional[str] = ..., basic: _Optional[_Union[BasicDevice, _Mapping]] = ...) -> None: ...

class DeviceAllocationConfiguration(_message.Message):
    __slots__ = ("source", "requests", "deviceConfiguration")
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    REQUESTS_FIELD_NUMBER: _ClassVar[int]
    DEVICECONFIGURATION_FIELD_NUMBER: _ClassVar[int]
    source: str
    requests: _containers.RepeatedScalarFieldContainer[str]
    deviceConfiguration: DeviceConfiguration
    def __init__(self, source: _Optional[str] = ..., requests: _Optional[_Iterable[str]] = ..., deviceConfiguration: _Optional[_Union[DeviceConfiguration, _Mapping]] = ...) -> None: ...

class DeviceAllocationResult(_message.Message):
    __slots__ = ("results", "config")
    RESULTS_FIELD_NUMBER: _ClassVar[int]
    CONFIG_FIELD_NUMBER: _ClassVar[int]
    results: _containers.RepeatedCompositeFieldContainer[DeviceRequestAllocationResult]
    config: _containers.RepeatedCompositeFieldContainer[DeviceAllocationConfiguration]
    def __init__(self, results: _Optional[_Iterable[_Union[DeviceRequestAllocationResult, _Mapping]]] = ..., config: _Optional[_Iterable[_Union[DeviceAllocationConfiguration, _Mapping]]] = ...) -> None: ...

class DeviceAttribute(_message.Message):
    __slots__ = ("int", "bool", "string", "version")
    INT_FIELD_NUMBER: _ClassVar[int]
    BOOL_FIELD_NUMBER: _ClassVar[int]
    STRING_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    int: int
    bool: bool
    string: str
    version: str
    def __init__(self, int: _Optional[int] = ..., bool: bool = ..., string: _Optional[str] = ..., version: _Optional[str] = ...) -> None: ...

class DeviceClaim(_message.Message):
    __slots__ = ("requests", "constraints", "config")
    REQUESTS_FIELD_NUMBER: _ClassVar[int]
    CONSTRAINTS_FIELD_NUMBER: _ClassVar[int]
    CONFIG_FIELD_NUMBER: _ClassVar[int]
    requests: _containers.RepeatedCompositeFieldContainer[DeviceRequest]
    constraints: _containers.RepeatedCompositeFieldContainer[DeviceConstraint]
    config: _containers.RepeatedCompositeFieldContainer[DeviceClaimConfiguration]
    def __init__(self, requests: _Optional[_Iterable[_Union[DeviceRequest, _Mapping]]] = ..., constraints: _Optional[_Iterable[_Union[DeviceConstraint, _Mapping]]] = ..., config: _Optional[_Iterable[_Union[DeviceClaimConfiguration, _Mapping]]] = ...) -> None: ...

class DeviceClaimConfiguration(_message.Message):
    __slots__ = ("requests", "deviceConfiguration")
    REQUESTS_FIELD_NUMBER: _ClassVar[int]
    DEVICECONFIGURATION_FIELD_NUMBER: _ClassVar[int]
    requests: _containers.RepeatedScalarFieldContainer[str]
    deviceConfiguration: DeviceConfiguration
    def __init__(self, requests: _Optional[_Iterable[str]] = ..., deviceConfiguration: _Optional[_Union[DeviceConfiguration, _Mapping]] = ...) -> None: ...

class DeviceClass(_message.Message):
    __slots__ = ("metadata", "spec")
    METADATA_FIELD_NUMBER: _ClassVar[int]
    SPEC_FIELD_NUMBER: _ClassVar[int]
    metadata: _generated_pb2_1_1.ObjectMeta
    spec: DeviceClassSpec
    def __init__(self, metadata: _Optional[_Union[_generated_pb2_1_1.ObjectMeta, _Mapping]] = ..., spec: _Optional[_Union[DeviceClassSpec, _Mapping]] = ...) -> None: ...

class DeviceClassConfiguration(_message.Message):
    __slots__ = ("deviceConfiguration",)
    DEVICECONFIGURATION_FIELD_NUMBER: _ClassVar[int]
    deviceConfiguration: DeviceConfiguration
    def __init__(self, deviceConfiguration: _Optional[_Union[DeviceConfiguration, _Mapping]] = ...) -> None: ...

class DeviceClassList(_message.Message):
    __slots__ = ("metadata", "items")
    METADATA_FIELD_NUMBER: _ClassVar[int]
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    metadata: _generated_pb2_1_1.ListMeta
    items: _containers.RepeatedCompositeFieldContainer[DeviceClass]
    def __init__(self, metadata: _Optional[_Union[_generated_pb2_1_1.ListMeta, _Mapping]] = ..., items: _Optional[_Iterable[_Union[DeviceClass, _Mapping]]] = ...) -> None: ...

class DeviceClassSpec(_message.Message):
    __slots__ = ("selectors", "config", "suitableNodes")
    SELECTORS_FIELD_NUMBER: _ClassVar[int]
    CONFIG_FIELD_NUMBER: _ClassVar[int]
    SUITABLENODES_FIELD_NUMBER: _ClassVar[int]
    selectors: _containers.RepeatedCompositeFieldContainer[DeviceSelector]
    config: _containers.RepeatedCompositeFieldContainer[DeviceClassConfiguration]
    suitableNodes: _generated_pb2.NodeSelector
    def __init__(self, selectors: _Optional[_Iterable[_Union[DeviceSelector, _Mapping]]] = ..., config: _Optional[_Iterable[_Union[DeviceClassConfiguration, _Mapping]]] = ..., suitableNodes: _Optional[_Union[_generated_pb2.NodeSelector, _Mapping]] = ...) -> None: ...

class DeviceConfiguration(_message.Message):
    __slots__ = ("opaque",)
    OPAQUE_FIELD_NUMBER: _ClassVar[int]
    opaque: OpaqueDeviceConfiguration
    def __init__(self, opaque: _Optional[_Union[OpaqueDeviceConfiguration, _Mapping]] = ...) -> None: ...

class DeviceConstraint(_message.Message):
    __slots__ = ("requests", "matchAttribute")
    REQUESTS_FIELD_NUMBER: _ClassVar[int]
    MATCHATTRIBUTE_FIELD_NUMBER: _ClassVar[int]
    requests: _containers.RepeatedScalarFieldContainer[str]
    matchAttribute: str
    def __init__(self, requests: _Optional[_Iterable[str]] = ..., matchAttribute: _Optional[str] = ...) -> None: ...

class DeviceRequest(_message.Message):
    __slots__ = ("name", "deviceClassName", "selectors", "allocationMode", "count", "adminAccess")
    NAME_FIELD_NUMBER: _ClassVar[int]
    DEVICECLASSNAME_FIELD_NUMBER: _ClassVar[int]
    SELECTORS_FIELD_NUMBER: _ClassVar[int]
    ALLOCATIONMODE_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    ADMINACCESS_FIELD_NUMBER: _ClassVar[int]
    name: str
    deviceClassName: str
    selectors: _containers.RepeatedCompositeFieldContainer[DeviceSelector]
    allocationMode: str
    count: int
    adminAccess: bool
    def __init__(self, name: _Optional[str] = ..., deviceClassName: _Optional[str] = ..., selectors: _Optional[_Iterable[_Union[DeviceSelector, _Mapping]]] = ..., allocationMode: _Optional[str] = ..., count: _Optional[int] = ..., adminAccess: bool = ...) -> None: ...

class DeviceRequestAllocationResult(_message.Message):
    __slots__ = ("request", "driver", "pool", "device")
    REQUEST_FIELD_NUMBER: _ClassVar[int]
    DRIVER_FIELD_NUMBER: _ClassVar[int]
    POOL_FIELD_NUMBER: _ClassVar[int]
    DEVICE_FIELD_NUMBER: _ClassVar[int]
    request: str
    driver: str
    pool: str
    device: str
    def __init__(self, request: _Optional[str] = ..., driver: _Optional[str] = ..., pool: _Optional[str] = ..., device: _Optional[str] = ...) -> None: ...

class DeviceSelector(_message.Message):
    __slots__ = ("cel",)
    CEL_FIELD_NUMBER: _ClassVar[int]
    cel: CELDeviceSelector
    def __init__(self, cel: _Optional[_Union[CELDeviceSelector, _Mapping]] = ...) -> None: ...

class OpaqueDeviceConfiguration(_message.Message):
    __slots__ = ("driver", "parameters")
    DRIVER_FIELD_NUMBER: _ClassVar[int]
    PARAMETERS_FIELD_NUMBER: _ClassVar[int]
    driver: str
    parameters: _generated_pb2_1_1_1.RawExtension
    def __init__(self, driver: _Optional[str] = ..., parameters: _Optional[_Union[_generated_pb2_1_1_1.RawExtension, _Mapping]] = ...) -> None: ...

class PodSchedulingContext(_message.Message):
    __slots__ = ("metadata", "spec", "status")
    METADATA_FIELD_NUMBER: _ClassVar[int]
    SPEC_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    metadata: _generated_pb2_1_1.ObjectMeta
    spec: PodSchedulingContextSpec
    status: PodSchedulingContextStatus
    def __init__(self, metadata: _Optional[_Union[_generated_pb2_1_1.ObjectMeta, _Mapping]] = ..., spec: _Optional[_Union[PodSchedulingContextSpec, _Mapping]] = ..., status: _Optional[_Union[PodSchedulingContextStatus, _Mapping]] = ...) -> None: ...

class PodSchedulingContextList(_message.Message):
    __slots__ = ("metadata", "items")
    METADATA_FIELD_NUMBER: _ClassVar[int]
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    metadata: _generated_pb2_1_1.ListMeta
    items: _containers.RepeatedCompositeFieldContainer[PodSchedulingContext]
    def __init__(self, metadata: _Optional[_Union[_generated_pb2_1_1.ListMeta, _Mapping]] = ..., items: _Optional[_Iterable[_Union[PodSchedulingContext, _Mapping]]] = ...) -> None: ...

class PodSchedulingContextSpec(_message.Message):
    __slots__ = ("selectedNode", "potentialNodes")
    SELECTEDNODE_FIELD_NUMBER: _ClassVar[int]
    POTENTIALNODES_FIELD_NUMBER: _ClassVar[int]
    selectedNode: str
    potentialNodes: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, selectedNode: _Optional[str] = ..., potentialNodes: _Optional[_Iterable[str]] = ...) -> None: ...

class PodSchedulingContextStatus(_message.Message):
    __slots__ = ("resourceClaims",)
    RESOURCECLAIMS_FIELD_NUMBER: _ClassVar[int]
    resourceClaims: _containers.RepeatedCompositeFieldContainer[ResourceClaimSchedulingStatus]
    def __init__(self, resourceClaims: _Optional[_Iterable[_Union[ResourceClaimSchedulingStatus, _Mapping]]] = ...) -> None: ...

class ResourceClaim(_message.Message):
    __slots__ = ("metadata", "spec", "status")
    METADATA_FIELD_NUMBER: _ClassVar[int]
    SPEC_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    metadata: _generated_pb2_1_1.ObjectMeta
    spec: ResourceClaimSpec
    status: ResourceClaimStatus
    def __init__(self, metadata: _Optional[_Union[_generated_pb2_1_1.ObjectMeta, _Mapping]] = ..., spec: _Optional[_Union[ResourceClaimSpec, _Mapping]] = ..., status: _Optional[_Union[ResourceClaimStatus, _Mapping]] = ...) -> None: ...

class ResourceClaimConsumerReference(_message.Message):
    __slots__ = ("apiGroup", "resource", "name", "uid")
    APIGROUP_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    UID_FIELD_NUMBER: _ClassVar[int]
    apiGroup: str
    resource: str
    name: str
    uid: str
    def __init__(self, apiGroup: _Optional[str] = ..., resource: _Optional[str] = ..., name: _Optional[str] = ..., uid: _Optional[str] = ...) -> None: ...

class ResourceClaimList(_message.Message):
    __slots__ = ("metadata", "items")
    METADATA_FIELD_NUMBER: _ClassVar[int]
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    metadata: _generated_pb2_1_1.ListMeta
    items: _containers.RepeatedCompositeFieldContainer[ResourceClaim]
    def __init__(self, metadata: _Optional[_Union[_generated_pb2_1_1.ListMeta, _Mapping]] = ..., items: _Optional[_Iterable[_Union[ResourceClaim, _Mapping]]] = ...) -> None: ...

class ResourceClaimSchedulingStatus(_message.Message):
    __slots__ = ("name", "unsuitableNodes")
    NAME_FIELD_NUMBER: _ClassVar[int]
    UNSUITABLENODES_FIELD_NUMBER: _ClassVar[int]
    name: str
    unsuitableNodes: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, name: _Optional[str] = ..., unsuitableNodes: _Optional[_Iterable[str]] = ...) -> None: ...

class ResourceClaimSpec(_message.Message):
    __slots__ = ("devices", "controller")
    DEVICES_FIELD_NUMBER: _ClassVar[int]
    CONTROLLER_FIELD_NUMBER: _ClassVar[int]
    devices: DeviceClaim
    controller: str
    def __init__(self, devices: _Optional[_Union[DeviceClaim, _Mapping]] = ..., controller: _Optional[str] = ...) -> None: ...

class ResourceClaimStatus(_message.Message):
    __slots__ = ("allocation", "reservedFor", "deallocationRequested")
    ALLOCATION_FIELD_NUMBER: _ClassVar[int]
    RESERVEDFOR_FIELD_NUMBER: _ClassVar[int]
    DEALLOCATIONREQUESTED_FIELD_NUMBER: _ClassVar[int]
    allocation: AllocationResult
    reservedFor: _containers.RepeatedCompositeFieldContainer[ResourceClaimConsumerReference]
    deallocationRequested: bool
    def __init__(self, allocation: _Optional[_Union[AllocationResult, _Mapping]] = ..., reservedFor: _Optional[_Iterable[_Union[ResourceClaimConsumerReference, _Mapping]]] = ..., deallocationRequested: bool = ...) -> None: ...

class ResourceClaimTemplate(_message.Message):
    __slots__ = ("metadata", "spec")
    METADATA_FIELD_NUMBER: _ClassVar[int]
    SPEC_FIELD_NUMBER: _ClassVar[int]
    metadata: _generated_pb2_1_1.ObjectMeta
    spec: ResourceClaimTemplateSpec
    def __init__(self, metadata: _Optional[_Union[_generated_pb2_1_1.ObjectMeta, _Mapping]] = ..., spec: _Optional[_Union[ResourceClaimTemplateSpec, _Mapping]] = ...) -> None: ...

class ResourceClaimTemplateList(_message.Message):
    __slots__ = ("metadata", "items")
    METADATA_FIELD_NUMBER: _ClassVar[int]
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    metadata: _generated_pb2_1_1.ListMeta
    items: _containers.RepeatedCompositeFieldContainer[ResourceClaimTemplate]
    def __init__(self, metadata: _Optional[_Union[_generated_pb2_1_1.ListMeta, _Mapping]] = ..., items: _Optional[_Iterable[_Union[ResourceClaimTemplate, _Mapping]]] = ...) -> None: ...

class ResourceClaimTemplateSpec(_message.Message):
    __slots__ = ("metadata", "spec")
    METADATA_FIELD_NUMBER: _ClassVar[int]
    SPEC_FIELD_NUMBER: _ClassVar[int]
    metadata: _generated_pb2_1_1.ObjectMeta
    spec: ResourceClaimSpec
    def __init__(self, metadata: _Optional[_Union[_generated_pb2_1_1.ObjectMeta, _Mapping]] = ..., spec: _Optional[_Union[ResourceClaimSpec, _Mapping]] = ...) -> None: ...

class ResourcePool(_message.Message):
    __slots__ = ("name", "generation", "resourceSliceCount")
    NAME_FIELD_NUMBER: _ClassVar[int]
    GENERATION_FIELD_NUMBER: _ClassVar[int]
    RESOURCESLICECOUNT_FIELD_NUMBER: _ClassVar[int]
    name: str
    generation: int
    resourceSliceCount: int
    def __init__(self, name: _Optional[str] = ..., generation: _Optional[int] = ..., resourceSliceCount: _Optional[int] = ...) -> None: ...

class ResourceSlice(_message.Message):
    __slots__ = ("metadata", "spec")
    METADATA_FIELD_NUMBER: _ClassVar[int]
    SPEC_FIELD_NUMBER: _ClassVar[int]
    metadata: _generated_pb2_1_1.ObjectMeta
    spec: ResourceSliceSpec
    def __init__(self, metadata: _Optional[_Union[_generated_pb2_1_1.ObjectMeta, _Mapping]] = ..., spec: _Optional[_Union[ResourceSliceSpec, _Mapping]] = ...) -> None: ...

class ResourceSliceList(_message.Message):
    __slots__ = ("metadata", "items")
    METADATA_FIELD_NUMBER: _ClassVar[int]
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    metadata: _generated_pb2_1_1.ListMeta
    items: _containers.RepeatedCompositeFieldContainer[ResourceSlice]
    def __init__(self, metadata: _Optional[_Union[_generated_pb2_1_1.ListMeta, _Mapping]] = ..., items: _Optional[_Iterable[_Union[ResourceSlice, _Mapping]]] = ...) -> None: ...

class ResourceSliceSpec(_message.Message):
    __slots__ = ("driver", "pool", "nodeName", "nodeSelector", "allNodes", "devices")
    DRIVER_FIELD_NUMBER: _ClassVar[int]
    POOL_FIELD_NUMBER: _ClassVar[int]
    NODENAME_FIELD_NUMBER: _ClassVar[int]
    NODESELECTOR_FIELD_NUMBER: _ClassVar[int]
    ALLNODES_FIELD_NUMBER: _ClassVar[int]
    DEVICES_FIELD_NUMBER: _ClassVar[int]
    driver: str
    pool: ResourcePool
    nodeName: str
    nodeSelector: _generated_pb2.NodeSelector
    allNodes: bool
    devices: _containers.RepeatedCompositeFieldContainer[Device]
    def __init__(self, driver: _Optional[str] = ..., pool: _Optional[_Union[ResourcePool, _Mapping]] = ..., nodeName: _Optional[str] = ..., nodeSelector: _Optional[_Union[_generated_pb2.NodeSelector, _Mapping]] = ..., allNodes: bool = ..., devices: _Optional[_Iterable[_Union[Device, _Mapping]]] = ...) -> None: ...
