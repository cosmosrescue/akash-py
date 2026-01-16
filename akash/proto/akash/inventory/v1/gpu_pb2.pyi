from gogoproto import gogo_pb2 as _gogo_pb2
from akash.inventory.v1 import resourcepair_pb2 as _resourcepair_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GPUInfo(_message.Message):
    __slots__ = ("vendor", "vendor_id", "name", "modelid", "interface", "memory_size")
    VENDOR_FIELD_NUMBER: _ClassVar[int]
    VENDOR_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    MODELID_FIELD_NUMBER: _ClassVar[int]
    INTERFACE_FIELD_NUMBER: _ClassVar[int]
    MEMORY_SIZE_FIELD_NUMBER: _ClassVar[int]
    vendor: str
    vendor_id: str
    name: str
    modelid: str
    interface: str
    memory_size: str
    def __init__(self, vendor: _Optional[str] = ..., vendor_id: _Optional[str] = ..., name: _Optional[str] = ..., modelid: _Optional[str] = ..., interface: _Optional[str] = ..., memory_size: _Optional[str] = ...) -> None: ...

class GPU(_message.Message):
    __slots__ = ("quantity", "info")
    QUANTITY_FIELD_NUMBER: _ClassVar[int]
    INFO_FIELD_NUMBER: _ClassVar[int]
    quantity: _resourcepair_pb2.ResourcePair
    info: _containers.RepeatedCompositeFieldContainer[GPUInfo]
    def __init__(self, quantity: _Optional[_Union[_resourcepair_pb2.ResourcePair, _Mapping]] = ..., info: _Optional[_Iterable[_Union[GPUInfo, _Mapping]]] = ...) -> None: ...
