from gogoproto import gogo_pb2 as _gogo_pb2
from akash.deployment.v1 import group_pb2 as _group_pb2
from akash.deployment.v1beta4 import groupspec_pb2 as _groupspec_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Group(_message.Message):
    __slots__ = ("id", "state", "group_spec", "created_at")
    class State(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        invalid: _ClassVar[Group.State]
        open: _ClassVar[Group.State]
        paused: _ClassVar[Group.State]
        insufficient_funds: _ClassVar[Group.State]
        closed: _ClassVar[Group.State]
    invalid: Group.State
    open: Group.State
    paused: Group.State
    insufficient_funds: Group.State
    closed: Group.State
    ID_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    GROUP_SPEC_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    id: _group_pb2.GroupID
    state: Group.State
    group_spec: _groupspec_pb2.GroupSpec
    created_at: int
    def __init__(self, id: _Optional[_Union[_group_pb2.GroupID, _Mapping]] = ..., state: _Optional[_Union[Group.State, str]] = ..., group_spec: _Optional[_Union[_groupspec_pb2.GroupSpec, _Mapping]] = ..., created_at: _Optional[int] = ...) -> None: ...
