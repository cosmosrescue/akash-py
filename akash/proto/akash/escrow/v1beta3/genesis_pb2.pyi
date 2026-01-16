from gogoproto import gogo_pb2 as _gogo_pb2
from akash.escrow.v1beta3 import types_pb2 as _types_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GenesisState(_message.Message):
    __slots__ = ("accounts", "payments")
    ACCOUNTS_FIELD_NUMBER: _ClassVar[int]
    PAYMENTS_FIELD_NUMBER: _ClassVar[int]
    accounts: _containers.RepeatedCompositeFieldContainer[_types_pb2.Account]
    payments: _containers.RepeatedCompositeFieldContainer[_types_pb2.FractionalPayment]
    def __init__(self, accounts: _Optional[_Iterable[_Union[_types_pb2.Account, _Mapping]]] = ..., payments: _Optional[_Iterable[_Union[_types_pb2.FractionalPayment, _Mapping]]] = ...) -> None: ...
