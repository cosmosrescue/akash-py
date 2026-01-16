from gogoproto import gogo_pb2 as _gogo_pb2
from akash.inventory.v1 import resourcepair_pb2 as _resourcepair_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MemoryInfo(_message.Message):
    __slots__ = ("vendor", "type", "total_size", "speed")
    VENDOR_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    TOTAL_SIZE_FIELD_NUMBER: _ClassVar[int]
    SPEED_FIELD_NUMBER: _ClassVar[int]
    vendor: str
    type: str
    total_size: str
    speed: str
    def __init__(self, vendor: _Optional[str] = ..., type: _Optional[str] = ..., total_size: _Optional[str] = ..., speed: _Optional[str] = ...) -> None: ...

class Memory(_message.Message):
    __slots__ = ("quantity", "info")
    QUANTITY_FIELD_NUMBER: _ClassVar[int]
    INFO_FIELD_NUMBER: _ClassVar[int]
    quantity: _resourcepair_pb2.ResourcePair
    info: _containers.RepeatedCompositeFieldContainer[MemoryInfo]
    def __init__(self, quantity: _Optional[_Union[_resourcepair_pb2.ResourcePair, _Mapping]] = ..., info: _Optional[_Iterable[_Union[MemoryInfo, _Mapping]]] = ...) -> None: ...
