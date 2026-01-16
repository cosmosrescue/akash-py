from k8s.io.api.core.v1 import generated_pb2 as _generated_pb2
from k8s.io.apimachinery.pkg.apis.meta.v1 import generated_pb2 as _generated_pb2_1
from k8s.io.apimachinery.pkg.runtime import generated_pb2 as _generated_pb2_1_1
from k8s.io.apimachinery.pkg.runtime.schema import generated_pb2 as _generated_pb2_1_1_1
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Event(_message.Message):
    __slots__ = ("metadata", "eventTime", "series", "reportingController", "reportingInstance", "action", "reason", "regarding", "related", "note", "type", "deprecatedSource", "deprecatedFirstTimestamp", "deprecatedLastTimestamp", "deprecatedCount")
    METADATA_FIELD_NUMBER: _ClassVar[int]
    EVENTTIME_FIELD_NUMBER: _ClassVar[int]
    SERIES_FIELD_NUMBER: _ClassVar[int]
    REPORTINGCONTROLLER_FIELD_NUMBER: _ClassVar[int]
    REPORTINGINSTANCE_FIELD_NUMBER: _ClassVar[int]
    ACTION_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    REGARDING_FIELD_NUMBER: _ClassVar[int]
    RELATED_FIELD_NUMBER: _ClassVar[int]
    NOTE_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    DEPRECATEDSOURCE_FIELD_NUMBER: _ClassVar[int]
    DEPRECATEDFIRSTTIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    DEPRECATEDLASTTIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    DEPRECATEDCOUNT_FIELD_NUMBER: _ClassVar[int]
    metadata: _generated_pb2_1.ObjectMeta
    eventTime: _generated_pb2_1.MicroTime
    series: EventSeries
    reportingController: str
    reportingInstance: str
    action: str
    reason: str
    regarding: _generated_pb2.ObjectReference
    related: _generated_pb2.ObjectReference
    note: str
    type: str
    deprecatedSource: _generated_pb2.EventSource
    deprecatedFirstTimestamp: _generated_pb2_1.Time
    deprecatedLastTimestamp: _generated_pb2_1.Time
    deprecatedCount: int
    def __init__(self, metadata: _Optional[_Union[_generated_pb2_1.ObjectMeta, _Mapping]] = ..., eventTime: _Optional[_Union[_generated_pb2_1.MicroTime, _Mapping]] = ..., series: _Optional[_Union[EventSeries, _Mapping]] = ..., reportingController: _Optional[str] = ..., reportingInstance: _Optional[str] = ..., action: _Optional[str] = ..., reason: _Optional[str] = ..., regarding: _Optional[_Union[_generated_pb2.ObjectReference, _Mapping]] = ..., related: _Optional[_Union[_generated_pb2.ObjectReference, _Mapping]] = ..., note: _Optional[str] = ..., type: _Optional[str] = ..., deprecatedSource: _Optional[_Union[_generated_pb2.EventSource, _Mapping]] = ..., deprecatedFirstTimestamp: _Optional[_Union[_generated_pb2_1.Time, _Mapping]] = ..., deprecatedLastTimestamp: _Optional[_Union[_generated_pb2_1.Time, _Mapping]] = ..., deprecatedCount: _Optional[int] = ...) -> None: ...

class EventList(_message.Message):
    __slots__ = ("metadata", "items")
    METADATA_FIELD_NUMBER: _ClassVar[int]
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    metadata: _generated_pb2_1.ListMeta
    items: _containers.RepeatedCompositeFieldContainer[Event]
    def __init__(self, metadata: _Optional[_Union[_generated_pb2_1.ListMeta, _Mapping]] = ..., items: _Optional[_Iterable[_Union[Event, _Mapping]]] = ...) -> None: ...

class EventSeries(_message.Message):
    __slots__ = ("count", "lastObservedTime")
    COUNT_FIELD_NUMBER: _ClassVar[int]
    LASTOBSERVEDTIME_FIELD_NUMBER: _ClassVar[int]
    count: int
    lastObservedTime: _generated_pb2_1.MicroTime
    def __init__(self, count: _Optional[int] = ..., lastObservedTime: _Optional[_Union[_generated_pb2_1.MicroTime, _Mapping]] = ...) -> None: ...
