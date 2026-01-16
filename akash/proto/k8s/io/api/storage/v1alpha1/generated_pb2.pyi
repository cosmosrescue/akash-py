from k8s.io.api.core.v1 import generated_pb2 as _generated_pb2
from k8s.io.apimachinery.pkg.api.resource import generated_pb2 as _generated_pb2_1
from k8s.io.apimachinery.pkg.apis.meta.v1 import generated_pb2 as _generated_pb2_1_1
from k8s.io.apimachinery.pkg.runtime import generated_pb2 as _generated_pb2_1_1_1
from k8s.io.apimachinery.pkg.runtime.schema import generated_pb2 as _generated_pb2_1_1_1_1
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CSIStorageCapacity(_message.Message):
    __slots__ = ("metadata", "nodeTopology", "storageClassName", "capacity", "maximumVolumeSize")
    METADATA_FIELD_NUMBER: _ClassVar[int]
    NODETOPOLOGY_FIELD_NUMBER: _ClassVar[int]
    STORAGECLASSNAME_FIELD_NUMBER: _ClassVar[int]
    CAPACITY_FIELD_NUMBER: _ClassVar[int]
    MAXIMUMVOLUMESIZE_FIELD_NUMBER: _ClassVar[int]
    metadata: _generated_pb2_1_1.ObjectMeta
    nodeTopology: _generated_pb2_1_1.LabelSelector
    storageClassName: str
    capacity: _generated_pb2_1.Quantity
    maximumVolumeSize: _generated_pb2_1.Quantity
    def __init__(self, metadata: _Optional[_Union[_generated_pb2_1_1.ObjectMeta, _Mapping]] = ..., nodeTopology: _Optional[_Union[_generated_pb2_1_1.LabelSelector, _Mapping]] = ..., storageClassName: _Optional[str] = ..., capacity: _Optional[_Union[_generated_pb2_1.Quantity, _Mapping]] = ..., maximumVolumeSize: _Optional[_Union[_generated_pb2_1.Quantity, _Mapping]] = ...) -> None: ...

class CSIStorageCapacityList(_message.Message):
    __slots__ = ("metadata", "items")
    METADATA_FIELD_NUMBER: _ClassVar[int]
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    metadata: _generated_pb2_1_1.ListMeta
    items: _containers.RepeatedCompositeFieldContainer[CSIStorageCapacity]
    def __init__(self, metadata: _Optional[_Union[_generated_pb2_1_1.ListMeta, _Mapping]] = ..., items: _Optional[_Iterable[_Union[CSIStorageCapacity, _Mapping]]] = ...) -> None: ...

class VolumeAttachment(_message.Message):
    __slots__ = ("metadata", "spec", "status")
    METADATA_FIELD_NUMBER: _ClassVar[int]
    SPEC_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    metadata: _generated_pb2_1_1.ObjectMeta
    spec: VolumeAttachmentSpec
    status: VolumeAttachmentStatus
    def __init__(self, metadata: _Optional[_Union[_generated_pb2_1_1.ObjectMeta, _Mapping]] = ..., spec: _Optional[_Union[VolumeAttachmentSpec, _Mapping]] = ..., status: _Optional[_Union[VolumeAttachmentStatus, _Mapping]] = ...) -> None: ...

class VolumeAttachmentList(_message.Message):
    __slots__ = ("metadata", "items")
    METADATA_FIELD_NUMBER: _ClassVar[int]
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    metadata: _generated_pb2_1_1.ListMeta
    items: _containers.RepeatedCompositeFieldContainer[VolumeAttachment]
    def __init__(self, metadata: _Optional[_Union[_generated_pb2_1_1.ListMeta, _Mapping]] = ..., items: _Optional[_Iterable[_Union[VolumeAttachment, _Mapping]]] = ...) -> None: ...

class VolumeAttachmentSource(_message.Message):
    __slots__ = ("persistentVolumeName", "inlineVolumeSpec")
    PERSISTENTVOLUMENAME_FIELD_NUMBER: _ClassVar[int]
    INLINEVOLUMESPEC_FIELD_NUMBER: _ClassVar[int]
    persistentVolumeName: str
    inlineVolumeSpec: _generated_pb2.PersistentVolumeSpec
    def __init__(self, persistentVolumeName: _Optional[str] = ..., inlineVolumeSpec: _Optional[_Union[_generated_pb2.PersistentVolumeSpec, _Mapping]] = ...) -> None: ...

class VolumeAttachmentSpec(_message.Message):
    __slots__ = ("attacher", "source", "nodeName")
    ATTACHER_FIELD_NUMBER: _ClassVar[int]
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    NODENAME_FIELD_NUMBER: _ClassVar[int]
    attacher: str
    source: VolumeAttachmentSource
    nodeName: str
    def __init__(self, attacher: _Optional[str] = ..., source: _Optional[_Union[VolumeAttachmentSource, _Mapping]] = ..., nodeName: _Optional[str] = ...) -> None: ...

class VolumeAttachmentStatus(_message.Message):
    __slots__ = ("attached", "attachmentMetadata", "attachError", "detachError")
    class AttachmentMetadataEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    ATTACHED_FIELD_NUMBER: _ClassVar[int]
    ATTACHMENTMETADATA_FIELD_NUMBER: _ClassVar[int]
    ATTACHERROR_FIELD_NUMBER: _ClassVar[int]
    DETACHERROR_FIELD_NUMBER: _ClassVar[int]
    attached: bool
    attachmentMetadata: _containers.ScalarMap[str, str]
    attachError: VolumeError
    detachError: VolumeError
    def __init__(self, attached: bool = ..., attachmentMetadata: _Optional[_Mapping[str, str]] = ..., attachError: _Optional[_Union[VolumeError, _Mapping]] = ..., detachError: _Optional[_Union[VolumeError, _Mapping]] = ...) -> None: ...

class VolumeAttributesClass(_message.Message):
    __slots__ = ("metadata", "driverName", "parameters")
    class ParametersEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    METADATA_FIELD_NUMBER: _ClassVar[int]
    DRIVERNAME_FIELD_NUMBER: _ClassVar[int]
    PARAMETERS_FIELD_NUMBER: _ClassVar[int]
    metadata: _generated_pb2_1_1.ObjectMeta
    driverName: str
    parameters: _containers.ScalarMap[str, str]
    def __init__(self, metadata: _Optional[_Union[_generated_pb2_1_1.ObjectMeta, _Mapping]] = ..., driverName: _Optional[str] = ..., parameters: _Optional[_Mapping[str, str]] = ...) -> None: ...

class VolumeAttributesClassList(_message.Message):
    __slots__ = ("metadata", "items")
    METADATA_FIELD_NUMBER: _ClassVar[int]
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    metadata: _generated_pb2_1_1.ListMeta
    items: _containers.RepeatedCompositeFieldContainer[VolumeAttributesClass]
    def __init__(self, metadata: _Optional[_Union[_generated_pb2_1_1.ListMeta, _Mapping]] = ..., items: _Optional[_Iterable[_Union[VolumeAttributesClass, _Mapping]]] = ...) -> None: ...

class VolumeError(_message.Message):
    __slots__ = ("time", "message")
    TIME_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    time: _generated_pb2_1_1.Time
    message: str
    def __init__(self, time: _Optional[_Union[_generated_pb2_1_1.Time, _Mapping]] = ..., message: _Optional[str] = ...) -> None: ...
