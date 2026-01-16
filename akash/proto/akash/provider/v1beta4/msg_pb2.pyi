from gogoproto import gogo_pb2 as _gogo_pb2
from cosmos.msg.v1 import msg_pb2 as _msg_pb2
from cosmos_proto import cosmos_pb2 as _cosmos_pb2
from akash.base.attributes.v1 import attribute_pb2 as _attribute_pb2
from akash.provider.v1beta4 import provider_pb2 as _provider_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MsgCreateProvider(_message.Message):
    __slots__ = ("owner", "host_uri", "attributes", "info")
    OWNER_FIELD_NUMBER: _ClassVar[int]
    HOST_URI_FIELD_NUMBER: _ClassVar[int]
    ATTRIBUTES_FIELD_NUMBER: _ClassVar[int]
    INFO_FIELD_NUMBER: _ClassVar[int]
    owner: str
    host_uri: str
    attributes: _containers.RepeatedCompositeFieldContainer[_attribute_pb2.Attribute]
    info: _provider_pb2.Info
    def __init__(self, owner: _Optional[str] = ..., host_uri: _Optional[str] = ..., attributes: _Optional[_Iterable[_Union[_attribute_pb2.Attribute, _Mapping]]] = ..., info: _Optional[_Union[_provider_pb2.Info, _Mapping]] = ...) -> None: ...

class MsgCreateProviderResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class MsgUpdateProvider(_message.Message):
    __slots__ = ("owner", "host_uri", "attributes", "info")
    OWNER_FIELD_NUMBER: _ClassVar[int]
    HOST_URI_FIELD_NUMBER: _ClassVar[int]
    ATTRIBUTES_FIELD_NUMBER: _ClassVar[int]
    INFO_FIELD_NUMBER: _ClassVar[int]
    owner: str
    host_uri: str
    attributes: _containers.RepeatedCompositeFieldContainer[_attribute_pb2.Attribute]
    info: _provider_pb2.Info
    def __init__(self, owner: _Optional[str] = ..., host_uri: _Optional[str] = ..., attributes: _Optional[_Iterable[_Union[_attribute_pb2.Attribute, _Mapping]]] = ..., info: _Optional[_Union[_provider_pb2.Info, _Mapping]] = ...) -> None: ...

class MsgUpdateProviderResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class MsgDeleteProvider(_message.Message):
    __slots__ = ("owner",)
    OWNER_FIELD_NUMBER: _ClassVar[int]
    owner: str
    def __init__(self, owner: _Optional[str] = ...) -> None: ...

class MsgDeleteProviderResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...
