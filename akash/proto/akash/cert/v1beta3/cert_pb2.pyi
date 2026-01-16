from gogoproto import gogo_pb2 as _gogo_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CertificateID(_message.Message):
    __slots__ = ("owner", "serial")
    OWNER_FIELD_NUMBER: _ClassVar[int]
    SERIAL_FIELD_NUMBER: _ClassVar[int]
    owner: str
    serial: str
    def __init__(self, owner: _Optional[str] = ..., serial: _Optional[str] = ...) -> None: ...

class Certificate(_message.Message):
    __slots__ = ("state", "cert", "pubkey")
    class State(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        invalid: _ClassVar[Certificate.State]
        valid: _ClassVar[Certificate.State]
        revoked: _ClassVar[Certificate.State]
    invalid: Certificate.State
    valid: Certificate.State
    revoked: Certificate.State
    STATE_FIELD_NUMBER: _ClassVar[int]
    CERT_FIELD_NUMBER: _ClassVar[int]
    PUBKEY_FIELD_NUMBER: _ClassVar[int]
    state: Certificate.State
    cert: bytes
    pubkey: bytes
    def __init__(self, state: _Optional[_Union[Certificate.State, str]] = ..., cert: _Optional[bytes] = ..., pubkey: _Optional[bytes] = ...) -> None: ...

class CertificateFilter(_message.Message):
    __slots__ = ("owner", "serial", "state")
    OWNER_FIELD_NUMBER: _ClassVar[int]
    SERIAL_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    owner: str
    serial: str
    state: str
    def __init__(self, owner: _Optional[str] = ..., serial: _Optional[str] = ..., state: _Optional[str] = ...) -> None: ...

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
    id: CertificateID
    def __init__(self, id: _Optional[_Union[CertificateID, _Mapping]] = ...) -> None: ...

class MsgRevokeCertificateResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...
