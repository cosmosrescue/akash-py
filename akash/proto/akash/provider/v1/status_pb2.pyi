from google.protobuf import timestamp_pb2 as _timestamp_pb2
from gogoproto import gogo_pb2 as _gogo_pb2
from akash.inventory.v1 import cluster_pb2 as _cluster_pb2
from k8s.io.apimachinery.pkg.api.resource import generated_pb2 as _generated_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ResourcesMetric(_message.Message):
    __slots__ = ("cpu", "memory", "gpu", "ephemeral_storage", "storage")
    class StorageEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: _generated_pb2.Quantity
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[_generated_pb2.Quantity, _Mapping]] = ...) -> None: ...
    CPU_FIELD_NUMBER: _ClassVar[int]
    MEMORY_FIELD_NUMBER: _ClassVar[int]
    GPU_FIELD_NUMBER: _ClassVar[int]
    EPHEMERAL_STORAGE_FIELD_NUMBER: _ClassVar[int]
    STORAGE_FIELD_NUMBER: _ClassVar[int]
    cpu: _generated_pb2.Quantity
    memory: _generated_pb2.Quantity
    gpu: _generated_pb2.Quantity
    ephemeral_storage: _generated_pb2.Quantity
    storage: _containers.MessageMap[str, _generated_pb2.Quantity]
    def __init__(self, cpu: _Optional[_Union[_generated_pb2.Quantity, _Mapping]] = ..., memory: _Optional[_Union[_generated_pb2.Quantity, _Mapping]] = ..., gpu: _Optional[_Union[_generated_pb2.Quantity, _Mapping]] = ..., ephemeral_storage: _Optional[_Union[_generated_pb2.Quantity, _Mapping]] = ..., storage: _Optional[_Mapping[str, _generated_pb2.Quantity]] = ...) -> None: ...

class Leases(_message.Message):
    __slots__ = ("active",)
    ACTIVE_FIELD_NUMBER: _ClassVar[int]
    active: int
    def __init__(self, active: _Optional[int] = ...) -> None: ...

class ReservationsMetric(_message.Message):
    __slots__ = ("count", "resources")
    COUNT_FIELD_NUMBER: _ClassVar[int]
    RESOURCES_FIELD_NUMBER: _ClassVar[int]
    count: int
    resources: ResourcesMetric
    def __init__(self, count: _Optional[int] = ..., resources: _Optional[_Union[ResourcesMetric, _Mapping]] = ...) -> None: ...

class Reservations(_message.Message):
    __slots__ = ("pending", "active")
    PENDING_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_FIELD_NUMBER: _ClassVar[int]
    pending: ReservationsMetric
    active: ReservationsMetric
    def __init__(self, pending: _Optional[_Union[ReservationsMetric, _Mapping]] = ..., active: _Optional[_Union[ReservationsMetric, _Mapping]] = ...) -> None: ...

class Inventory(_message.Message):
    __slots__ = ("cluster", "reservations")
    CLUSTER_FIELD_NUMBER: _ClassVar[int]
    RESERVATIONS_FIELD_NUMBER: _ClassVar[int]
    cluster: _cluster_pb2.Cluster
    reservations: Reservations
    def __init__(self, cluster: _Optional[_Union[_cluster_pb2.Cluster, _Mapping]] = ..., reservations: _Optional[_Union[Reservations, _Mapping]] = ...) -> None: ...

class ClusterStatus(_message.Message):
    __slots__ = ("leases", "inventory")
    LEASES_FIELD_NUMBER: _ClassVar[int]
    INVENTORY_FIELD_NUMBER: _ClassVar[int]
    leases: Leases
    inventory: Inventory
    def __init__(self, leases: _Optional[_Union[Leases, _Mapping]] = ..., inventory: _Optional[_Union[Inventory, _Mapping]] = ...) -> None: ...

class BidEngineStatus(_message.Message):
    __slots__ = ("orders",)
    ORDERS_FIELD_NUMBER: _ClassVar[int]
    orders: int
    def __init__(self, orders: _Optional[int] = ...) -> None: ...

class ManifestStatus(_message.Message):
    __slots__ = ("deployments",)
    DEPLOYMENTS_FIELD_NUMBER: _ClassVar[int]
    deployments: int
    def __init__(self, deployments: _Optional[int] = ...) -> None: ...

class Status(_message.Message):
    __slots__ = ("errors", "cluster", "bid_engine", "manifest", "public_hostnames", "timestamp")
    ERRORS_FIELD_NUMBER: _ClassVar[int]
    CLUSTER_FIELD_NUMBER: _ClassVar[int]
    BID_ENGINE_FIELD_NUMBER: _ClassVar[int]
    MANIFEST_FIELD_NUMBER: _ClassVar[int]
    PUBLIC_HOSTNAMES_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    errors: _containers.RepeatedScalarFieldContainer[str]
    cluster: ClusterStatus
    bid_engine: BidEngineStatus
    manifest: ManifestStatus
    public_hostnames: _containers.RepeatedScalarFieldContainer[str]
    timestamp: _timestamp_pb2.Timestamp
    def __init__(self, errors: _Optional[_Iterable[str]] = ..., cluster: _Optional[_Union[ClusterStatus, _Mapping]] = ..., bid_engine: _Optional[_Union[BidEngineStatus, _Mapping]] = ..., manifest: _Optional[_Union[ManifestStatus, _Mapping]] = ..., public_hostnames: _Optional[_Iterable[str]] = ..., timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...
