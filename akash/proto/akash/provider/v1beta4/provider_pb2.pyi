from gogoproto import gogo_pb2 as _gogo_pb2
from cosmos_proto import cosmos_pb2 as _cosmos_pb2
from akash.base.attributes.v1 import attribute_pb2 as _attribute_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Info(_message.Message):
    __slots__ = ("email", "website")
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    WEBSITE_FIELD_NUMBER: _ClassVar[int]
    email: str
    website: str
    def __init__(self, email: _Optional[str] = ..., website: _Optional[str] = ...) -> None: ...

class Provider(_message.Message):
    __slots__ = ("owner", "host_uri", "attributes", "info")
    OWNER_FIELD_NUMBER: _ClassVar[int]
    HOST_URI_FIELD_NUMBER: _ClassVar[int]
    ATTRIBUTES_FIELD_NUMBER: _ClassVar[int]
    INFO_FIELD_NUMBER: _ClassVar[int]
    owner: str
    host_uri: str
    attributes: _containers.RepeatedCompositeFieldContainer[_attribute_pb2.Attribute]
    info: Info
    def __init__(self, owner: _Optional[str] = ..., host_uri: _Optional[str] = ..., attributes: _Optional[_Iterable[_Union[_attribute_pb2.Attribute, _Mapping]]] = ..., info: _Optional[_Union[Info, _Mapping]] = ...) -> None: ...
