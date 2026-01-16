from gogoproto import gogo_pb2 as _gogo_pb2
from akash.deployment.v1beta4 import groupspec_pb2 as _groupspec_pb2
from akash.market.v1 import order_pb2 as _order_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Order(_message.Message):
    __slots__ = ("id", "state", "spec", "created_at")
    class State(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        invalid: _ClassVar[Order.State]
        open: _ClassVar[Order.State]
        active: _ClassVar[Order.State]
        closed: _ClassVar[Order.State]
    invalid: Order.State
    open: Order.State
    active: Order.State
    closed: Order.State
    ID_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    SPEC_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    id: _order_pb2.OrderID
    state: Order.State
    spec: _groupspec_pb2.GroupSpec
    created_at: int
    def __init__(self, id: _Optional[_Union[_order_pb2.OrderID, _Mapping]] = ..., state: _Optional[_Union[Order.State, str]] = ..., spec: _Optional[_Union[_groupspec_pb2.GroupSpec, _Mapping]] = ..., created_at: _Optional[int] = ...) -> None: ...
