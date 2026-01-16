from gogoproto import gogo_pb2 as _gogo_pb2
from akash.market.v1beta4 import order_pb2 as _order_pb2
from akash.market.v1beta4 import lease_pb2 as _lease_pb2
from akash.market.v1beta4 import bid_pb2 as _bid_pb2
from akash.market.v1beta4 import params_pb2 as _params_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GenesisState(_message.Message):
    __slots__ = ("params", "orders", "leases", "bids")
    PARAMS_FIELD_NUMBER: _ClassVar[int]
    ORDERS_FIELD_NUMBER: _ClassVar[int]
    LEASES_FIELD_NUMBER: _ClassVar[int]
    BIDS_FIELD_NUMBER: _ClassVar[int]
    params: _params_pb2.Params
    orders: _containers.RepeatedCompositeFieldContainer[_order_pb2.Order]
    leases: _containers.RepeatedCompositeFieldContainer[_lease_pb2.Lease]
    bids: _containers.RepeatedCompositeFieldContainer[_bid_pb2.Bid]
    def __init__(self, params: _Optional[_Union[_params_pb2.Params, _Mapping]] = ..., orders: _Optional[_Iterable[_Union[_order_pb2.Order, _Mapping]]] = ..., leases: _Optional[_Iterable[_Union[_lease_pb2.Lease, _Mapping]]] = ..., bids: _Optional[_Iterable[_Union[_bid_pb2.Bid, _Mapping]]] = ...) -> None: ...
