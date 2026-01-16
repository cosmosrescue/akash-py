from gogoproto import gogo_pb2 as _gogo_pb2
from akash.manifest.v2beta3 import httpoptions_pb2 as _httpoptions_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ServiceExpose(_message.Message):
    __slots__ = ("port", "external_port", "proto", "service", "hosts", "http_options", "ip", "endpoint_sequence_number")
    PORT_FIELD_NUMBER: _ClassVar[int]
    EXTERNAL_PORT_FIELD_NUMBER: _ClassVar[int]
    PROTO_FIELD_NUMBER: _ClassVar[int]
    SERVICE_FIELD_NUMBER: _ClassVar[int]
    GLOBAL_FIELD_NUMBER: _ClassVar[int]
    HOSTS_FIELD_NUMBER: _ClassVar[int]
    HTTP_OPTIONS_FIELD_NUMBER: _ClassVar[int]
    IP_FIELD_NUMBER: _ClassVar[int]
    ENDPOINT_SEQUENCE_NUMBER_FIELD_NUMBER: _ClassVar[int]
    port: int
    external_port: int
    proto: str
    service: str
    hosts: _containers.RepeatedScalarFieldContainer[str]
    http_options: _httpoptions_pb2.ServiceExposeHTTPOptions
    ip: str
    endpoint_sequence_number: int
    def __init__(self, port: _Optional[int] = ..., external_port: _Optional[int] = ..., proto: _Optional[str] = ..., service: _Optional[str] = ..., hosts: _Optional[_Iterable[str]] = ..., http_options: _Optional[_Union[_httpoptions_pb2.ServiceExposeHTTPOptions, _Mapping]] = ..., ip: _Optional[str] = ..., endpoint_sequence_number: _Optional[int] = ..., **kwargs) -> None: ...
