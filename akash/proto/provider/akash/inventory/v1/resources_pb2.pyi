from gogoproto import gogo_pb2 as _gogo_pb2
from akash.inventory.v1 import cpu_pb2 as _cpu_pb2
from akash.inventory.v1 import gpu_pb2 as _gpu_pb2
from akash.inventory.v1 import memory_pb2 as _memory_pb2
from akash.inventory.v1 import resourcepair_pb2 as _resourcepair_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class NodeResources(_message.Message):
    __slots__ = ("cpu", "memory", "gpu", "ephemeral_storage", "volumes_attached", "volumes_mounted")
    CPU_FIELD_NUMBER: _ClassVar[int]
    MEMORY_FIELD_NUMBER: _ClassVar[int]
    GPU_FIELD_NUMBER: _ClassVar[int]
    EPHEMERAL_STORAGE_FIELD_NUMBER: _ClassVar[int]
    VOLUMES_ATTACHED_FIELD_NUMBER: _ClassVar[int]
    VOLUMES_MOUNTED_FIELD_NUMBER: _ClassVar[int]
    cpu: _cpu_pb2.CPU
    memory: _memory_pb2.Memory
    gpu: _gpu_pb2.GPU
    ephemeral_storage: _resourcepair_pb2.ResourcePair
    volumes_attached: _resourcepair_pb2.ResourcePair
    volumes_mounted: _resourcepair_pb2.ResourcePair
    def __init__(self, cpu: _Optional[_Union[_cpu_pb2.CPU, _Mapping]] = ..., memory: _Optional[_Union[_memory_pb2.Memory, _Mapping]] = ..., gpu: _Optional[_Union[_gpu_pb2.GPU, _Mapping]] = ..., ephemeral_storage: _Optional[_Union[_resourcepair_pb2.ResourcePair, _Mapping]] = ..., volumes_attached: _Optional[_Union[_resourcepair_pb2.ResourcePair, _Mapping]] = ..., volumes_mounted: _Optional[_Union[_resourcepair_pb2.ResourcePair, _Mapping]] = ...) -> None: ...
