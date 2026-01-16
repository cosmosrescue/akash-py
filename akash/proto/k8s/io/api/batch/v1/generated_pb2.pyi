from k8s.io.api.core.v1 import generated_pb2 as _generated_pb2
from k8s.io.apimachinery.pkg.apis.meta.v1 import generated_pb2 as _generated_pb2_1
from k8s.io.apimachinery.pkg.runtime import generated_pb2 as _generated_pb2_1_1
from k8s.io.apimachinery.pkg.runtime.schema import generated_pb2 as _generated_pb2_1_1_1
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
    metadata: _generated_pb2_1.ObjectMeta
    spec: CronJobSpec
    status: CronJobStatus
    def __init__(self, metadata: _Optional[_Union[_generated_pb2_1.ObjectMeta, _Mapping]] = ..., spec: _Optional[_Union[CronJobSpec, _Mapping]] = ..., status: _Optional[_Union[CronJobStatus, _Mapping]] = ...) -> None: ...

class CronJobList(_message.Message):
    __slots__ = ("metadata", "items")
    METADATA_FIELD_NUMBER: _ClassVar[int]
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    metadata: _generated_pb2_1.ListMeta
    items: _containers.RepeatedCompositeFieldContainer[CronJob]
    def __init__(self, metadata: _Optional[_Union[_generated_pb2_1.ListMeta, _Mapping]] = ..., items: _Optional[_Iterable[_Union[CronJob, _Mapping]]] = ...) -> None: ...

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
    active: _containers.RepeatedCompositeFieldContainer[_generated_pb2.ObjectReference]
    lastScheduleTime: _generated_pb2_1.Time
    lastSuccessfulTime: _generated_pb2_1.Time
    def __init__(self, active: _Optional[_Iterable[_Union[_generated_pb2.ObjectReference, _Mapping]]] = ..., lastScheduleTime: _Optional[_Union[_generated_pb2_1.Time, _Mapping]] = ..., lastSuccessfulTime: _Optional[_Union[_generated_pb2_1.Time, _Mapping]] = ...) -> None: ...

class Job(_message.Message):
    __slots__ = ("metadata", "spec", "status")
    METADATA_FIELD_NUMBER: _ClassVar[int]
    SPEC_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    metadata: _generated_pb2_1.ObjectMeta
    spec: JobSpec
    status: JobStatus
    def __init__(self, metadata: _Optional[_Union[_generated_pb2_1.ObjectMeta, _Mapping]] = ..., spec: _Optional[_Union[JobSpec, _Mapping]] = ..., status: _Optional[_Union[JobStatus, _Mapping]] = ...) -> None: ...

class JobCondition(_message.Message):
    __slots__ = ("type", "status", "lastProbeTime", "lastTransitionTime", "reason", "message")
    TYPE_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    LASTPROBETIME_FIELD_NUMBER: _ClassVar[int]
    LASTTRANSITIONTIME_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    type: str
    status: str
    lastProbeTime: _generated_pb2_1.Time
    lastTransitionTime: _generated_pb2_1.Time
    reason: str
    message: str
    def __init__(self, type: _Optional[str] = ..., status: _Optional[str] = ..., lastProbeTime: _Optional[_Union[_generated_pb2_1.Time, _Mapping]] = ..., lastTransitionTime: _Optional[_Union[_generated_pb2_1.Time, _Mapping]] = ..., reason: _Optional[str] = ..., message: _Optional[str] = ...) -> None: ...

class JobList(_message.Message):
    __slots__ = ("metadata", "items")
    METADATA_FIELD_NUMBER: _ClassVar[int]
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    metadata: _generated_pb2_1.ListMeta
    items: _containers.RepeatedCompositeFieldContainer[Job]
    def __init__(self, metadata: _Optional[_Union[_generated_pb2_1.ListMeta, _Mapping]] = ..., items: _Optional[_Iterable[_Union[Job, _Mapping]]] = ...) -> None: ...

class JobSpec(_message.Message):
    __slots__ = ("parallelism", "completions", "activeDeadlineSeconds", "podFailurePolicy", "successPolicy", "backoffLimit", "backoffLimitPerIndex", "maxFailedIndexes", "selector", "manualSelector", "template", "ttlSecondsAfterFinished", "completionMode", "suspend", "podReplacementPolicy", "managedBy")
    PARALLELISM_FIELD_NUMBER: _ClassVar[int]
    COMPLETIONS_FIELD_NUMBER: _ClassVar[int]
    ACTIVEDEADLINESECONDS_FIELD_NUMBER: _ClassVar[int]
    PODFAILUREPOLICY_FIELD_NUMBER: _ClassVar[int]
    SUCCESSPOLICY_FIELD_NUMBER: _ClassVar[int]
    BACKOFFLIMIT_FIELD_NUMBER: _ClassVar[int]
    BACKOFFLIMITPERINDEX_FIELD_NUMBER: _ClassVar[int]
    MAXFAILEDINDEXES_FIELD_NUMBER: _ClassVar[int]
    SELECTOR_FIELD_NUMBER: _ClassVar[int]
    MANUALSELECTOR_FIELD_NUMBER: _ClassVar[int]
    TEMPLATE_FIELD_NUMBER: _ClassVar[int]
    TTLSECONDSAFTERFINISHED_FIELD_NUMBER: _ClassVar[int]
    COMPLETIONMODE_FIELD_NUMBER: _ClassVar[int]
    SUSPEND_FIELD_NUMBER: _ClassVar[int]
    PODREPLACEMENTPOLICY_FIELD_NUMBER: _ClassVar[int]
    MANAGEDBY_FIELD_NUMBER: _ClassVar[int]
    parallelism: int
    completions: int
    activeDeadlineSeconds: int
    podFailurePolicy: PodFailurePolicy
    successPolicy: SuccessPolicy
    backoffLimit: int
    backoffLimitPerIndex: int
    maxFailedIndexes: int
    selector: _generated_pb2_1.LabelSelector
    manualSelector: bool
    template: _generated_pb2.PodTemplateSpec
    ttlSecondsAfterFinished: int
    completionMode: str
    suspend: bool
    podReplacementPolicy: str
    managedBy: str
    def __init__(self, parallelism: _Optional[int] = ..., completions: _Optional[int] = ..., activeDeadlineSeconds: _Optional[int] = ..., podFailurePolicy: _Optional[_Union[PodFailurePolicy, _Mapping]] = ..., successPolicy: _Optional[_Union[SuccessPolicy, _Mapping]] = ..., backoffLimit: _Optional[int] = ..., backoffLimitPerIndex: _Optional[int] = ..., maxFailedIndexes: _Optional[int] = ..., selector: _Optional[_Union[_generated_pb2_1.LabelSelector, _Mapping]] = ..., manualSelector: bool = ..., template: _Optional[_Union[_generated_pb2.PodTemplateSpec, _Mapping]] = ..., ttlSecondsAfterFinished: _Optional[int] = ..., completionMode: _Optional[str] = ..., suspend: bool = ..., podReplacementPolicy: _Optional[str] = ..., managedBy: _Optional[str] = ...) -> None: ...

class JobStatus(_message.Message):
    __slots__ = ("conditions", "startTime", "completionTime", "active", "succeeded", "failed", "terminating", "completedIndexes", "failedIndexes", "uncountedTerminatedPods", "ready")
    CONDITIONS_FIELD_NUMBER: _ClassVar[int]
    STARTTIME_FIELD_NUMBER: _ClassVar[int]
    COMPLETIONTIME_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_FIELD_NUMBER: _ClassVar[int]
    SUCCEEDED_FIELD_NUMBER: _ClassVar[int]
    FAILED_FIELD_NUMBER: _ClassVar[int]
    TERMINATING_FIELD_NUMBER: _ClassVar[int]
    COMPLETEDINDEXES_FIELD_NUMBER: _ClassVar[int]
    FAILEDINDEXES_FIELD_NUMBER: _ClassVar[int]
    UNCOUNTEDTERMINATEDPODS_FIELD_NUMBER: _ClassVar[int]
    READY_FIELD_NUMBER: _ClassVar[int]
    conditions: _containers.RepeatedCompositeFieldContainer[JobCondition]
    startTime: _generated_pb2_1.Time
    completionTime: _generated_pb2_1.Time
    active: int
    succeeded: int
    failed: int
    terminating: int
    completedIndexes: str
    failedIndexes: str
    uncountedTerminatedPods: UncountedTerminatedPods
    ready: int
    def __init__(self, conditions: _Optional[_Iterable[_Union[JobCondition, _Mapping]]] = ..., startTime: _Optional[_Union[_generated_pb2_1.Time, _Mapping]] = ..., completionTime: _Optional[_Union[_generated_pb2_1.Time, _Mapping]] = ..., active: _Optional[int] = ..., succeeded: _Optional[int] = ..., failed: _Optional[int] = ..., terminating: _Optional[int] = ..., completedIndexes: _Optional[str] = ..., failedIndexes: _Optional[str] = ..., uncountedTerminatedPods: _Optional[_Union[UncountedTerminatedPods, _Mapping]] = ..., ready: _Optional[int] = ...) -> None: ...

class JobTemplateSpec(_message.Message):
    __slots__ = ("metadata", "spec")
    METADATA_FIELD_NUMBER: _ClassVar[int]
    SPEC_FIELD_NUMBER: _ClassVar[int]
    metadata: _generated_pb2_1.ObjectMeta
    spec: JobSpec
    def __init__(self, metadata: _Optional[_Union[_generated_pb2_1.ObjectMeta, _Mapping]] = ..., spec: _Optional[_Union[JobSpec, _Mapping]] = ...) -> None: ...

class PodFailurePolicy(_message.Message):
    __slots__ = ("rules",)
    RULES_FIELD_NUMBER: _ClassVar[int]
    rules: _containers.RepeatedCompositeFieldContainer[PodFailurePolicyRule]
    def __init__(self, rules: _Optional[_Iterable[_Union[PodFailurePolicyRule, _Mapping]]] = ...) -> None: ...

class PodFailurePolicyOnExitCodesRequirement(_message.Message):
    __slots__ = ("containerName", "operator", "values")
    CONTAINERNAME_FIELD_NUMBER: _ClassVar[int]
    OPERATOR_FIELD_NUMBER: _ClassVar[int]
    VALUES_FIELD_NUMBER: _ClassVar[int]
    containerName: str
    operator: str
    values: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, containerName: _Optional[str] = ..., operator: _Optional[str] = ..., values: _Optional[_Iterable[int]] = ...) -> None: ...

class PodFailurePolicyOnPodConditionsPattern(_message.Message):
    __slots__ = ("type", "status")
    TYPE_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    type: str
    status: str
    def __init__(self, type: _Optional[str] = ..., status: _Optional[str] = ...) -> None: ...

class PodFailurePolicyRule(_message.Message):
    __slots__ = ("action", "onExitCodes", "onPodConditions")
    ACTION_FIELD_NUMBER: _ClassVar[int]
    ONEXITCODES_FIELD_NUMBER: _ClassVar[int]
    ONPODCONDITIONS_FIELD_NUMBER: _ClassVar[int]
    action: str
    onExitCodes: PodFailurePolicyOnExitCodesRequirement
    onPodConditions: _containers.RepeatedCompositeFieldContainer[PodFailurePolicyOnPodConditionsPattern]
    def __init__(self, action: _Optional[str] = ..., onExitCodes: _Optional[_Union[PodFailurePolicyOnExitCodesRequirement, _Mapping]] = ..., onPodConditions: _Optional[_Iterable[_Union[PodFailurePolicyOnPodConditionsPattern, _Mapping]]] = ...) -> None: ...

class SuccessPolicy(_message.Message):
    __slots__ = ("rules",)
    RULES_FIELD_NUMBER: _ClassVar[int]
    rules: _containers.RepeatedCompositeFieldContainer[SuccessPolicyRule]
    def __init__(self, rules: _Optional[_Iterable[_Union[SuccessPolicyRule, _Mapping]]] = ...) -> None: ...

class SuccessPolicyRule(_message.Message):
    __slots__ = ("succeededIndexes", "succeededCount")
    SUCCEEDEDINDEXES_FIELD_NUMBER: _ClassVar[int]
    SUCCEEDEDCOUNT_FIELD_NUMBER: _ClassVar[int]
    succeededIndexes: str
    succeededCount: int
    def __init__(self, succeededIndexes: _Optional[str] = ..., succeededCount: _Optional[int] = ...) -> None: ...

class UncountedTerminatedPods(_message.Message):
    __slots__ = ("succeeded", "failed")
    SUCCEEDED_FIELD_NUMBER: _ClassVar[int]
    FAILED_FIELD_NUMBER: _ClassVar[int]
    succeeded: _containers.RepeatedScalarFieldContainer[str]
    failed: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, succeeded: _Optional[_Iterable[str]] = ..., failed: _Optional[_Iterable[str]] = ...) -> None: ...
