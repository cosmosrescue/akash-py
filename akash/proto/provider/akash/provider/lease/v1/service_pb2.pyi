from gogoproto import gogo_pb2 as _gogo_pb2
from akash.manifest.v2beta3 import group_pb2 as _group_pb2
from akash.market.v1 import lease_pb2 as _lease_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class LeaseServiceStatus(_message.Message):
    __slots__ = ("available", "total", "uris", "observed_generation", "replicas", "updated_replicas", "ready_replicas", "available_replicas")
    AVAILABLE_FIELD_NUMBER: _ClassVar[int]
    TOTAL_FIELD_NUMBER: _ClassVar[int]
    URIS_FIELD_NUMBER: _ClassVar[int]
    OBSERVED_GENERATION_FIELD_NUMBER: _ClassVar[int]
    REPLICAS_FIELD_NUMBER: _ClassVar[int]
    UPDATED_REPLICAS_FIELD_NUMBER: _ClassVar[int]
    READY_REPLICAS_FIELD_NUMBER: _ClassVar[int]
    AVAILABLE_REPLICAS_FIELD_NUMBER: _ClassVar[int]
    available: int
    total: int
    uris: _containers.RepeatedScalarFieldContainer[str]
    observed_generation: int
    replicas: int
    updated_replicas: int
    ready_replicas: int
    available_replicas: int
    def __init__(self, available: _Optional[int] = ..., total: _Optional[int] = ..., uris: _Optional[_Iterable[str]] = ..., observed_generation: _Optional[int] = ..., replicas: _Optional[int] = ..., updated_replicas: _Optional[int] = ..., ready_replicas: _Optional[int] = ..., available_replicas: _Optional[int] = ...) -> None: ...

class LeaseIPStatus(_message.Message):
    __slots__ = ("port", "external_port", "protocol", "ip")
    PORT_FIELD_NUMBER: _ClassVar[int]
    EXTERNAL_PORT_FIELD_NUMBER: _ClassVar[int]
    PROTOCOL_FIELD_NUMBER: _ClassVar[int]
    IP_FIELD_NUMBER: _ClassVar[int]
    port: int
    external_port: int
    protocol: str
    ip: str
    def __init__(self, port: _Optional[int] = ..., external_port: _Optional[int] = ..., protocol: _Optional[str] = ..., ip: _Optional[str] = ...) -> None: ...

class ForwarderPortStatus(_message.Message):
    __slots__ = ("host", "port", "external_port", "proto", "name")
    HOST_FIELD_NUMBER: _ClassVar[int]
    PORT_FIELD_NUMBER: _ClassVar[int]
    EXTERNAL_PORT_FIELD_NUMBER: _ClassVar[int]
    PROTO_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    host: str
    port: int
    external_port: int
    proto: str
    name: str
    def __init__(self, host: _Optional[str] = ..., port: _Optional[int] = ..., external_port: _Optional[int] = ..., proto: _Optional[str] = ..., name: _Optional[str] = ...) -> None: ...

class ServiceStatus(_message.Message):
    __slots__ = ("name", "status", "ports", "ips")
    NAME_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    PORTS_FIELD_NUMBER: _ClassVar[int]
    IPS_FIELD_NUMBER: _ClassVar[int]
    name: str
    status: LeaseServiceStatus
    ports: _containers.RepeatedCompositeFieldContainer[ForwarderPortStatus]
    ips: _containers.RepeatedCompositeFieldContainer[LeaseIPStatus]
    def __init__(self, name: _Optional[str] = ..., status: _Optional[_Union[LeaseServiceStatus, _Mapping]] = ..., ports: _Optional[_Iterable[_Union[ForwarderPortStatus, _Mapping]]] = ..., ips: _Optional[_Iterable[_Union[LeaseIPStatus, _Mapping]]] = ...) -> None: ...

class SendManifestRequest(_message.Message):
    __slots__ = ("lease_id", "manifest")
    LEASE_ID_FIELD_NUMBER: _ClassVar[int]
    MANIFEST_FIELD_NUMBER: _ClassVar[int]
    lease_id: _lease_pb2.LeaseID
    manifest: _containers.RepeatedCompositeFieldContainer[_group_pb2.Group]
    def __init__(self, lease_id: _Optional[_Union[_lease_pb2.LeaseID, _Mapping]] = ..., manifest: _Optional[_Iterable[_Union[_group_pb2.Group, _Mapping]]] = ...) -> None: ...

class SendManifestResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ServiceLogsRequest(_message.Message):
    __slots__ = ("lease_id", "services")
    LEASE_ID_FIELD_NUMBER: _ClassVar[int]
    SERVICES_FIELD_NUMBER: _ClassVar[int]
    lease_id: _lease_pb2.LeaseID
    services: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, lease_id: _Optional[_Union[_lease_pb2.LeaseID, _Mapping]] = ..., services: _Optional[_Iterable[str]] = ...) -> None: ...

class ServiceLogs(_message.Message):
    __slots__ = ("name", "logs")
    NAME_FIELD_NUMBER: _ClassVar[int]
    LOGS_FIELD_NUMBER: _ClassVar[int]
    name: str
    logs: bytes
    def __init__(self, name: _Optional[str] = ..., logs: _Optional[bytes] = ...) -> None: ...

class ServiceLogsResponse(_message.Message):
    __slots__ = ("services",)
    SERVICES_FIELD_NUMBER: _ClassVar[int]
    services: _containers.RepeatedCompositeFieldContainer[ServiceLogs]
    def __init__(self, services: _Optional[_Iterable[_Union[ServiceLogs, _Mapping]]] = ...) -> None: ...

class ShellRequest(_message.Message):
    __slots__ = ("lease_id",)
    LEASE_ID_FIELD_NUMBER: _ClassVar[int]
    lease_id: _lease_pb2.LeaseID
    def __init__(self, lease_id: _Optional[_Union[_lease_pb2.LeaseID, _Mapping]] = ...) -> None: ...

class ServiceStatusRequest(_message.Message):
    __slots__ = ("lease_id", "services")
    LEASE_ID_FIELD_NUMBER: _ClassVar[int]
    SERVICES_FIELD_NUMBER: _ClassVar[int]
    lease_id: _lease_pb2.LeaseID
    services: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, lease_id: _Optional[_Union[_lease_pb2.LeaseID, _Mapping]] = ..., services: _Optional[_Iterable[str]] = ...) -> None: ...

class ServiceStatusResponse(_message.Message):
    __slots__ = ("services",)
    SERVICES_FIELD_NUMBER: _ClassVar[int]
    services: _containers.RepeatedCompositeFieldContainer[ServiceStatus]
    def __init__(self, services: _Optional[_Iterable[_Union[ServiceStatus, _Mapping]]] = ...) -> None: ...
