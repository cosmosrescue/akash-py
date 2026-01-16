from gogoproto import gogo_pb2 as _gogo_pb2
from akash.inventory.v1 import resourcepair_pb2 as _resourcepair_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CPUInfo(_message.Message):
    __slots__ = ("id", "vendor", "model", "vcores")
    ID_FIELD_NUMBER: _ClassVar[int]
    VENDOR_FIELD_NUMBER: _ClassVar[int]
    MODEL_FIELD_NUMBER: _ClassVar[int]
    VCORES_FIELD_NUMBER: _ClassVar[int]
    id: str
    vendor: str
    model: str
    vcores: int
    def __init__(self, id: _Optional[str] = ..., vendor: _Optional[str] = ..., model: _Optional[str] = ..., vcores: _Optional[int] = ...) -> None: ...

class CPU(_message.Message):
    __slots__ = ("quantity", "info")
    QUANTITY_FIELD_NUMBER: _ClassVar[int]
    INFO_FIELD_NUMBER: _ClassVar[int]
    quantity: _resourcepair_pb2.ResourcePair
    info: _containers.RepeatedCompositeFieldContainer[CPUInfo]
    def __init__(self, quantity: _Optional[_Union[_resourcepair_pb2.ResourcePair, _Mapping]] = ..., info: _Optional[_Iterable[_Union[CPUInfo, _Mapping]]] = ...) -> None: ...
