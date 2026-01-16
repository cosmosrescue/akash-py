from gogoproto import gogo_pb2 as _gogo_pb2
from cosmos.base.v1beta1 import coin_pb2 as _coin_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Source(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    invalid: _ClassVar[Source]
    balance: _ClassVar[Source]
    grant: _ClassVar[Source]
invalid: Source
balance: Source
grant: Source

class Deposit(_message.Message):
    __slots__ = ("amount", "sources")
    AMOUNT_FIELD_NUMBER: _ClassVar[int]
    SOURCES_FIELD_NUMBER: _ClassVar[int]
    amount: _coin_pb2.Coin
    sources: _containers.RepeatedScalarFieldContainer[Source]
    def __init__(self, amount: _Optional[_Union[_coin_pb2.Coin, _Mapping]] = ..., sources: _Optional[_Iterable[_Union[Source, str]]] = ...) -> None: ...
