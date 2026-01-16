from gogoproto import gogo_pb2 as _gogo_pb2
from cosmos_proto import cosmos_pb2 as _cosmos_pb2
from cosmos.msg.v1 import msg_pb2 as _msg_pb2
from akash.cert.v1 import cert_pb2 as _cert_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MsgCreateCertificate(_message.Message):
    __slots__ = ("owner", "cert", "pubkey")
    OWNER_FIELD_NUMBER: _ClassVar[int]
    CERT_FIELD_NUMBER: _ClassVar[int]
    PUBKEY_FIELD_NUMBER: _ClassVar[int]
    owner: str
    cert: bytes
    pubkey: bytes
    def __init__(self, owner: _Optional[str] = ..., cert: _Optional[bytes] = ..., pubkey: _Optional[bytes] = ...) -> None: ...

class MsgCreateCertificateResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class MsgRevokeCertificate(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: _cert_pb2.ID
    def __init__(self, id: _Optional[_Union[_cert_pb2.ID, _Mapping]] = ...) -> None: ...

class MsgRevokeCertificateResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...
