from gogoproto import gogo_pb2 as _gogo_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from typing import ClassVar as _ClassVar

DESCRIPTOR: _descriptor.FileDescriptor

class LeaseClosedReason(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    lease_closed_invalid: _ClassVar[LeaseClosedReason]
    lease_closed_owner: _ClassVar[LeaseClosedReason]
    lease_closed_reason_unstable: _ClassVar[LeaseClosedReason]
    lease_closed_reason_decommission: _ClassVar[LeaseClosedReason]
    lease_closed_reason_unspecified: _ClassVar[LeaseClosedReason]
    lease_closed_reason_manifest_timeout: _ClassVar[LeaseClosedReason]
    lease_closed_reason_insufficient_funds: _ClassVar[LeaseClosedReason]
lease_closed_invalid: LeaseClosedReason
lease_closed_owner: LeaseClosedReason
lease_closed_reason_unstable: LeaseClosedReason
lease_closed_reason_decommission: LeaseClosedReason
lease_closed_reason_unspecified: LeaseClosedReason
lease_closed_reason_manifest_timeout: LeaseClosedReason
lease_closed_reason_insufficient_funds: LeaseClosedReason
