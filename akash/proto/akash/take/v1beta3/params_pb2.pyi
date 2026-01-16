from gogoproto import gogo_pb2 as _gogo_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DenomTakeRate(_message.Message):
    __slots__ = ("denom", "rate")
    DENOM_FIELD_NUMBER: _ClassVar[int]
    RATE_FIELD_NUMBER: _ClassVar[int]
    denom: str
    rate: int
    def __init__(self, denom: _Optional[str] = ..., rate: _Optional[int] = ...) -> None: ...

class Params(_message.Message):
    __slots__ = ("denom_take_rates", "default_take_rate")
    DENOM_TAKE_RATES_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_TAKE_RATE_FIELD_NUMBER: _ClassVar[int]
    denom_take_rates: _containers.RepeatedCompositeFieldContainer[DenomTakeRate]
    default_take_rate: int
    def __init__(self, denom_take_rates: _Optional[_Iterable[_Union[DenomTakeRate, _Mapping]]] = ..., default_take_rate: _Optional[int] = ...) -> None: ...
