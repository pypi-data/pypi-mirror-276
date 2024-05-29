from common import Common_pb2 as _Common_pb2
from common import Command_pb2 as _Command_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

CODE_CACHE_USAGE: PoolType
DESCRIPTOR: _descriptor.FileDescriptor
METASPACE_USAGE: PoolType
NEW: GCPhase
NEWGEN_USAGE: PoolType
NORMAL: GCPhase
OLD: GCPhase
OLDGEN_USAGE: PoolType
PERMGEN_USAGE: PoolType
SURVIVOR_USAGE: PoolType

class Class(_message.Message):
    __slots__ = ["loadedClassCount", "totalLoadedClassCount", "totalUnloadedClassCount"]
    LOADEDCLASSCOUNT_FIELD_NUMBER: _ClassVar[int]
    TOTALLOADEDCLASSCOUNT_FIELD_NUMBER: _ClassVar[int]
    TOTALUNLOADEDCLASSCOUNT_FIELD_NUMBER: _ClassVar[int]
    loadedClassCount: int
    totalLoadedClassCount: int
    totalUnloadedClassCount: int
    def __init__(self, loadedClassCount: _Optional[int] = ..., totalUnloadedClassCount: _Optional[int] = ..., totalLoadedClassCount: _Optional[int] = ...) -> None: ...

class GC(_message.Message):
    __slots__ = ["count", "phase", "time"]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    PHASE_FIELD_NUMBER: _ClassVar[int]
    TIME_FIELD_NUMBER: _ClassVar[int]
    count: int
    phase: GCPhase
    time: int
    def __init__(self, phase: _Optional[_Union[GCPhase, str]] = ..., count: _Optional[int] = ..., time: _Optional[int] = ...) -> None: ...

class JVMMetric(_message.Message):
    __slots__ = ["clazz", "cpu", "gc", "memory", "memoryPool", "thread", "time"]
    CLAZZ_FIELD_NUMBER: _ClassVar[int]
    CPU_FIELD_NUMBER: _ClassVar[int]
    GC_FIELD_NUMBER: _ClassVar[int]
    MEMORYPOOL_FIELD_NUMBER: _ClassVar[int]
    MEMORY_FIELD_NUMBER: _ClassVar[int]
    THREAD_FIELD_NUMBER: _ClassVar[int]
    TIME_FIELD_NUMBER: _ClassVar[int]
    clazz: Class
    cpu: _Common_pb2.CPU
    gc: _containers.RepeatedCompositeFieldContainer[GC]
    memory: _containers.RepeatedCompositeFieldContainer[Memory]
    memoryPool: _containers.RepeatedCompositeFieldContainer[MemoryPool]
    thread: Thread
    time: int
    def __init__(self, time: _Optional[int] = ..., cpu: _Optional[_Union[_Common_pb2.CPU, _Mapping]] = ..., memory: _Optional[_Iterable[_Union[Memory, _Mapping]]] = ..., memoryPool: _Optional[_Iterable[_Union[MemoryPool, _Mapping]]] = ..., gc: _Optional[_Iterable[_Union[GC, _Mapping]]] = ..., thread: _Optional[_Union[Thread, _Mapping]] = ..., clazz: _Optional[_Union[Class, _Mapping]] = ...) -> None: ...

class JVMMetricCollection(_message.Message):
    __slots__ = ["metrics", "service", "serviceInstance"]
    METRICS_FIELD_NUMBER: _ClassVar[int]
    SERVICEINSTANCE_FIELD_NUMBER: _ClassVar[int]
    SERVICE_FIELD_NUMBER: _ClassVar[int]
    metrics: _containers.RepeatedCompositeFieldContainer[JVMMetric]
    service: str
    serviceInstance: str
    def __init__(self, metrics: _Optional[_Iterable[_Union[JVMMetric, _Mapping]]] = ..., service: _Optional[str] = ..., serviceInstance: _Optional[str] = ...) -> None: ...

class Memory(_message.Message):
    __slots__ = ["committed", "init", "isHeap", "max", "used"]
    COMMITTED_FIELD_NUMBER: _ClassVar[int]
    INIT_FIELD_NUMBER: _ClassVar[int]
    ISHEAP_FIELD_NUMBER: _ClassVar[int]
    MAX_FIELD_NUMBER: _ClassVar[int]
    USED_FIELD_NUMBER: _ClassVar[int]
    committed: int
    init: int
    isHeap: bool
    max: int
    used: int
    def __init__(self, isHeap: bool = ..., init: _Optional[int] = ..., max: _Optional[int] = ..., used: _Optional[int] = ..., committed: _Optional[int] = ...) -> None: ...

class MemoryPool(_message.Message):
    __slots__ = ["committed", "init", "max", "type", "used"]
    COMMITTED_FIELD_NUMBER: _ClassVar[int]
    INIT_FIELD_NUMBER: _ClassVar[int]
    MAX_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    USED_FIELD_NUMBER: _ClassVar[int]
    committed: int
    init: int
    max: int
    type: PoolType
    used: int
    def __init__(self, type: _Optional[_Union[PoolType, str]] = ..., init: _Optional[int] = ..., max: _Optional[int] = ..., used: _Optional[int] = ..., committed: _Optional[int] = ...) -> None: ...

class Thread(_message.Message):
    __slots__ = ["blockedStateThreadCount", "daemonCount", "liveCount", "peakCount", "runnableStateThreadCount", "timedWaitingStateThreadCount", "waitingStateThreadCount"]
    BLOCKEDSTATETHREADCOUNT_FIELD_NUMBER: _ClassVar[int]
    DAEMONCOUNT_FIELD_NUMBER: _ClassVar[int]
    LIVECOUNT_FIELD_NUMBER: _ClassVar[int]
    PEAKCOUNT_FIELD_NUMBER: _ClassVar[int]
    RUNNABLESTATETHREADCOUNT_FIELD_NUMBER: _ClassVar[int]
    TIMEDWAITINGSTATETHREADCOUNT_FIELD_NUMBER: _ClassVar[int]
    WAITINGSTATETHREADCOUNT_FIELD_NUMBER: _ClassVar[int]
    blockedStateThreadCount: int
    daemonCount: int
    liveCount: int
    peakCount: int
    runnableStateThreadCount: int
    timedWaitingStateThreadCount: int
    waitingStateThreadCount: int
    def __init__(self, liveCount: _Optional[int] = ..., daemonCount: _Optional[int] = ..., peakCount: _Optional[int] = ..., runnableStateThreadCount: _Optional[int] = ..., blockedStateThreadCount: _Optional[int] = ..., waitingStateThreadCount: _Optional[int] = ..., timedWaitingStateThreadCount: _Optional[int] = ...) -> None: ...

class PoolType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class GCPhase(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
