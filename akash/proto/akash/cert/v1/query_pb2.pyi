from gogoproto import gogo_pb2 as _gogo_pb2
from google.api import annotations_pb2 as _annotations_pb2
from cosmos.base.query.v1beta1 import pagination_pb2 as _pagination_pb2
from akash.cert.v1 import cert_pb2 as _cert_pb2
from akash.cert.v1 import filters_pb2 as _filters_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CertificateResponse(_message.Message):
    __slots__ = ("certificate", "serial")
    CERTIFICATE_FIELD_NUMBER: _ClassVar[int]
    SERIAL_FIELD_NUMBER: _ClassVar[int]
    certificate: _cert_pb2.Certificate
    serial: str
    def __init__(self, certificate: _Optional[_Union[_cert_pb2.Certificate, _Mapping]] = ..., serial: _Optional[str] = ...) -> None: ...

class QueryCertificatesRequest(_message.Message):
    __slots__ = ("filter", "pagination")
    FILTER_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    filter: _filters_pb2.CertificateFilter
    pagination: _pagination_pb2.PageRequest
    def __init__(self, filter: _Optional[_Union[_filters_pb2.CertificateFilter, _Mapping]] = ..., pagination: _Optional[_Union[_pagination_pb2.PageRequest, _Mapping]] = ...) -> None: ...

class QueryCertificatesResponse(_message.Message):
    __slots__ = ("certificates", "pagination")
    CERTIFICATES_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    certificates: _containers.RepeatedCompositeFieldContainer[CertificateResponse]
    pagination: _pagination_pb2.PageResponse
    def __init__(self, certificates: _Optional[_Iterable[_Union[CertificateResponse, _Mapping]]] = ..., pagination: _Optional[_Union[_pagination_pb2.PageResponse, _Mapping]] = ...) -> None: ...
