from gogoproto import gogo_pb2 as _gogo_pb2
from cosmos_proto import cosmos_pb2 as _cosmos_pb2
from akash.cert.v1 import cert_pb2 as _cert_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GenesisCertificate(_message.Message):
    __slots__ = ("owner", "certificate")
    OWNER_FIELD_NUMBER: _ClassVar[int]
    CERTIFICATE_FIELD_NUMBER: _ClassVar[int]
    owner: str
    certificate: _cert_pb2.Certificate
    def __init__(self, owner: _Optional[str] = ..., certificate: _Optional[_Union[_cert_pb2.Certificate, _Mapping]] = ...) -> None: ...

class GenesisState(_message.Message):
    __slots__ = ("certificates",)
    CERTIFICATES_FIELD_NUMBER: _ClassVar[int]
    certificates: _containers.RepeatedCompositeFieldContainer[GenesisCertificate]
    def __init__(self, certificates: _Optional[_Iterable[_Union[GenesisCertificate, _Mapping]]] = ...) -> None: ...
