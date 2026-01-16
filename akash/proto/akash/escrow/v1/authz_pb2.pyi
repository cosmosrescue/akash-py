from amino import amino_pb2 as _amino_pb2
from gogoproto import gogo_pb2 as _gogo_pb2
from cosmos_proto import cosmos_pb2 as _cosmos_pb2
from cosmos.base.v1beta1 import coin_pb2 as _coin_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DepositAuthorization(_message.Message):
    __slots__ = ("spend_limit", "scopes")
    class Scope(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        invalid: _ClassVar[DepositAuthorization.Scope]
        deployment: _ClassVar[DepositAuthorization.Scope]
        bid: _ClassVar[DepositAuthorization.Scope]
    invalid: DepositAuthorization.Scope
    deployment: DepositAuthorization.Scope
    bid: DepositAuthorization.Scope
    SPEND_LIMIT_FIELD_NUMBER: _ClassVar[int]
    SCOPES_FIELD_NUMBER: _ClassVar[int]
    spend_limit: _coin_pb2.Coin
    scopes: _containers.RepeatedScalarFieldContainer[DepositAuthorization.Scope]
    def __init__(self, spend_limit: _Optional[_Union[_coin_pb2.Coin, _Mapping]] = ..., scopes: _Optional[_Iterable[_Union[DepositAuthorization.Scope, str]]] = ...) -> None: ...
