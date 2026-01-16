from gogoproto import gogo_pb2 as _gogo_pb2
from akash.base.resources.v1beta4 import cpu_pb2 as _cpu_pb2
from akash.base.resources.v1beta4 import gpu_pb2 as _gpu_pb2
from akash.base.resources.v1beta4 import memory_pb2 as _memory_pb2
from akash.base.resources.v1beta4 import storage_pb2 as _storage_pb2
from akash.base.resources.v1beta4 import endpoint_pb2 as _endpoint_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Resources(_message.Message):
    __slots__ = ("id", "cpu", "memory", "storage", "gpu", "endpoints")
    ID_FIELD_NUMBER: _ClassVar[int]
    CPU_FIELD_NUMBER: _ClassVar[int]
    MEMORY_FIELD_NUMBER: _ClassVar[int]
    STORAGE_FIELD_NUMBER: _ClassVar[int]
    GPU_FIELD_NUMBER: _ClassVar[int]
    ENDPOINTS_FIELD_NUMBER: _ClassVar[int]
    id: int
    cpu: _cpu_pb2.CPU
    memory: _memory_pb2.Memory
    storage: _containers.RepeatedCompositeFieldContainer[_storage_pb2.Storage]
    gpu: _gpu_pb2.GPU
    endpoints: _containers.RepeatedCompositeFieldContainer[_endpoint_pb2.Endpoint]
    def __init__(self, id: _Optional[int] = ..., cpu: _Optional[_Union[_cpu_pb2.CPU, _Mapping]] = ..., memory: _Optional[_Union[_memory_pb2.Memory, _Mapping]] = ..., storage: _Optional[_Iterable[_Union[_storage_pb2.Storage, _Mapping]]] = ..., gpu: _Optional[_Union[_gpu_pb2.GPU, _Mapping]] = ..., endpoints: _Optional[_Iterable[_Union[_endpoint_pb2.Endpoint, _Mapping]]] = ...) -> None: ...
