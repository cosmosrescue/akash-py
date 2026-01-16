from gogoproto import gogo_pb2 as _gogo_pb2
from cosmos_proto import cosmos_pb2 as _cosmos_pb2
from cosmos.msg.v1 import msg_pb2 as _msg_pb2
from akash.escrow.id.v1 import id_pb2 as _id_pb2
from akash.base.deposit.v1 import deposit_pb2 as _deposit_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MsgAccountDeposit(_message.Message):
    __slots__ = ("signer", "id", "deposit")
    SIGNER_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    DEPOSIT_FIELD_NUMBER: _ClassVar[int]
    signer: str
    id: _id_pb2.Account
    deposit: _deposit_pb2.Deposit
    def __init__(self, signer: _Optional[str] = ..., id: _Optional[_Union[_id_pb2.Account, _Mapping]] = ..., deposit: _Optional[_Union[_deposit_pb2.Deposit, _Mapping]] = ...) -> None: ...

class MsgAccountDepositResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...
