from gogoproto import gogo_pb2 as _gogo_pb2
from cosmos_proto import cosmos_pb2 as _cosmos_pb2
from cosmos.msg.v1 import msg_pb2 as _msg_pb2
from akash.base.attributes.v1 import attribute_pb2 as _attribute_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MsgSignProviderAttributes(_message.Message):
    __slots__ = ("owner", "auditor", "attributes")
    OWNER_FIELD_NUMBER: _ClassVar[int]
    AUDITOR_FIELD_NUMBER: _ClassVar[int]
    ATTRIBUTES_FIELD_NUMBER: _ClassVar[int]
    owner: str
    auditor: str
    attributes: _containers.RepeatedCompositeFieldContainer[_attribute_pb2.Attribute]
    def __init__(self, owner: _Optional[str] = ..., auditor: _Optional[str] = ..., attributes: _Optional[_Iterable[_Union[_attribute_pb2.Attribute, _Mapping]]] = ...) -> None: ...

class MsgSignProviderAttributesResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class MsgDeleteProviderAttributes(_message.Message):
    __slots__ = ("owner", "auditor", "keys")
    OWNER_FIELD_NUMBER: _ClassVar[int]
    AUDITOR_FIELD_NUMBER: _ClassVar[int]
    KEYS_FIELD_NUMBER: _ClassVar[int]
    owner: str
    auditor: str
    keys: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, owner: _Optional[str] = ..., auditor: _Optional[str] = ..., keys: _Optional[_Iterable[str]] = ...) -> None: ...

class MsgDeleteProviderAttributesResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...
