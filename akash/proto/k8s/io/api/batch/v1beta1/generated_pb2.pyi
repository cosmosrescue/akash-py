from k8s.io.api.batch.v1 import generated_pb2 as _generated_pb2
from k8s.io.api.core.v1 import generated_pb2 as _generated_pb2_1
from k8s.io.apimachinery.pkg.apis.meta.v1 import generated_pb2 as _generated_pb2_1_1
from k8s.io.apimachinery.pkg.runtime import generated_pb2 as _generated_pb2_1_1_1
from k8s.io.apimachinery.pkg.runtime.schema import generated_pb2 as _generated_pb2_1_1_1_1
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CronJob(_message.Message):
    __slots__ = ("metadata", "spec", "status")
    METADATA_FIELD_NUMBER: _ClassVar[int]
    SPEC_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    metadata: _generated_pb2_1_1.ObjectMeta
    spec: CronJobSpec
    status: CronJobStatus
    def __init__(self, metadata: _Optional[_Union[_generated_pb2_1_1.ObjectMeta, _Mapping]] = ..., spec: _Optional[_Union[CronJobSpec, _Mapping]] = ..., status: _Optional[_Union[CronJobStatus, _Mapping]] = ...) -> None: ...

class CronJobList(_message.Message):
    __slots__ = ("metadata", "items")
    METADATA_FIELD_NUMBER: _ClassVar[int]
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    metadata: _generated_pb2_1_1.ListMeta
    items: _containers.RepeatedCompositeFieldContainer[CronJob]
    def __init__(self, metadata: _Optional[_Union[_generated_pb2_1_1.ListMeta, _Mapping]] = ..., items: _Optional[_Iterable[_Union[CronJob, _Mapping]]] = ...) -> None: ...

class CronJobSpec(_message.Message):
    __slots__ = ("schedule", "timeZone", "startingDeadlineSeconds", "concurrencyPolicy", "suspend", "jobTemplate", "successfulJobsHistoryLimit", "failedJobsHistoryLimit")
    SCHEDULE_FIELD_NUMBER: _ClassVar[int]
    TIMEZONE_FIELD_NUMBER: _ClassVar[int]
    STARTINGDEADLINESECONDS_FIELD_NUMBER: _ClassVar[int]
    CONCURRENCYPOLICY_FIELD_NUMBER: _ClassVar[int]
    SUSPEND_FIELD_NUMBER: _ClassVar[int]
    JOBTEMPLATE_FIELD_NUMBER: _ClassVar[int]
    SUCCESSFULJOBSHISTORYLIMIT_FIELD_NUMBER: _ClassVar[int]
    FAILEDJOBSHISTORYLIMIT_FIELD_NUMBER: _ClassVar[int]
    schedule: str
    timeZone: str
    startingDeadlineSeconds: int
    concurrencyPolicy: str
    suspend: bool
    jobTemplate: JobTemplateSpec
    successfulJobsHistoryLimit: int
    failedJobsHistoryLimit: int
    def __init__(self, schedule: _Optional[str] = ..., timeZone: _Optional[str] = ..., startingDeadlineSeconds: _Optional[int] = ..., concurrencyPolicy: _Optional[str] = ..., suspend: bool = ..., jobTemplate: _Optional[_Union[JobTemplateSpec, _Mapping]] = ..., successfulJobsHistoryLimit: _Optional[int] = ..., failedJobsHistoryLimit: _Optional[int] = ...) -> None: ...

class CronJobStatus(_message.Message):
    __slots__ = ("active", "lastScheduleTime", "lastSuccessfulTime")
    ACTIVE_FIELD_NUMBER: _ClassVar[int]
    LASTSCHEDULETIME_FIELD_NUMBER: _ClassVar[int]
    LASTSUCCESSFULTIME_FIELD_NUMBER: _ClassVar[int]
    active: _containers.RepeatedCompositeFieldContainer[_generated_pb2_1.ObjectReference]
    lastScheduleTime: _generated_pb2_1_1.Time
    lastSuccessfulTime: _generated_pb2_1_1.Time
    def __init__(self, active: _Optional[_Iterable[_Union[_generated_pb2_1.ObjectReference, _Mapping]]] = ..., lastScheduleTime: _Optional[_Union[_generated_pb2_1_1.Time, _Mapping]] = ..., lastSuccessfulTime: _Optional[_Union[_generated_pb2_1_1.Time, _Mapping]] = ...) -> None: ...

class JobTemplateSpec(_message.Message):
    __slots__ = ("metadata", "spec")
    METADATA_FIELD_NUMBER: _ClassVar[int]
    SPEC_FIELD_NUMBER: _ClassVar[int]
    metadata: _generated_pb2_1_1.ObjectMeta
    spec: _generated_pb2.JobSpec
    def __init__(self, metadata: _Optional[_Union[_generated_pb2_1_1.ObjectMeta, _Mapping]] = ..., spec: _Optional[_Union[_generated_pb2.JobSpec, _Mapping]] = ...) -> None: ...
