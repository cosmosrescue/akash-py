from gogoproto import gogo_pb2 as _gogo_pb2
from akash.inventory.v1 import resourcepair_pb2 as _resourcepair_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class StorageInfo(_message.Message):
    __slots__ = ("iops",)
    CLASS_FIELD_NUMBER: _ClassVar[int]
    IOPS_FIELD_NUMBER: _ClassVar[int]
    iops: str
    def __init__(self, iops: _Optional[str] = ..., **kwargs) -> None: ...

class Storage(_message.Message):
    __slots__ = ("quantity", "info")
    QUANTITY_FIELD_NUMBER: _ClassVar[int]
    INFO_FIELD_NUMBER: _ClassVar[int]
    quantity: _resourcepair_pb2.ResourcePair
    info: StorageInfo
    def __init__(self, quantity: _Optional[_Union[_resourcepair_pb2.ResourcePair, _Mapping]] = ..., info: _Optional[_Union[StorageInfo, _Mapping]] = ...) -> None: ...
