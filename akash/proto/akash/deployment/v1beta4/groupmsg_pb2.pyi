from gogoproto import gogo_pb2 as _gogo_pb2
from akash.deployment.v1 import group_pb2 as _group_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MsgCloseGroup(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: _group_pb2.GroupID
    def __init__(self, id: _Optional[_Union[_group_pb2.GroupID, _Mapping]] = ...) -> None: ...

class MsgCloseGroupResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class MsgPauseGroup(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: _group_pb2.GroupID
    def __init__(self, id: _Optional[_Union[_group_pb2.GroupID, _Mapping]] = ...) -> None: ...

class MsgPauseGroupResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class MsgStartGroup(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: _group_pb2.GroupID
    def __init__(self, id: _Optional[_Union[_group_pb2.GroupID, _Mapping]] = ...) -> None: ...

class MsgStartGroupResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...
